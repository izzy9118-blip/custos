from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import Field, model_validator

from .base import (
    AuditEvent,
    EngineMode,
    InquiryState,
    StrictModel,
    TerminationReason,
)


class StateTransition(StrictModel):
    from_state: InquiryState | None = None
    to_state: InquiryState
    reason: str = Field(min_length=1)
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StateResult(StrictModel):
    completed: bool
    observations_created: list[str] = Field(default_factory=list)
    evidence_added: list[str] = Field(default_factory=list)
    hypotheses_created: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    next_state: InquiryState | None = None
    termination_reason: TerminationReason | None = None
    notes: dict[str, Any] = Field(default_factory=dict)


class InquiryRun(StrictModel):
    run_id: str = Field(min_length=1)
    mode: EngineMode
    initiating_question: str = Field(min_length=1)
    documentary_boundary: str = Field(min_length=1)
    repository_full_name: str = Field(pattern=r"^[^/]+/[^/]+$")
    git_commit: str = Field(min_length=7)
    cognitive_memory_manifest_id: str = Field(min_length=1)
    projection_manifest_id: str | None = None
    governing_specification_ids: list[str] = Field(min_length=1)
    source_entity_ids: list[str] = Field(default_factory=list)
    current_state: InquiryState = InquiryState.DOCUMENTARY_INTAKE
    state_history: list[StateTransition] = Field(default_factory=list)
    observation_ids: list[str] = Field(default_factory=list)
    hypothesis_ids: list[str] = Field(default_factory=list)
    evidence_chain_ids: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    termination_reason: TerminationReason | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audit_history: list[AuditEvent] = Field(default_factory=list)

    @model_validator(mode="after")
    def production_and_termination_rules(self) -> "InquiryRun":
        if self.mode == EngineMode.PRODUCTION and not self.projection_manifest_id:
            raise ValueError("PRODUCTION InquiryRun requires projection_manifest_id")
        if self.current_state == InquiryState.TERMINATED and not self.termination_reason:
            raise ValueError("TERMINATED InquiryRun requires termination_reason")
        return self


class TerminationRecord(StrictModel):
    run_id: str
    final_state: InquiryState = InquiryState.TERMINATED
    reason: TerminationReason
    explanation: str = Field(min_length=1)
    unresolved_questions: list[str] = Field(default_factory=list)
    incomplete_tasks: list[str] = Field(default_factory=list)
    evidence_exhausted: bool
    authorized_unit_completed: bool
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
