from datetime import datetime, timezone

import pytest

from custos_engine.graph.neo4j_projection import Neo4jProjectionStore
from custos_engine.graph.projector import ProjectionEdge, ProjectionNode, ProjectionPlan
from custos_engine.graph.queries import PROJECTION_CONSTRAINT_QUERY
from custos_engine.models.artifacts import ProjectionManifest


class FakeClient:
    def __init__(self):
        self.writes = []
        self.transactions = []
        self.read_rows = []

    def execute_write(self, query, parameters):
        self.writes.append((query, parameters))

    def execute_write_transaction(self, statements):
        self.transactions.append(list(statements))

    def execute_read(self, query, parameters):
        return self.read_rows


def _plan(edge_object_id="VAL-000000001"):
    return ProjectionPlan(
        git_commit="a" * 40,
        cognitive_memory_manifest_id="MAN-000000001",
        source_file_count=2,
        nodes=[
            ProjectionNode(
                canonical_id="SPEC-000000001",
                canonical_class="Specification",
                labels=["CanonicalEntity", "Specification"],
                properties={"github_path": "records/spec.yaml"},
            ),
            ProjectionNode(
                canonical_id="VAL-000000001",
                canonical_class="Validation",
                labels=["CanonicalEntity", "Validation"],
                properties={"github_path": "records/val.yaml"},
            ),
        ],
        edges=[
            ProjectionEdge(
                edge_key="edge-1",
                subject_id="SPEC-000000001",
                relationship_type="VALIDATED_BY",
                object_id=edge_object_id,
                properties={"source_field": "validation_record_id"},
            )
        ],
    )


def _manifest():
    return ProjectionManifest(
        projection_id="PRJ-000000001",
        repository_full_name="izzy9118-blip/custos",
        git_commit="a" * 40,
        cognitive_memory_manifest_id="MAN-000000001",
        projector_version="1.0.0",
        schema_versions={"projection_manifest": "1.0.0"},
        source_file_count=2,
        node_counts={"Specification": 1, "Validation": 1},
        relationship_counts={"VALIDATED_BY": 1},
        validation_status="PASS",
        integrity_sha256="b" * 64,
        build_timestamp=datetime(2026, 7, 20, tzinfo=timezone.utc),
    )


def test_projection_store_replaces_only_named_projection_in_one_transaction():
    client = FakeClient()

    Neo4jProjectionStore(client).replace(_plan(), _manifest())

    assert client.writes == [(PROJECTION_CONSTRAINT_QUERY, {})]
    assert len(client.transactions) == 1
    statements = client.transactions[0]
    assert len(statements) == 4
    assert statements[0][1] == {"projection_id": "PRJ-000000001"}
    assert len(statements[1][1]["nodes"]) == 2
    assert statements[2][1]["edges"][0]["properties"]["derivative"] is True
    assert statements[3][1]["metadata"]["integrity_sha256"] == "b" * 64
    assert isinstance(statements[3][1]["metadata"]["node_counts_json"], str)


def test_projection_store_rejects_missing_edge_endpoint():
    with pytest.raises(ValueError, match="Missing object node"):
        Neo4jProjectionStore(FakeClient()).replace(
            _plan(edge_object_id="VAL-999999999"),
            _manifest(),
        )


def test_projection_store_requires_exactly_one_snapshot():
    client = FakeClient()
    with pytest.raises(ValueError, match="exactly one"):
        Neo4jProjectionStore(client).projection_metadata("PRJ-000000001")


def test_projection_store_rejects_nested_neo4j_properties():
    plan = _plan()
    plan.nodes[0].properties["nested"] = {"not": "portable"}

    with pytest.raises(ValueError, match="not a Neo4j scalar"):
        Neo4jProjectionStore(FakeClient()).replace(plan, _manifest())
