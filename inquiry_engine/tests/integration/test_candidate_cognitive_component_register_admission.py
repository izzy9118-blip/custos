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


def test_candidate_register_is_admitted_active_and_empty():
    repo_root = _repo_root()
    register = _load_yaml(
        repo_root
        / "registers/candidate-cognitive-component-register/REG-000000003.yaml"
    )

    assert register["id"] == "REG-000000003"
    assert register["class"] == "Register"
    assert register["register_type"] == "Candidate Cognitive Component Register"
    assert register["admission_status"] == "ADMITTED"
    assert register["lifecycle_status"]["label"] == "ACTIVE"
    assert register["admission_decision_id"] == "DDR-000000007"
    assert register["entries"] == []
    assert register["entry_count"] == 0
    assert register["append_only"] is True


def test_candidate_register_implements_the_complete_specification_contract():
    repo_root = _repo_root()
    register = _load_yaml(
        repo_root
        / "registers/candidate-cognitive-component-register/REG-000000003.yaml"
    )
    required_fields = set(register["entry_schema"]["required_fields"])

    assert required_fields == {
        "component_canonical_identifier",
        "native_class",
        "source_inquiry",
        "documentary_basis",
        "reason_for_candidacy",
        "candidacy_decision",
        "intended_scope",
        "intended_use",
        "known_limitations",
        "validation_status",
        "current_outcome",
        "audit_history",
    }
    assert register["entry_rules"]["native_admission_required"] is True
    assert (
        register["entry_rules"]["candidate_designation_confers_production_authority"]
        is False
    )
    assert register["entry_rules"]["rejected_candidates_remain_preserved"] is True
    assert register["ordering_rule"] == (
        "designation_date_then_component_identifier"
    )


def test_admission_decision_resolves_register_and_fixity():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000007.yaml")
    register_path = repo_root / decision["candidate"]["content_path"]

    assert decision["decision_type"] == "NATIVE_OBJECT_ADMISSION"
    assert decision["decision_outcome"] == "ADMITTED"
    assert decision["candidate"]["identifier"] == "REG-000000003"
    assert decision["candidate"]["declared_class"] == "Register"
    assert (
        decision["responsible_admission_authority"]["authority_id"]
        == "CAG-000000006"
    )
    assert decision["identifier_allocation_authority"]["authority_id"] == (
        "CAG-000000002"
    )
    assert register_path.is_file()
    assert hashlib.sha256(register_path.read_bytes()).hexdigest() == (
        decision["fixity"]["register_content"]["digest"]
    )
    assert all(value == "PASS" for value in decision["validation_findings"].values())


def test_specialized_determinations_are_distinct_and_authority_legible():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000007.yaml")
    expected_authorities = {
        "VAL-000000021": "CAG-000000001",
        "VAL-000000022": "CAG-000000002",
        "VAL-000000023": "CAG-000000003",
        "VAL-000000024": "CAG-000000004",
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
        assert validation["subject_id"] == "REG-000000003"
        assert validation["validation_outcome"] == "PASS"
        assert validation["responsible_authority"]["authority_id"] == authority_id
        subject_path = repo_root / validation["subject_path"]
        assert hashlib.sha256(subject_path.read_bytes()).hexdigest() == (
            validation["subject_fixity"]["digest"]
        )


def test_register_admission_identifier_allocations_preserve_jurisdiction():
    repo_root = _repo_root()
    assignments_dir = repo_root / "ledgers/identifier-assignment-ledger/assignments"
    identifiers = [
        "DDR-000000007",
        "REG-000000003",
        "VAL-000000021",
        "VAL-000000022",
        "VAL-000000023",
        "VAL-000000024",
        "VER-000000017",
        "VER-000000018",
    ]

    for identifier in identifiers:
        assignment = _load_yaml(assignments_dir / f"{identifier}.yaml")
        assert assignment["assignment_authority"]["authority_id"] == (
            "CAG-000000002"
        )
        assert assignment["source_decision_id"] == "DDR-000000007"

    decision = _load_yaml(repo_root / "records/decisions/DDR-000000007.yaml")
    assert (
        decision["responsible_admission_authority"]["authority_id"]
        == "CAG-000000006"
    )


def test_register_admission_and_ledger_versions_are_recorded():
    repo_root = _repo_root()
    register_version = _load_yaml(repo_root / "records/versions/VER-000000017.yaml")
    ledger_version = _load_yaml(repo_root / "records/versions/VER-000000018.yaml")

    assert register_version["entity_id"] == "REG-000000003"
    assert register_version["previous_version"] is None
    assert register_version["current_version"] == "1.0"
    assert register_version["change_type"] == "INITIAL_ADMISSION"
    assert register_version["source_decision_id"] == "DDR-000000007"
    assert register_version["authority_id"] == "CAG-000000006"

    assert ledger_version["entity_id"] == "LDG-000000001"
    assert ledger_version["previous_version"] == "1.11"
    assert ledger_version["current_version"] == "1.12"
    assert ledger_version["source_decision_id"] == "DDR-000000007"
    assert ledger_version["authority_id"] == "CAG-000000002"


def test_identifier_ledger_contains_the_coherent_register_admission_unit():
    repo_root = _repo_root()
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )
    expected_unit = [
        "DDR-000000007",
        "REG-000000003",
        "VAL-000000021",
        "VAL-000000022",
        "VAL-000000023",
        "VAL-000000024",
        "VER-000000017",
        "VER-000000018",
    ]

    assert tuple(map(int, ledger["version"].split("."))) >= (1, 12)
    start = ledger["entries"].index("DDR-000000007")
    assert ledger["entries"][start : start + len(expected_unit)] == expected_unit


def test_admission_decision_instrument_fixity_resolves():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000007.yaml")
    instrument_path = repo_root / decision["decision_instrument_path"]
    fixity = decision["fixity"]["decision_instrument"]

    assert instrument_path.is_file()
    assert fixity["target_path"] == decision["decision_instrument_path"]
    assert hashlib.sha256(instrument_path.read_bytes()).hexdigest() == fixity["digest"]


def test_register_admission_designates_no_candidate_or_downstream_authority():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000007.yaml")
    register = _load_yaml(
        repo_root
        / "registers/candidate-cognitive-component-register/REG-000000003.yaml"
    )
    non_authorizations = set(decision["non_authorizations"])

    assert register["entries"] == []
    assert not any(
        entry.get("component_canonical_identifier") == "HOC-000000001"
        for entry in register["entries"]
    )
    assert (
        "Does not designate or register HOC-000000001 or any other cognitive candidate."
        in non_authorizations
    )
    assert (
        "Does not grant candidate-designation jurisdiction to CAG-000000006 or another authority."
        in non_authorizations
    )
    assert decision["next_governed_action"] == (
        "RESOLVE_CANDIDATE_DESIGNATION_AUTHORITY_THEN_REVIEW_HOC-000000001"
    )
