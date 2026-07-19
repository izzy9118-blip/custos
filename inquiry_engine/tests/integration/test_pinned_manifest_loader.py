import json
import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.cognition.cognitive_memory_loader import load_cognitive_memory_manifest
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


def _build_schema(manifest_id_pattern: str = ".+") -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["manifest_id", "repository_commit"],
        "properties": {
            "manifest_id": {"type": "string", "pattern": manifest_id_pattern},
            "repository_commit": {"type": "string", "minLength": 7},
        },
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
    schema_path = repo / "schema.json"
    committed_manifest = _build_manifest(governed_source_commit)
    committed_schema = _build_schema(r"^MAN-[0-9]{9}$")
    manifest_path.write_text(json.dumps(committed_manifest), encoding="utf-8")
    schema_path.write_text(json.dumps(committed_schema), encoding="utf-8")
    _git(repo, "add", "manifest.json", "schema.json")
    _git(repo, "commit", "-q", "-m", "manifest and schema commit")
    manifest_commit = _git(repo, "rev-parse", "HEAD")

    working_tree_manifest = dict(committed_manifest)
    working_tree_manifest["manifest_id"] = "MAN-999999999"
    working_tree_manifest["repository_commit"] = "deadbee"
    working_tree_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["manifest_id"],
        "properties": {"manifest_id": {"const": "MAN-123123123"}},
    }
    manifest_path.write_text(json.dumps(working_tree_manifest), encoding="utf-8")
    schema_path.write_text(json.dumps(working_tree_schema), encoding="utf-8")

    governed_reader = LocalGitReader(repo, governed_source_commit)
    manifest_reader = LocalGitReader(repo, manifest_commit)

    manifest = load_cognitive_memory_manifest(
        manifest_reader=manifest_reader,
        manifest_repository_path="manifest.json",
        manifest_schema_repository_path="schema.json",
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
    schema_path = repo / "schema.json"
    manifest_path.write_text(
        json.dumps(_build_manifest(different_source_commit)),
        encoding="utf-8",
    )
    schema_path.write_text(json.dumps(_build_schema(r"^MAN-[0-9]{9}$")), encoding="utf-8")
    _git(repo, "add", "manifest.json", "schema.json")
    _git(repo, "commit", "-q", "-m", "manifest and schema")
    manifest_commit = _git(repo, "rev-parse", "HEAD")

    governed_reader = LocalGitReader(repo, governed_source_commit)
    manifest_reader = LocalGitReader(repo, manifest_commit)

    with pytest.raises(ValueError, match="repository_commit"):
        load_cognitive_memory_manifest(
            manifest_reader=manifest_reader,
            manifest_repository_path="manifest.json",
            manifest_schema_repository_path="schema.json",
            governed_git_commit=governed_reader.resolved_commit,
        )


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_pinned_manifest_schema_cannot_be_bypassed_by_working_tree_schema(
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
    governed_source_commit = _git(repo, "rev-parse", "HEAD")

    manifest_path = repo / "manifest.json"
    schema_path = repo / "schema.json"
    constrained_schema = _build_schema(r"^MAN-[0-9]{9}$")
    violating_manifest = _build_manifest(governed_source_commit)
    violating_manifest["manifest_id"] = "MANIFEST-FREEFORM"
    manifest_path.write_text(json.dumps(violating_manifest), encoding="utf-8")
    schema_path.write_text(json.dumps(constrained_schema), encoding="utf-8")
    _git(repo, "add", "manifest.json", "schema.json")
    _git(repo, "commit", "-q", "-m", "pinned manifest and schema")
    manifest_commit = _git(repo, "rev-parse", "HEAD")

    schema_path.write_text("{}", encoding="utf-8")

    governed_reader = LocalGitReader(repo, governed_source_commit)
    manifest_reader = LocalGitReader(repo, manifest_commit)

    with pytest.raises(SchemaValidationError):
        load_cognitive_memory_manifest(
            manifest_reader=manifest_reader,
            manifest_repository_path="manifest.json",
            manifest_schema_repository_path="schema.json",
            governed_git_commit=governed_reader.resolved_commit,
        )
