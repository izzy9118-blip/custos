import hashlib
import json
from pathlib import Path

import yaml

from custos_engine.models.taxonomy import TaxonomyComponent
from custos_engine.repository.validators import validate_against_schema


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"Expected mapping: {path}")
    return value


def test_df_synthesis_fixity_and_lacunae_are_preserved():
    root = _repo_root()
    source = root / (
        "engine_training/"
        "Documentary_Findings_DF-000001_to_DF-000150_Coherent_Synthesis_v1.0.txt"
    )
    text = source.read_text(encoding="utf-8")

    assert hashlib.sha256(source.read_bytes()).hexdigest() == (
        "c3c70e5d01cd75bd2cc6ddf5413f6ac1c7b16fda84a81c6d0f2a0b685a2496d9"
    )
    for lacuna in (
        "DF-000130–DF-000143",
        "DF-000145",
        "DF-000148–DF-000149",
    ):
        assert lacuna in text
    assert "No missing finding has been silently reconstructed" in text


def test_iar_is_the_complete_ten_phase_thirty_seven_step_outer_process():
    root = _repo_root()
    iar = _yaml(root / "records/inquiry-architecture/IAR-000000001.yaml")
    schema = json.loads(
        (root / "inquiry_engine/src/custos_engine/schemas/procedure.schema.json").read_text(
            encoding="utf-8"
        )
    )

    validate_against_schema(iar, schema)
    assert iar["id"] == "IAR-000000001"
    assert iar["class"] == "Inquiry Architecture Record"
    assert iar["documentary_basis"]["preserved_lacunae"] == [
        "DF-000130_THROUGH_DF-000143",
        "DF-000145",
        "DF-000148_THROUGH_DF-000149",
    ]
    phases = iar["ordered_stages"]
    assert [phase["phase"] for phase in phases] == list(range(1, 11))
    assert [phase["state"] for phase in phases] == [
        "DOCUMENTARY_INTAKE",
        "HORIZON_AUDIT",
        "INDEPENDENT_RECONSTRUCTION",
        "AUTHORIAL_AUTHORIZATION",
        "PURPOSE_AUDIENCE_FUNCTION",
        "ARCHITECTURAL_MAPPING",
        "PROBLEM_FORMATION",
        "ADVERSARIAL_TESTING",
        "PROGRESSIVE_DISCLOSURE",
        "SYNTHESIS_LIMITATION",
    ]
    steps = [step for phase in phases for step in phase["steps"]]
    assert [step["sequence"] for step in steps] == list(range(1, 38))
    assert all(
        phase["inner_sanctum_access"].startswith("DENIED")
        for phase in phases[:7]
    )
    assert phases[7]["inner_sanctum_access"] == (
        "ELIGIBLE_ONLY_AFTER_INNER_SANCTUM_GATE"
    )


def test_machine_taxonomy_preserves_all_twenty_two_distinct_components():
    root = _repo_root()
    path = root / "inquiry_engine/cognitive_memory/HOC-000000001.taxonomy.json"
    components = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(
        (
            root
            / "inquiry_engine/src/custos_engine/schemas/taxonomy_component.schema.json"
        ).read_text(encoding="utf-8")
    )

    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "5ba195af2716cadd6adfd0e1503ea9ee742f1322aada163ab7d2d05af12433ce"
    )
    assert [item["component_id"] for item in components] == [
        f"LC-{number:03d}" for number in range(1, 23)
    ]
    for item in components:
        validate_against_schema(item, schema)
        component = TaxonomyComponent.model_validate(item)
        assert component.source.canonical_id == "HOC-000000001"
        assert component.prohibited_inferences
        assert component.ordinary_alternatives


def test_cognitive_memory_register_integrates_the_ordered_pair():
    root = _repo_root()
    register = _yaml(
        root / "registers/cognitive-memory-register/REG-000000004.yaml"
    )

    assert register["id"] == "REG-000000004"
    assert register["register_type"] == "Cognitive Memory Register"
    assert register["entry_count"] == 2
    entries = {
        entry["component_canonical_identifier"]: entry
        for entry in register["entries"]
    }
    assert set(entries) == {"HOC-000000001", "IAR-000000001"}
    assert "IAR-000000001" in entries["HOC-000000001"]["dependencies"]
    assert entries["HOC-000000001"]["certification_record_identifier"] == (
        "CER-000000001"
    )
    assert entries["IAR-000000001"]["integration_decision_identifier"] == (
        "DDR-000000008"
    )
    assert any(
        "No entry authorizes Neo4j projection" in boundary
        for boundary in register["governance_boundaries"]
    )


def test_hoc_version_1_1_is_bounded_and_manifest_conditional():
    root = _repo_root()
    hoc = _yaml(
        root
        / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    )

    assert hoc["version"] == "1.1"
    assert hoc["reconstruction_status"]["corpus_wide_verification"] == (
        "NOT_YET_COMPLETE"
    )
    assert hoc["certification_eligibility"]["certification_record_id"] == (
        "CER-000000001"
    )
    assert hoc["cognitive_memory_integration"]["dependency"] == "IAR-000000001"
    assert "ONLY_WHEN_PINNED" in hoc["engine_use_authorization_state"]["status"]


def test_single_validation_certification_and_decision_are_coherent():
    root = _repo_root()
    validation = _yaml(root / "records/validations/VAL-000000025.yaml")
    certification = _yaml(root / "records/certifications/CER-000000001.yaml")
    decision = _yaml(root / "records/decisions/DDR-000000008.yaml")

    assert all(
        outcome == "PASS" for outcome in validation["validation_findings"].values()
    )
    assert certification["validation_record_ids"] == ["VAL-000000025"]
    assert {item["identifier"] for item in certification["certified_components"]} == {
        "HOC-000000001",
        "IAR-000000001",
    }
    assert decision["authority_basis"]["lane"] == "ROUTINE_OPERATIONAL_LANE"
    actions = {item["action"] for item in decision["declared_actions"]}
    assert actions == {
        "ADMIT",
        "CERTIFY_BOUNDED_SCOPE",
        "INTEGRATE",
        "RELEASE",
        "ACTIVATE_FOR_LATER_VERSION_PINNED_RUNS",
    }
    assert any("Neo4j" in item for item in decision["non_authorizations"])


def test_identifier_ledger_records_the_complete_routine_unit():
    root = _repo_root()
    ledger = _yaml(root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml")
    expected = [
        "CER-000000001",
        "DDR-000000008",
        "IAR-000000001",
        "MAN-000000001",
        "REG-000000004",
        "VAL-000000025",
        "VER-000000020",
        "VER-000000021",
        "VER-000000022",
        "VER-000000023",
        "VER-000000024",
    ]

    assert ledger["version"] == "1.14"
    assert ledger["entries"][-len(expected) :] == expected
    for identifier in expected:
        assignment = _yaml(
            root
            / "ledgers/identifier-assignment-ledger/assignments"
            / f"{identifier}.yaml"
        )
        assert assignment["assignment_authority"]["authority_id"] == (
            "CAG-000000002"
        )
        assert assignment["source_decision_id"] == "DDR-000000008"
