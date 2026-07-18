from __future__ import annotations

from pathlib import Path

from custos_engine.models.cognitive_memory import CognitiveMemoryManifest
from custos_engine.repository.manifest_loader import ManifestLoader


def load_cognitive_memory_manifest(
    manifest_path: Path,
    schema_path: Path,
    resolved_git_commit: str,
) -> CognitiveMemoryManifest:
    loader = ManifestLoader(schema_path)
    manifest = loader.load_local(manifest_path)
    loader.assert_commit_match(manifest, resolved_git_commit)
    return manifest
