from __future__ import annotations

import json
from pathlib import Path

from custos_engine.models.cognitive_memory import CognitiveMemoryManifest

from .validators import validate_against_schema


class ManifestLoader:
    def __init__(self, schema_path: Path) -> None:
        self.schema_path = schema_path

    def load_local(self, manifest_path: Path) -> CognitiveMemoryManifest:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_against_schema(data, self.schema_path)
        return CognitiveMemoryManifest.model_validate(data)

    @staticmethod
    def assert_commit_match(
        manifest: CognitiveMemoryManifest,
        resolved_git_commit: str,
    ) -> None:
        if manifest.repository_commit != resolved_git_commit:
            raise ValueError(
                "Manifest commit does not match declared run commit: "
                f"{manifest.repository_commit} != {resolved_git_commit}"
            )
