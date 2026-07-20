from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_CHAPTER_OPENING_SIGNAL = "CANDIDATE_CHAPTER_OPENING_SIGNAL"
    CORROBORATED_CHAPTER_OPENING_SIGNAL = "CORROBORATED_CHAPTER_OPENING_SIGNAL"


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
    source_investigative_requirement: str = Field(min_length=1)


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
        if self.technique_key != "LC-017":
            raise ValueError("This package operationalizes LC-017 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class ChapterOpeningRecord(StrictModel):
    chapter_id: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    chapter_boundary_confirmed: bool
    boundary_basis: list[str] = Field(default_factory=list)
    opening_text: str = Field(min_length=1)
    source_language_opening: str | None = None
    extraction_unit_count: int = Field(ge=1)
    extraction_unit_type: Literal["WORD", "TOKEN", "PHRASE"]
    first_authorial_expression_confirmed: bool
    editorial_paratext_excluded: bool
    local_context: str = Field(min_length=1)
    architectonic_location: str = Field(min_length=1)
    speaker_or_source: str = Field(min_length=1)


class OpeningRelationRecord(StrictModel):
    relation_id: str = Field(min_length=1)
    target_chapter_id: str = Field(min_length=1)
    relation_type_local_noncanonical: Literal[
        "SUBJECT_SIGNAL",
        "DIVISION_SIGNAL",
        "DOCTRINAL_RELATION",
        "SEQUENCE",
        "CONTRAST",
        "ARCHITECTONIC_CORRESPONDENCE",
        "OTHER",
    ]
    description: str = Field(min_length=1)
    opening_support: list[str] = Field(min_length=1)
    chapter_or_work_support: list[str] = Field(min_length=1)
    initial_placement_material_to_relation: bool
    relation_documented: bool


class LC017EvaluationInput(StrictModel):
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    openings: list[ChapterOpeningRecord] = Field(min_length=1)
    target_relation: OpeningRelationRecord
    opening_index_complete_for_scope: bool
    fixed_extraction_rule_documented: bool
    same_extraction_rule_applied: bool
    source_integrity_confirmed: bool
    chapter_boundaries_confirmed_for_scope: bool
    editorial_status_review_complete: bool
    local_contexts_reconstructed: bool
    architectonic_structure_reconstructed: bool
    speaker_and_source_attribution_complete: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    comparison_across_all_openings_complete: bool
    negative_cases_collected: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_index(self):
        ids = [item.chapter_id for item in self.openings]
        if len(set(ids)) != len(ids):
            raise ValueError("Chapter identifiers must be unique")
        if self.target_relation.target_chapter_id not in set(ids):
            raise ValueError("Target relation must refer to an indexed chapter")
        extraction_rules = {
            (item.extraction_unit_count, item.extraction_unit_type)
            for item in self.openings
        }
        if self.same_extraction_rule_applied and len(extraction_rules) != 1:
            raise ValueError(
                "All openings must use the same extraction rule when declared"
            )
        return self


class LC017EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-017$")
    outcome: LocalEvaluationOutcome
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    openings: list[ChapterOpeningRecord]
    target_relation: OpeningRelationRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    hidden_meaning_inferred: bool = False
    intended_meaning_selected: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    doctrinal_truth_selected: bool = False
    editorial_heading_treated_as_authorial: bool = False
    arbitrary_extraction_rule_used: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.hidden_meaning_inferred:
            raise ValueError("LC-017 may not infer hidden meaning")
        if self.intended_meaning_selected:
            raise ValueError("LC-017 may not select intended meaning")
        if self.authorial_intention_inferred:
            raise ValueError("LC-017 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-017 may not infer intended audience")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-017 may not select doctrinal truth")
        if self.editorial_heading_treated_as_authorial:
            raise ValueError("Editorial headings must not be treated as authorial openings")
        if self.arbitrary_extraction_rule_used:
            raise ValueError("Opening extraction must follow a fixed rule")
        return self
