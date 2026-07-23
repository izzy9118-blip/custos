from __future__ import annotations

import argparse
import json
import os
import shlex
from pathlib import Path

from custos_engine.cognition.cognitive_memory_loader import (
    load_cognitive_memory_manifest,
)
from custos_engine.cognition.hermeneutic_gate import (
    HermeneuticGateContext,
    evaluate_inner_sanctum_gate,
)
from custos_engine.cognition.procedure_loader import ProcedureLoader
from custos_engine.cognition.taxonomy_loader import TaxonomyLoader
from custos_engine.config.settings import EngineSettings
from custos_engine.federation.adapter import (
    FederationRunConfig,
    execute_federation_run,
)
from custos_engine.graph.projection_manifest_loader import ProjectionManifestLoader
from custos_engine.graph.documentary_retrieval import VerifiedGraphDocumentaryRetriever
from custos_engine.graph.neo4j_client import Neo4jClient
from custos_engine.graph.neo4j_projection import Neo4jProjectionStore
from custos_engine.graph.projection_manifest import build_projection_manifest
from custos_engine.graph.repository_projector import (
    DEFAULT_PROJECTION_PREFIXES,
    RepositoryProjectionBuilder,
)
from custos_engine.models.base import EngineMode, TerminationReason
from custos_engine.models.inquiry import InquiryRun, TerminationRecord
from custos_engine.models.reasoning import (
    DocumentaryInput,
    PhaseReasoningRequest,
    PhaseReasoningResponse,
)
from custos_engine.outputs.inquiry_package import InquiryPackageWriter
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.runtime.reasoning import (
    InquiryReasoningExecutor,
    SubprocessPhaseReasoner,
)
from custos_engine.runtime.state_machine import InquiryStateMachine


def reasoning_schema_command(args: argparse.Namespace) -> int:
    schemas = {
        "request": PhaseReasoningRequest.model_json_schema(),
        "response": PhaseReasoningResponse.model_json_schema(),
    }
    value = schemas if args.kind == "both" else schemas[args.kind]
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def federation_run_command(args: argparse.Namespace) -> int:
    output = execute_federation_run(
        FederationRunConfig(
            repo_root=Path(args.repo_root),
            release_commit=args.release_commit,
            envelope_path=Path(args.envelope),
            evidence_bundle_path=Path(args.evidence_bundle),
            output_dir=Path(args.output),
            reasoner_command=args.reasoner_command,
            reasoner_timeout_seconds=args.reasoner_timeout_seconds,
            reasoner_provider=args.reasoner_provider,
            reasoner_model=args.reasoner_model,
            reasoner_model_revision=args.reasoner_model_revision,
            prompt_id=args.prompt_id,
            prompt_version=args.prompt_version,
        )
    )
    print(output)
    return 0


