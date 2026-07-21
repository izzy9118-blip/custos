import hashlib
import subprocess
from pathlib import Path

import pytest

from custos_engine.graph.documentary_retrieval import VerifiedGraphDocumentaryRetriever
from custos_engine.models.artifacts import ProjectionManifest
from custos_engine.repository.github_reader import LocalGitReader


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


class FakeGraph:
    def __init__(self, metadata, rows, related_rows=None):
        self.metadata = metadata
        self.rows = rows
        self.related_rows = related_rows or []

    def projection_metadata(self, projection_id):
        return self.metadata

    def documentary_nodes(self, projection_id, canonical_ids):
        wanted = set(canonical_ids)
        return [row for row in self.rows if row.get("requested_id") in wanted]

    def related_documentary_nodes(
        self, projection_id, canonical_ids, relationship_types, limit
    ):
        return self.related_rows[:limit]


@pytest.fixture
def retrieval_fixture(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    path = repo / "records/specifications/SPEC-000000001.yaml"
    path.parent.mkdir(parents=True)
    text = 'identifier: "SPEC-000000001"\nclass: "Specification"\ntitle: "Fixed source"\n'
    path.write_text(text, encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "fixed source")
    commit = _git(repo, "rev-parse", "HEAD")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    projection = ProjectionManifest(
        projection_id="PRJ-000000001",
        repository_full_name="izzy9118-blip/custos",
        git_commit=commit,
        cognitive_memory_manifest_id="MAN-000000001",
        projector_version="1.0.0",
        schema_versions={"projection_manifest": "1.0.0"},
        source_file_count=1,
        node_counts={"Specification": 1},
        relationship_counts={},
        validation_status="PASS",
        integrity_sha256="c" * 64,
    )
    metadata = {
        "projection_id": projection.projection_id,
        "repository_full_name": projection.repository_full_name,
        "git_commit": commit,
        "cognitive_memory_manifest_id": projection.cognitive_memory_manifest_id,
        "integrity_sha256": projection.integrity_sha256,
        "projector_version": projection.projector_version,
    }
    row = {
        "requested_id": "SPEC-000000001",
        "canonical_id": "SPEC-000000001",
        "canonical_class": "Specification",
        "github_path": "records/specifications/SPEC-000000001.yaml",
        "git_commit": commit,
        "cognitive_memory_manifest_id": "MAN-000000001",
        "source_fixity_sha256": digest,
        "source_role": "REPOSITORY_CONTEXT",
        "title": "Fixed source",
    }
    return LocalGitReader(repo, commit), projection, metadata, row, text


def test_graph_selection_is_revalidated_and_converted_to_documentary_input(
    retrieval_fixture,
):
    reader, projection, metadata, row, text = retrieval_fixture
    retriever = VerifiedGraphDocumentaryRetriever(
        FakeGraph(metadata, [row]), reader, projection
    )

    inputs, receipt = retriever.retrieve(["SPEC-000000001"])

    assert len(inputs) == 1
    assert inputs[0].evidence_id == "SPEC-000000001"
    assert inputs[0].source_role == "REPOSITORY_CONTEXT"
    assert inputs[0].text == text
    assert inputs[0].source_entity_id == "SPEC-000000001"
    assert receipt.projection_id == "PRJ-000000001"
    assert receipt.retrieved_items[0].source_fixity_sha256 == row["source_fixity_sha256"]


def test_graph_retrieval_rejects_stale_snapshot(retrieval_fixture):
    reader, projection, metadata, row, _ = retrieval_fixture
    metadata["integrity_sha256"] = "d" * 64

    with pytest.raises(ValueError, match="pinned Manifest"):
        VerifiedGraphDocumentaryRetriever(
            FakeGraph(metadata, [row]), reader, projection
        ).retrieve(["SPEC-000000001"])


def test_graph_retrieval_rejects_hash_mismatch(retrieval_fixture):
    reader, projection, metadata, row, _ = retrieval_fixture
    row["source_fixity_sha256"] = "e" * 64

    with pytest.raises(ValueError, match="fixity verification"):
        VerifiedGraphDocumentaryRetriever(
            FakeGraph(metadata, [row]), reader, projection
        ).retrieve(["SPEC-000000001"])


def test_graph_retrieval_rejects_missing_requested_entity(retrieval_fixture):
    reader, projection, metadata, _, _ = retrieval_fixture

    with pytest.raises(ValueError, match="lacks requested canonical entities"):
        VerifiedGraphDocumentaryRetriever(
            FakeGraph(metadata, [{"requested_id": "SPEC-000000001", "canonical_id": None}]),
            reader,
            projection,
        ).retrieve(["SPEC-000000001"])


def test_graph_retrieval_expands_only_declared_relationship_types(
    retrieval_fixture,
):
    reader, projection, metadata, row, _ = retrieval_fixture
    related_path = "records/validations/VAL-000000001.yaml"
    repo = reader.repo_root
    # Create a second immutable commit and bind a matching projection fixture to it.
    path = repo / related_path
    path.parent.mkdir(parents=True, exist_ok=True)
    related_text = 'identifier: "VAL-000000001"\nclass: "Validation Record"\n'
    path.write_text(related_text, encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "related source")
    commit = _git(repo, "rev-parse", "HEAD")
    projection = projection.model_copy(update={"git_commit": commit})
    metadata["git_commit"] = commit
    row["git_commit"] = commit
    related_row = {
        "requested_id": "VAL-000000001",
        "canonical_id": "VAL-000000001",
        "canonical_class": "Validation Record",
        "github_path": related_path,
        "git_commit": commit,
        "cognitive_memory_manifest_id": "MAN-000000001",
        "source_fixity_sha256": hashlib.sha256(
            related_text.encode("utf-8")
        ).hexdigest(),
        "source_role": "REPOSITORY_CONTEXT",
        "title": "Validation",
    }
    graph = FakeGraph(
        metadata,
        [row, related_row],
        related_rows=[
            {
                "seed_id": "SPEC-000000001",
                "relationship_type": "VALIDATED_BY",
                "source_field": "validation_record_ids",
                "canonical_id": "VAL-000000001",
            }
        ],
    )

    inputs, receipt = VerifiedGraphDocumentaryRetriever(
        graph, LocalGitReader(repo, commit), projection
    ).retrieve(
        ["SPEC-000000001"],
        relationship_types=["VALIDATED_BY"],
    )

    assert [item.evidence_id for item in inputs] == [
        "SPEC-000000001",
        "VAL-000000001",
    ]
    assert receipt.expanded_canonical_ids == ["VAL-000000001"]
    assert receipt.relationships[0].relationship_type == "VALIDATED_BY"
