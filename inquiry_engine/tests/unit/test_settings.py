from pathlib import Path

import pytest
from pydantic import ValidationError

from custos_engine.config.settings import EngineSettings
from custos_engine.models.base import EngineMode


def _build_settings(tmp_path: Path, manifest_schema_path: str) -> EngineSettings:
    question_path = tmp_path / "question.json"
    question_path.write_text("{}", encoding="utf-8")
    return EngineSettings(
        mode=EngineMode.DEVELOPMENT,
        repo_root=tmp_path,
        git_commit="1234567",
        manifest_git_commit="7654321",
        manifest_path="manifest.json",
        manifest_schema_path=manifest_schema_path,
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
        _build_settings(tmp_path, manifest_schema_path)
