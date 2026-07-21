import subprocess
from pathlib import Path

import pytest

from custos_engine.graph.repository_projector import RepositoryProjectionBuilder
from custos_engine.repository.github_reader import LocalGitReader


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def projection_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    assignment_root = repo / "ledgers/identifier-assignment-ledger/assignments"
    _write(
        assignment_root / "SPEC-000000001.yaml",
        'identifier: "SPEC-000000001"\nassigned_class: "Specification"\nassignment_status: "ASSIGNED"\n',
    )
    _write(
        assignment_root / "VAL-000000001.yaml",
        'identifier: "VAL-000000001"\nassigned_class: "Validation"\nassignment_status: "ASSIGNED"\n',
    )
    _write(
        repo / "records/specifications/SPEC-000000001.yaml",
        'identifier: "SPEC-000000001"\nclass: "Specification"\ntitle: "Governed specification"\nversion: "1.0"\nvalidation_record_ids: ["VAL-000000001"]\n',
    )
    _write(
        repo / "records/validations/VAL-000000001.yaml",
        'identifier: "VAL-000000001"\nclass: "Validation Record"\ntitle: "Validation"\n',
    )
    _write(
        repo / "records/specifications/SPEC-999999999.yaml",
        'identifier: "SPEC-999999999"\nclass: "Specification"\n',
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "projection fixture")
    return repo, _git(repo, "rev-parse", "HEAD")


def test_repository_projection_uses_assigned_canonical_records(projection_repo):
    repo, commit = projection_repo

    plan = RepositoryProjectionBuilder(LocalGitReader(repo, commit)).build(
        "MAN-000000001"
    )

    assert [node.canonical_id for node in plan.nodes] == [
        "SPEC-000000001",
        "VAL-000000001",
    ]
    specification = plan.nodes[0]
    assert specification.properties["github_path"] == (
        "records/specifications/SPEC-000000001.yaml"
    )
    assert specification.properties["git_commit"] == commit
    assert len(specification.properties["source_fixity_sha256"]) == 64
    assert plan.source_file_count == 2
    assert len(plan.edges) == 1
    assert plan.edges[0].subject_id == "SPEC-000000001"
    assert plan.edges[0].object_id == "VAL-000000001"
    assert plan.edges[0].relationship_type == "VALIDATED_BY"
    assert plan.edges[0].derivative is True


def test_repository_projection_is_deterministic(projection_repo):
    repo, commit = projection_repo
    builder = RepositoryProjectionBuilder(LocalGitReader(repo, commit))

    first = builder.build("MAN-000000001")
    second = builder.build("MAN-000000001")

    assert first.model_dump(mode="json") == second.model_dump(mode="json")
