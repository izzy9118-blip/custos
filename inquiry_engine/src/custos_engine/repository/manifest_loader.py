from __future__ import annotations

import json
from pathlib import Path

from custos_engine.models.cognitive_memory import CognitiveMemoryManifest
from custos_engine.repository.github_reader import LocalGitReader

from .validators import validate_against_schema


class ManifestLoader:
    def __init__(self, schema_path: Path, reader: LocalGitReader) -> None:
        self.schema_path = schema_path
        self.reader = reader

    def load_repository(self, repository_path: str) -> CognitiveMemoryManifest:
        data = json.loads(self.reader.read_text(repository_path))
        validate_against_schema(data, self.schema_path)
        return CognitiveMemoryManifest.model_validate(data)

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