def _neo4j_client(args: argparse.Namespace) -> Neo4jClient:
    required = {
        "neo4j_uri": args.neo4j_uri,
        "neo4j_username": args.neo4j_username,
        "neo4j_password_env": args.neo4j_password_env,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(
            "Neo4j configuration is incomplete; missing fields: "
            + ", ".join(missing)
        )
    password = os.environ.get(args.neo4j_password_env)
    if not password:
        raise ValueError(
            f"Neo4j password environment variable is unset: {args.neo4j_password_env}"
        )
    client = Neo4jClient(args.neo4j_uri, args.neo4j_username, password)
    client.verify_connectivity()
    return client


def project_neo4j_command(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).expanduser().resolve()
    repository_reader = LocalGitReader(repo_root, args.git_commit)
    manifest_reader = LocalGitReader(repo_root, args.manifest_git_commit)
    cognitive_manifest = load_cognitive_memory_manifest(
        manifest_reader,
        args.manifest,
        args.manifest_schema,
        repository_reader.resolved_commit,
    )
    prefixes = tuple(args.prefix or DEFAULT_PROJECTION_PREFIXES)
    plan = RepositoryProjectionBuilder(repository_reader, prefixes).build(
        cognitive_manifest.manifest_id
    )
    projection = build_projection_manifest(
        projection_id=args.projection_id,
        repository_full_name=cognitive_manifest.repository_full_name,
        plan=plan,
        projector_version="1.0.0",
        schema_versions={
            "projection_manifest": "1.0.0",
            "repository_projection": "1.0.0",
        },
    )

    output = Path(args.manifest_output).expanduser().resolve()
    if output.exists():
        raise FileExistsError(f"Projection Manifest output already exists: {output}")

    client = _neo4j_client(args)
    try:
        Neo4jProjectionStore(client).replace(plan, projection)
    finally:
        client.close()

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(
            projection.model_dump(mode="json"),
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")
    print(output)
    return 0


def run_command(args: argparse.Namespace) -> int:
    settings = EngineSettings(
        mode=EngineMode(args.mode),
        repo_root=Path(args.repo_root),
        git_commit=args.git_commit,
        manifest_git_commit=args.manifest_git_commit,
        manifest_path=args.manifest,
        manifest_schema_path=args.manifest_schema,
        taxonomy_schema_path=args.taxonomy_schema,
        procedure_schema_path=args.procedure_schema,
        projection_git_commit=args.projection_git_commit,
        projection_manifest_path=args.projection_manifest,
        projection_manifest_schema_path=args.projection_manifest_schema,
        question_path=Path(args.question),
        output_dir=Path(args.output),
    )

    repository_reader = LocalGitReader(settings.repo_root, settings.git_commit)
    manifest_reader = LocalGitReader(settings.repo_root, settings.manifest_git_commit)
    manifest = load_cognitive_memory_manifest(
        manifest_reader,
        settings.manifest_path,
        settings.manifest_schema_path,
        repository_reader.resolved_commit,
    )
    taxonomy_loader = TaxonomyLoader(repository_reader)
    taxonomy_components = taxonomy_loader.load_manifest_source(
        manifest.taxonomy_source,
        settings.taxonomy_schema_path,
        repository_reader.resolved_commit,
    )
    procedure_loader = ProcedureLoader(repository_reader)
    procedure = procedure_loader.load_manifest_source(
        manifest.procedure_source,
        settings.procedure_schema_path,
        repository_reader.resolved_commit,
    )

    question = json.loads(settings.question_path.read_text(encoding="utf-8"))
    required = {"run_id", "initiating_question", "documentary_boundary"}
    missing = sorted(required.difference(question))
    if missing:
        raise ValueError(f"Question file is missing fields: {missing}")

    projection_id = None
    projection = None
    if settings.projection_manifest_path:
        projection_reader = LocalGitReader(
            settings.repo_root,
            settings.projection_git_commit,
        )
        projection_loader = ProjectionManifestLoader(projection_reader)
        projection = projection_loader.load_repository(
            settings.projection_manifest_path,
            settings.projection_manifest_schema_path,
        )
        projection_loader.assert_bindings(
            projection,
            repository_reader.resolved_commit,
            manifest.manifest_id,
            manifest.repository_full_name,
        )
        projection_id = projection.projection_id

    run = InquiryRun(
        run_id=question["run_id"],
        mode=settings.mode,
        initiating_question=question["initiating_question"],
        documentary_boundary=question["documentary_boundary"],
        repository_full_name=manifest.repository_full_name,
        git_commit=repository_reader.resolved_commit,
        cognitive_memory_manifest_id=manifest.manifest_id,
        projection_manifest_id=projection_id,
        governing_specification_ids=manifest.governing_specification_ids,
        source_entity_ids=question.get("source_entity_ids", []),
    )

    supplied_gate_context = question.get("inner_sanctum_gate_context", {})
    if not isinstance(supplied_gate_context, dict):
        raise ValueError("inner_sanctum_gate_context must be an object")
    gate_context_data = {
        "procedure_id": manifest.procedure_source.canonical_id,
        "taxonomy_id": manifest.taxonomy_source.canonical_id,
        "cognitive_memory_manifest_id": manifest.manifest_id,
        "current_state": run.current_state,
    }
    gate_context_data.update(supplied_gate_context)
    gate_context = HermeneuticGateContext.model_validate(gate_context_data)
    gate_decision_model = evaluate_inner_sanctum_gate(gate_context)
    gate_decision = gate_decision_model.model_dump(mode="json")
    if not gate_decision_model.authorized:
        raise PermissionError(
            "The canonical always-open Inner Sanctum could not initialize: "
            + " ".join(gate_decision_model.reasons)
        )

    declared_focus_technique_ids = question.get("inner_sanctum_technique_ids", [])
    if not isinstance(declared_focus_technique_ids, list) or not all(
        isinstance(technique_id, str)
        for technique_id in declared_focus_technique_ids
    ):
        raise ValueError("inner_sanctum_technique_ids must be an array of strings")
    available_technique_ids = {
        component.component_id for component in taxonomy_components
    }
    unavailable_technique_ids = sorted(
        set(declared_focus_technique_ids).difference(available_technique_ids)
    )
    if unavailable_technique_ids:
        raise ValueError(
            "Declared Taxonomy focus techniques are not present in the pinned Manifest: "
            + ", ".join(unavailable_technique_ids)
        )

    phase_reasoning_records = None
    graph_retrieval_receipt = None
    if args.reasoner_command:
        raw_inputs = question.get("documentary_inputs", [])
        if not isinstance(raw_inputs, list):
            raise ValueError("documentary_inputs must be an array")
        documentary_inputs = [
            DocumentaryInput.model_validate(item) for item in raw_inputs
        ]

        if run.source_entity_ids:
            if projection is None:
                raise ValueError(
                    "Graph-selected source_entity_ids require a pinned Projection Manifest"
                )
            relationship_types = question.get("graph_relationship_types", [])
            if not isinstance(relationship_types, list) or not all(
                isinstance(value, str) for value in relationship_types
            ):
                raise ValueError("graph_relationship_types must be an array of strings")
            max_related = question.get("graph_max_related", 50)
            if not isinstance(max_related, int):
                raise ValueError("graph_max_related must be an integer")
            client = _neo4j_client(args)
            try:
                graph_inputs, receipt = VerifiedGraphDocumentaryRetriever(
                    Neo4jProjectionStore(client),
                    repository_reader,
                    projection,
                ).retrieve(
                    run.source_entity_ids,
                    relationship_types,
                    max_related,
                )
            finally:
                client.close()
            documentary_inputs.extend(graph_inputs)
            graph_retrieval_receipt = receipt.model_dump(mode="json")

        evidence_ids = [item.evidence_id for item in documentary_inputs]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError(
                "Explicit and graph-retrieved documentary evidence identifiers must be unique"
            )
        if not documentary_inputs:
            raise ValueError(
                "A field reasoning run requires explicit documentary_inputs or graph-selected source_entity_ids"
            )
        command = shlex.split(args.reasoner_command)
        reasoner = SubprocessPhaseReasoner(
            command,
            timeout_seconds=args.reasoner_timeout_seconds,
        )
        phase_reasoning_records = InquiryReasoningExecutor(reasoner).run_to_termination(
            run,
            procedure,
            documentary_inputs,
            inner_sanctum_authorized=True,
            permitted_taxonomy_techniques=taxonomy_components,
        )
    else:
        InquiryStateMachine().run_to_termination(run)

    termination = TerminationRecord(
        run_id=run.run_id,
        reason=run.termination_reason,
        explanation=(
            "The inquiry runtime completed or boundedly terminated the authorized "
            "state sequence. "
            "No certification or Repository admission is conferred."
        ),
        unresolved_questions=run.unresolved_questions,
        incomplete_tasks=(
            []
            if run.termination_reason == TerminationReason.COMPLETED_AUTHORIZED_UNIT
            else ["The authorized inquiry unit terminated before ordinary completion."]
        ),
        evidence_exhausted=(
            run.termination_reason == TerminationReason.EVIDENCE_EXHAUSTED
        ),
        authorized_unit_completed=(
            run.termination_reason == TerminationReason.COMPLETED_AUTHORIZED_UNIT
        ),
    )

    writer = InquiryPackageWriter(settings.output_dir)
    writer.write(
        run,
        question,
        termination,
        gate_decision=gate_decision,
        phase_reasoning_records=(
            [record.model_dump(mode="json") for record in phase_reasoning_records]
            if phase_reasoning_records is not None
            else None
        ),
        graph_retrieval_receipt=graph_retrieval_receipt,
    )
    print(settings.output_dir)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="custos-inquiry")
    subcommands = parser.add_subparsers(dest="command", required=True)

    run_parser = subcommands.add_parser("run")
    run_parser.add_argument("--mode", choices=["DEVELOPMENT", "PRODUCTION"], required=True)
    run_parser.add_argument("--repo-root", required=True)
    run_parser.add_argument("--git-commit", required=True)
    run_parser.add_argument("--manifest-git-commit", required=True)
    run_parser.add_argument("--manifest", required=True)
    run_parser.add_argument("--manifest-schema", required=True)
    run_parser.add_argument("--taxonomy-schema", required=True)
    run_parser.add_argument("--procedure-schema", required=True)
    run_parser.add_argument("--projection-git-commit")
    run_parser.add_argument("--projection-manifest")
    run_parser.add_argument("--projection-manifest-schema")
    run_parser.add_argument("--neo4j-uri")
    run_parser.add_argument("--neo4j-username")
    run_parser.add_argument("--neo4j-password-env", default="NEO4J_PASSWORD")
    run_parser.add_argument("--question", required=True)
    run_parser.add_argument("--output", required=True)
    run_parser.add_argument(
        "--reasoner-command",
        help=(
            "Provider-neutral command that reads one PhaseReasoningRequest JSON "
            "object from stdin and writes one PhaseReasoningResponse JSON object "
            "to stdout. The command is executed without a shell."
        ),
    )
    run_parser.add_argument(
        "--reasoner-timeout-seconds",
        type=float,
        default=120.0,
    )
    run_parser.set_defaults(handler=run_command)

    schema_parser = subcommands.add_parser(
        "reasoning-schema",
        help="Print the strict JSON contract for an external phase reasoner.",
    )
    schema_parser.add_argument(
        "--kind",
        choices=["request", "response", "both"],
        default="both",
    )
    schema_parser.set_defaults(handler=reasoning_schema_command)

    federation_parser = subcommands.add_parser(
        "federation-run",
        help=(
            "Validate a Sanctum Inquiry Envelope, execute an isolated Custos "
            "inquiry, and emit a candidate Ministerial Report."
        ),
    )
    federation_parser.add_argument("--repo-root", required=True)
    federation_parser.add_argument(
        "--release-commit",
        required=True,
        help=(
            "Exact Custos release commit selected by the Inquiry Envelope; "
            "the checkout must be clean and at this commit."
        ),
    )
    federation_parser.add_argument("--envelope", required=True)
    federation_parser.add_argument("--evidence-bundle", required=True)
    federation_parser.add_argument("--output", required=True)
    federation_parser.add_argument(
        "--reasoner-command",
        required=True,
        help=(
            "Provider-neutral phase reasoner command. It is executed directly "
            "without a shell."
        ),
    )
    federation_parser.add_argument(
        "--reasoner-timeout-seconds",
        type=float,
        default=120.0,
    )
    federation_parser.add_argument("--reasoner-provider", required=True)
    federation_parser.add_argument("--reasoner-model", required=True)
    federation_parser.add_argument("--reasoner-model-revision")
    federation_parser.add_argument("--prompt-id", required=True)
    federation_parser.add_argument("--prompt-version", required=True)
    federation_parser.set_defaults(handler=federation_run_command)

    project_parser = subcommands.add_parser(
        "project-neo4j",
        help="Build and persist a commit-pinned, rebuildable Neo4j projection.",
    )
    project_parser.add_argument("--repo-root", required=True)
    project_parser.add_argument("--git-commit", required=True)
    project_parser.add_argument("--manifest-git-commit", required=True)
    project_parser.add_argument("--manifest", required=True)
    project_parser.add_argument("--manifest-schema", required=True)
    project_parser.add_argument("--projection-id", required=True)
    project_parser.add_argument("--manifest-output", required=True)
    project_parser.add_argument("--neo4j-uri", required=True)
    project_parser.add_argument("--neo4j-username", required=True)
    project_parser.add_argument("--neo4j-password-env", default="NEO4J_PASSWORD")
    project_parser.add_argument(
        "--prefix",
        action="append",
        help="Repository-relative projection prefix; repeat to select multiple roots.",
    )
    project_parser.set_defaults(handler=project_neo4j_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
