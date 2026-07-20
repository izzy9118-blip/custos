from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    """Noncanonical development outcomes for LC-003 evaluation."""

    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_IMPLICATION_CONTRADICTION = "CANDIDATE_IMPLICATION_CONTRADICTION"
    CORROBORATED_IMPLICATION_CONTRADICTION = (
        "CORROBORATED_IMPLICATION_CONTRADICTION"
    )


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_formulation: str = Field(min_length=1)
    source_symbol: str = Field(min_length=1)
    source_examples: list[str] = Field(min_length=1)
    bracketed_proposition_note: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_source_pages(self):
        if any(page < 1 for page in self.source_pages):
            raise ValueError("Source pages must be positive integers")
        if len(set(self.source_pages)) != len(self.source_pages):
            raise ValueError("Source pages must be unique")
        return self


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
    local_evaluation_outcomes: list[LocalEvaluationOutcome] = Field(min_length=1)
    version_history: list[VersionRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_lc003_identity(self):
        if self.technique_key != "LC-003":
            raise ValueError("This package operationalizes LC-003 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        return self


class LC003EvaluationInput(StrictModel):
    anchor_statement_id: str = Field(min_length=1)
    bridge_statement_ids: list[str] = Field(min_length=1)
    contrary_statement_id: str = Field(min_length=1)
    anchor_proposition: str = Field(min_length=1)
    bridge_propositions: list[str] = Field(min_length=1)
    derived_implication: str = Field(min_length=1)
    contrary_proposition: str = Field(min_length=1)
    implication_rule: str = Field(min_length=1)
    same_work: bool
    bridge_chain_present: bool
    derived_implication_unpronounced: bool
    selected_contrary_directly_denies_anchor: bool
    contrary_denies_derived_implication: bool
    term_identity_or_equivalence_documented: bool
    implication_rule_validated: bool
    source_integrity_confirmed: bool
    local_contexts_reconstructed: bool
    speaker_or_voice_resolved: bool
    proposition_normalization_documented: bool
    derivation_provenance_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_chain_identity(self):
        ids = [
            self.anchor_statement_id,
            *self.bridge_statement_ids,
            self.contrary_statement_id,
        ]
        if len(set(ids)) != len(ids):
            raise ValueError("Anchor, bridge, and contrary statement identifiers must be distinct")
        if len(self.bridge_statement_ids) != len(self.bridge_propositions):
            raise ValueError("Each bridge statement must have exactly one normalized proposition")
        return self


class LC003EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-003$")
    outcome: LocalEvaluationOutcome
    anchor_statement_id: str = Field(min_length=1)
    bridge_statement_ids: list[str] = Field(min_length=1)
    contrary_statement_id: str = Field(min_length=1)
    derived_implication: str = Field(min_length=1)
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    derived_implication_treated_as_quote: bool = False
    anchor_statement_rejected: bool = False
    true_statement_selected: None = None
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-003 evaluation may not prove concealment")
        if self.derived_implication_treated_as_quote:
            raise ValueError("A reconstructed implication may not be treated as a quotation")
        if self.anchor_statement_rejected:
            raise ValueError("LC-003 may not reject the anchor statement")
        if self.true_statement_selected is not None:
            raise ValueError("LC-003 evaluation may not select the true statement")
        return self
