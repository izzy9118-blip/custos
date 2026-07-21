from __future__ import annotations

import hashlib
import re
from typing import Any, Protocol, Sequence

from pydantic import Field

from custos_engine.models.artifacts import ProjectionManifest
from custos_engine.models.base import StrictModel
from custos_engine.models.reasoning import DocumentaryInput
from custos_engine.repository.github_reader import LocalGitReader


class DocumentaryGraph(Protocol):
    def projection_metadata(self, projection_id: str) -> dict[str, Any]: ...

    def documentary_nodes(
        self,
        projection_id: str,
        canonical_ids: Sequence[str],
    ) -> list[dict[str, Any]]: ...

    def related_documentary_nodes(
        self,
        projection_id: str,
        canonical_ids: Sequence[str],
        relationship_types: Sequence[str],
        limit: int,
    ) -> list[dict[str, Any]]: ...


class GraphRetrievalItem(StrictModel):
    canonical_id: str
    canonical_class: str
    github_path: str
    git_commit: str
    source_fixity_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_role: str = Field(pattern=r"^(PRIMARY|SECONDARY|REPOSITORY_CONTEXT)$")


class GraphRetrievedRelationship(StrictModel):
    seed_id: str
    relationship_type: str = Field(pattern=r"^[A-Z][A-Z0-9_]*$")
    source_field: str
    canonical_id: str


class GraphRetrievalReceipt(StrictModel):
    projection_id: str
    projection_integrity_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    git_commit: str
    cognitive_memory_manifest_id: str
    requested_canonical_ids: list[str]
    expanded_canonical_ids: list[str] = Field(default_factory=list)
    relationships: list[GraphRetrievedRelationship] = Field(default_factory=list)
    retrieved_items: list[GraphRetrievalItem]


class VerifiedGraphDocumentaryRetriever:
    """Turn graph-selected records into Git-verified reasoning evidence."""

    def __init__(
        self,
        graph: DocumentaryGraph,
        reader: LocalGitReader,
        projection: ProjectionManifest,
    ) -> None:
        self.graph = graph
        self.reader = reader
        self.projection = projection

    def _assert_snapshot(self) -> None:
        metadata = self.graph.projection_metadata(self.projection.projection_id)
        expected = {
            "projection_id": self.projection.projection_id,
            "repository_full_name": self.projection.repository_full_name,
            "git_commit": self.projection.git_commit,
            "cognitive_memory_manifest_id": self.projection.cognitive_memory_manifest_id,
            "integrity_sha256": self.projection.integrity_sha256,
            "projector_version": self.projection.projector_version,
        }
        mismatches = [
            key for key, value in expected.items() if metadata.get(key) != value
        ]
        if mismatches:
            raise ValueError(
                "Neo4j projection snapshot does not match its pinned Manifest: "
                + ", ".join(mismatches)
            )

    def retrieve(
        self,
        canonical_ids: Sequence[str],
        relationship_types: Sequence[str] = (),
        max_related: int = 50,
    ) -> tuple[list[DocumentaryInput], GraphRetrievalReceipt]:
        requested = list(dict.fromkeys(canonical_ids))
        if not requested:
            raise ValueError("Graph retrieval requires at least one canonical identifier")
        if len(requested) != len(canonical_ids):
            raise ValueError("Graph retrieval canonical identifiers must be unique")
        self._assert_snapshot()

        invalid_relationship_types = [
            value
            for value in relationship_types
            if not isinstance(value, str)
            or not re.fullmatch(r"[A-Z][A-Z0-9_]*", value)
        ]
        if invalid_relationship_types:
            raise ValueError(
                "Invalid graph relationship types: "
                + ", ".join(map(str, invalid_relationship_types))
            )
        if max_related <= 0 or max_related > 500:
            raise ValueError("graph max_related must be between 1 and 500")

        relationship_rows = []
        if relationship_types:
            relationship_rows = self.graph.related_documentary_nodes(
                self.projection.projection_id,
                requested,
                relationship_types,
                max_related,
            )
        relationships = [
            GraphRetrievedRelationship.model_validate(row)
            for row in relationship_rows
        ]
        expanded = sorted(
            {
                relationship.canonical_id
                for relationship in relationships
                if relationship.canonical_id not in requested
            }
        )
        selected = [*requested, *expanded]
        rows = self.graph.documentary_nodes(self.projection.projection_id, selected)
        by_requested = {row.get("requested_id"): row for row in rows}
        missing = sorted(
            canonical_id
            for canonical_id in selected
            if not by_requested.get(canonical_id, {}).get("canonical_id")
        )
        if missing:
            raise ValueError(
                "Neo4j projection lacks requested canonical entities: "
                + ", ".join(missing)
            )

        documentary_inputs: list[DocumentaryInput] = []
        receipt_items: list[GraphRetrievalItem] = []
        for canonical_id in selected:
            row = by_requested[canonical_id]
            if row.get("git_commit") != self.reader.resolved_commit:
                raise ValueError(
                    f"Graph entity {canonical_id} is not pinned to the governed Git commit"
                )
            if row.get("cognitive_memory_manifest_id") != self.projection.cognitive_memory_manifest_id:
                raise ValueError(
                    f"Graph entity {canonical_id} has the wrong cognitive-memory binding"
                )
            github_path = row.get("github_path")
            if not isinstance(github_path, str) or not github_path:
                raise ValueError(f"Graph entity {canonical_id} lacks a Git source path")
            text = self.reader.read_text(github_path)
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if digest != row.get("source_fixity_sha256"):
                raise ValueError(
                    f"Graph entity {canonical_id} failed canonical Git fixity verification"
                )
            role = row.get("source_role") or "REPOSITORY_CONTEXT"
            if role not in {"PRIMARY", "SECONDARY", "REPOSITORY_CONTEXT"}:
                raise ValueError(f"Invalid documentary source role for {canonical_id}: {role}")
            canonical_class = row.get("canonical_class")
            if not isinstance(canonical_class, str) or not canonical_class:
                raise ValueError(f"Graph entity {canonical_id} lacks a canonical class")
            citation_title = row.get("title")
            citation = (
                f"{citation_title} ({github_path}@{self.reader.resolved_commit})"
                if isinstance(citation_title, str) and citation_title
                else f"{canonical_id} ({github_path}@{self.reader.resolved_commit})"
            )
            documentary_inputs.append(
                DocumentaryInput(
                    evidence_id=canonical_id,
                    source_role=role,
                    citation=citation,
                    text=text,
                    source_fixity_sha256=digest,
                    source_entity_id=canonical_id,
                    note="Selected through Neo4j and revalidated against canonical Git.",
                )
            )
            receipt_items.append(
                GraphRetrievalItem(
                    canonical_id=canonical_id,
                    canonical_class=canonical_class,
                    github_path=github_path,
                    git_commit=self.reader.resolved_commit,
                    source_fixity_sha256=digest,
                    source_role=role,
                )
            )

        receipt = GraphRetrievalReceipt(
            projection_id=self.projection.projection_id,
            projection_integrity_sha256=self.projection.integrity_sha256,
            git_commit=self.reader.resolved_commit,
            cognitive_memory_manifest_id=self.projection.cognitive_memory_manifest_id,
            requested_canonical_ids=requested,
            expanded_canonical_ids=expanded,
            relationships=relationships,
            retrieved_items=receipt_items,
        )
        return documentary_inputs, receipt
