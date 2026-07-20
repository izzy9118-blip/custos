from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    """Noncanonical development outcomes for LC-004 evaluation."""

    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_MINUTE_VARIATION_CONTRADICTION = (
        "CANDIDATE_MINUTE_VARIATION_CONTRADICTION"
    )
    CORROBORATED_MINUTE_VARIATION_CONTRADICTION = (
        "CORROBORATED_MINUTE_VARIATION_CONTRADICTION"
    )


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_formulation: str = Field(min_length=1)
    source_example_status: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_source_pages(self):
        if any(page < 1 for page in self.source_pages):
            raise ValueError("Source pages must be positive integers")
        if len(set(self.source_pages)) != len(self.source_pages):
            raise ValueError("Source pages must be unique")
        return self


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
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=4)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_lc004_identity(self):
        if self.technique_key != "LC-004":
            raise ValueError("This package operationalizes LC-004 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class TextualDifference(StrictModel):
    operation: Literal["ADDITION", "OMISSION"]
    expression: str = Field(min_length=1)
    earlier_form: str
    later_form: str
    alignment_location: str = Field(min_length=1)
    minute_relative_to_shared_text: bool
    semantic_effect: str = Field(min_length=1)
    semantic_effect_documented: bool


class LC004EvaluationInput(StrictModel):
    earlier_statement_id: str = Field(min_length=1)
    later_statement_id: str = Field(min_length=1)
    earlier_text: str = Field(min_length=1)
    later_text: str = Field(min_length=1)
    earlier_proposition: str = Field(min_length=1)
    later_proposition: str = Field(min_length=1)
    same_work: bool
    same_subject: bool
    parallel_relation_documented: bool
    later_presents_as_repetition: bool
    differences: list[TextualDifference] = Field(default_factory=list)
    substantive_contradiction_established: bool
    source_integrity_confirmed: bool
    local_contexts_reconstructed: bool
    speaker_or_voice_resolved: bool
    word_alignment_complete: bool
    proposition_normalization_documented: bool
    translation_and_variant_review_complete: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_pair(self):
        if self.earlier_statement_id == self.later_statement_id:
            raise ValueError("Earlier and later statement identifiers must differ")
        return self


class LC004EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-004$")
    outcome: LocalEvaluationOutcome
    earlier_statement_id: str = Field(min_length=1)
    later_statement_id: str = Field(min_length=1)
    recorded_differences: list[TextualDifference] = Field(default_factory=list)
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    wording_difference_alone_treated_as_contradiction: bool = False
    earlier_statement_rejected: bool = False
    later_statement_rejected: bool = False
    true_statement_selected: None = None
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-004 evaluation may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-004 evaluation may not infer authorial intention")
        if self.wording_difference_alone_treated_as_contradiction:
            raise ValueError(
                "A wording difference alone may not be treated as a contradiction"
            )
        if self.earlier_statement_rejected or self.later_statement_rejected:
            raise ValueError("LC-004 may not reject either statement")
        if self.true_statement_selected is not None:
            raise ValueError("LC-004 evaluation may not select the true statement")
        return self
