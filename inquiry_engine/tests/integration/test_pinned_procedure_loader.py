import json
import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.cognition.procedure_loader import ProcedureLoader
from custos_engine.models.base import CanonicalReference
from custos_engine.repository.github_reader import LocalGitReader
from custos_engine.repository.validators import SchemaValidationError


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    return repo


def _build_procedure(purpose: str = "Procedure purpose") -> dict[str, object]:
    return {
        "purpose": purpose,
        "triggering_conditions": [],
        "required_inputs": [],
        "ordered_stages": [{}],
        "permitted_operations": [],
        "prohibited_operations": [],
        "evidence_requirements": [],
        "branch_conditions": [],
        "failure_conditions": [],
        "termination_conditions": [{}],
        "positive_validation_cases": [],
        "negative_validation_cases": [],
        "adversarial_validation_cases": [],
        "version_history": [],
        "validation_record_ids": ["VR-001"],
        "certification_record_id": "CER-001",
        "integration_status": "INTEGRATED",
    }


def _build_schema(purpose_pattern: str = ".+") -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "purpose",
            "triggering_conditions",
            "required_inputs",
            "ordered_stages",
            "permitted_operations",
            "prohibited_operations",
            "evidence_requirements",
            "branch_conditions",
            "failure_conditions",
            "termination_conditions",
            "positive_validation_cases",
            "negative_validation_cases",
            "adversarial_validation_cases",
            "version_history",
            "validation_record_ids",
            "certification_record_id",
            "integration_status",
        ],
        "properties": {
            "purpose": {"type": "string", "minLength": 1, "pattern": purpose_pattern},
            "triggering_conditions": {"type": "array"},
            "required_inputs": {"type": "array"},
            "ordered_stages": {"type": "array", "minItems": 1},
            "permitted_operations": {"type": "array"},
            "prohibited_operations": {"type": "array"},
            "evidence_requirements": {"type": "array"},
            "branch_conditions": {"type": "array"},
            "failure_conditions": {"type": "array"},
            "termination_conditions": {"type": "array", "minItems": 1},
            "positive_validation_cases": {"type": "array"},
            "negative_validation_cases": {"type": "array"},
            "adversarial_validation_cases": {"type": "array"},
            "version_history": {"type": "array"},
            "validation_record_ids": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "certification_record_id": {"type": "string", "minLength": 1},
            "integration_status": {"type": "string", "minLength": 1},
        },
    }


