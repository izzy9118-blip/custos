from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    """Noncanonical development outcomes for LC-002 evaluation."""

    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_UNEQUAL_PROMINENCE_PAIR = "CANDIDATE_UNEQUAL_PROMINENCE_PAIR"
    CORROBORATED_UNEQUAL_PROMINENCE_CONTRADICTION = (
        "CORROBORATED_UNEQUAL_PROMINENCE_CONTRADICTION"
    )


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_page: int = Field(ge=1)
    source_formulation: str = Field(min_length=1)
    source_example: str = Field(min_length=1)


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
    projection_status: str = Field(pattern=r"^DEVELOPMENT_ONLY$")
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
    def enforce_lc002_identity(self):
        if self.technique_key != "LC-002":
            raise ValueError("This package operationalizes LC-002 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        return self


class LC002EvaluationInput(StrictModel):
    statement_a_id: str = Field(min_length=1)
    statement_b_id: str = Field(min_length=1)
    incidental_statement_id: str = Field(min_length=1)
    prominent_statement_id: str = Field(min_length=1)
    same_work: bool
    same_subject: bool
    mutually_incompatible: bool
    incidental_placement_observed: bool
    other_statement_prominent: bool
    prominence_basis_documented: bool
    source_integrity_confirmed: bool
    local_contexts_reconstructed: bool
    speaker_or_voice_resolved: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_pair_roles(self):
        pair = {self.statement_a_id, self.statement_b_id}
        if len(pair) != 2:
            raise ValueError("LC-002 requires two distinct statement records")
        if self.incidental_statement_id not in pair:
            raise ValueError("incidental_statement_id must identify one statement in the pair")
        if self.prominent_statement_id not in pair:
            raise ValueError("prominent_statement_id must identify one statement in the pair")
        if self.incidental_statement_id == self.prominent_statement_id:
            raise ValueError("Incidental and prominent roles must belong to different statements")
        return self


class LC002EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-002$")
    outcome: LocalEvaluationOutcome
    incidental_statement_id: str = Field(min_length=1)
    prominent_statement_id: str = Field(min_length=1)
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    incidental_statement_preferred: bool = False
    true_statement_selected: None = None
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-002 evaluation may not prove concealment")
        if self.incidental_statement_preferred:
            raise ValueError("LC-002 may not prefer the incidental statement")
        if self.true_statement_selected is not None:
            raise ValueError("LC-002 evaluation may not select the true statement")
        return self
