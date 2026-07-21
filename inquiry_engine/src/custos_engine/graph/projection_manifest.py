from __future__ import annotations

from custos_engine.models.artifacts import ProjectionManifest

from .integrity import sha256_hex
from .projector import ProjectionPlan


def build_projection_manifest(
    projection_id: str,
    repository_full_name: str,
    plan: ProjectionPlan,
    projector_version: str,
    schema_versions: dict[str, str],
) -> ProjectionManifest:
    deterministic = plan.deterministic()
    node_counts: dict[str, int] = {}
    for node in deterministic.nodes:
        node_counts[node.canonical_class] = node_counts.get(node.canonical_class, 0) + 1

    relationship_counts: dict[str, int] = {}
    for edge in deterministic.edges:
        relationship_counts[edge.relationship_type] = (
            relationship_counts.get(edge.relationship_type, 0) + 1
        )

    return ProjectionManifest(
        projection_id=projection_id,
        repository_full_name=repository_full_name,
        git_commit=plan.git_commit,
        cognitive_memory_manifest_id=plan.cognitive_memory_manifest_id,
        projector_version=projector_version,
        schema_versions=schema_versions,
        source_file_count=deterministic.source_file_count,
        node_counts=node_counts,
        relationship_counts=relationship_counts,
        validation_status="PASS",
        integrity_sha256=sha256_hex(deterministic.model_dump(mode="json")),
    )
