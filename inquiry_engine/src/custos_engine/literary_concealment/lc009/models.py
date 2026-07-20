from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_SECRET_TERMINOLOGY_PATTERN = (
        "CANDIDATE_SECRET_TERMINOLOGY_PATTERN"
    )
    CORROBORATED_SECRET_TERMINOLOGY_PATTERN = (
        "CORROBORATED_SECRET_TERMINOLOGY_PATTERN"
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
    source_examples: list[str] = Field(min_length=1)
    source_example_note: str = Field(min_length=1)


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
    def enforce_lc009_identity(self):
        if self.technique_key != "LC-009":
            raise ValueError("This package operationalizes LC-009 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class OccurrenceRecord(StrictModel):
    occurrence_id: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    surface_form: str = Field(min_length=1)
    normalized_form: str = Field(min_length=1)
    source_language_form: str | None = None
    speaker_or_source: str = Field(min_length=1)
    local_context: str = Field(min_length=1)
    architectonic_location: str = Field(min_length=1)
    usage_class: Literal[
        "ORDINARY",
        "TECHNICAL",
        "AMBIGUOUS",
        "CANDIDATE_CODED",
        "UNRESOLVED",
    ]
    normalized_proposition: str = Field(min_length=1)
    candidate_function: str = Field(min_length=1)
    function_documented: bool


class LC009EvaluationInput(StrictModel):
    terminology_label: str = Field(min_length=1)
    candidate_term: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    occurrences: list[OccurrenceRecord] = Field(min_length=1)
    occurrence_index_complete_for_scope: bool
    variants_normalized: bool
    multiple_context_classes_present: bool
    stable_pattern_documented: bool
    pattern_nontrivial_beyond_frequency: bool
    source_integrity_confirmed: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    speaker_and_source_attribution_complete: bool
    local_contexts_reconstructed: bool
    architectonic_distribution_reconstructed: bool
    negative_cases_collected: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_occurrence_ids(self):
        ids = [occ.occurrence_id for occ in self.occurrences]
        if len(set(ids)) != len(ids):
            raise ValueError("Occurrence identifiers must be unique")
        return self


class LC009EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-009$")
    outcome: LocalEvaluationOutcome
    terminology_label: str = Field(min_length=1)
    candidate_term: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    occurrences: list[OccurrenceRecord]
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    hidden_meaning_inferred: bool = False
    authorial_intention_inferred: bool = False
    audience_inferred: bool = False
    doctrinal_truth_selected: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-009 evaluation may not prove concealment")
        if self.hidden_meaning_inferred:
            raise ValueError("LC-009 evaluation may not infer hidden meaning")
        if self.authorial_intention_inferred:
            raise ValueError("LC-009 evaluation may not infer authorial intention")
        if self.audience_inferred:
            raise ValueError("LC-009 evaluation may not infer audience")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-009 evaluation may not select doctrinal truth")
        return self