def _source_ref(path: str, commit: str | None) -> CanonicalReference:
    return CanonicalReference(
        canonical_id="IAR-000000001",
        canonical_class="Inquiry Architecture Record",
        github_path=path,
        git_commit=commit,
        version="1.0",
    )


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_json_procedure_loads_from_pinned_commit(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text(json.dumps(_build_procedure()), encoding="utf-8")
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    procedure = loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)

    assert procedure["purpose"] == "Procedure purpose"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_yaml_procedure_loads_from_pinned_commit(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.yaml").write_text(
        """purpose: Procedure purpose
triggering_conditions: []
required_inputs: []
ordered_stages:
  - {}
permitted_operations: []
prohibited_operations: []
evidence_requirements: []
branch_conditions: []
failure_conditions: []
termination_conditions:
  - {}
positive_validation_cases: []
negative_validation_cases: []
adversarial_validation_cases: []
version_history: []
validation_record_ids:
  - VR-001
certification_record_id: CER-001
integration_status: INTEGRATED
""",
        encoding="utf-8",
    )
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure.yaml", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    procedure = loader.load_manifest_source(_source_ref("procedure.yaml", commit), "procedure_schema.json", commit)

    assert procedure["purpose"] == "Procedure purpose"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_working_tree_source_cannot_override_pinned_procedure(tmp_path: Path):
    repo = _init_repo(tmp_path)
    source = repo / "procedure.json"
    schema = repo / "procedure_schema.json"
    source.write_text(json.dumps(_build_procedure("Committed")), encoding="utf-8")
    schema.write_text(json.dumps(_build_schema(r"^Committed$")), encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    source.write_text(json.dumps(_build_procedure("Working")), encoding="utf-8")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    procedure = loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)

    assert procedure["purpose"] == "Committed"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_working_tree_schema_cannot_override_pinned_schema(tmp_path: Path):
    repo = _init_repo(tmp_path)
    source = repo / "procedure.json"
    schema = repo / "procedure_schema.json"
    source.write_text(json.dumps(_build_procedure("Committed")), encoding="utf-8")
    schema.write_text(json.dumps(_build_schema(r"^Committed$")), encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    schema.write_text("{}", encoding="utf-8")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    procedure = loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)

    assert procedure["purpose"] == "Committed"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_source_missing_at_pinned_commit_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "schema only")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Procedure source is missing"):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_schema_missing_at_pinned_commit_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text(json.dumps(_build_procedure()), encoding="utf-8")
    _git(repo, "add", "procedure.json")
    _git(repo, "commit", "-q", "-m", "source only")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Procedure schema is missing"):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_source_commit_mismatch_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    _git(repo, "commit", "--allow-empty", "-q", "-m", "first")
    governed = _git(repo, "rev-parse", "HEAD")
    _git(repo, "commit", "--allow-empty", "-q", "-m", "second")
    different = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, governed))
    with pytest.raises(ValueError, match="procedure_source.git_commit"):
        loader.load_manifest_source(_source_ref("procedure.json", different), "procedure_schema.json", governed)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_reader_commit_mismatch_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    _git(repo, "commit", "--allow-empty", "-q", "-m", "first")
    governed = _git(repo, "rev-parse", "HEAD")
    _git(repo, "commit", "--allow-empty", "-q", "-m", "second")
    other = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, other))
    with pytest.raises(ValueError, match="Procedure reader commit"):
        loader.load_manifest_source(_source_ref("procedure.json", governed), "procedure_schema.json", governed)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_missing_source_github_path_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    _git(repo, "commit", "--allow-empty", "-q", "-m", "base")
    commit = _git(repo, "rev-parse", "HEAD")

    source = _source_ref("procedure.json", commit).model_copy(update={"github_path": None})
    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="procedure_source.github_path"):
        loader.load_manifest_source(source, "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_empty_source_github_path_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    _git(repo, "commit", "--allow-empty", "-q", "-m", "base")
    commit = _git(repo, "rev-parse", "HEAD")

    source = _source_ref("procedure.json", commit).model_copy(update={"github_path": "   "})
    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="procedure_source.github_path"):
        loader.load_manifest_source(source, "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_missing_source_git_commit_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    _git(repo, "commit", "--allow-empty", "-q", "-m", "base")
    commit = _git(repo, "rev-parse", "HEAD")

    source = _source_ref("procedure.json", commit).model_copy(update={"git_commit": None})
    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="procedure_source.git_commit"):
        loader.load_manifest_source(source, "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_unsupported_suffix_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.txt").write_text("text", encoding="utf-8")
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure.txt", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Unsupported procedure source suffix"):
        loader.load_manifest_source(_source_ref("procedure.txt", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_malformed_json_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text("{", encoding="utf-8")
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Invalid procedure JSON"):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_malformed_yaml_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.yaml").write_text("purpose: [", encoding="utf-8")
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure.yaml", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Invalid procedure YAML"):
        loader.load_manifest_source(_source_ref("procedure.yaml", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_non_object_root_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text("[]", encoding="utf-8")
    (repo / "procedure_schema.json").write_text(json.dumps(_build_schema()), encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Procedure source root must be an object"):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_malformed_schema_json_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text(json.dumps(_build_procedure()), encoding="utf-8")
    (repo / "procedure_schema.json").write_text("{", encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(ValueError, match="Invalid procedure schema JSON"):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_invalid_json_schema_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text(json.dumps(_build_procedure()), encoding="utf-8")
    invalid_schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": 7}
    (repo / "procedure_schema.json").write_text(json.dumps(invalid_schema), encoding="utf-8")
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(SchemaValidationError, match="Invalid JSON schema"):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_schema_invalid_procedure_fails(tmp_path: Path):
    repo = _init_repo(tmp_path)
    (repo / "procedure.json").write_text(json.dumps(_build_procedure("wrong")), encoding="utf-8")
    (repo / "procedure_schema.json").write_text(
        json.dumps(_build_schema(r"^required-purpose$")),
        encoding="utf-8",
    )
    _git(repo, "add", "procedure.json", "procedure_schema.json")
    _git(repo, "commit", "-q", "-m", "procedure and schema")
    commit = _git(repo, "rev-parse", "HEAD")

    loader = ProcedureLoader(LocalGitReader(repo, commit))
    with pytest.raises(SchemaValidationError):
        loader.load_manifest_source(_source_ref("procedure.json", commit), "procedure_schema.json", commit)
