from __future__ import annotations

import json
from pathlib import PurePosixPath
from typing import Any

import yaml

from custos_engine.models.base import CanonicalReference
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.validators import validate_against_schema


class ProcedureLoader:
    def __init__(self, reader: LocalGitReader) -> None:
        self.reader = reader

    def load_manifest_source(
        self,
        source: CanonicalReference,
        schema_repository_path: str,
        governed_git_commit: str,
    ) -> dict[str, Any]:
        if source.github_path is None:
            raise ValueError("procedure_source.github_path is required")
        source_path = source.github_path.strip()
        if not source_path:
            raise ValueError("procedure_source.github_path must be non-empty")
        if source.git_commit is None:
            raise ValueError("procedure_source.git_commit is required")
        if source.git_commit != governed_git_commit:
            raise ValueError(
                "procedure_source.git_commit does not match governed repository "
                f"commit: {source.git_commit} != {governed_git_commit}"
            )
        if self.reader.resolved_commit != governed_git_commit:
            raise ValueError(
                "Procedure reader commit does not match governed repository commit: "
                f"{self.reader.resolved_commit} != {governed_git_commit}"
            )

        if not self.reader.file_exists(source_path):
            raise ValueError(
                "Procedure source is missing at governed commit: "
                f"{source_path}@{governed_git_commit}"
            )
        if not self.reader.file_exists(schema_repository_path):
            raise ValueError(
                "Procedure schema is missing at governed commit: "
                f"{schema_repository_path}@{governed_git_commit}"
            )

        source_text = self.reader.read_text(source_path)
        schema_text = self.reader.read_text(schema_repository_path)

        try:
            schema = json.loads(schema_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid procedure schema JSON at {schema_repository_path}: {exc.msg}"
            ) from exc

        source_suffix = PurePosixPath(source_path).suffix.lower()
        if source_suffix == ".json":
            try:
                value: Any = json.loads(source_text)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid procedure JSON at {source_path}: {exc.msg}"
                ) from exc
        elif source_suffix in {".yaml", ".yml"}:
            try:
                value = yaml.safe_load(source_text)
            except yaml.YAMLError as exc:
                raise ValueError(f"Invalid procedure YAML at {source_path}: {exc}") from exc
        else:
            raise ValueError(
                "Unsupported procedure source suffix for "
                f"{source_path}: {source_suffix or '<none>'}"
            )

        if not isinstance(value, dict):
            raise ValueError(f"Procedure source root must be an object at {source_path}")

        validate_against_schema(value, schema)
        return value


def load_procedure(
    reader: LocalGitReader,
    source: CanonicalReference,
    schema_repository_path: str,
    governed_git_commit: str,
) -> dict[str, Any]:
    return ProcedureLoader(reader).load_manifest_source(
        source,
        schema_repository_path,
        governed_git_commit,
    )
