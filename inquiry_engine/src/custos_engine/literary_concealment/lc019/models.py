from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_CONVENTIONAL_REPETITION_PATTERN = (
        "CANDIDATE_CONVENTIONAL_REPETITION_PATTERN"
    )
    CORROBORATED_CONVENTIONAL_REPETITION_PATTERN = (
        "CORROBORATED_CONVENTIONAL_REPETITION_PATTERN"
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
    source_documentary_function: str = Field(min_length=1)
    source_relationship: str = Field(min_length=1)


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
        if self.technique_key != "LC-019":
            raise ValueError("This package operationalizes LC-019 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class PropositionFamily(StrictModel):
    family_id: str = Field(min_length=1)
    normalized_proposition: str = Field(min_length=1)
    classification: Literal["CONVENTIONAL", "COUNTERPART"]
    classification_basis: list[str] = Field(default_factory=list)
    classification_independent_of_frequency: bool


class StatementOccurrence(StrictModel):
    occurrence_id: str = Field(min_length=1)
    family_id: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    passage_text: str = Field(min_length=1)
    occurrence_type: Literal[
        "DIRECT_STATEMENT",
        "PARAPHRASE",
        "IMPLICATION",
        "QUOTATION",
        "OBJECTION",
        "HYPOTHETICAL",
        "REPORTED_OPINION",
    ]
    speaker_or_source: str = Field(min_length=1)
    local_context: str = Field(min_length=1)
    architectonic_location: str = Field(min_length=1)
    normalized_scope: str = Field(min_length=1)
    modality_and_qualification: str = Field(min_length=1)
    family_link_documented: bool


class ContradictionRecord(StrictModel):
    relation_id: str = Field(min_length=1)
    conventional_family_id: str = Field(min_length=1)
    counterpart_family_id: str = Field(min_length=1)
    governing_scope: str = Field(min_length=1)
    contradiction_description: str = Field(min_length=1)
    contradiction_documented: bool
    qualification_scope_and_modality_aligned: bool


class RepetitionOpportunity(StrictModel):
    opportunity_id: str = Field(min_length=1)
    witness_or_structural_location: str = Field(min_length=1)
    opportunity_basis: str = Field(min_length=1)
    relevant_to_conventional_family: bool
    conventional_family_repeated_here: bool
    occurrence_id: str | None = None

    @model_validator(mode="after")
    def validate_occurrence_link(self):
        if self.conventional_family_repeated_here and not self.occurrence_id:
            raise ValueError(
                "Occupied repetition opportunity requires an occurrence identifier"
            )
        if not self.conventional_family_repeated_here and self.occurrence_id is not None:
            raise ValueError(
                "Unoccupied repetition opportunity must not carry an occurrence identifier"
            )
        return self


class LC019EvaluationInput(StrictModel):
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    families: list[PropositionFamily] = Field(min_length=2, max_length=2)
    contradiction: ContradictionRecord
    occurrences: list[StatementOccurrence] = Field(min_length=1)
    opportunities: list[RepetitionOpportunity] = Field(min_length=1)
    occurrence_index_complete_for_scope: bool
    inclusion_exclusion_rules_documented: bool
    opportunity_map_complete_for_scope: bool
    opportunity_rules_documented: bool
    distributed_across_multiple_contexts: bool
    source_integrity_confirmed: bool
    occurrence_witnesses_confirmed: bool
    speaker_and_source_attribution_complete: bool
    proposition_family_classification_complete: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    negative_search_complete_within_scope: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_structure(self):
        family_ids = [family.family_id for family in self.families]
        if len(set(family_ids)) != 2:
            raise ValueError("Exactly two unique proposition families are required")
        classes = {family.classification for family in self.families}
        if classes != {"CONVENTIONAL", "COUNTERPART"}:
            raise ValueError(
                "One conventional and one counterpart family are required"
            )
        conventional_id = next(
            family.family_id
            for family in self.families
            if family.classification == "CONVENTIONAL"
        )
        counterpart_id = next(
            family.family_id
            for family in self.families
            if family.classification == "COUNTERPART"
        )
        if self.contradiction.conventional_family_id != conventional_id:
            raise ValueError(
                "Contradiction record must identify the conventional family"
            )
        if self.contradiction.counterpart_family_id != counterpart_id:
            raise ValueError(
                "Contradiction record must identify the counterpart family"
            )

        occurrence_ids = [item.occurrence_id for item in self.occurrences]
        if len(set(occurrence_ids)) != len(occurrence_ids):
            raise ValueError("Occurrence identifiers must be unique")
        unknown_families = {
            item.family_id for item in self.occurrences
        } - set(family_ids)
        if unknown_families:
            raise ValueError("Every occurrence must refer to an indexed family")

        opportunity_ids = [item.opportunity_id for item in self.opportunities]
        if len(set(opportunity_ids)) != len(opportunity_ids):
            raise ValueError("Opportunity identifiers must be unique")

        known_occurrence_ids = set(occurrence_ids)
        unknown_occurrences = {
            item.occurrence_id
            for item in self.opportunities
            if item.occurrence_id is not None
        } - known_occurrence_ids
        if unknown_occurrences:
            raise ValueError(
                "Every occupied opportunity must refer to an indexed occurrence"
            )
        return self


class LC019EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-019$")
    outcome: LocalEvaluationOutcome
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    families: list[PropositionFamily]
    contradiction: ContradictionRecord
    occurrences: list[StatementOccurrence]
    opportunities: list[RepetitionOpportunity]
    occurrence_counts: dict[str, int]
    relevant_opportunity_count: int
    occupied_relevant_opportunity_count: int
    repetition_opportunity_coverage: float
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    frequent_view_declared_false: bool = False
    frequent_view_declared_exoteric: bool = False
    insincerity_inferred: bool = False
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    counterpart_declared_true: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.frequent_view_declared_false:
            raise ValueError("LC-019 may not declare the frequent view false")
        if self.frequent_view_declared_exoteric:
            raise ValueError("LC-019 may not declare the frequent view exoteric")
        if self.insincerity_inferred:
            raise ValueError("LC-019 may not infer insincerity")
        if self.concealment_proven:
            raise ValueError("LC-019 may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-019 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-019 may not infer intended audience")
        if self.counterpart_declared_true:
            raise ValueError("LC-019 may not declare the counterpart true")
        if not 0.0 <= self.repetition_opportunity_coverage <= 1.0:
            raise ValueError("Opportunity coverage must be between zero and one")
        return self
