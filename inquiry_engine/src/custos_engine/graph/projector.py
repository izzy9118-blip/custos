from __future__ import annotations

from pydantic import Field

from custos_engine.models.base import StrictModel


class ProjectionNode(StrictModel):
    canonical_id: str
    canonical_class: str
    labels: list[str] = Field(min_length=1)
    properties: dict[str, object] = Field(default_factory=dict)


class ProjectionEdge(StrictModel):
    edge_key: str
    subject_id: str
    relationship_type: str
    object_id: str
    rel_id: str | None = None
    derivative: bool = True
    properties: dict[str, object] = Field(default_factory=dict)


class ProjectionPlan(StrictModel):
    git_commit: str
    cognitive_memory_manifest_id: str
    source_file_count: int = Field(default=0, ge=0)
    nodes: list[ProjectionNode] = Field(default_factory=list)
    edges: list[ProjectionEdge] = Field(default_factory=list)

    def deterministic(self) -> "ProjectionPlan":
        return ProjectionPlan(
            git_commit=self.git_commit,
            cognitive_memory_manifest_id=self.cognitive_memory_manifest_id,
            source_file_count=self.source_file_count,
            nodes=sorted(self.nodes, key=lambda node: node.canonical_id),
            edges=sorted(self.edges, key=lambda edge: edge.edge_key),
        )
