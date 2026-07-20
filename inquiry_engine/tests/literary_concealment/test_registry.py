from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from custos_engine.literary_concealment import (
    CERTIFICATION_RECORD,
    INTEGRATION_STATUS,
    SUPPORTED_COMPONENT_IDS,
    evaluate_component,
    get_component_runtime,
    load_component_schema,
    load_technique,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
AUTHORITATIVE_TAXONOMY = (
    REPOSITORY_ROOT
    / "engine_training"
    / "Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt"
)
AUTHORITATIVE_TAXONOMY_SHA256 = (
    "0a155194f72a4517d267256b37fe4b68fe1144e0ef8ec3a1a26c3b3ad5b9f0e5"
)
INTEGRATION_MANIFEST = (
    REPOSITORY_ROOT
    / "inquiry_engine"
    / "literary_concealment"
    / "INTEGRATION_MANIFEST.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_registry_contains_exactly_lc001_through_lc022():
    assert SUPPORTED_COMPONENT_IDS == tuple(
        f"LC-{number:03d}" for number in range(1, 23)
    )


@pytest.mark.parametrize("component_id", SUPPORTED_COMPONENT_IDS)
def test_each_component_has_an_isolated_runtime(component_id):
    runtime = get_component_runtime(component_id)
    digits = component_id.removeprefix("LC-")

    assert runtime.component_id == component_id
    assert runtime.module_name.endswith(f".lc{digits}")
    assert runtime.input_model.__name__ == f"LC{digits}EvaluationInput"
    assert runtime.result_model.__name__ == f"LC{digits}EvaluationResult"
    assert runtime.evaluator.__name__ == f"evaluate_lc{digits}"
    assert runtime.integration_status == "CERTIFIED_TECHNICAL_INTEGRATION"
    assert runtime.certification_record == CERTIFICATION_RECORD


@pytest.mark.parametrize("component_id", SUPPORTED_COMPONENT_IDS)
def test_each_projection_validates_as_certified_integrated_runtime(component_id):
    technique = load_technique(component_id)
    schema = load_component_schema(component_id)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(technique.model_dump(mode="json"))

    assert technique.technique_key == component_id
    assert technique.projection_status == "CERTIFIED_TECHNICAL_INTEGRATION"
    assert technique.canonical_identifier is None
    assert technique.identifier_status == "NOT_ASSIGNED"
    assert technique.source.authoritative_object_sha256 == AUTHORITATIVE_TAXONOMY_SHA256
    assert technique.source.repository_commit == (
        "7100700ef10d68621f4859b5fe94fac6e5e0fcea"
    )


def test_authoritative_taxonomy_fixity_matches_all_component_projections():
    assert _sha256(AUTHORITATIVE_TAXONOMY) == AUTHORITATIVE_TAXONOMY_SHA256


def test_integration_manifest_defines_one_certified_active_runtime():
    manifest = json.loads(INTEGRATION_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["integration_status"] == "CERTIFIED_TECHNICAL_INTEGRATION"
    assert manifest["component_range"] == {
        "first": "LC-001",
        "last": "LC-022",
        "count": 22,
    }
    assert manifest["component_ids"] == list(SUPPORTED_COMPONENT_IDS)
    assert manifest["technical_certification"] == {
        "record_path": CERTIFICATION_RECORD,
        "certified_scope": "LC-001_THROUGH_LC-022_COMBINED_EXECUTABLE_SUBSYSTEM",
        "result": INTEGRATION_STATUS,
        "effective_date": "2026-07-20",
        "continuous_validation_workflow": ".github/workflows/inquiry-engine-ci.yml",
        "complete_suite_result": "382_PASSED",
    }

    assert manifest["active_runtime"]["source_of_truth"] == (
        "ACTIVE_INTEGRATED_RUNTIME_ONLY"
    )
    assert manifest["consolidation"] == {
        "duplicate_package_tree_retained": False,
        "working_tree_policy": "ONE_ACTIVE_COPY",
        "prior_upload_commit": "9d0cc71de73de2fce1e47968e9cb5b9456754bc3",
    }


def test_dispatcher_preserves_component_specific_result_type():
    result = evaluate_component(
        "LC-001",
        {
            "statement_a_id": "S-A",
            "statement_b_id": "S-B",
            "same_work": True,
            "same_subject": True,
            "mutually_incompatible": False,
            "positionally_separated": True,
            "source_integrity_confirmed": True,
            "local_contexts_reconstructed": True,
            "speaker_or_voice_resolved": True,
        },
    )

    assert type(result).__name__ == "LC001EvaluationResult"
    assert result.outcome.value == "NOT_TRIGGERED"


@pytest.mark.parametrize("component_id", ["LC-000", "LC-023", "LC-1", ""])
def test_registry_rejects_unintegrated_or_malformed_component_ids(component_id):
    with pytest.raises(KeyError):
        get_component_runtime(component_id)
