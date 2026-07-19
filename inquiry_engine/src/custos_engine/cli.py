from __future__ import annotations

import argparse
import json
from pathlib import Path

from custos_engine.cognition.cognitive_memory_loader import (
    load_cognitive_memory_manifest,
)
from custos_engine.cognition.taxonomy_loader import TaxonomyLoader
from custos_engine.config.settings import EngineSettings
from custos_engine.graph.projection_manifest_loader import ProjectionManifestLoader
from custos_engine.models.base import EngineMode
from custos_engine.models.inquiry import InquiryRun, TerminationRecord
from custos_engine.outputs.inquiry_package import InquiryPackageWriter
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.runtime.state_machine import InquiryStateMachine


def run_command(args: argparse.Namespace) -> int:
    settings = EngineSettings(
        mode=EngineMode(args.mode),
        repo_root=Path(args.repo_root),
        git_commit=args.git_commit,
        manifest_git_commit=args.manifest_git_commit,
        manifest_path=args.manifest,
        manifest_schema_path=args.manifest_schema,
        taxonomy_schema_path=args.taxonomy_schema,
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

    machine = InquiryStateMachine()
    machine.run_to_termination(run)

    termination = TerminationRecord(
        run_id=run.run_id,
        reason=run.termination_reason,
        explanation=(
            "The deterministic scaffold completed the authorized state sequence. "
            "No certification or Repository admission is conferred."
        ),
        unresolved_questions=run.unresolved_questions,
        incomplete_tasks=[],
        evidence_exhausted=False,
        authorized_unit_completed=True,
    )

    writer = InquiryPackageWriter(settings.output_dir)
    writer.write(run, question, termination)
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
    run_parser.add_argument("--projection-git-commit")
    run_parser.add_argument("--projection-manifest")
    run_parser.add_argument("--projection-manifest-schema")
    run_parser.add_argument("--question", required=True)
    run_parser.add_argument("--output", required=True)
    run_parser.set_defaults(handler=run_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
