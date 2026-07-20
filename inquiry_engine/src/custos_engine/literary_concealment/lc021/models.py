from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL = (
        "CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL"
    )
    CORROBORATED_INAPPROPRIATE_EXPRESSION_SIGNAL = (
        "CORROBORATED_INAPPROPRIATE_EXPRESSION_SIGNAL"
    )


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_mechanism: str = Field(min_length=1)
    documentary_limit: str = Field(min_length=1)


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
    def enforce_identity(self):
        if self.technique_key != "LC-021":
            raise ValueError("This package operationalizes LC-021 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class FitBaselineRecord(StrictModel):
    baseline_id: str = Field(min_length=1)
    baseline_type: Literal[
        "LOCAL_GRAMMAR",
        "AUTHORIAL_USAGE",
        "PARALLEL_PASSAGE",
        "SOURCE_LANGUAGE_USAGE",
        "TECHNICAL_VOCABULARY",
        "GENRE_CONVENTION",
        "SOURCE_TEXT",
        "OTHER",
    ]
    expected_fit: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    historically_appropriate: bool
    scope_relevant: bool


class ExpressionMismatchRecord(StrictModel):
    expression_id: str = Field(min_length=1)
    expression_text: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    textual_boundary: str = Field(min_length=1)
    local_sentence_or_clause: str = Field(min_length=1)
    source_language_form: str | None = None
    mismatch_type: Literal[
        "LEXICAL",
        "SEMANTIC",
        "GRAMMATICAL",
        "REGISTER",
        "PRAGMATIC",
        "TECHNICAL",
        "CONTEXTUAL",
        "OTHER",
    ]
    mismatch_description: str = Field(min_length=1)
    mismatch_documented: bool
    materially_disrupts_surface_reading: bool
    functions_as_stumbling_block: bool
    stumbling_block_support: list[str] = Field(default_factory=list)


class AttentionQuestionRecord(StrictModel):
    question_id: str = Field(min_length=1)
    question_text: str = Field(min_length=1)
    target_textual_problem: str = Field(min_length=1)
    bounded_by_expression: bool
    asserts_hidden_answer: bool = False


class AlternativeExplanationRecord(StrictModel):
    alternative_id: str = Field(min_length=1)
    explanation_type: Literal[
        "IDIOM",
        "ARCHAIC_OR_DIALECTAL_USAGE",
        "TECHNICAL_USAGE",
        "TRANSLATION",
        "GRAMMATICAL_NECESSITY",
        "RHETORICAL_STYLE",
        "GENRE",
        "SPEAKER_CHARACTERIZATION",
        "QUOTED_SOURCE",
        "TEXTUAL_VARIANT_OR_CORRUPTION",
        "REVISION_OR_IMPRECISION",
        "MISTAKEN_BASELINE",
        "MERELY_INAPPROPRIATE",
        "OTHER",
    ]
    explanation: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    tested: bool
    remains_viable: bool


class LC021EvaluationInput(StrictModel):
    inquiry_id: str = Field(min_length=1)
    baseline: FitBaselineRecord
    expression: ExpressionMismatchRecord
    question: AttentionQuestionRecord
    alternatives: list[AlternativeExplanationRecord] = Field(default_factory=list)
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    authorial_usage_review_complete: bool
    genre_and_technical_usage_review_complete: bool
    adjacent_technique_review_complete: bool
    evidence_path_complete: bool
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_records(self):
        if self.question.asserts_hidden_answer:
            raise ValueError("The attention question may not assert a hidden answer")
        alternative_ids = [item.alternative_id for item in self.alternatives]
        if len(set(alternative_ids)) != len(alternative_ids):
            raise ValueError("Alternative identifiers must be unique")
        return self


class LC021EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-021$")
    outcome: LocalEvaluationOutcome
    inquiry_id: str = Field(min_length=1)
    baseline: FitBaselineRecord
    expression: ExpressionMismatchRecord
    question: AttentionQuestionRecord
    alternatives: list[AlternativeExplanationRecord]
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    evidentiary_force: Literal["WEAK_POSSIBLE_SIGNAL"] = "WEAK_POSSIBLE_SIGNAL"
    inquiry_compelled_as_contradiction: bool = False
    hidden_meaning_inferred: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    concealment_proven: bool = False
    doctrinal_truth_selected: bool = False
    merely_inappropriate_excluded_with_certainty: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.inquiry_compelled_as_contradiction:
            raise ValueError("LC-021 may not compel inquiry as strongly as contradiction")
        if self.hidden_meaning_inferred:
            raise ValueError("LC-021 may not infer hidden meaning")
        if self.authorial_intention_inferred:
            raise ValueError("LC-021 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-021 may not infer intended audience")
        if self.concealment_proven:
            raise ValueError("LC-021 may not prove concealment")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-021 may not select doctrinal truth")
        if self.merely_inappropriate_excluded_with_certainty:
            raise ValueError(
                "LC-021 must preserve the possibility of mere inappropriateness"
            )
        return self
