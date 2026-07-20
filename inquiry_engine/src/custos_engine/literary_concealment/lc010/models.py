from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_SOPHISTIC_STRUCTURE = "CANDIDATE_SOPHISTIC_STRUCTURE"
    CORROBORATED_SOPHISTIC_STRUCTURE = "CORROBORATED_SOPHISTIC_STRUCTURE"


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_formulation: str = Field(min_length=1)
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
    def enforce_lc010_identity(self):
        if self.technique_key != "LC-010":
            raise ValueError("This package operationalizes LC-010 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class PremiseRecord(StrictModel):
    premise_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    status: Literal["EXPLICIT", "RECONSTRUCTED"]
    witness_support: list[str] = Field(default_factory=list)
    reconstruction_basis: str | None = None

    @model_validator(mode="after")
    def validate_reconstruction_basis(self):
        if self.status == "RECONSTRUCTED" and not self.reconstruction_basis:
            raise ValueError("Reconstructed premises require a reconstruction basis")
        if self.status == "EXPLICIT" and self.reconstruction_basis is not None:
            raise ValueError("Explicit premises must not carry a reconstruction basis")
        return self


class InferenceStep(StrictModel):
    step_id: str = Field(min_length=1)
    from_ids: list[str] = Field(min_length=1)
    result_text: str = Field(min_length=1)
    rule_or_relation: str = Field(min_length=1)
    textually_explicit: bool


class DefectRecord(StrictModel):
    local_label_noncanonical: str = Field(min_length=1)
    description: str = Field(min_length=1)
    governing_standard: str = Field(min_length=1)
    documentary_support: list[str] = Field(min_length=1)
    defect_documented: bool
    materially_affects_support: bool
    corrected_argument_summary: str = Field(min_length=1)
    correction_changes_support: bool


class LC010EvaluationInput(StrictModel):
    argument_id: str = Field(min_length=1)
    argument_text: str = Field(min_length=1)
    premises: list[PremiseRecord] = Field(min_length=1)
    inference_steps: list[InferenceStep] = Field(min_length=1)
    conclusion_text: str = Field(min_length=1)
    defect: DefectRecord
    bounded_argument_reconstructed: bool
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    counterfactual_analysis_complete: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)
    direct_intentionality_evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_record_ids(self):
        premise_ids = [premise.premise_id for premise in self.premises]
        step_ids = [step.step_id for step in self.inference_steps]
        if len(set(premise_ids)) != len(premise_ids):
            raise ValueError("Premise identifiers must be unique")
        if len(set(step_ids)) != len(step_ids):
            raise ValueError("Inference-step identifiers must be unique")
        if set(premise_ids) & set(step_ids):
            raise ValueError("Premise and inference-step identifiers must not overlap")
        return self


class LC010EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-010$")
    outcome: LocalEvaluationOutcome
    argument_id: str = Field(min_length=1)
    defect: DefectRecord
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    preserved_intentionality_evidence: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    intentional_sophism_declared: bool = False
    hidden_teaching_inferred: bool = False
    authorial_position_selected: bool = False
    canonical_subtype_assigned: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-010 evaluation may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-010 evaluation may not infer authorial intention")
        if self.intentional_sophism_declared:
            raise ValueError("v0.1 may not declare a passage an intentional sophism")
        if self.hidden_teaching_inferred:
            raise ValueError("LC-010 evaluation may not infer hidden teaching")
        if self.authorial_position_selected:
            raise ValueError("LC-010 evaluation may not select the author's position")
        if self.canonical_subtype_assigned:
            raise ValueError("The source does not authorize canonical subtypes")
        return self
