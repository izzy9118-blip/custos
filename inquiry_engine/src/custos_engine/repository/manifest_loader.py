from __future__ import annotations

import json

from custos_engine.models.cognitive_memory import CognitiveMemoryManifest
from custos_engine.repository.github_reader import LocalGitReader

from .validators import validate_against_schema


class ManifestLoader:
    def __init__(self, reader: LocalGitReader) -> None:
        self.reader = reader

    def load_repository(
        self,
        manifest_repository_path: str,
        schema_repository_path: str,
    ) -> CognitiveMemoryManifest:
        manifest_data = json.loads(self.reader.read_text(manifest_repository_path))
        schema_data = json.loads(self.reader.read_text(schema_repository_path))
        validate_against_schema(manifest_data, schema_data)
        return CognitiveMemoryManifest.model_validate(manifest_data)

    @staticmethod
    def assert_commit_match(
        manifest: CognitiveMemoryManifest,
        resolved_git_commit: str,
    ) -> None:
        if manifest.repository_commit != resolved_git_commit:
            raise ValueError(
                "Manifest repository_commit does not match governed repository "
                "resolved commit: "
                f"{manifest.repository_commit} != {resolved_git_commit}"
            )
