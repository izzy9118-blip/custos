from pathlib import Path

import pytest
from pydantic import ValidationError

from custos_engine.config.settings import EngineSettings
from custos_engine.models.base import EngineMode


def _build_settings(
    tmp_path: Path,
    *,
    mode: EngineMode = EngineMode.DEVELOPMENT,
    manifest_path: str = "manifest.json",
    manifest_schema_path: str = "schema.json",
    taxonomy_schema_path: str = "taxonomy_schema.json",
    procedure_schema_path: str = "procedure_schema.json",
    projection_git_commit: str | None = None,
    projection_manifest_path: str | None = None,
    projection_manifest_schema_path: str | None = None,
) -> EngineSettings:
    question_path = tmp_path / "question.json"
    question_path.write_text("{}", encoding="utf-8")
    return EngineSettings(
        mode=mode,
        repo_root=tmp_path,
        git_commit="1234567",
        manifest_git_commit="7654321",
        manifest_path=manifest_path,
        manifest_schema_path=manifest_schema_path,
        taxonomy_schema_path=taxonomy_schema_path,
        procedure_schema_path=procedure_schema_path,
        projection_git_commit=projection_git_commit,
        projection_manifest_path=projection_manifest_path,
        projection_manifest_schema_path=projection_manifest_schema_path,
        question_path=question_path,
        output_dir=tmp_path / "out",
    )


@pytest.mark.parametrize(
    ("manifest_schema_path", "expected_error"),
    [
        ("   ", "Manifest schema path must be non-empty"),
        ("/abs/schema.json", "Manifest schema path must be repository-relative"),
        ("../schema.json", "Manifest schema path must not contain '..'"),
    ],
)
def test_manifest_schema_path_rejects_invalid_values(
    tmp_path: Path,
    manifest_schema_path: str,
    expected_error: str,
):
    with pytest.raises(ValidationError, match=expected_error):
        _build_settings(tmp_path, manifest_schema_path=manifest_schema_path)


@pytest.mark.parametrize(
    ("taxonomy_schema_path", "expected_error"),
    [
        ("   ", "Taxonomy schema path must be non-empty"),
        ("/abs/taxonomy_schema.json", "Taxonomy schema path must be repository-relative"),
        ("../taxonomy_schema.json", "Taxonomy schema path must not contain '..'"),
    ],
)
def test_taxonomy_schema_path_rejects_invalid_values(
    tmp_path: Path,
    taxonomy_schema_path: str,
    expected_error: str,
):
    with pytest.raises(ValidationError, match=expected_error):
        _build_settings(tmp_path, taxonomy_schema_path=taxonomy_schema_path)


def test_taxonomy_schema_path_accepts_repository_relative_path(tmp_path: Path):
    settings = _build_settings(tmp_path, taxonomy_schema_path="schemas/taxonomy.json")
    assert settings.taxonomy_schema_path == "schemas/taxonomy.json"


@pytest.mark.parametrize(
    ("procedure_schema_path", "expected_error"),
    [
        ("", "Procedure schema path must be non-empty"),
        ("   ", "Procedure schema path must be non-empty"),
        (
            "/abs/procedure_schema.json",
            "Procedure schema path must be repository-relative",
        ),
        (
            "../procedure_schema.json",
            "Procedure schema path must not contain '..'",
        ),
    ],
)
def test_procedure_schema_path_rejects_invalid_values(
    tmp_path: Path,
    procedure_schema_path: str,
    expected_error: str,
):
    with pytest.raises(ValidationError, match=expected_error):
        _build_settings(tmp_path, procedure_schema_path=procedure_schema_path)


def test_procedure_schema_path_accepts_repository_relative_path(tmp_path: Path):
    settings = _build_settings(tmp_path, procedure_schema_path="schemas/procedure.json")
    assert settings.procedure_schema_path == "schemas/procedure.json"


