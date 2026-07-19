from __future__ import annotations

import json

from custos_engine.models.artifacts import ProjectionManifest
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.validators import validate_against_schema


class ProjectionManifestLoader:
    def __init__(self, reader: LocalGitReader) -> None:
        self.reader = reader

    def load_repository(
        self,
        manifest_repository_path: str,
        schema_repository_path: str,
    ) -> ProjectionManifest:
        manifest_text = self.reader.read_text(manifest_repository_path)
        schema_text = self.reader.read_text(schema_repository_path)

        try:
            manifest_data = json.loads(manifest_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid Projection Manifest JSON at "
                f"{manifest_repository_path}: {exc.msg}"
            ) from exc

        try:
            schema_data = json.loads(schema_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid Projection Manifest schema JSON at "
                f"{schema_repository_path}: {exc.msg}"
            ) from exc

        validate_against_schema(manifest_data, schema_data)
        return ProjectionManifest.model_validate(manifest_data)

    @staticmethod
    def assert_bindings(
        projection: ProjectionManifest,
        governed_git_commit: str,
        cognitive_memory_manifest_id: str,
        repository_full_name: str,
    ) -> None:
        if projection.git_commit != governed_git_commit:
            raise ValueError(
                "Projection Manifest git_commit does not match governed repository "
                "resolved commit: "
                f"{projection.git_commit} != {governed_git_commit}"
            )
        if projection.cognitive_memory_manifest_id != cognitive_memory_manifest_id:
            raise ValueError(
                "Projection Manifest cognitive_memory_manifest_id does not match "
                "loaded Cognitive Memory Manifest ID: "
                f"{projection.cognitive_memory_manifest_id} != "
                f"{cognitive_memory_manifest_id}"
            )
        if projection.repository_full_name != repository_full_name:
            raise ValueError(
                "Projection Manifest repository_full_name does not match loaded "
                "Cognitive Memory Manifest repository_full_name: "
                f"{projection.repository_full_name} != {repository_full_name}"
            )
