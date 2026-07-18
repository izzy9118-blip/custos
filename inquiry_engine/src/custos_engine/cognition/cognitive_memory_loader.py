from __future__ import annotations

from pathlib import Path

from custos_engine.models.cognitive_memory import CognitiveMemoryManifest
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.manifest_loader import ManifestLoader


def load_cognitive_memory_manifest(
    manifest_reader: LocalGitReader,
    manifest_repository_path: str,
    schema_path: Path,
    governed_git_commit: str,
) -> CognitiveMemoryManifest:
    loader = ManifestLoader(schema_path, manifest_reader)
    manifest = loader.load_repository(manifest_repository_path)
    loader.assert_commit_match(manifest, governed_git_commit)
    return manifest
