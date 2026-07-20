from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_HINT_PATH = "CANDIDATE_HINT_PATH"
    CORROBORATED_HINT_PATH = "CORROBORATED_HINT_PATH"


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
    strauss_distinction: str = Field(min_length=1)
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
    distinctions: list[str] = Field(min_length=1)
    operational: OperationalRequirements
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=4)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_identity(self):
        if self.technique_key != "LC-020":
            raise ValueError("This package operationalizes LC-020 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class HintCueRecord(StrictModel):
    cue_id: str = Field(min_length=1)
    cue_text: str = Field(min_length=1)
    witness_location: str = Field(min_length=1)
    textual_boundary: str = Field(min_length=1)
    source_language_form: str | None = None
    cue_type_local_noncanonical: Literal[
        "LEXICAL",
        "GRAMMATICAL",
        "REFERENTIAL",
        "ARCHITECTONIC",
        "OMISSIONAL",
        "CONTRASTIVE",
        "OTHER",
    ]
    directly_states_result: bool
    materially_guides_inquiry: bool
    material_guidance_description: str = Field(min_length=1)


class HintTargetRecord(StrictModel):
    target_id: str = Field(min_length=1)
    target_type: Literal[
        "CONTRADICTION_DISCOVERY",
        "CONTRADICTORY_STATEMENT_DISCERNMENT",
    ]
    target_description: str = Field(min_length=1)
    independently_documented: bool
    independent_evidence: list[str] = Field(default_factory=list)
    target_scope: str = Field(min_length=1)


class DiscoveryStep(StrictModel):
    step_id: str = Field(min_length=1)
    sequence_number: int = Field(ge=1)
    from_element: str = Field(min_length=1)
    to_element: str = Field(min_length=1)
    inference_description: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    supported: bool


class AlternativePathRecord(StrictModel):
    alternative_id: str = Field(min_length=1)
    alternative_target_or_explanation: str = Field(min_length=1)
    documentary_support: list[str] = Field(default_factory=list)
    tested: bool
    remains_viable: bool


class LC020EvaluationInput(StrictModel):
    inquiry_id: str = Field(min_length=1)
    cue: HintCueRecord
    target: HintTargetRecord
    discovery_steps: list[DiscoveryStep] = Field(min_length=1)
    alternative_paths: list[AlternativePathRecord] = Field(default_factory=list)
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    adjacent_technique_review_complete: bool
    alternative_target_testing_complete: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_path(self):
        step_ids = [step.step_id for step in self.discovery_steps]
        if len(set(step_ids)) != len(step_ids):
            raise ValueError("Discovery-step identifiers must be unique")
        sequence = [step.sequence_number for step in self.discovery_steps]
        if sequence != list(range(1, len(sequence) + 1)):
            raise ValueError(
                "Discovery steps must be ordered consecutively beginning with 1"
            )
        alternative_ids = [item.alternative_id for item in self.alternative_paths]
        if len(set(alternative_ids)) != len(alternative_ids):
            raise ValueError("Alternative-path identifiers must be unique")
        return self


class LC020EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-020$")
    outcome: LocalEvaluationOutcome
    inquiry_id: str = Field(min_length=1)
    cue: HintCueRecord
    target: HintTargetRecord
    discovery_steps: list[DiscoveryStep]
    alternative_paths: list[AlternativePathRecord]
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unsupported_step_ids: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    hidden_teaching_inferred: bool = False
    doctrinal_truth_selected: bool = False
    authorial_intention_inferred: bool = False
    intended_audience_inferred: bool = False
    concealment_proven: bool = False
    unlimited_association_used: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_boundary(self):
        if self.hidden_teaching_inferred:
            raise ValueError("LC-020 may not infer hidden teaching")
        if self.doctrinal_truth_selected:
            raise ValueError("LC-020 may not select doctrinal truth")
        if self.authorial_intention_inferred:
            raise ValueError("LC-020 may not infer authorial intention")
        if self.intended_audience_inferred:
            raise ValueError("LC-020 may not infer intended audience")
        if self.concealment_proven:
            raise ValueError("LC-020 may not prove concealment")
        if self.unlimited_association_used:
            raise ValueError("LC-020 requires a finite supported discovery path")
        return self
