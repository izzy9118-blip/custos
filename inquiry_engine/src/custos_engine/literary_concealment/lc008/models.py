from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_COMMON_WORD_SIGNAL = "CANDIDATE_COMMON_WORD_SIGNAL"
    CORROBORATED_COMMON_WORD_SIGNAL = "CORROBORATED_COMMON_WORD_SIGNAL"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_description: str = Field(min_length=1)


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
    def enforce_lc008_identity(self):
        if self.technique_key != "LC-008":
            raise ValueError("This package operationalizes LC-008 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class WordSignalRecord(StrictModel):
    word: str = Field(min_length=1)
    source_language_form: str | None = None
    sentence_text: str = Field(min_length=1)
    word_location: str = Field(min_length=1)
    commonness_evidence: list[str] = Field(default_factory=list)
    common_in_relevant_horizon: bool
    sentence_low_prominence: bool
    word_low_prominence: bool
    independent_trigger: str = Field(min_length=1)
    independent_trigger_documented: bool
    semantic_or_structural_effect: str = Field(min_length=1)
    effect_documented: bool
    counterfactual_rendering: str = Field(min_length=1)
    counterfactual_material_change: bool


class LC008EvaluationInput(StrictModel):
    passage_id: str = Field(min_length=1)
    signal: WordSignalRecord
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    morphology_and_syntax_review_complete: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    prominence_assessment_documented: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)


class LC008EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-008$")
    outcome: LocalEvaluationOutcome
    passage_id: str = Field(min_length=1)
    signal: WordSignalRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    hidden_meaning_inferred: bool = False
    authorial_intention_inferred: bool = False
    secret_audience_inferred: bool = False
    doctrinal_truth_selected: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-008 evaluation may not prove concealment")
        if self.hidden_meaning_inferred:
            raise ValueError("LC-008 evaluation may not infer hidden meaning")
        if self.authorial_intention_inferred:
            raise ValueError("LC-008 evaluation may not infer authorial intention")
        if self.secret_audience_inferred:
            raise ValueError("LC-008 evaluation may not infer a secret audience")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-008 evaluation may not select doctrinal truth")
        return self
