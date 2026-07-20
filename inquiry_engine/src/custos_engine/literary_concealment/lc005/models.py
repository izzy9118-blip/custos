from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE = (
        "CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE"
    )
    CORROBORATED_CREEPING_CONTRADICTION_SEQUENCE = (
        "CORROBORATED_CREEPING_CONTRADICTION_SEQUENCE"
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
    source_explanation: str = Field(min_length=1)
    source_example_status: str = Field(min_length=1)


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
    def enforce_lc005_identity(self):
        if self.technique_key != "LC-005":
            raise ValueError("This package operationalizes LC-005 only")
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
    intermediary_form: str
    final_form: str
    alignment_location: str = Field(min_length=1)
    minute_relative_to_shared_text: bool
    semantic_effect: str = Field(min_length=1)
    semantic_effect_documented: bool


class LC005EvaluationInput(StrictModel):
    first_statement_id: str = Field(min_length=1)
    intermediary_statement_id: str = Field(min_length=1)
    final_statement_id: str = Field(min_length=1)
    first_text: str = Field(min_length=1)
    intermediary_text: str = Field(min_length=1)
    final_text: str = Field(min_length=1)
    first_proposition: str = Field(min_length=1)
    intermediary_proposition: str = Field(min_length=1)
    final_proposition: str = Field(min_length=1)
    same_work: bool
    same_subject: bool
    sequence_order_confirmed: bool
    intermediary_compatible_with_first: bool
    final_repeats_intermediary: bool
    differences: list[TextualDifference] = Field(default_factory=list)
    final_contradicts_first: bool
    source_integrity_confirmed: bool
    local_contexts_reconstructed: bool
    speaker_or_voice_resolved: bool
    intermediary_final_alignment_complete: bool
    proposition_normalization_documented: bool
    transition_sequence_reconstructed: bool
    translation_and_variant_review_complete: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_distinct_sequence(self):
        ids = {
            self.first_statement_id,
            self.intermediary_statement_id,
            self.final_statement_id,
        }
        if len(ids) != 3:
            raise ValueError("The first, intermediary, and final statement identifiers must differ")
        return self


class LC005EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-005$")
    outcome: LocalEvaluationOutcome
    first_statement_id: str = Field(min_length=1)
    intermediary_statement_id: str = Field(min_length=1)
    final_statement_id: str = Field(min_length=1)
    recorded_differences: list[TextualDifference] = Field(default_factory=list)
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    intermediary_rejected: bool = False
    first_statement_rejected: bool = False
    final_statement_rejected: bool = False
    true_statement_selected: None = None
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-005 evaluation may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-005 evaluation may not infer authorial intention")
        if (
            self.intermediary_rejected
            or self.first_statement_rejected
            or self.final_statement_rejected
        ):
            raise ValueError("LC-005 may not reject any statement")
        if self.true_statement_selected is not None:
            raise ValueError("LC-005 evaluation may not select the true statement")
        return self
