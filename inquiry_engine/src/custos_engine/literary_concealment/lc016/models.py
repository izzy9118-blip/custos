from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_LEITMOTIF_PATTERN = "CANDIDATE_LEITMOTIF_PATTERN"
    CORROBORATED_LEITMOTIF_PATTERN = "CORROBORATED_LEITMOTIF_PATTERN"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_description: str = Field(min_length=1)
    source_mechanism: str = Field(min_length=1)
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
    def enforce_identity(self):
        if self.technique_key != "LC-016":
            raise ValueError("This package operationalizes LC-016 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class SourceQuotationRecord(StrictModel):
    source_id: str = Field(min_length=1)
    source_text: str = Field(min_length=1)
    source_author: str | None = None
    source_work: str | None = None
    source_location: str | None = None
    source_recovered: bool
    source_context_recovered: bool
    source_context: str | None = None

    @model_validator(mode="after")
    def validate_source_context(self):
        if self.source_recovered and not self.source_location:
            raise ValueError("Recovered source quotation requires a source location")
        if self.source_context_recovered and not self.source_context:
            raise ValueError("Recovered source context must be recorded")
        return self


class OccurrenceDifference(StrictModel):
    difference_id: str = Field(min_length=1)
    operation: Literal["ADDITION", "OMISSION", "SUBSTITUTION", "REORDERING"]
    expression: str = Field(min_length=1)
    source_form: str
    occurrence_form: str
    material_effect: str = Field(min_length=1)
    material_effect_documented: bool


class LeitmotifOccurrence(StrictModel):
    occurrence_id: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    occurrence_text: str = Field(min_length=1)
    form_type: Literal["EXACT", "ALTERED", "INCOMPLETE", "UNRESOLVED"]
    quotation_family_link_documented: bool
    local_context: str = Field(min_length=1)
    local_function: str = Field(min_length=1)
    architectonic_location: str = Field(min_length=1)
    speaker_or_source: str = Field(min_length=1)
    differences: list[OccurrenceDifference] = Field(default_factory=list)


class LC016EvaluationInput(StrictModel):
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    source_quotation: SourceQuotationRecord
    occurrences: list[LeitmotifOccurrence] = Field(min_length=1)
    same_work_or_scope: bool
    express_quotation_relation_confirmed: bool
    distributed_across_multiple_contexts: bool
    recurrence_nontrivial_beyond_frequency: bool
    occurrence_index_complete_for_scope: bool
    collation_complete: bool
    source_integrity_confirmed: bool
    occurrence_witnesses_confirmed: bool
    local_contexts_reconstructed: bool
    architectonic_distribution_reconstructed: bool
    speaker_and_source_attribution_complete: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    negative_search_complete_within_scope: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_occurrence_ids(self):
        ids = [item.occurrence_id for item in self.occurrences]
        if len(set(ids)) != len(ids):
            raise ValueError("Occurrence identifiers must be unique")
        difference_ids = [
            difference.difference_id
            for item in self.occurrences
            for difference in item.differences
        ]
        if len(set(difference_ids)) != len(difference_ids):
            raise ValueError("Difference identifiers must be unique across the pattern")
        return self


class LC016EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-016$")
    outcome: LocalEvaluationOutcome
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    source_quotation: SourceQuotationRecord
    occurrences: list[LeitmotifOccurrence]
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    hidden_significance_inferred: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    concealed_teaching_inferred: bool = False
    doctrinal_meaning_selected: bool = False
    occurrence_variants_silently_normalized: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.hidden_significance_inferred:
            raise ValueError("LC-016 may not infer hidden significance")
        if self.authorial_intention_inferred:
            raise ValueError("LC-016 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-016 may not infer intended audience")
        if self.concealed_teaching_inferred:
            raise ValueError("LC-016 may not infer concealed teaching")
        if self.doctrinal_meaning_selected:
            raise ValueError("LC-016 may not select doctrinal meaning")
        if self.occurrence_variants_silently_normalized:
            raise ValueError("Occurrence variants must remain separate evidence")
        return self
