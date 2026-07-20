from __future__ import annotations

from datetime import date, datetime

from pydantic import Field, model_validator

from .base import CanonicalReference, EngineMode, StrictModel


class ManifestComponent(StrictModel):
    component: CanonicalReference
    certification_record_id: str
    integration_decision_id: str
    permitted_use: str = Field(min_length=1)
    prohibited_use: list[str] = Field(min_length=1)
    dependencies: list[str] = Field(default_factory=list)


class CognitiveMemoryManifest(StrictModel):
    manifest_id: str
    version: str
    release_status: str = Field(pattern=r"^(DEVELOPMENT|RELEASED|WITHDRAWN)$")
    repository_full_name: str = Field(pattern=r"^[^/]+/[^/]+$")
    repository_commit: str = Field(min_length=7)
    governing_specification_ids: list[str] = Field(min_length=1)
    taxonomy_source: CanonicalReference
    procedure_source: CanonicalReference
    included_components: list[ManifestComponent] = Field(default_factory=list)
    dependency_graph: dict[str, list[str]] = Field(default_factory=dict)
    excluded_component_ids: list[str] = Field(default_factory=list)
    known_conflicts: list[str] = Field(default_factory=list)
    permitted_engine_mode: EngineMode
    predecessor_manifest_id: str | None = None
    fixity_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    fixity_scope_paths: list[str] = Field(default_factory=list)
    fixity_construction: str | None = None
    build_date: date | None = None
    changelog: list[str] = Field(default_factory=list)
    released_at: datetime | None = None
    responsible_authority_id: str

    @model_validator(mode="after")
    def release_rules(self) -> "CognitiveMemoryManifest":
        if self.release_status == "DEVELOPMENT":
            if self.permitted_engine_mode != EngineMode.DEVELOPMENT:
                raise ValueError(
                    "DEVELOPMENT manifest may permit only DEVELOPMENT engine mode"
                )
        if self.release_status == "RELEASED":
            if self.permitted_engine_mode != EngineMode.PRODUCTION:
                raise ValueError("RELEASED manifest must permit PRODUCTION mode")
            if self.released_at is None:
                raise ValueError("RELEASED manifest requires released_at")
        included = {
            entry.component.canonical_id for entry in self.included_components
        }
        overlap = included.intersection(self.excluded_component_ids)
        if overlap:
            raise ValueError(
                f"Components cannot be both included and excluded: {sorted(overlap)}"
            )
        if self.release_status == "RELEASED":
            if not self.fixity_scope_paths or not self.fixity_construction:
                raise ValueError(
                    "RELEASED manifest requires an explicit fixity scope and construction"
                )
            if self.build_date is None or not self.changelog:
                raise ValueError(
                    "RELEASED manifest requires build_date and changelog"
                )
            if set(self.dependency_graph) != included:
                raise ValueError(
                    "RELEASED manifest dependency_graph must contain every included component"
                )
        return self
