from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


CANONICAL_ID_PATTERN = r"^[A-Z]{2,5}-[0-9]{9}$"


class EngineMode(StrEnum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"


class InquiryState(StrEnum):
    DOCUMENTARY_INTAKE = "DOCUMENTARY_INTAKE"
    HORIZON_AUDIT = "HORIZON_AUDIT"
    INDEPENDENT_RECONSTRUCTION = "INDEPENDENT_RECONSTRUCTION"
    AUTHORIAL_AUTHORIZATION = "AUTHORIAL_AUTHORIZATION"
    PURPOSE_AUDIENCE_FUNCTION = "PURPOSE_AUDIENCE_FUNCTION"
    ARCHITECTURAL_MAPPING = "ARCHITECTURAL_MAPPING"
    PROBLEM_FORMATION = "PROBLEM_FORMATION"
    ADVERSARIAL_TESTING = "ADVERSARIAL_TESTING"
    PROGRESSIVE_DISCLOSURE = "PROGRESSIVE_DISCLOSURE"
    SYNTHESIS_LIMITATION = "SYNTHESIS_LIMITATION"
    CERTIFICATION_PREPARATION = "CERTIFICATION_PREPARATION"
    TERMINATED = "TERMINATED"


class EpistemicClassification(StrEnum):
    DOCUMENTED_FINDING = "DOCUMENTED_FINDING"
    SUPPORTED_INFERENCE = "SUPPORTED_INFERENCE"
    WORKING_HYPOTHESIS = "WORKING_HYPOTHESIS"
    UNRESOLVED_QUESTION = "UNRESOLVED_QUESTION"
    CONSTITUTIONAL_PRINCIPLE = "CONSTITUTIONAL_PRINCIPLE"


class TerminationReason(StrEnum):
    COMPLETED_AUTHORIZED_UNIT = "COMPLETED_AUTHORIZED_UNIT"
    EVIDENCE_EXHAUSTED = "EVIDENCE_EXHAUSTED"
    MISSING_SOURCE_BLOCK = "MISSING_SOURCE_BLOCK"
    UNDERDETERMINED = "UNDERDETERMINED"
    SCOPE_EXCEEDED = "SCOPE_EXCEEDED"
    MANIFEST_INVALID = "MANIFEST_INVALID"
    PROJECTION_INVALID = "PROJECTION_INVALID"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    AUTHORITY_STOP = "AUTHORITY_STOP"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class CanonicalReference(StrictModel):
    canonical_id: str = Field(pattern=CANONICAL_ID_PATTERN)
    canonical_class: str = Field(min_length=1)
    github_path: str | None = None
    git_commit: str | None = Field(default=None, min_length=7)
    version: str | None = None

    @field_validator("github_path")
    @classmethod
    def repository_relative_path(cls, value: str | None) -> str | None:
        if value and value.startswith("/"):
            raise ValueError("github_path must be repository-relative")
        if value and ".." in value.split("/"):
            raise ValueError("github_path may not contain parent traversal")
        return value


class AuditEvent(StrictModel):
    event_type: str = Field(min_length=1)
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str | None = None
    note: str = Field(min_length=1)
    data: dict[str, Any] = Field(default_factory=dict)
