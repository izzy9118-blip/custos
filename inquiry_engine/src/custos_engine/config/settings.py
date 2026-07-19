from __future__ import annotations

from pathlib import Path

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from custos_engine.models.base import EngineMode


class EngineSettings(BaseModel):
    """Immutable inputs governing one engine execution."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    mode: EngineMode
    repo_root: Path
    git_commit: str = Field(min_length=7)
    manifest_git_commit: str = Field(min_length=7)
    manifest_path: str
    manifest_schema_path: str
    question_path: Path
    output_dir: Path
    projection_manifest_path: Path | None = None

    @field_validator("repo_root", "question_path")
    @classmethod
    def required_paths_exist(cls, value: Path) -> Path:
        resolved = value.expanduser().resolve()
        if not resolved.exists():
            raise ValueError(f"Required path does not exist: {resolved}")
        return resolved

    @field_validator("manifest_path", "manifest_schema_path")
    @classmethod
    def validate_manifest_repository_path(
        cls,
        value: str,
        info: ValidationInfo,
    ) -> str:
        field_name = info.field_name or "path"
        label = field_name.replace("_", " ")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{label.capitalize()} must be non-empty")

        path = Path(normalized)
        if path.is_absolute():
            raise ValueError(f"{label.capitalize()} must be repository-relative")
        if ".." in path.parts:
            raise ValueError(f"{label.capitalize()} must not contain '..'")
        return normalized

    @field_validator("output_dir")
    @classmethod
    def normalize_output(cls, value: Path) -> Path:
        return value.expanduser().resolve()

    @field_validator("projection_manifest_path")
    @classmethod
    def projection_path_exists(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        resolved = value.expanduser().resolve()
        if not resolved.exists():
            raise ValueError(f"Projection manifest does not exist: {resolved}")
        return resolved

    @model_validator(mode="after")
    def production_requires_projection_manifest(self) -> "EngineSettings":
        if self.mode == EngineMode.PRODUCTION and self.projection_manifest_path is None:
            raise ValueError("PRODUCTION mode requires projection_manifest_path")
        return self
