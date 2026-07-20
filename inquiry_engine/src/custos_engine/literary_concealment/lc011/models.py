from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_IRONIC_DIVERGENCE = "CANDIDATE_IRONIC_DIVERGENCE"
    CORROBORATED_IRONIC_DIVERGENCE = "CORROBORATED_IRONIC_DIVERGENCE"


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
    def enforce_lc011_identity(self):
        if self.technique_key != "LC-011":
            raise ValueError("This package operationalizes LC-011 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class PropositionRecord(StrictModel):
    proposition_id: str = Field(min_length=1)
    layer: Literal["SURFACE", "CANDIDATE_NONLITERAL"]
    proposition: str = Field(min_length=1)
    textual_support: list[str] = Field(min_length=1)
    reconstruction_basis: str | None = None

    @model_validator(mode="after")
    def validate_reconstruction_basis(self):
        if self.layer == "CANDIDATE_NONLITERAL" and not self.reconstruction_basis:
            raise ValueError(
                "Candidate nonliteral propositions require a reconstruction basis"
            )
        if self.layer == "SURFACE" and self.reconstruction_basis is not None:
            raise ValueError(
                "Surface propositions must not carry a reconstruction basis"
            )
        return self


class IronyMarker(StrictModel):
    marker_id: str = Field(min_length=1)
    marker_type: Literal[
        "CONTEXTUAL_CONFLICT",
        "DRAMATIC_INCONGRUITY",
        "EXAGGERATION",
        "UNDERSTATEMENT",
        "PRAISE_OR_BLAME_MISMATCH",
        "REACTION",
        "ARCHITECTONIC_SIGNAL",
        "LEXICAL_SIGNAL",
        "SOURCE_COMPARISON",
        "OTHER",
    ]
    description: str = Field(min_length=1)
    documentary_support: list[str] = Field(min_length=1)
    supports_divergence: bool


class LC011EvaluationInput(StrictModel):
    remark_id: str = Field(min_length=1)
    remark_text: str = Field(min_length=1)
    surface: PropositionRecord
    candidate_nonliteral: PropositionRecord
    divergence_relation: str = Field(min_length=1)
    materially_distinct_propositions: bool
    markers: list[IronyMarker] = Field(default_factory=list)
    source_integrity_confirmed: bool
    textual_boundary_confirmed: bool
    local_context_reconstructed: bool
    architectonic_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    target_or_object_review_complete: bool
    literal_coherence_tested: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_layers_and_ids(self):
        if self.surface.layer != "SURFACE":
            raise ValueError("surface must have layer SURFACE")
        if self.candidate_nonliteral.layer != "CANDIDATE_NONLITERAL":
            raise ValueError(
                "candidate_nonliteral must have layer CANDIDATE_NONLITERAL"
            )
        if self.surface.proposition_id == self.candidate_nonliteral.proposition_id:
            raise ValueError("Surface and nonliteral proposition identifiers must differ")
        marker_ids = [marker.marker_id for marker in self.markers]
        if len(set(marker_ids)) != len(marker_ids):
            raise ValueError("Marker identifiers must be unique")
        return self


class LC011EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-011$")
    outcome: LocalEvaluationOutcome
    remark_id: str = Field(min_length=1)
    surface: PropositionRecord
    candidate_nonliteral: PropositionRecord
    supporting_markers: list[IronyMarker] = Field(default_factory=list)
    countermarkers: list[IronyMarker] = Field(default_factory=list)
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    irony_intended_proven: bool = False
    authorial_intention_inferred: bool = False
    hidden_teaching_inferred: bool = False
    intended_meaning_selected: bool = False
    authorial_position_selected: bool = False
    canonical_subtype_assigned: bool = False
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.irony_intended_proven:
            raise ValueError("LC-011 evaluation may not prove intended irony")
        if self.authorial_intention_inferred:
            raise ValueError("LC-011 evaluation may not infer authorial intention")
        if self.hidden_teaching_inferred:
            raise ValueError("LC-011 evaluation may not infer hidden teaching")
        if self.intended_meaning_selected:
            raise ValueError("LC-011 evaluation may not select intended meaning")
        if self.authorial_position_selected:
            raise ValueError("LC-011 evaluation may not select the author's position")
        if self.canonical_subtype_assigned:
            raise ValueError("The source does not authorize canonical irony subtypes")
        return self
