from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_RARITY_PRESUMPTION = "CANDIDATE_RARITY_PRESUMPTION"
    CORROBORATED_RARITY_PRESUMPTION = "CORROBORATED_RARITY_PRESUMPTION"


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
    strauss_rule: str = Field(min_length=1)


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
        if self.technique_key != "LC-018":
            raise ValueError("This package operationalizes LC-018 only")
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
    classification: Literal["CONVENTIONAL", "UNCONVENTIONAL"]
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
    normalized_scope: str = Field(min_length=1)
    modality_and_qualification: str = Field(min_length=1)
    family_link_documented: bool


class ContradictionRecord(StrictModel):
    relation_id: str = Field(min_length=1)
    family_a_id: str = Field(min_length=1)
    family_b_id: str = Field(min_length=1)
    governing_scope: str = Field(min_length=1)
    contradiction_description: str = Field(min_length=1)
    contradiction_documented: bool
    qualification_scope_and_modality_aligned: bool


class LC018EvaluationInput(StrictModel):
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    families: list[PropositionFamily] = Field(min_length=2, max_length=2)
    contradiction: ContradictionRecord
    occurrences: list[StatementOccurrence] = Field(min_length=1)
    occurrence_index_complete_for_scope: bool
    inclusion_exclusion_rules_documented: bool
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
        if classes != {"CONVENTIONAL", "UNCONVENTIONAL"}:
            raise ValueError(
                "One conventional and one unconventional family are required"
            )
        if {
            self.contradiction.family_a_id,
            self.contradiction.family_b_id,
        } != set(family_ids):
            raise ValueError(
                "Contradiction record must refer to both proposition families"
            )
        occurrence_ids = [item.occurrence_id for item in self.occurrences]
        if len(set(occurrence_ids)) != len(occurrence_ids):
            raise ValueError("Occurrence identifiers must be unique")
        unknown = {
            item.family_id for item in self.occurrences
        } - set(family_ids)
        if unknown:
            raise ValueError("Every occurrence must refer to an indexed family")
        return self


class LC018EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-018$")
    outcome: LocalEvaluationOutcome
    pattern_id: str = Field(min_length=1)
    declared_scope: str = Field(min_length=1)
    families: list[PropositionFamily]
    contradiction: ContradictionRecord
    occurrences: list[StatementOccurrence]
    occurrence_counts: dict[str, int]
    less_frequent_family_id: str | None = None
    straussian_presumption_applicable: bool = False
    presumption_statement: str | None = None
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    doctrinal_truth_selected: bool = False
    final_authorial_preference_declared: bool = False
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.doctrinal_truth_selected:
            raise ValueError("LC-018 may not select doctrinal truth")
        if self.final_authorial_preference_declared:
            raise ValueError("LC-018 may not declare final authorial preference")
        if self.concealment_proven:
            raise ValueError("LC-018 may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-018 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-018 may not infer intended audience")
        if self.straussian_presumption_applicable:
            if not self.less_frequent_family_id or not self.presumption_statement:
                raise ValueError(
                    "Applicable presumption requires a less-frequent family and statement"
                )
        return self
