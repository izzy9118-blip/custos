from __future__ import annotations

from custos_engine.models.cognitive_memory import CognitiveMemoryManifest
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.manifest_loader import ManifestLoader


def load_cognitive_memory_manifest(
    manifest_reader: LocalGitReader,
    manifest_repository_path: str,
    manifest_schema_repository_path: str,
    governed_git_commit: str,
) -> CognitiveMemoryManifest:
    loader = ManifestLoader(manifest_reader)
    manifest = loader.load_repository(
        manifest_repository_path,
        manifest_schema_repository_path,
    )
    loader.assert_commit_match(manifest, governed_git_commit)
    return manifest
