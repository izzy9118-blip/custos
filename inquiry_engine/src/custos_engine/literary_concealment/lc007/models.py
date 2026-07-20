from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_TWO_FACED_SPEECH = "CANDIDATE_TWO_FACED_SPEECH"
    CORROBORATED_TWO_FACED_SPEECH = "CORROBORATED_TWO_FACED_SPEECH"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_description: str = Field(min_length=1)
    source_relationship: str = Field(min_length=1)


class OperationalRequirements(StrictModel):
    trigger_conditions: list[str] = Field(min_length=1)
    minimum_evidence: list[str] = Field(min_length=1)
    corroboration_indicators: list[str] = Field(min_length=1)
    ordinary_alternatives: list[str] = Field(min_length=1)
    disqualifying_conditions: list[str] = Field(min_length=1)
    authorized_response: list[str] = Field(min_length=1)
    prohibited_inferences: list[str] = Field(min_length=1)
    uncertainty_rule: str = Field(min_length=1)
    termination_rule: str = Field(min_length=1)


class VersionRecord(StrictModel):
    version: str = Field(min_length=1)
    status: str = Field(min_length=1)
    change_note: str = Field(min_length=1)


class LiteraryConcealmentTechnique(StrictModel):
    projection_version: str = Field(min_length=1)
    projection_status: str = Field(pattern=r"^CERTIFIED_TECHNICAL_INTEGRATION$")
    technique_key: str = Field(pattern=r"^LC-[0-9]{3}$")
    canonical_identifier: None = None
    identifier_status: str = Field(pattern=r"^NOT_ASSIGNED$")
    name: str = Field(min_length=1)
    strauss_status: str = Field(min_length=1)
    source: SourceProjection
    mechanism: str = Field(min_length=1)
    investigative_requirement: str = Field(min_length=1)
    distinctions: list[str] = Field(min_length=1)
    operational: OperationalRequirements
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=4)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_lc007_identity(self):
        if self.technique_key != "LC-007":
            raise ValueError("This package operationalizes LC-007 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class ReadingRecord(StrictModel):
    reading_id: str = Field(min_length=1)
    face: Literal["EXTERIOR", "INTERIOR"]
    reading_summary: str = Field(min_length=1)
    normalized_proposition: str = Field(min_length=1)
    textual_support: list[str] = Field(min_length=1)
    communicative_function: str = Field(min_length=1)
    function_documented: bool
    audience_horizon: str = Field(min_length=1)
    audience_horizon_documented: bool
    same_verbal_surface_preserved: bool


class LC007EvaluationInput(StrictModel):
    passage_id: str = Field(min_length=1)
    passage_text: str = Field(min_length=1)
    exterior_reading: ReadingRecord
    interior_reading: ReadingRecord
    materially_distinct_readings: bool
    distinct_functions: bool
    distinct_audience_horizons: bool
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    genre_and_pedagogy_review_complete: bool
    translation_and_variant_review_complete: bool
    audience_evidence_review_complete: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_reading_roles(self):
        if self.exterior_reading.face != "EXTERIOR":
            raise ValueError("exterior_reading must have face EXTERIOR")
        if self.interior_reading.face != "INTERIOR":
            raise ValueError("interior_reading must have face INTERIOR")
        if self.exterior_reading.reading_id == self.interior_reading.reading_id:
            raise ValueError("Exterior and interior reading identifiers must differ")
        return self


class LC007EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-007$")
    outcome: LocalEvaluationOutcome
    passage_id: str = Field(min_length=1)
    exterior_reading: ReadingRecord
    interior_reading: ReadingRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    persecution_inferred: bool = False
    actual_reader_classification_inferred: bool = False
    exterior_reading_rejected: bool = False
    interior_reading_selected_as_true: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-007 evaluation may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-007 evaluation may not infer authorial intention")
        if self.persecution_inferred:
            raise ValueError("LC-007 evaluation may not infer persecution")
        if self.actual_reader_classification_inferred:
            raise ValueError("LC-007 may not classify actual readers without evidence")
        if self.exterior_reading_rejected:
            raise ValueError("LC-007 may not reject the exterior reading")
        if self.interior_reading_selected_as_true:
            raise ValueError("LC-007 may not select the interior reading as true")
        return self
