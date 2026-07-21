from __future__ import annotations

import json
from typing import Any, Protocol, Sequence

from custos_engine.models.artifacts import ProjectionManifest

from .integrity import verify_edge_endpoints
from .projector import ProjectionPlan
from .queries import (
    CLEAR_PROJECTION_QUERY,
    DOCUMENTARY_NODES_QUERY,
    PROJECTION_CONSTRAINT_QUERY,
    PROJECTION_METADATA_QUERY,
    RELATED_DOCUMENTARY_NODES_QUERY,
    WRITE_EDGES_QUERY,
    WRITE_NODES_QUERY,
    WRITE_PROJECTION_METADATA_QUERY,
)


class GraphClient(Protocol):
    def execute_write(self, query: str, parameters: dict[str, Any]) -> None: ...

    def execute_write_transaction(
        self,
        statements: Sequence[tuple[str, dict[str, Any]]],
    ) -> None: ...

    def execute_read(
        self,
        query: str,
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]: ...


class Neo4jProjectionStore:
    """Replace and query one explicitly identified, rebuildable projection."""

    def __init__(self, client: GraphClient) -> None:
        self.client = client

    @staticmethod
    def _assert_property_map(properties: dict[str, object], label: str) -> None:
        for key, value in properties.items():
            if not isinstance(key, str) or not key:
                raise ValueError(f"{label} contains an invalid Neo4j property key")
            if value is None or isinstance(value, (str, int, float, bool)):
                continue
            if isinstance(value, list) and all(
                item is None or isinstance(item, (str, int, float, bool))
                for item in value
            ):
                continue
            raise ValueError(
                f"{label} property {key} is not a Neo4j scalar or scalar array"
            )

    @staticmethod
    def _node_rows(plan: ProjectionPlan, projection_id: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for node in plan.deterministic().nodes:
            rows.append(
                {
                    "projection_id": projection_id,
                    "canonical_id": node.canonical_id,
                    "canonical_class": node.canonical_class,
                    "projected_labels": node.labels,
                    **node.properties,
                }
            )
        return rows

    @staticmethod
    def _edge_rows(plan: ProjectionPlan, projection_id: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for edge in plan.deterministic().edges:
            rows.append(
                {
                    "subject_id": edge.subject_id,
                    "object_id": edge.object_id,
                    "properties": {
                        "projection_id": projection_id,
                        "edge_key": edge.edge_key,
                        "relationship_type": edge.relationship_type,
                        "rel_id": edge.rel_id,
                        "derivative": edge.derivative,
                        **edge.properties,
                    },
                }
            )
        return rows

    def replace(self, plan: ProjectionPlan, manifest: ProjectionManifest) -> None:
        deterministic = plan.deterministic()
        if deterministic.git_commit != manifest.git_commit:
            raise ValueError("Projection plan and Manifest git_commit differ")
        if deterministic.cognitive_memory_manifest_id != manifest.cognitive_memory_manifest_id:
            raise ValueError("Projection plan and Manifest cognitive-memory binding differ")
        endpoint_errors = verify_edge_endpoints(
            {node.canonical_id for node in deterministic.nodes},
            [edge.model_dump(mode="json") for edge in deterministic.edges],
        )
        if endpoint_errors:
            raise ValueError("Invalid projection endpoints: " + "; ".join(endpoint_errors))
        for node in deterministic.nodes:
            self._assert_property_map(
                node.properties,
                f"Projection node {node.canonical_id}",
            )
        for edge in deterministic.edges:
            self._assert_property_map(
                edge.properties,
                f"Projection edge {edge.edge_key}",
            )

        self.client.execute_write(PROJECTION_CONSTRAINT_QUERY, {})
        statements = [
            (CLEAR_PROJECTION_QUERY, {"projection_id": manifest.projection_id}),
            (
                WRITE_NODES_QUERY,
                {"nodes": self._node_rows(deterministic, manifest.projection_id)},
            ),
            (
                WRITE_EDGES_QUERY,
                {
                    "projection_id": manifest.projection_id,
                    "edges": self._edge_rows(deterministic, manifest.projection_id),
                },
            ),
            (
                WRITE_PROJECTION_METADATA_QUERY,
                {
                    "metadata": {
                        "projection_id": manifest.projection_id,
                        "repository_full_name": manifest.repository_full_name,
                        "git_commit": manifest.git_commit,
                        "cognitive_memory_manifest_id": manifest.cognitive_memory_manifest_id,
                        "projector_version": manifest.projector_version,
                        "schema_versions_json": json.dumps(
                            manifest.schema_versions, sort_keys=True
                        ),
                        "source_file_count": manifest.source_file_count,
                        "node_counts_json": json.dumps(
                            manifest.node_counts, sort_keys=True
                        ),
                        "relationship_counts_json": json.dumps(
                            manifest.relationship_counts, sort_keys=True
                        ),
                        "validation_status": manifest.validation_status,
                        "integrity_sha256": manifest.integrity_sha256,
                        "build_timestamp": manifest.build_timestamp.isoformat(),
                    }
                },
            ),
        ]
        self.client.execute_write_transaction(statements)

    def projection_metadata(self, projection_id: str) -> dict[str, Any]:
        rows = self.client.execute_read(
            PROJECTION_METADATA_QUERY,
            {"projection_id": projection_id},
        )
        if len(rows) != 1:
            raise ValueError(
                f"Expected exactly one Neo4j projection snapshot for {projection_id}"
            )
        return rows[0]

    def documentary_nodes(
        self,
        projection_id: str,
        canonical_ids: Sequence[str],
    ) -> list[dict[str, Any]]:
        unique_ids = list(dict.fromkeys(canonical_ids))
        if not unique_ids:
            return []
        return self.client.execute_read(
            DOCUMENTARY_NODES_QUERY,
            {"projection_id": projection_id, "canonical_ids": unique_ids},
        )

    def related_documentary_nodes(
        self,
        projection_id: str,
        canonical_ids: Sequence[str],
        relationship_types: Sequence[str],
        limit: int,
    ) -> list[dict[str, Any]]:
        if limit <= 0:
            raise ValueError("Related-document retrieval limit must be positive")
        return self.client.execute_read(
            RELATED_DOCUMENTARY_NODES_QUERY,
            {
                "projection_id": projection_id,
                "canonical_ids": list(dict.fromkeys(canonical_ids)),
                "relationship_types": list(dict.fromkeys(relationship_types)),
                "limit": limit,
            },
        )
