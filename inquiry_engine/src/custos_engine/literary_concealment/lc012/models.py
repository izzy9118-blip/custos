from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_READER_ADDRESS_SIGNAL = "CANDIDATE_READER_ADDRESS_SIGNAL"
    CORROBORATED_READER_ADDRESS_SIGNAL = "CORROBORATED_READER_ADDRESS_SIGNAL"


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
    projection_status: str = Field(pattern=r"^CERTIFIED_TECHNICAL_INTEGRATION$")
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
    def enforce_lc012_identity(self):
        if self.technique_key != "LC-012":
            raise ValueError("This package operationalizes LC-012 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class ReaderAddressRecord(StrictModel):
    address_text: str = Field(min_length=1)
    source_language_form: str | None = None
    grammatical_form: Literal[
        "VOCATIVE",
        "IMPERATIVE",
        "SECOND_PERSON",
        "DIRECT_NOMINAL_ADDRESS",
        "OTHER",
    ]
    resolved_addressee: str = Field(min_length=1)
    addressee_is_reader: bool
    addressee_evidence: list[str] = Field(default_factory=list)
    placement: str = Field(min_length=1)
    placement_documented: bool
    local_function_label_noncanonical: str = Field(min_length=1)
    communicative_effect: str = Field(min_length=1)
    communicative_effect_documented: bool
    modifies_surrounding_exposition: bool


class LC012EvaluationInput(StrictModel):
    address_id: str = Field(min_length=1)
    address: ReaderAddressRecord
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    speaker_or_voice_resolved: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    genre_convention_review_complete: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    comparison_index_complete_for_claimed_scope: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)


class LC012EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-012$")
    outcome: LocalEvaluationOutcome
    address_id: str = Field(min_length=1)
    address: ReaderAddressRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    intended_reader_identified: bool = False
    differentiated_audience_inferred: bool = False
    hidden_instruction_inferred: bool = False
    authorial_intention_inferred: bool = False
    canonical_subtype_assigned: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-012 evaluation may not prove concealment")
        if self.intended_reader_identified:
            raise ValueError("LC-012 evaluation may not identify the intended reader")
        if self.differentiated_audience_inferred:
            raise ValueError("LC-012 may not infer differentiated audiences")
        if self.hidden_instruction_inferred:
            raise ValueError("LC-012 evaluation may not infer hidden instruction")
        if self.authorial_intention_inferred:
            raise ValueError("LC-012 evaluation may not infer authorial intention")
        if self.canonical_subtype_assigned:
            raise ValueError("The source does not authorize canonical subtypes")
        return self
