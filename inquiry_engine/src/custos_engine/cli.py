from __future__ import annotations

import argparse
import json
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
from custos_engine.graph.projection_manifest_loader import ProjectionManifestLoader
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

    gate_decision = None
    gate_context_data = question.get("inner_sanctum_gate_context")
    if gate_context_data is not None:
        gate_context = HermeneuticGateContext.model_validate(gate_context_data)
        gate_decision = evaluate_inner_sanctum_gate(gate_context).model_dump(
            mode="json"
        )

    requested_technique_ids = question.get("inner_sanctum_technique_ids", [])
    if not isinstance(requested_technique_ids, list) or not all(
        isinstance(technique_id, str) for technique_id in requested_technique_ids
    ):
        raise ValueError("inner_sanctum_technique_ids must be an array of strings")
    available_technique_ids = {
        component.component_id for component in taxonomy_components
    }
    unavailable_technique_ids = sorted(
        set(requested_technique_ids).difference(available_technique_ids)
    )
    if unavailable_technique_ids:
        raise ValueError(
            "Requested Taxonomy techniques are not present in the pinned Manifest: "
            + ", ".join(unavailable_technique_ids)
        )
    gate_authorized = bool(gate_decision and gate_decision["authorized"])
    if requested_technique_ids and not gate_authorized:
        raise PermissionError(
            "Inner Sanctum techniques were requested while the recorded gate is closed"
        )
    if gate_authorized and not requested_technique_ids:
        raise ValueError(
            "An authorized Inner Sanctum inquiry must name at least one Taxonomy technique"
        )

    phase_reasoning_records = None
    if args.reasoner_command:
        raw_inputs = question.get("documentary_inputs")
        if not isinstance(raw_inputs, list) or not raw_inputs:
            raise ValueError(
                "A field reasoning run requires at least one documentary_inputs record"
            )
        documentary_inputs = [
            DocumentaryInput.model_validate(item) for item in raw_inputs
        ]
        command = shlex.split(args.reasoner_command)
        reasoner = SubprocessPhaseReasoner(
            command,
            timeout_seconds=args.reasoner_timeout_seconds,
        )
        phase_reasoning_records = InquiryReasoningExecutor(reasoner).run_to_termination(
            run,
            procedure,
            documentary_inputs,
            inner_sanctum_authorized=gate_authorized,
            permitted_taxonomy_techniques=[
                component
                for component in taxonomy_components
                if component.component_id in requested_technique_ids
            ],
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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
