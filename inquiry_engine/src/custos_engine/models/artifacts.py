from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import Field

from .base import StrictModel


class CandidateArtifact(StrictModel):
    candidate_id: str
    declared_class: str = Field(min_length=1)
    title: str = Field(min_length=1)
    run_id: str
    content: dict[str, Any]
    documentary_basis_ids: list[str] = Field(default_factory=list)
    governing_specification_ids: list[str] = Field(default_factory=list)
    certification_status: str = "NOT_CERTIFIED"
    admission_status: str = "NOT_ADMITTED"


class ValidationIssue(StrictModel):
    code: str
    severity: str = Field(pattern=r"^(ERROR|WARNING|INFO)$")
    message: str
    field_path: str | None = None


class ValidationReport(StrictModel):
    validation_id: str
    target_id: str
    valid: bool
    issues: list[ValidationIssue] = Field(default_factory=list)
    validator_version: str = "0.1.0"
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProjectionManifest(StrictModel):
    projection_id: str
    repository_full_name: str = Field(pattern=r"^[^/]+/[^/]+$")
    git_commit: str = Field(min_length=7)
    cognitive_memory_manifest_id: str
    projector_version: str
    schema_versions: dict[str, str]
    source_file_count: int = Field(ge=0)
    node_counts: dict[str, int] = Field(default_factory=dict)
    relationship_counts: dict[str, int] = Field(default_factory=dict)
    validation_status: str = Field(pattern=r"^(PASS|FAIL|WARNING)$")
    integrity_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    build_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
