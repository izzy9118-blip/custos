from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class LocalEvaluationOutcome(StrEnum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    CANDIDATE_LEXICAL_AMBIGUITY = "CANDIDATE_LEXICAL_AMBIGUITY"
    CORROBORATED_LEXICAL_AMBIGUITY = "CORROBORATED_LEXICAL_AMBIGUITY"


class SourceExample(StrictModel):
    surface_statement: str = Field(min_length=1)
    possible_meanings: list[str] = Field(min_length=2)


class SourceProjection(StrictModel):
    authoritative_object_path: str = Field(min_length=1)
    authoritative_object_version: str = Field(min_length=1)
    authoritative_object_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    repository_commit: str = Field(min_length=7)
    primary_work: str = Field(min_length=1)
    primary_essay: str = Field(min_length=1)
    source_pages: list[int] = Field(min_length=1)
    source_formulation: str = Field(min_length=1)
    source_example: SourceExample


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
    def enforce_lc006_identity(self):
        if self.technique_key != "LC-006":
            raise ValueError("This package operationalizes LC-006 only")
        if self.canonical_identifier is not None:
            raise ValueError("No canonical identifier has been assigned")
        if len(set(self.local_evaluation_outcomes)) != len(
            self.local_evaluation_outcomes
        ):
            raise ValueError("Local evaluation outcomes must be unique")
        return self


class SenseCandidate(StrictModel):
    sense_id: str = Field(min_length=1)
    gloss: str = Field(min_length=1)
    documentary_attestation: list[str] = Field(default_factory=list)
    source_language_supported: bool
    syntactically_viable: bool
    locally_viable: bool
    rendered_passage: str = Field(min_length=1)
    normalized_proposition: str = Field(min_length=1)


class LC006EvaluationInput(StrictModel):
    passage_id: str = Field(min_length=1)
    passage_text: str = Field(min_length=1)
    lexical_item: str = Field(min_length=1)
    source_language_form: str | None = None
    senses: list[SenseCandidate] = Field(min_length=1)
    materially_distinct_propositions: bool
    source_integrity_confirmed: bool
    local_context_reconstructed: bool
    speaker_or_voice_resolved: bool
    morphology_and_syntax_review_complete: bool
    source_language_review_complete: bool
    translation_and_variant_review_complete: bool
    contextual_disambiguation_tested: bool
    evidence_path_complete: bool
    ordinary_alternatives_tested: list[str] = Field(default_factory=list)
    unresolved_ordinary_alternatives: list[str] = Field(default_factory=list)
    corroborating_indicators: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_sense_ids(self):
        ids = [sense.sense_id for sense in self.senses]
        if len(set(ids)) != len(ids):
            raise ValueError("Sense identifiers must be unique")
        return self


class LC006EvaluationResult(StrictModel):
    technique_key: str = Field(pattern=r"^LC-006$")
    outcome: LocalEvaluationOutcome
    passage_id: str = Field(min_length=1)
    lexical_item: str = Field(min_length=1)
    viable_senses: list[SenseCandidate] = Field(default_factory=list)
    rejected_senses: list[SenseCandidate] = Field(default_factory=list)
    reasons: list[str] = Field(min_length=1)
    authorized_next_actions: list[str] = Field(default_factory=list)
    unresolved_alternatives: list[str] = Field(default_factory=list)
    concealment_proven: bool = False
    authorial_intention_inferred: bool = False
    audience_differentiation_inferred: bool = False
    secret_terminology_inferred: bool = False
    true_sense_selected: None = None
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def enforce_noninterpretive_boundary(self):
        if self.concealment_proven:
            raise ValueError("LC-006 evaluation may not prove concealment")
        if self.authorial_intention_inferred:
            raise ValueError("LC-006 evaluation may not infer authorial intention")
        if self.audience_differentiation_inferred:
            raise ValueError("LC-006 evaluation may not infer audience differentiation")
        if self.secret_terminology_inferred:
            raise ValueError("LC-006 evaluation may not infer secret terminology")
        if self.true_sense_selected is not None:
            raise ValueError("LC-006 evaluation may not select the true sense")
        return self
