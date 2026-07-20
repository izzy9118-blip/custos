from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_SIGNIFICANT_OMISSION = "CANDIDATE_SIGNIFICANT_OMISSION"
    CORROBORATED_SIGNIFICANT_OMISSION = "CORROBORATED_SIGNIFICANT_OMISSION"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_formulation: str = Field(min_length=1)
    source_examples: list[str] = Field(min_length=1)
    source_documentary_function: str = Field(min_length=1)


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
    def enforce_lc014_identity(self):
        if self.technique_key != "LC-014":
            raise ValueError("This package operationalizes LC-014 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class ExpectationBaseline(StrictModel):
    baseline_id: str = Field(min_length=1)
    baseline_type: Literal[
        "RECOVERED_SOURCE",
        "PARALLEL_PASSAGE",
        "PROMISED_SCOPE",
        "ENUMERATION",
        "DEFINITION",
        "DOCTRINAL_FRAMEWORK",
        "GENRE_CONVENTION",
        "OTHER",
    ]
    expected_item: str = Field(min_length=1)
    basis_description: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    historically_appropriate: bool
    scope_relevant: bool


class OmissionRecord(StrictModel):
    bounded_unit_id: str = Field(min_length=1)
    bounded_unit_text: str = Field(min_length=1)
    textual_scope: str = Field(min_length=1)
    expected_item: str = Field(min_length=1)
    item_absent_in_relevant_witness: bool
    absence_verification: list[str] = Field(default_factory=list)
    omission_effect_type: Literal[
        "COMPLETENESS",
        "STATUS",
        "SCOPE",
        "ATTRIBUTION",
        "DOCTRINAL_FORCE",
        "OTHER",
    ]
    material_effect: str = Field(min_length=1)
    material_effect_documented: bool
    counterfactual_inclusion: str = Field(min_length=1)
    counterfactual_changes_passage: bool


class LC014EvaluationInput(StrictModel):
    omission_id: str = Field(min_length=1)
    baseline: ExpectationBaseline
    omission: OmissionRecord
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    doctrinal_scope_confirmed: bool
    speaker_or_voice_resolved: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    negative_search_complete_within_scope: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_expected_item_consistency(self):
        if self.baseline.expected_item != self.omission.expected_item:
            raise ValueError(
                "Expectation baseline and omission record must identify the same expected item"
            )
        return self


class LC014EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-014$")
    outcome: LocalEvaluationOutcome
    omission_id: str = Field(min_length=1)
    baseline: ExpectationBaseline
    omission: OmissionRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    deliberate_silence_proven: bool = False
    authorial_intention_inferred: bool = False
    missing_teaching_supplied: bool = False
    intended_reader_identified: bool = False
    exoteric_status_declared: bool = False
    doctrinal_truth_selected: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.deliberate_silence_proven:
            raise ValueError("LC-014 evaluation may not prove deliberate silence")
        if self.authorial_intention_inferred:
            raise ValueError("LC-014 evaluation may not infer authorial intention")
        if self.missing_teaching_supplied:
            raise ValueError("LC-014 evaluation may not supply the missing teaching")
        if self.intended_reader_identified:
            raise ValueError("LC-014 evaluation may not identify the intended reader")
        if self.exoteric_status_declared:
            raise ValueError("LC-014 evaluation may not declare a passage exoteric")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-014 evaluation may not select doctrinal truth")
        return self
