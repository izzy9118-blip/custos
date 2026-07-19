from __future__ import annotations

import json
from pathlib import PurePosixPath
from typing import Any

import yaml

from custos_engine.models.base import CanonicalReference
from custos_engine.models.taxonomy import TaxonomyComponent
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.validators import validate_against_schema


class TaxonomyLoader:
    def __init__(self, reader: LocalGitReader) -> None:
        self.reader = reader

    def load_manifest_source(
        self,
        source: CanonicalReference,
        schema_repository_path: str,
        governed_git_commit: str,
    ) -> list[TaxonomyComponent]:
        if source.github_path is None:
            raise ValueError("taxonomy_source.github_path is required")
        if not source.github_path.strip():
            raise ValueError("taxonomy_source.github_path must be non-empty")
        if source.git_commit is None:
            raise ValueError("taxonomy_source.git_commit is required")
        if source.git_commit != governed_git_commit:
            raise ValueError(
                "taxonomy_source.git_commit does not match governed repository commit: "
                f"{source.git_commit} != {governed_git_commit}"
            )
        if self.reader.resolved_commit != governed_git_commit:
            raise ValueError(
                "Taxonomy reader commit does not match governed repository commit: "
                f"{self.reader.resolved_commit} != {governed_git_commit}"
            )

        source_path = source.github_path.strip()
        source_text = self.reader.read_text(source_path)
        schema_text = self.reader.read_text(schema_repository_path)

        try:
            schema = json.loads(schema_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid Taxonomy schema JSON at "
                f"{schema_repository_path}: {exc.msg}"
            ) from exc

        source_suffix = PurePosixPath(source_path).suffix.lower()

        if source_suffix == ".json":
            try:
                raw: Any = json.loads(source_text)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Invalid Taxonomy JSON at "
                    f"{source_path}: {exc.msg}"
                ) from exc
        elif source_suffix in {".yaml", ".yml"}:
            try:
                raw = yaml.safe_load(source_text)
            except yaml.YAMLError as exc:
                raise ValueError(
                    "Invalid Taxonomy YAML at "
                    f"{source_path}: {exc}"
                ) from exc
        else:
            raise ValueError(
                "Unsupported Taxonomy source suffix for "
                f"{source_path}: {source_suffix or '<none>'}"
            )

        if not isinstance(raw, list):
            raise ValueError(
                "Taxonomy source root must be an array at "
                f"{source_path}"
            )

        components: list[TaxonomyComponent] = []
        for item in raw:
            validate_against_schema(item, schema)
            components.append(TaxonomyComponent.model_validate(item))

        return sorted(components, key=lambda component: component.component_id)


def load_taxonomy_components(
    reader: LocalGitReader,
    source: CanonicalReference,
    schema_repository_path: str,
    governed_git_commit: str,
) -> list[TaxonomyComponent]:
    return TaxonomyLoader(reader).load_manifest_source(
        source,
        schema_repository_path,
        governed_git_commit,
    )
