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
    taxonomy_schema_path: str
    procedure_schema_path: str
    projection_git_commit: str | None = Field(default=None, min_length=7)
    projection_manifest_path: str | None = None
    projection_manifest_schema_path: str | None = None
    question_path: Path
    output_dir: Path

    @field_validator("repo_root", "question_path")
    @classmethod
    def required_paths_exist(cls, value: Path) -> Path:
        resolved = value.expanduser().resolve()
        if not resolved.exists():
            raise ValueError(f"Required path does not exist: {resolved}")
        return resolved

    @field_validator(
        "manifest_path",
        "manifest_schema_path",
        "taxonomy_schema_path",
        "procedure_schema_path",
        "projection_manifest_path",
        "projection_manifest_schema_path",
    )
    @classmethod
    def validate_manifest_repository_path(
        cls,
        value: str | None,
        info: ValidationInfo,
    ) -> str | None:
        if value is None:
            return None

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

    @model_validator(mode="after")
    def projection_configuration_is_all_or_none(self) -> "EngineSettings":
        projection_fields = {
            "projection_git_commit": self.projection_git_commit,
            "projection_manifest_path": self.projection_manifest_path,
            "projection_manifest_schema_path": self.projection_manifest_schema_path,
        }
        missing = [name for name, value in projection_fields.items() if value is None]
        present = [name for name, value in projection_fields.items() if value is not None]

        if present and missing:
            raise ValueError(
                "Projection configuration is incomplete; missing fields: "
                + ", ".join(missing)
            )

        return self
