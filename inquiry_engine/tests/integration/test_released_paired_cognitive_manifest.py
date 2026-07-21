import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.cognition.cognitive_memory_loader import (
    load_cognitive_memory_manifest,
)
from custos_engine.cognition.procedure_loader import ProcedureLoader
from custos_engine.cognition.taxonomy_loader import TaxonomyLoader
from custos_engine.repository.github_reader import LocalGitReader


MANIFEST_PATH = "manifests/cognitive-memory/MAN-000000001.json"
MANIFEST_SCHEMA_PATH = (
    "inquiry_engine/src/custos_engine/schemas/cognitive_memory_manifest.schema.json"
)
PROCEDURE_SCHEMA_PATH = (
    "inquiry_engine/src/custos_engine/schemas/procedure.schema.json"
)
TAXONOMY_SCHEMA_PATH = (
    "inquiry_engine/src/custos_engine/schemas/taxonomy_component.schema.json"
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _git_text(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_bytes(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
    )
    return result.stdout


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_released_manifest_loads_both_pinned_sanctums_from_governed_commit():
    repo = _repo_root()
    manifest_reader = LocalGitReader(repo, "HEAD")
    manifest_data = json.loads(manifest_reader.read_text(MANIFEST_PATH))
    governed_commit = manifest_data["repository_commit"]
    governed_reader = LocalGitReader(repo, governed_commit)

    manifest = load_cognitive_memory_manifest(
        manifest_reader=manifest_reader,
        manifest_repository_path=MANIFEST_PATH,
        manifest_schema_repository_path=MANIFEST_SCHEMA_PATH,
        governed_git_commit=governed_reader.resolved_commit,
    )
    taxonomy = TaxonomyLoader(governed_reader).load_manifest_source(
        manifest.taxonomy_source,
        TAXONOMY_SCHEMA_PATH,
        governed_reader.resolved_commit,
    )
    procedure = ProcedureLoader(governed_reader).load_manifest_source(
        manifest.procedure_source,
        PROCEDURE_SCHEMA_PATH,
        governed_reader.resolved_commit,
    )

    assert manifest.release_status == "RELEASED"
    assert manifest.permitted_engine_mode == "PRODUCTION"
    assert [component.component_id for component in taxonomy] == [
        f"LC-{number:03d}" for number in range(1, 23)
    ]
    assert procedure["id"] == "IAR-000000001"
    assert len(procedure["ordered_stages"]) == 10
    assert [
        step["sequence"]
        for stage in procedure["ordered_stages"]
        for step in stage["steps"]
    ] == list(range(1, 38))


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_manifest_fixity_covers_exact_governed_bytes():
    repo = _repo_root()
    manifest = json.loads((repo / MANIFEST_PATH).read_text(encoding="utf-8"))
    governed_commit = manifest["repository_commit"]
    paths = manifest["fixity_scope_paths"]

    assert paths == sorted(set(paths))
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_git_bytes(repo, "show", f"{governed_commit}:{path}"))
        digest.update(b"\0")

    assert digest.hexdigest() == manifest["fixity_sha256"]


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_manifest_governed_commit_remains_in_release_history():
    repo = _repo_root()
    manifest = json.loads((repo / MANIFEST_PATH).read_text(encoding="utf-8"))
    governed_commit = manifest["repository_commit"]

    assert _git_text(repo, "cat-file", "-t", governed_commit) == "commit"
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "merge-base",
            "--is-ancestor",
            governed_commit,
            "HEAD",
        ],
        check=False,
        capture_output=True,
    )
    assert result.returncode == 0, (
        "MAN-000000001 requires a history-preserving merge; squash or rebase "
        "would sever the released Manifest from its governed source commit."
    )


def test_manifest_dependency_order_preserves_outer_before_inner():
    manifest = json.loads(
        (_repo_root() / MANIFEST_PATH).read_text(encoding="utf-8")
    )

    assert set(manifest["dependency_graph"]) == {
        "HOC-000000001",
        "IAR-000000001",
    }
    assert "IAR-000000001" in manifest["dependency_graph"]["HOC-000000001"]
    assert "HOC-000000001" not in manifest["dependency_graph"]["IAR-000000001"]
    assert any(
        "Neo4j projection is neither included nor authorized" in conflict
        for conflict in manifest["known_conflicts"]
    )
