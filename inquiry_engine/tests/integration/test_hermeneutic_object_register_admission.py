import hashlib
from pathlib import Path

import yaml


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"Expected mapping document: {path}")
    return data


def test_hermeneutic_object_register_is_admitted_and_internally_consistent():
    repo_root = _repo_root()
    register = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/REG-000000002.yaml"
    )

    assert register["id"] == "REG-000000002"
    assert register["class"] == "Register"
    assert register["register_type"] == "Hermeneutic Object Register"
    assert register["admission_status"] == "ADMITTED"
    assert register["responsible_admission_authority_id"] == "CAG-000000006"
    assert register["identifier_allocation_authority_id"] == "CAG-000000002"
    assert register["admission_decision_id"] == "DDR-000000003"
    assert register["entry_count"] == len(register["entries"])
    assert register["ordering_rule"] == "admission_date_then_identifier"
    assert register["append_only"] is True


def test_register_implements_the_complete_specification_entry_contract():
    repo_root = _repo_root()
    register = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/REG-000000002.yaml"
    )
    expected_fields = [
        "canonical_identifier",
        "ontology_class",
        "identifier_family",
        "title",
        "lifecycle_status",
        "reconstruction_status",
        "certification_eligibility",
        "engine_use_authorization_state",
        "governing_references",
        "current_version",
        "version_history_location",
        "admission_record_reference",
    ]

    assert register["entry_schema"]["required_fields"] == expected_fields
    assert register["permitted_ontology_classes"] == [
        "Hermeneutic Object",
        "Hermeneutic Object A",
        "Hermeneutic Object B",
        "Hermeneutic Object C",
    ]
    assert register["permitted_identifier_families"] == ["HO", "HOA", "HOB", "HOC"]
    assert register["entry_storage_pattern"] == (
        "registers/hermeneutic-object-register/objects/"
        "<canonical-identifier>.yaml"
    )


def test_register_admission_decision_is_final_and_authority_legible():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000003.yaml")

    assert decision["decision_type"] == "NATIVE_OBJECT_ADMISSION"
    assert decision["decision_outcome"] == "ADMITTED"
    assert decision["candidate"]["identifier"] == "REG-000000002"
    assert decision["candidate"]["declared_class"] == "Register"
    assert decision["responsible_admission_authority"]["authority_id"] == (
        "CAG-000000006"
    )
    assert decision["identifier_allocation_authority"]["authority_id"] == (
        "CAG-000000002"
    )
    assert all(value == "PASS" for value in decision["validation_findings"].values())


def test_initial_empty_state_is_recorded_without_freezing_the_live_register():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000003.yaml")
    register = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/REG-000000002.yaml"
    )

    assert decision["initial_register_state"]["version"] == "1.0"
    assert decision["initial_register_state"]["entry_count"] == 0
    assert decision["initial_register_state"]["entries"] == []
    assert register["version_history"][0]["version_record_id"] == "VER-000000008"
    assert register["version_history"][0]["action"] == "INITIAL_ADMISSION"


def test_specialized_determinations_remain_distinct_and_attributable():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000003.yaml")
    expected_authorities = {
        "VAL-000000005": "CAG-000000001",
        "VAL-000000006": "CAG-000000002",
        "VAL-000000007": "CAG-000000003",
        "VAL-000000008": "CAG-000000004",
    }

    actual_authorities = {
        item["validation_record_id"]: item["authority_id"]
        for item in decision["specialized_determinations"]
    }
    assert actual_authorities == expected_authorities

    for validation_id, authority_id in expected_authorities.items():
        validation = _load_yaml(
            repo_root / f"records/validations/{validation_id}.yaml"
        )
        assert validation["subject_id"] == "REG-000000002"
        assert validation["validation_outcome"] == "PASS"
        assert validation["responsible_authority"]["authority_id"] == authority_id
        assert validation["related_admission_decision_id"] == "DDR-000000003"


def test_admission_unit_allocations_do_not_collapse_jurisdiction():
    repo_root = _repo_root()
    assignments_dir = repo_root / "ledgers/identifier-assignment-ledger/assignments"
    identifiers = [
        "DDR-000000003",
        "REG-000000002",
        "VAL-000000005",
        "VAL-000000006",
        "VAL-000000007",
        "VAL-000000008",
        "VER-000000008",
        "VER-000000009",
    ]

    for identifier in identifiers:
        assignment = _load_yaml(assignments_dir / f"{identifier}.yaml")
        assert assignment["assignment_authority"]["authority_id"] == (
            "CAG-000000002"
        )
        assert assignment["source_decision_id"] == "DDR-000000003"

    decision = _load_yaml(repo_root / "records/decisions/DDR-000000003.yaml")
    assert decision["responsible_admission_authority"]["authority_id"] == (
        "CAG-000000006"
    )


def test_register_and_ledger_versions_are_recorded():
    repo_root = _repo_root()
    register_version = _load_yaml(repo_root / "records/versions/VER-000000008.yaml")
    ledger_version = _load_yaml(repo_root / "records/versions/VER-000000009.yaml")

    assert register_version["entity_id"] == "REG-000000002"
    assert register_version["previous_version"] is None
    assert register_version["current_version"] == "1.0"
    assert register_version["change_type"] == "INITIAL_ADMISSION"
    assert register_version["source_decision_id"] == "DDR-000000003"
    assert register_version["authority_id"] == "CAG-000000006"

    assert ledger_version["entity_id"] == "LDG-000000001"
    assert ledger_version["previous_version"] == "1.7"
    assert ledger_version["current_version"] == "1.8"
    assert ledger_version["source_decision_id"] == "DDR-000000003"
    assert ledger_version["authority_id"] == "CAG-000000002"


def test_identifier_ledger_contains_the_coherent_register_admission_unit():
    repo_root = _repo_root()
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )
    expected_unit = [
        "DDR-000000003",
        "REG-000000002",
        "VAL-000000005",
        "VAL-000000006",
        "VAL-000000007",
        "VAL-000000008",
        "VER-000000008",
        "VER-000000009",
    ]

    start = ledger["entries"].index("DDR-000000003")
    assert ledger["entries"][start : start + len(expected_unit)] == expected_unit


def test_decision_fixity_and_downstream_withholding_are_explicit():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000003.yaml")
    instrument_path = repo_root / decision["decision_instrument_path"]
    instrument_fixity = decision["fixity"]["decision_instrument"]

    assert instrument_path.is_file()
    assert instrument_fixity["target_path"] == decision["decision_instrument_path"]
    assert hashlib.sha256(instrument_path.read_bytes()).hexdigest() == (
        instrument_fixity["digest"]
    )

    non_authorizations = set(decision["non_authorizations"])
    assert "Does not admit any HO, HOA, HOB, or HOC entity." in non_authorizations
    assert (
        "Does not admit Strauss's Taxonomy of Literary Concealment."
        in non_authorizations
    )
    assert "Does not validate or certify any cognitive component." in non_authorizations
    assert "Does not issue a cognitive-integration decision." in non_authorizations
    assert "Does not release a Cognitive Memory Manifest." in non_authorizations
    assert decision["next_governed_action"] == (
        "CONSTITUTIONAL_ADMISSION_REVIEW_OF_STRAUSS_TAXONOMY"
    )
