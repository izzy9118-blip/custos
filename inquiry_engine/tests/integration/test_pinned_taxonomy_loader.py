import json
import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.cognition.taxonomy_loader import TaxonomyLoader
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


def _build_taxonomy_component(
    *,
    component_id: str = "LC-001",
    name: str = "Example component",
    source: CanonicalReference,
) -> dict[str, object]:
    return {
        "component_id": component_id,
        "name": name,
        "source": source.model_dump(mode="json"),
        "strauss_formulation": "A documentary test formulation.",
        "mechanism": "Identifies documentary features.",
        "documentary_function": "Supports committed source loading.",
        "investigative_requirement": "Requires repository-pinned loading.",
        "examples": ["Example one"],
        "reconstruction_status": "Established",
        "related_technique_ids": ["TECH-1"],
        "distinguished_from": ["DIST-1"],
        "minimum_trigger_features": ["feature-a"],
        "required_corroboration_features": ["corroboration-a"],
        "ordinary_alternatives": ["alternative-a"],
        "disqualifying_conditions": ["condition-a"],
        "authorized_engine_action": "Proceed",
        "prohibited_inferences": ["No shortcut inference"],
        "uncertainty_note": "Committed fixture.",
    }


def _build_taxonomy_schema(name_pattern: str = ".+") -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "component_id",
            "name",
            "source",
            "strauss_formulation",
            "mechanism",
            "documentary_function",
            "investigative_requirement",
            "reconstruction_status",
            "minimum_trigger_features",
            "ordinary_alternatives",
            "authorized_engine_action",
            "prohibited_inferences",
            "uncertainty_note",
        ],
        "properties": {
            "component_id": {"type": "string", "pattern": "^LC-[0-9]{3}$"},
            "name": {"type": "string", "pattern": name_pattern},
            "source": {"type": "object"},
            "strauss_formulation": {"type": "string", "minLength": 1},
            "mechanism": {"type": "string", "minLength": 1},
            "documentary_function": {"type": "string", "minLength": 1},
            "investigative_requirement": {"type": "string", "minLength": 1},
            "examples": {"type": "array", "items": {"type": "string"}},
            "reconstruction_status": {"type": "string", "minLength": 1},
            "related_technique_ids": {"type": "array", "items": {"type": "string"}},
            "distinguished_from": {"type": "array", "items": {"type": "string"}},
            "minimum_trigger_features": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string"},
            },
            "required_corroboration_features": {
                "type": "array",
                "items": {"type": "string"},
            },
            "ordinary_alternatives": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string"},
            },
            "disqualifying_conditions": {"type": "array", "items": {"type": "string"}},
            "authorized_engine_action": {"type": "string", "minLength": 1},
            "prohibited_inferences": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string"},
            },
            "uncertainty_note": {"type": "string", "minLength": 1},
        },
    }


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_uses_pinned_governed_commit_not_working_tree(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "taxonomy.json"
    schema_file = repo / "taxonomy_schema.json"

    governed_commit = "1234567890123456789012345678901234567890"
    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit=governed_commit,
        version="1.0",
    )
    committed_component = _build_taxonomy_component(source=source_ref)
    committed_schema = _build_taxonomy_schema(r"^Example component$")
    source_file.write_text(json.dumps([committed_component]), encoding="utf-8")
    schema_file.write_text(json.dumps(committed_schema), encoding="utf-8")
    _git(repo, "add", "taxonomy.json", "taxonomy_schema.json")
    _git(repo, "commit", "-q", "-m", "taxonomy source and schema")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    source_ref = source_ref.model_copy(update={"git_commit": governed_git_commit})

    committed_component["name"] = "Committed component"
    source_file.write_text(
        json.dumps([_build_taxonomy_component(source=source_ref, name="Working tree")]),
        encoding="utf-8",
    )
    schema_file.write_text(json.dumps(_build_taxonomy_schema(r"^No match$")), encoding="utf-8")

    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)
    components = loader.load_manifest_source(
        source_ref,
        "taxonomy_schema.json",
        governed_git_commit,
    )

    assert len(components) == 1
    assert components[0].name == "Example component"
    assert components[0].component_id == "LC-001"
    assert components[0].source.github_path == "taxonomy.json"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_pinned_taxonomy_schema_cannot_be_bypassed_by_working_tree_schema(
    tmp_path: Path,
):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    governed_git_commit = "1234567890123456789012345678901234567890"
    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit=governed_git_commit,
        version="1.0",
    )
    committed_component = _build_taxonomy_component(source=source_ref, name="Violates schema")
    committed_schema = _build_taxonomy_schema(r"^Allowed component$")

    source_file = repo / "taxonomy.json"
    schema_file = repo / "taxonomy_schema.json"
    source_file.write_text(json.dumps([committed_component]), encoding="utf-8")
    schema_file.write_text(json.dumps(committed_schema), encoding="utf-8")
    _git(repo, "add", "taxonomy.json", "taxonomy_schema.json")
    _git(repo, "commit", "-q", "-m", "taxonomy source and schema")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    source_ref = source_ref.model_copy(update={"git_commit": governed_git_commit})

    schema_file.write_text("{}", encoding="utf-8")

    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(SchemaValidationError):
        loader.load_manifest_source(
            source_ref,
            "taxonomy_schema.json",
            governed_git_commit,
        )


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_rejects_source_commit_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    _git(repo, "commit", "--allow-empty", "-q", "-m", "first")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    _git(repo, "commit", "--allow-empty", "-q", "-m", "second")
    different_commit = _git(repo, "rev-parse", "HEAD")

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit=different_commit,
        version="1.0",
    )
    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(ValueError, match="taxonomy_source.git_commit"):
        loader.load_manifest_source(source_ref, "taxonomy_schema.json", governed_git_commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_rejects_reader_commit_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    _git(repo, "commit", "--allow-empty", "-q", "-m", "first")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    _git(repo, "commit", "--allow-empty", "-q", "-m", "second")
    other_commit = _git(repo, "rev-parse", "HEAD")

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit=governed_git_commit,
        version="1.0",
    )
    reader = LocalGitReader(repo, other_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(ValueError, match="Taxonomy reader commit"):
        loader.load_manifest_source(source_ref, "taxonomy_schema.json", governed_git_commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_rejects_missing_source_path(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    _git(repo, "commit", "--allow-empty", "-q", "-m", "governed")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path=None,
        git_commit=governed_git_commit,
        version="1.0",
    )
    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(ValueError, match="taxonomy_source.github_path"):
        loader.load_manifest_source(source_ref, "taxonomy_schema.json", governed_git_commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_rejects_missing_source_commit(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    _git(repo, "commit", "--allow-empty", "-q", "-m", "governed")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit=None,
        version="1.0",
    )
    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(ValueError, match="taxonomy_source.git_commit"):
        loader.load_manifest_source(source_ref, "taxonomy_schema.json", governed_git_commit)


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_supports_json_source(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "taxonomy.json"
    schema_file = repo / "taxonomy_schema.json"

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit="1234567890123456789012345678901234567890",
        version="1.0",
    )
    source_file.write_text(
        json.dumps([_build_taxonomy_component(source=source_ref)]),
        encoding="utf-8",
    )
    schema_file.write_text(json.dumps(_build_taxonomy_schema()), encoding="utf-8")
    _git(repo, "add", "taxonomy.json", "taxonomy_schema.json")
    _git(repo, "commit", "-q", "-m", "taxonomy source and schema")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    source_ref = source_ref.model_copy(update={"git_commit": governed_git_commit})

    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)
    components = loader.load_manifest_source(
        source_ref,
        "taxonomy_schema.json",
        governed_git_commit,
    )

    assert len(components) == 1
    assert components[0].component_id == "LC-001"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_supports_yaml_source(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "taxonomy.yaml"
    schema_file = repo / "taxonomy_schema.json"

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.yaml",
        git_commit="1234567890123456789012345678901234567890",
        version="1.0",
    )
    source_file.write_text(
        f"""- component_id: LC-001
  name: Example component
  source:
    canonical_id: LC-000000001
    canonical_class: Taxonomy Component
    github_path: taxonomy.yaml
    git_commit: "{source_ref.git_commit}"
    version: '1.0'
  strauss_formulation: A documentary test formulation.
  mechanism: Identifies documentary features.
  documentary_function: Supports committed source loading.
  investigative_requirement: Requires repository-pinned loading.
  examples:
    - Example one
  reconstruction_status: Established
  related_technique_ids:
    - TECH-1
  distinguished_from:
    - DIST-1
  minimum_trigger_features:
    - feature-a
  required_corroboration_features:
    - corroboration-a
  ordinary_alternatives:
    - alternative-a
  disqualifying_conditions:
    - condition-a
  authorized_engine_action: Proceed
  prohibited_inferences:
    - No shortcut inference
  uncertainty_note: Committed fixture.
""",
        encoding="utf-8",
    )
    schema_file.write_text(json.dumps(_build_taxonomy_schema()), encoding="utf-8")
    _git(repo, "add", "taxonomy.yaml", "taxonomy_schema.json")
    _git(repo, "commit", "-q", "-m", "taxonomy source and schema")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    source_ref = source_ref.model_copy(update={"git_commit": governed_git_commit})

    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)
    components = loader.load_manifest_source(
        source_ref,
        "taxonomy_schema.json",
        governed_git_commit,
    )

    assert len(components) == 1
    assert components[0].component_id == "LC-001"


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_rejects_unsupported_suffix(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "taxonomy.txt"
    schema_file = repo / "taxonomy_schema.json"

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.txt",
        git_commit="1234567890123456789012345678901234567890",
        version="1.0",
    )
    source_file.write_text("unsupported", encoding="utf-8")
    schema_file.write_text(json.dumps(_build_taxonomy_schema()), encoding="utf-8")
    _git(repo, "add", "taxonomy.txt", "taxonomy_schema.json")
    _git(repo, "commit", "-q", "-m", "taxonomy source and schema")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    source_ref = source_ref.model_copy(update={"git_commit": governed_git_commit})

    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(ValueError, match="Unsupported Taxonomy source suffix"):
        loader.load_manifest_source(
            source_ref,
            "taxonomy_schema.json",
            governed_git_commit,
        )


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_taxonomy_loader_rejects_non_array_root(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    source_file = repo / "taxonomy.json"
    schema_file = repo / "taxonomy_schema.json"

    source_ref = CanonicalReference(
        canonical_id="LC-000000001",
        canonical_class="Taxonomy Component",
        github_path="taxonomy.json",
        git_commit="1234567890123456789012345678901234567890",
        version="1.0",
    )
    source_file.write_text(json.dumps({"component_id": "LC-001"}), encoding="utf-8")
    schema_file.write_text(json.dumps(_build_taxonomy_schema()), encoding="utf-8")
    _git(repo, "add", "taxonomy.json", "taxonomy_schema.json")
    _git(repo, "commit", "-q", "-m", "taxonomy source and schema")
    governed_git_commit = _git(repo, "rev-parse", "HEAD")
    source_ref = source_ref.model_copy(update={"git_commit": governed_git_commit})

    reader = LocalGitReader(repo, governed_git_commit)
    loader = TaxonomyLoader(reader)

    with pytest.raises(ValueError, match="Taxonomy source root must be an array"):
        loader.load_manifest_source(
            source_ref,
            "taxonomy_schema.json",
            governed_git_commit,
        )
