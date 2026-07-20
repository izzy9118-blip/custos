from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_CLUMSY_TRANSITION_SIGNAL = "CANDIDATE_CLUMSY_TRANSITION_SIGNAL"
    CORROBORATED_CLUMSY_TRANSITION_SIGNAL = (
        "CORROBORATED_CLUMSY_TRANSITION_SIGNAL"
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
        if self.technique_key != "LC-022":
            raise ValueError("This package operationalizes LC-022 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class TextualUnitRecord(StrictModel):
    unit_id: str = Field(min_length=1)
    side: Literal["BEFORE", "AFTER"]
    witness_location: str = Field(min_length=1)
    unit_text: str = Field(min_length=1)
    reconstructed_subject_or_task: str = Field(min_length=1)
    reconstruction_support: list[str] = Field(default_factory=list)
    speaker_or_source: str = Field(min_length=1)


class TransitionBaselineRecord(StrictModel):
    baseline_id: str = Field(min_length=1)
    baseline_type: Literal[
        "LOCAL_ARGUMENT",
        "AUTHORIAL_PRACTICE",
        "PARALLEL_PASSAGE",
        "SOURCE_LANGUAGE_DISCOURSE",
        "GENRE_CONVENTION",
        "PROMISED_SEQUENCE",
        "OTHER",
    ]
    expected_transition: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    historically_appropriate: bool
    scope_relevant: bool


class TransitionMismatchRecord(StrictModel):
    transition_id: str = Field(min_length=1)
    boundary_location: str = Field(min_length=1)
    transition_expression: str
    adjacency_or_explicit_link_confirmed: bool
    mismatch_type: Literal[
        "ABRUPT_TOPIC_SHIFT",
        "MISSING_INTERMEDIATE_STEP",
        "DISCOURSE_MARKER_MISMATCH",
        "LEVEL_SHIFT",
        "SPEAKER_SHIFT",
        "STRUCTURAL_BREAK",
        "OTHER",
    ]
    mismatch_description: str = Field(min_length=1)
    mismatch_documented: bool
    materially_interrupts_continuity: bool
    material_structural_effect: str = Field(min_length=1)
    structural_effect_documented: bool
    functions_as_attention_directing_anomaly: bool
    attention_function_support: list[str] = Field(default_factory=list)


class StructuralQuestionRecord(StrictModel):
    question_id: str = Field(min_length=1)
    question_text: str = Field(min_length=1)
    target_relation_or_break: str = Field(min_length=1)
    bounded_by_transition: bool
    asserts_hidden_relation: bool = False


class AlternativeExplanationRecord(StrictModel):
    alternative_id: str = Field(min_length=1)
    explanation_type: Literal[
        "ORDINARY_TOPIC_CHANGE",
        "ELLIPSIS",
        "PEDAGOGY",
        "SUMMARY_THEN_NEW_SUBJECT",
        "GENRE_CONVENTION",
        "SPEAKER_OR_SOURCE_SHIFT",
        "RHETORICAL_ACCELERATION",
        "TRANSLATION",
        "EDITORIAL_SEGMENTATION",
        "TEXTUAL_DAMAGE",
        "COMPOSITE_SOURCE",
        "REVISION_OR_CLUMSINESS",
        "MISTAKEN_BASELINE",
        "MISTAKEN_BOUNDARY_OR_SUBJECT",
        "OTHER",
    ]
    explanation: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    tested: bool
    remains_viable: bool


class LC022EvaluationInput(StrictModel):
    inquiry_id: str = Field(min_length=1)
    before_unit: TextualUnitRecord
    after_unit: TextualUnitRecord
    baseline: TransitionBaselineRecord
    transition: TransitionMismatchRecord
    question: StructuralQuestionRecord
    alternatives: list[AlternativeExplanationRecord] = Field(default_factory=list)
    source_integrity_confirmed: bool
    transition_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_and_source_attribution_complete: bool
    source_language_review_complete: bool
    translation_paragraphing_and_variant_review_complete: bool
    authorial_transition_practice_review_complete: bool
    adjacent_technique_review_complete: bool
    evidence_path_complete: bool
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_records(self):
        if self.before_unit.side != "BEFORE":
            raise ValueError("before_unit must have side BEFORE")
        if self.after_unit.side != "AFTER":
            raise ValueError("after_unit must have side AFTER")
        if self.before_unit.unit_id == self.after_unit.unit_id:
            raise ValueError("Before and after units must have distinct identifiers")
        if self.question.asserts_hidden_relation:
            raise ValueError("The structural question may not assert a hidden relation")
        alternative_ids = [item.alternative_id for item in self.alternatives]
        if len(set(alternative_ids)) != len(alternative_ids):
            raise ValueError("Alternative identifiers must be unique")
        return self


class LC022EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-022$")
    outcome: LocalEvaluationOutcome
    inquiry_id: str = Field(min_length=1)
    before_unit: TextualUnitRecord
    after_unit: TextualUnitRecord
    baseline: TransitionBaselineRecord
    transition: TransitionMismatchRecord
    question: StructuralQuestionRecord
    alternatives: list[AlternativeExplanationRecord]
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    evidentiary_force: Literal["WEAK_POSSIBLE_SIGNAL"] = "WEAK_POSSIBLE_SIGNAL"
    inquiry_compelled_as_contradiction: bool = False
    concealed_relation_inferred: bool = False
    structural_break_declared_final: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    concealment_proven: bool = False
    doctrinal_truth_selected: bool = False
    mere_clumsiness_excluded_with_certainty: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.inquiry_compelled_as_contradiction:
            raise ValueError("LC-022 may not compel inquiry as strongly as contradiction")
        if self.concealed_relation_inferred:
            raise ValueError("LC-022 may not infer a concealed relation")
        if self.structural_break_declared_final:
            raise ValueError("LC-022 may not finally declare a structural break")
        if self.authorial_intention_inferred:
            raise ValueError("LC-022 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-022 may not infer intended audience")
        if self.concealment_proven:
            raise ValueError("LC-022 may not prove concealment")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-022 may not select doctrinal truth")
        if self.mere_clumsiness_excluded_with_certainty:
            raise ValueError("LC-022 must preserve the possibility of mere clumsiness")
        return self
