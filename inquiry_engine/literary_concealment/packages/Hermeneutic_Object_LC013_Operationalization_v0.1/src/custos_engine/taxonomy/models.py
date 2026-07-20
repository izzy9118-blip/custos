from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_MOTTO_ALLUSION = "CANDIDATE_MOTTO_ALLUSION"
    CORROBORATED_MOTTO_ALLUSION = "CORROBORATED_MOTTO_ALLUSION"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_formulation: str = Field(min_length=1)
    source_mechanism: str = Field(min_length=1)
    source_documentary_function: str = Field(min_length=1)
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
    documentary_constraints: list[str] = Field(min_length=1)
    operational: OperationalRequirements
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=4)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_lc013_identity(self):
        if self.technique_key != "LC-013":
            raise ValueError("This package operationalizes LC-013 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class MottoSourceRecord(StrictModel):
    attribution: str = Field(min_length=1)
    source_text: str = Field(min_length=1)
    source_location: str | None = None
    source_context: str | None = None
    source_recovered: bool
    source_context_recovered: bool


class MottoRecord(StrictModel):
    motto_text: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    placement_type: Literal[
        "WHOLE_WORK",
        "BOOK",
        "PART",
        "CHAPTER",
        "SECTION",
        "OTHER_BOUNDED_DIVISION",
    ]
    governed_scope: str = Field(min_length=1)
    governed_scope_documented: bool
    present_in_authorially_relevant_witness: bool
    provenance_status: Literal[
        "AUTHORIAL",
        "AUTHORIALLY_ADOPTED",
        "EDITORIAL",
        "PUBLISHER_SUPPLIED",
        "TRANSLATOR_SUPPLIED",
        "LATER_HAND",
        "UNRESOLVED",
    ]
    provenance_evidence: list[str] = Field(default_factory=list)
    source: MottoSourceRecord
    surface_function: str = Field(min_length=1)
    surface_function_documented: bool


class AllusiveRelationRecord(StrictModel):
    relation_id: str = Field(min_length=1)
    relation_type_local_noncanonical: Literal[
        "LEXICAL_CORRESPONDENCE",
        "IMAGISTIC_CORRESPONDENCE",
        "STRUCTURAL_SEQUENCE",
        "CONTRAST",
        "QUALIFICATION",
        "SOURCE_CONTEXT_KEY",
        "OTHER",
    ]
    description: str = Field(min_length=1)
    motto_support: list[str] = Field(min_length=1)
    governed_scope_support: list[str] = Field(min_length=1)
    materially_specific_beyond_theme: bool
    relation_documented: bool


class LC013EvaluationInput(StrictModel):
    motto_id: str = Field(min_length=1)
    motto: MottoRecord
    relation: AllusiveRelationRecord
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    governed_scope_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    editorial_provenance_review_complete: bool
    comparison_index_complete_for_claimed_scope: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)


class LC013EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-013$")
    outcome: LocalEvaluationOutcome
    motto_id: str = Field(min_length=1)
    motto: MottoRecord
    relation: AllusiveRelationRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    hidden_key_declared: bool = False
    intended_meaning_selected: bool = False
    intended_audience_inferred: bool = False
    authorial_intention_inferred: bool = False
    doctrinal_truth_selected: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-013 evaluation may not prove concealment")
        if self.hidden_key_declared:
            raise ValueError("LC-013 evaluation may not declare a hidden key")
        if self.intended_meaning_selected:
            raise ValueError("LC-013 evaluation may not select intended meaning")
        if self.intended_audience_inferred:
            raise ValueError("LC-013 evaluation may not infer intended audience")
        if self.authorial_intention_inferred:
            raise ValueError("LC-013 evaluation may not infer authorial intention")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-013 evaluation may not select doctrinal truth")
        return self
