import json
import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.graph.projection_manifest_loader import ProjectionManifestLoader
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.validators import SchemaValidationError


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _build_projection_manifest(
    *,
    projection_id: str,
    repository_full_name: str,
    git_commit: str,
    cognitive_memory_manifest_id: str,
) -> dict[str, object]:
    return {
        "projection_id": projection_id,
        "repository_full_name": repository_full_name,
        "git_commit": git_commit,
        "cognitive_memory_manifest_id": cognitive_memory_manifest_id,
        "projector_version": "0.1.0",
        "schema_versions": {"projection_manifest": "1.0.0"},
        "source_file_count": 1,
        "node_counts": {"Hermeneutic Object": 1},
        "relationship_counts": {"INTERPRETS": 1},
        "validation_status": "PASS",
        "integrity_sha256": "0" * 64,
        "build_timestamp": "2026-01-01T00:00:00Z",
    }


def _build_projection_schema(projection_id_pattern: str = ".+") -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "projection_id",
            "repository_full_name",
            "git_commit",
            "cognitive_memory_manifest_id",
        ],
        "properties": {
            "projection_id": {
                "type": "string",
                "pattern": projection_id_pattern,
            },
            "repository_full_name": {
                "type": "string",
                "pattern": "^[^/]+/[^/]+$",
            },
            "git_commit": {"type": "string", "minLength": 7},
            "cognitive_memory_manifest_id": {"type": "string"},
        },
    }


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_projection_loader_uses_pinned_projection_commit_for_manifest_and_schema(
    tmp_path: Path,
):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("governed-source\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "governed source")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")

    committed_manifest = _build_projection_manifest(
        projection_id="PRJ-000000001",
        repository_full_name="izzy9118-blip/custos",
        git_commit=governed_git_commit,
        cognitive_memory_manifest_id="MAN-000000001",
    )
    committed_schema = _build_projection_schema(r"^PRJ-[0-9]{9}$")

    projection_path = repo / "projection.json"
    projection_schema_path = repo / "projection_schema.json"
    projection_path.write_text(json.dumps(committed_manifest), encoding="utf-8")
    projection_schema_path.write_text(json.dumps(committed_schema), encoding="utf-8")
    _git(repo, "add", "projection.json", "projection_schema.json")
    _git(repo, "commit", "-q", "-m", "projection manifest and schema")
    projection_git_commit = _git(repo, "rev-parse", "HEAD")

    working_tree_manifest = dict(committed_manifest)
    working_tree_manifest["git_commit"] = "deadbee"
    working_tree_manifest["cognitive_memory_manifest_id"] = "MAN-WORKTREE"
    working_tree_manifest["repository_full_name"] = "other/repo"
    working_tree_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["projection_id"],
        "properties": {"projection_id": {"const": "PRJ-999999999"}},
    }
    projection_path.write_text(json.dumps(working_tree_manifest), encoding="utf-8")
    projection_schema_path.write_text(json.dumps(working_tree_schema), encoding="utf-8")

    projection_reader = LocalGitReader(repo, projection_git_commit)
    loader = ProjectionManifestLoader(projection_reader)
    projection = loader.load_repository("projection.json", "projection_schema.json")
    loader.assert_bindings(
        projection,
        governed_git_commit,
        "MAN-000000001",
        "izzy9118-blip/custos",
    )

    assert projection.projection_id == committed_manifest["projection_id"]
    assert projection.git_commit == governed_git_commit
    assert projection.cognitive_memory_manifest_id == "MAN-000000001"
    assert projection.repository_full_name == "izzy9118-blip/custos"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_pinned_projection_schema_cannot_be_bypassed_by_working_tree_schema(
    tmp_path: Path,
):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("governed-source\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "governed source")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_manifest = _build_projection_manifest(
        projection_id="PROJECTION-FREEFORM",
        repository_full_name="izzy9118-blip/custos",
        git_commit=governed_git_commit,
        cognitive_memory_manifest_id="MAN-000000001",
    )
    constrained_schema = _build_projection_schema(r"^PRJ-[0-9]{9}$")

    projection_path = repo / "projection.json"
    projection_schema_path = repo / "projection_schema.json"
    projection_path.write_text(json.dumps(projection_manifest), encoding="utf-8")
    projection_schema_path.write_text(json.dumps(constrained_schema), encoding="utf-8")
    _git(repo, "add", "projection.json", "projection_schema.json")
    _git(repo, "commit", "-q", "-m", "pinned projection and schema")
    projection_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_schema_path.write_text("{}", encoding="utf-8")

    projection_reader = LocalGitReader(repo, projection_git_commit)
    loader = ProjectionManifestLoader(projection_reader)

    with pytest.raises(SchemaValidationError):
        loader.load_repository("projection.json", "projection_schema.json")


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_projection_binding_rejects_governed_commit_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("first\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "first")
    first_commit = _git(repo, "rev-parse", "HEAD")

    source_file.write_text("second\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "second")
    second_commit = _git(repo, "rev-parse", "HEAD")

    projection_manifest = _build_projection_manifest(
        projection_id="PRJ-000000001",
        repository_full_name="izzy9118-blip/custos",
        git_commit=second_commit,
        cognitive_memory_manifest_id="MAN-000000001",
    )
    projection_schema = _build_projection_schema(r"^PRJ-[0-9]{9}$")

    projection_path = repo / "projection.json"
    projection_schema_path = repo / "projection_schema.json"
    projection_path.write_text(json.dumps(projection_manifest), encoding="utf-8")
    projection_schema_path.write_text(json.dumps(projection_schema), encoding="utf-8")
    _git(repo, "add", "projection.json", "projection_schema.json")
    _git(repo, "commit", "-q", "-m", "projection manifest and schema")
    projection_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_reader = LocalGitReader(repo, projection_git_commit)
    loader = ProjectionManifestLoader(projection_reader)
    projection = loader.load_repository("projection.json", "projection_schema.json")

    with pytest.raises(ValueError, match="git_commit"):
        loader.assert_bindings(
            projection,
            first_commit,
            "MAN-000000001",
            "izzy9118-blip/custos",
        )


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_projection_binding_rejects_manifest_id_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("governed-source\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "governed source")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_manifest = _build_projection_manifest(
        projection_id="PRJ-000000001",
        repository_full_name="izzy9118-blip/custos",
        git_commit=governed_git_commit,
        cognitive_memory_manifest_id="MAN-OTHER0001",
    )
    projection_schema = _build_projection_schema(r"^PRJ-[0-9]{9}$")

    projection_path = repo / "projection.json"
    projection_schema_path = repo / "projection_schema.json"
    projection_path.write_text(json.dumps(projection_manifest), encoding="utf-8")
    projection_schema_path.write_text(json.dumps(projection_schema), encoding="utf-8")
    _git(repo, "add", "projection.json", "projection_schema.json")
    _git(repo, "commit", "-q", "-m", "projection manifest and schema")
    projection_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_reader = LocalGitReader(repo, projection_git_commit)
    loader = ProjectionManifestLoader(projection_reader)
    projection = loader.load_repository("projection.json", "projection_schema.json")

    with pytest.raises(ValueError, match="cognitive_memory_manifest_id"):
        loader.assert_bindings(
            projection,
            governed_git_commit,
            "MAN-000000001",
            "izzy9118-blip/custos",
        )


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_projection_binding_rejects_repository_full_name_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "source.txt"
    source_file.write_text("governed-source\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-q", "-m", "governed source")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_manifest = _build_projection_manifest(
        projection_id="PRJ-000000001",
        repository_full_name="other-org/other-repo",
        git_commit=governed_git_commit,
        cognitive_memory_manifest_id="MAN-000000001",
    )
    projection_schema = _build_projection_schema(r"^PRJ-[0-9]{9}$")

    projection_path = repo / "projection.json"
    projection_schema_path = repo / "projection_schema.json"
    projection_path.write_text(json.dumps(projection_manifest), encoding="utf-8")
    projection_schema_path.write_text(json.dumps(projection_schema), encoding="utf-8")
    _git(repo, "add", "projection.json", "projection_schema.json")
    _git(repo, "commit", "-q", "-m", "projection manifest and schema")
    projection_git_commit = _git(repo, "rev-parse", "HEAD")

    projection_reader = LocalGitReader(repo, projection_git_commit)
    loader = ProjectionManifestLoader(projection_reader)
    projection = loader.load_repository("projection.json", "projection_schema.json")

    with pytest.raises(ValueError, match="repository_full_name"):
        loader.assert_bindings(
            projection,
            governed_git_commit,
            "MAN-000000001",
            "izzy9118-blip/custos",
        )
