import json
import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.cognition.cognitive_memory_loader import load_cognitive_memory_manifest
from custos_engine.repository.github_reader import LocalGitReader


SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "custos_engine"
    / "schemas"
    / "cognitive_memory_manifest.schema.json"
)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _build_manifest(repository_commit: str) -> dict[str, object]:
    return {
        "manifest_id": "MAN-000000001",
        "version": "0.1.0",
        "release_status": "DEVELOPMENT",
        "repository_full_name": "izzy9118-blip/custos",
        "repository_commit": repository_commit,
        "governing_specification_ids": ["SPEC-000000007"],
        "taxonomy_source": {
            "canonical_id": "HO-000000001",
            "canonical_class": "Hermeneutic Object",
            "github_path": "engine_training/taxonomy.txt",
            "git_commit": repository_commit,
            "version": "1.0",
        },
        "procedure_source": {
            "canonical_id": "IAR-000000001",
            "canonical_class": "Inquiry Architecture Record",
            "github_path": "engine_training/procedure.txt",
            "git_commit": repository_commit,
            "version": "1.0",
        },
        "included_components": [],
        "excluded_component_ids": [],
        "known_conflicts": ["Integration test fixture"],
        "permitted_engine_mode": "DEVELOPMENT",
        "predecessor_manifest_id": None,
        "fixity_sha256": "0" * 64,
        "released_at": None,
        "responsible_authority_id": "AUR-000000001",
    }


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_manifest_loader_uses_pinned_manifest_commit_not_working_tree(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("governed-source\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "governed source")
    governed_source_commit = _git(repo, "rev-parse", "HEAD")

    manifest_path = repo / "manifest.json"
    committed_manifest = _build_manifest(governed_source_commit)
    manifest_path.write_text(json.dumps(committed_manifest), encoding="utf-8")
    _git(repo, "add", "manifest.json")
    _git(repo, "commit", "-q", "-m", "manifest commit")
    manifest_commit = _git(repo, "rev-parse", "HEAD")

    working_tree_manifest = dict(committed_manifest)
    working_tree_manifest["manifest_id"] = "MAN-999999999"
    working_tree_manifest["repository_commit"] = "deadbee"
    manifest_path.write_text(json.dumps(working_tree_manifest), encoding="utf-8")

    governed_reader = LocalGitReader(repo, governed_source_commit)
    manifest_reader = LocalGitReader(repo, manifest_commit)

    manifest = load_cognitive_memory_manifest(
        manifest_reader=manifest_reader,
        manifest_repository_path="manifest.json",
        schema_path=SCHEMA_PATH,
        governed_git_commit=governed_reader.resolved_commit,
    )

    assert manifest.manifest_id == committed_manifest["manifest_id"]
    assert manifest.manifest_id != working_tree_manifest["manifest_id"]
    assert manifest.repository_commit == governed_reader.resolved_commit


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_manifest_loader_rejects_manifest_governing_different_repository_commit(
    tmp_path: Path,
):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("first\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "first")
    governed_source_commit = _git(repo, "rev-parse", "HEAD")

    source_file.write_text("second\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "second")
    different_source_commit = _git(repo, "rev-parse", "HEAD")

    manifest_path = repo / "manifest.json"
    manifest_path.write_text(
        json.dumps(_build_manifest(different_source_commit)),
        encoding="utf-8",
    )
    _git(repo, "add", "manifest.json")
    _git(repo, "commit", "-q", "-m", "manifest")
    manifest_commit = _git(repo, "rev-parse", "HEAD")

    governed_reader = LocalGitReader(repo, governed_source_commit)
    manifest_reader = LocalGitReader(repo, manifest_commit)

    with pytest.raises(ValueError, match="repository_commit"):
        load_cognitive_memory_manifest(
            manifest_reader=manifest_reader,
            manifest_repository_path="manifest.json",
            schema_path=SCHEMA_PATH,
            governed_git_commit=governed_reader.resolved_commit,
        )