@pytest.mark.parametrize("mode", [EngineMode.DEVELOPMENT, EngineMode.PRODUCTION])
def test_taxonomy_schema_path_is_required(tmp_path: Path, mode: EngineMode):
    (tmp_path / "question.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValidationError, match="taxonomy_schema_path"):
        EngineSettings(
            mode=mode,
            repo_root=tmp_path,
            git_commit="1234567",
            manifest_git_commit="7654321",
            manifest_path="manifest.json",
            manifest_schema_path="schema.json",
            taxonomy_schema_path=None,
            procedure_schema_path="procedure_schema.json",
            question_path=tmp_path / "question.json",
            output_dir=tmp_path / "out",
        )


@pytest.mark.parametrize("mode", [EngineMode.DEVELOPMENT, EngineMode.PRODUCTION])
def test_procedure_schema_path_is_required(tmp_path: Path, mode: EngineMode):
    (tmp_path / "question.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValidationError, match="procedure_schema_path"):
        EngineSettings(
            mode=mode,
            repo_root=tmp_path,
            git_commit="1234567",
            manifest_git_commit="7654321",
            manifest_path="manifest.json",
            manifest_schema_path="schema.json",
            taxonomy_schema_path="taxonomy_schema.json",
            procedure_schema_path=None,
            question_path=tmp_path / "question.json",
            output_dir=tmp_path / "out",
        )


@pytest.mark.parametrize(
    ("projection_manifest_path", "expected_error"),
    [
        ("   ", "Projection manifest path must be non-empty"),
        ("/abs/projection.json", "Projection manifest path must be repository-relative"),
        ("../projection.json", "Projection manifest path must not contain '..'"),
    ],
)
def test_projection_manifest_path_rejects_invalid_values(
    tmp_path: Path,
    projection_manifest_path: str,
    expected_error: str,
):
    with pytest.raises(ValidationError, match=expected_error):
        _build_settings(
            tmp_path,
            projection_git_commit="1111111",
            projection_manifest_path=projection_manifest_path,
            projection_manifest_schema_path="projection_schema.json",
        )


@pytest.mark.parametrize(
    ("projection_manifest_schema_path", "expected_error"),
    [
        ("   ", "Projection manifest schema path must be non-empty"),
        (
            "/abs/projection_schema.json",
            "Projection manifest schema path must be repository-relative",
        ),
        (
            "../projection_schema.json",
            "Projection manifest schema path must not contain '..'",
        ),
    ],
)
def test_projection_manifest_schema_path_rejects_invalid_values(
    tmp_path: Path,
    projection_manifest_schema_path: str,
    expected_error: str,
):
    with pytest.raises(ValidationError, match=expected_error):
        _build_settings(
            tmp_path,
            projection_git_commit="1111111",
            projection_manifest_path="projection.json",
            projection_manifest_schema_path=projection_manifest_schema_path,
        )


def test_development_accepts_projection_fields_absent(tmp_path: Path):
    settings = _build_settings(tmp_path, mode=EngineMode.DEVELOPMENT)
    assert settings.projection_git_commit is None
    assert settings.projection_manifest_path is None
    assert settings.projection_manifest_schema_path is None


def test_development_accepts_projection_fields_present(tmp_path: Path):
    settings = _build_settings(
        tmp_path,
        mode=EngineMode.DEVELOPMENT,
        projection_git_commit="1111111",
        projection_manifest_path="projection.json",
        projection_manifest_schema_path="projection_schema.json",
    )
    assert settings.projection_git_commit == "1111111"
    assert settings.projection_manifest_path == "projection.json"
    assert settings.projection_manifest_schema_path == "projection_schema.json"


@pytest.mark.parametrize(
    (
        "projection_git_commit",
        "projection_manifest_path",
        "projection_manifest_schema_path",
        "missing_field",
    ),
    [
        (None, "projection.json", "projection_schema.json", "projection_git_commit"),
        ("1111111", None, "projection_schema.json", "projection_manifest_path"),
        ("1111111", "projection.json", None, "projection_manifest_schema_path"),
        (None, None, "projection_schema.json", "projection_git_commit"),
        (None, "projection.json", None, "projection_git_commit"),
        ("1111111", None, None, "projection_manifest_path"),
    ],
)
def test_development_rejects_partial_projection_configuration(
    tmp_path: Path,
    projection_git_commit: str | None,
    projection_manifest_path: str | None,
    projection_manifest_schema_path: str | None,
    missing_field: str,
):
    with pytest.raises(ValidationError, match=missing_field):
        _build_settings(
            tmp_path,
            mode=EngineMode.DEVELOPMENT,
            projection_git_commit=projection_git_commit,
            projection_manifest_path=projection_manifest_path,
            projection_manifest_schema_path=projection_manifest_schema_path,
        )


def test_production_rejects_projection_fields_absent(tmp_path: Path):
    with pytest.raises(ValidationError, match="projection_git_commit"):
        _build_settings(tmp_path, mode=EngineMode.PRODUCTION)


def test_production_accepts_projection_fields_present(tmp_path: Path):
    settings = _build_settings(
        tmp_path,
        mode=EngineMode.PRODUCTION,
        projection_git_commit="1111111",
        projection_manifest_path="projection.json",
        projection_manifest_schema_path="projection_schema.json",
    )
    assert settings.mode == EngineMode.PRODUCTION
