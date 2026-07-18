from __future__ import annotations

from enum import StrEnum

from pydantic import Field, model_validator

from .base import CanonicalReference, EpistemicClassification, StrictModel


class EvidenceType(StrEnum):
    DOCUMENTARY = "DOCUMENTARY"
    PROCEDURAL = "PROCEDURAL"
    COMPARATIVE = "COMPARATIVE"
    STRUCTURAL = "STRUCTURAL"
    REPOSITORY = "REPOSITORY"


class RelationshipAssertion(StrictModel):
    relationship_id: str = Field(pattern=r"^REL-[0-9]{9}$")
    subject: CanonicalReference
    predicate_id: str = Field(pattern=r"^PRD-[0-9]{9}$")
    object: CanonicalReference
    evidence_type: EvidenceType
    epistemic_classification: EpistemicClassification
    lifecycle_status: str
    supporting_evidence_record_ids: list[str] = Field(default_factory=list)
    source_relationship_ids: list[str] = Field(default_factory=list)
    governing_inference_rule_id: str | None = None

    @model_validator(mode="after")
    def inference_rules(self) -> "RelationshipAssertion":
        if self.epistemic_classification == EpistemicClassification.SUPPORTED_INFERENCE:
            if self.evidence_type != EvidenceType.PROCEDURAL:
                raise ValueError(
                    "Materialized inference must use PROCEDURAL evidence type"
                )
            if not self.source_relationship_ids:
                raise ValueError(
                    "Materialized inference requires source Relationship Assertions"
                )
            if not self.governing_inference_rule_id:
                raise ValueError(
                    "Materialized inference requires a governing inference rule"
                )
        return self
