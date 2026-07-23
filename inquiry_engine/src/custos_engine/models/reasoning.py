from __future__ import annotations

from datetime import datetime, timezone

from pydantic import Field, field_validator, model_validator

from .base import (
    EpistemicClassification,
    InquiryState,
    StrictModel,
    TerminationReason,
)
from .taxonomy import TaxonomyComponent


class DocumentaryInput(StrictModel):
    """A fixed excerpt supplied to a field reasoner as documentary evidence."""

    evidence_id: str = Field(min_length=1)
    source_role: str = Field(pattern=r"^(PRIMARY|SECONDARY|REPOSITORY_CONTEXT)$")
    citation: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_fixity_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_entity_id: str | None = None
    note: str | None = None


class PhaseInstruction(StrictModel):
    sequence: int = Field(ge=1, le=37)
    instruction: str = Field(min_length=1)


class PhaseReasoningRequest(StrictModel):
    run_id: str = Field(min_length=1)
    repository_full_name: str = Field(pattern=r"^[^/]+/[^/]+$")
    git_commit: str = Field(min_length=7)
    cognitive_memory_manifest_id: str = Field(min_length=1)
    governing_specification_ids: list[str] = Field(min_length=1)
    state: InquiryState
    phase_number: int = Field(ge=1, le=10)
    phase_name: str = Field(min_length=1)
    instructions: list[PhaseInstruction] = Field(min_length=1)
    initiating_question: str = Field(min_length=1)
    documentary_boundary: str = Field(min_length=1)
    documentary_inputs: list[DocumentaryInput] = Field(min_length=1)
    prior_phase_summaries: list[str] = Field(default_factory=list)
    inner_sanctum_authorized: bool = True
    inner_sanctum_status: str = Field(
        default="ALWAYS_OPEN",
        pattern=r"^ALWAYS_OPEN$",
    )
    permitted_taxonomy_techniques: list[TaxonomyComponent] = Field(min_length=1)
    epistemic_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def always_open_taxonomy_contract(self) -> "PhaseReasoningRequest":
        evidence_ids = [item.evidence_id for item in self.documentary_inputs]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("Documentary input evidence identifiers must be unique")
        if not self.inner_sanctum_authorized:
            raise ValueError(
                "The Inner Sanctum is a mandatory always-open feature of text analysis"
            )
        return self


class CandidateStatement(StrictModel):
    candidate_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    epistemic_classification: EpistemicClassification
    evidence_record_ids: list[str] = Field(min_length=1)
    limitations: list[str] = Field(default_factory=list)

    @field_validator("epistemic_classification")
    @classmethod
    def candidate_only_classification(
        cls,
        value: EpistemicClassification,
    ) -> EpistemicClassification:
        prohibited = {
            EpistemicClassification.DOCUMENTED_FINDING,
            EpistemicClassification.CONSTITUTIONAL_PRINCIPLE,
        }
        if value in prohibited:
            raise ValueError(
                "A field reasoner may not create documented findings or constitutional principles"
            )
        return value

    @field_validator("evidence_record_ids")
    @classmethod
    def evidence_references_are_unique(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("Candidate evidence references must be unique")
        return value


class PhaseReasoningResponse(StrictModel):
    run_id: str = Field(min_length=1)
    state: InquiryState
    completed: bool
    summary: str = Field(min_length=1)
    candidate_statements: list[CandidateStatement] = Field(default_factory=list)
    ordinary_explanations: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    requested_taxonomy_technique_ids: list[str] = Field(default_factory=list)
    termination_reason: TerminationReason | None = None

    @field_validator("requested_taxonomy_technique_ids")
    @classmethod
    def technique_identifier_format(cls, value: list[str]) -> list[str]:
        invalid = [
            technique_id
            for technique_id in value
            if len(technique_id) != 6
            or not technique_id.startswith("LC-")
            or not technique_id[3:].isdigit()
        ]
        if invalid:
            raise ValueError(f"Invalid Taxonomy technique identifiers: {invalid}")
        return value

    @model_validator(mode="after")
    def completion_or_bounded_termination(self) -> "PhaseReasoningResponse":
        candidate_ids = [
            statement.candidate_id for statement in self.candidate_statements
        ]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("Candidate identifiers must be unique within a phase")
        if len(self.requested_taxonomy_technique_ids) != len(
            set(self.requested_taxonomy_technique_ids)
        ):
            raise ValueError("Requested Taxonomy technique identifiers must be unique")
        if self.completed and self.termination_reason is not None:
            raise ValueError("A completed phase cannot also request termination")
        if not self.completed and self.termination_reason is None:
            raise ValueError("An incomplete phase must state a termination reason")
        if self.termination_reason in {
            TerminationReason.COMPLETED_AUTHORIZED_UNIT,
            TerminationReason.MANIFEST_INVALID,
            TerminationReason.PROJECTION_INVALID,
            TerminationReason.VALIDATION_FAILED,
        }:
            raise ValueError(
                "A field reasoner may not claim completion or make infrastructure validity decisions"
            )
        return self


class PhaseReasoningRecord(StrictModel):
    record_id: str = Field(min_length=1)
    adapter_id: str = Field(min_length=1)
    request: PhaseReasoningRequest
    response: PhaseReasoningResponse
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
