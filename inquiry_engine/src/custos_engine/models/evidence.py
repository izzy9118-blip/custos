from __future__ import annotations

from datetime import datetime, timezone

from pydantic import Field, model_validator

from .base import CanonicalReference, EpistemicClassification, StrictModel


class DocumentaryObservation(StrictModel):
    observation_id: str
    canonical_class: str = "Observation"
    source_passage: CanonicalReference
    witness: CanonicalReference
    location_ids: list[str] = Field(min_length=1)
    exact_feature: str = Field(min_length=1)
    context: str = Field(min_length=1)
    recovery_method: str = Field(min_length=1)
    epistemic_classification: EpistemicClassification = (
        EpistemicClassification.DOCUMENTED_FINDING
    )
    provenance_ids: list[str] = Field(min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def must_be_documented(self) -> "DocumentaryObservation":
        if self.epistemic_classification != EpistemicClassification.DOCUMENTED_FINDING:
            raise ValueError(
                "DocumentaryObservation must be classified DOCUMENTED_FINDING"
            )
        return self


class EvidenceRecord(StrictModel):
    evidence_record_id: str
    canonical_class: str = "Evidence Record"
    evidence_bearing_entity: CanonicalReference
    target_entity: CanonicalReference
    relevance_statement: str = Field(min_length=1)
    direct_or_derived: str = Field(pattern=r"^(DIRECT|DERIVED)$")
    epistemic_classification: EpistemicClassification
    provenance_ids: list[str] = Field(min_length=1)
    verified: bool = False

    @model_validator(mode="after")
    def derived_cannot_be_documented(self) -> "EvidenceRecord":
        if (
            self.direct_or_derived == "DERIVED"
            and self.epistemic_classification
            == EpistemicClassification.DOCUMENTED_FINDING
        ):
            raise ValueError(
                "Derived evidence cannot be classified DOCUMENTED_FINDING"
            )
        return self


class EvidenceChain(StrictModel):
    evidence_chain_id: str
    canonical_class: str = "Evidence Chain"
    target_entity: CanonicalReference
    ordered_evidence_record_ids: list[str] = Field(min_length=1)
    chain_statement: str = Field(min_length=1)
    complete: bool = False
    unresolved_gaps: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def completed_chain_has_no_gaps(self) -> "EvidenceChain":
        if self.complete and self.unresolved_gaps:
            raise ValueError("A complete EvidenceChain cannot retain unresolved gaps")
        return self
