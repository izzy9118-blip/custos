from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    """Noncanonical development outcomes for a structured candidate pair."""

    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_PAIR = "CANDIDATE_PAIR"
    CORROBORATED_CONTRADICTION = "CORROBORATED_CONTRADICTION"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_page: int = Field(ge=1)
    source_formulation: str = Field(min_length=1)
    source_symbol: str = Field(min_length=1)


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
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=1)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_lc001_identity(self):
        if self.technique_key != "LC-001":
            raise ValueError("This package operationalizes LC-001 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        return self


class LC001EvaluationInput(StrictModel):
    statement_a_id: str = Field(min_length=1)
    statement_b_id: str = Field(min_length=1)
    same_work: bool
    same_subject: bool
    mutually_incompatible: bool
    positionally_separated: bool
    source_integrity_confirmed: bool
    local_contexts_reconstructed: bool
    speaker_or_voice_resolved: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def prevent_self_pair(self):
        if self.statement_a_id == self.statement_b_id:
            raise ValueError("LC-001 requires two distinct statement records")
        return self


class LC001EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-001$")
    outcome: LocalEvaluationOutcome
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    true_statement_selected: None = None
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-001 evaluation may not prove concealment")
        if self.true_statement_selected is not None:
            raise ValueError("LC-001 evaluation may not select the true statement")
        return self
