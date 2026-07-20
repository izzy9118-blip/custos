from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_QUOTATION_OMISSION = "CANDIDATE_QUOTATION_OMISSION"
    CORROBORATED_QUOTATION_OMISSION = "CORROBORATED_QUOTATION_OMISSION"


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
    distinctions: list[str] = Field(min_length=1)
    operational: OperationalRequirements
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=4)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_identity(self):
        if self.technique_key != "LC-015":
            raise ValueError("This package operationalizes LC-015 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class SourceWitnessRecord(StrictModel):
    source_id: str = Field(min_length=1)
    source_author: str = Field(min_length=1)
    source_work: str = Field(min_length=1)
    source_location: str = Field(min_length=1)
    source_text: str = Field(min_length=1)
    source_version: str = Field(min_length=1)
    source_language: str | None = None
    witness_support: list[str] = Field(min_length=1)


class QuotationRecord(StrictModel):
    quotation_id: str = Field(min_length=1)
    quotation_text: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    presents_as: Literal["DIRECT_QUOTATION", "CITATION", "IDENTIFIABLE_REPRODUCTION"]
    quotation_status_documented: bool
    speaker_or_source: str = Field(min_length=1)


class OmittedExpression(StrictModel):
    omission_id: str = Field(min_length=1)
    source_expression: str = Field(min_length=1)
    source_location_within_passage: str = Field(min_length=1)
    quotation_location_after_omission: str = Field(min_length=1)
    effect_type: Literal[
        "MEANING",
        "SCOPE",
        "QUALIFICATION",
        "ATTRIBUTION",
        "STATUS",
        "DOCTRINAL_FORCE",
        "OTHER",
    ]
    material_effect: str = Field(min_length=1)
    material_effect_documented: bool


class PropositionStatusRecord(StrictModel):
    layer: Literal["FULL_SOURCE", "SHORTENED_QUOTATION"]
    normalized_proposition: str = Field(min_length=1)
    attribution_status: str = Field(min_length=1)
    epistemic_or_rhetorical_status: str = Field(min_length=1)


class LC015EvaluationInput(StrictModel):
    case_id: str = Field(min_length=1)
    source: SourceWitnessRecord
    quotation: QuotationRecord
    omissions: list[OmittedExpression] = Field(default_factory=list)
    full_source_record: PropositionStatusRecord
    shortened_quotation_record: PropositionStatusRecord
    source_relation_confirmed: bool
    collation_complete: bool
    material_difference_established: bool
    source_integrity_confirmed: bool
    quotation_witness_integrity_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    source_language_review_complete: bool
    alternate_source_versions_review_complete: bool
    translation_and_variant_review_complete: bool
    quotation_boundary_confirmed: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)
    direct_intentionality_evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_layers_and_ids(self):
        if self.full_source_record.layer != "FULL_SOURCE":
            raise ValueError("full_source_record must have layer FULL_SOURCE")
        if self.shortened_quotation_record.layer != "SHORTENED_QUOTATION":
            raise ValueError(
                "shortened_quotation_record must have layer SHORTENED_QUOTATION"
            )
        ids = [item.omission_id for item in self.omissions]
        if len(set(ids)) != len(ids):
            raise ValueError("Omission identifiers must be unique")
        return self


class LC015EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-015$")
    outcome: LocalEvaluationOutcome
    case_id: str = Field(min_length=1)
    source: SourceWitnessRecord
    quotation: QuotationRecord
    omissions: list[OmittedExpression]
    full_source_record: PropositionStatusRecord
    shortened_quotation_record: PropositionStatusRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    preserved_intentionality_evidence: list[str] = Field(default_factory=list)
    deliberate_misquotation_proven: bool = False
    authorial_intention_inferred: bool = False
    concealment_proven: bool = False
    hidden_teaching_inferred: bool = False
    intended_reader_identified: bool = False
    fuller_source_selected_as_authorial_truth: bool = False
    shortened_quotation_rejected_as_false: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.deliberate_misquotation_proven:
            raise ValueError("v0.1 may not prove deliberate misquotation")
        if self.authorial_intention_inferred:
            raise ValueError("LC-015 may not infer authorial intention")
        if self.concealment_proven:
            raise ValueError("LC-015 may not prove concealment")
        if self.hidden_teaching_inferred:
            raise ValueError("LC-015 may not infer hidden teaching")
        if self.intended_reader_identified:
            raise ValueError("LC-015 may not identify intended readers")
        if self.fuller_source_selected_as_authorial_truth:
            raise ValueError("LC-015 may not select the source as authorial truth")
        if self.shortened_quotation_rejected_as_false:
            raise ValueError("LC-015 may not reject the quotation as false")
        return self
