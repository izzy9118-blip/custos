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


def test_document_000008_is_one_admitted_canonical_specification():
    repo_root = _repo_root()
    canonical_path = (
        repo_root
        / "specifications/000008_Inquiry_Engine_Authority_Specification_v1.0.md"
    )
    content = canonical_path.read_text(encoding="utf-8")

    assert canonical_path.is_file()
    assert "Canonical Identifier:** SPEC-000000002" in content
    assert "Status:** ADMITTED — ACTIVE" in content
    assert "Admission Decision:** DDR-000000005" in content
    assert "Responsible Admission Authority:** CAG-000000006" in content
    assert "Finalized for Repository Admission" not in content
    assert "Identifier:** Not assigned" not in content


def test_specification_record_resolves_content_and_fixity():
    repo_root = _repo_root()
    specification = _load_yaml(
        repo_root / "records/specifications/SPEC-000000002.yaml"
    )
    content_path = repo_root / specification["content_path"]

    assert specification["class"] == "Specification"
    assert specification["document_number"] == "000008"
    assert specification["admission_status"] == "ADMITTED"
    assert specification["responsible_admission_authority_id"] == "CAG-000000006"
    assert specification["admission_decision_id"] == "DDR-000000005"
    assert content_path.is_file()
    assert specification["fixity"]["target_path"] == specification["content_path"]
    assert hashlib.sha256(content_path.read_bytes()).hexdigest() == (
        specification["fixity"]["digest"]
    )


def test_admission_decision_is_issued_by_repository_admission_authority():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000005.yaml")

    assert decision["decision_type"] == "NATIVE_OBJECT_ADMISSION"
    assert decision["decision_outcome"] == "ADMITTED"
    assert decision["candidate"]["identifier"] == "SPEC-000000002"
    assert decision["candidate"]["declared_class"] == "Specification"
    assert decision["candidate"]["document_number"] == "000008"
    assert (
        decision["responsible_admission_authority"]["authority_id"]
        == "CAG-000000006"
    )
    assert decision["identifier_allocation_authority"]["authority_id"] == (
        "CAG-000000002"
    )
    assert all(value == "PASS" for value in decision["validation_findings"].values())


def test_specialized_determinations_are_distinct_and_authority_legible():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000005.yaml")
    expected_authorities = {
        "VAL-000000013": "CAG-000000001",
        "VAL-000000014": "CAG-000000002",
        "VAL-000000015": "CAG-000000003",
        "VAL-000000016": "CAG-000000004",
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
        assert validation["subject_id"] == "SPEC-000000002"
        assert validation["validation_outcome"] == "PASS"
        assert validation["responsible_authority"]["authority_id"] == authority_id
        subject_path = repo_root / validation["subject_path"]
        assert hashlib.sha256(subject_path.read_bytes()).hexdigest() == (
            validation["subject_fixity"]["digest"]
        )


def test_admission_unit_identifier_allocations_preserve_jurisdiction():
    repo_root = _repo_root()
    assignments_dir = repo_root / "ledgers/identifier-assignment-ledger/assignments"
    identifiers = [
        "DDR-000000005",
        "SPEC-000000002",
        "VAL-000000013",
        "VAL-000000014",
        "VAL-000000015",
        "VAL-000000016",
        "VER-000000013",
        "VER-000000014",
    ]

    for identifier in identifiers:
        assignment = _load_yaml(assignments_dir / f"{identifier}.yaml")
        assert assignment["assignment_authority"]["authority_id"] == (
            "CAG-000000002"
        )
        assert assignment["source_decision_id"] == "DDR-000000005"

    decision = _load_yaml(repo_root / "records/decisions/DDR-000000005.yaml")
    assert (
        decision["responsible_admission_authority"]["authority_id"]
        == "CAG-000000006"
    )


def test_document_admission_and_ledger_versions_are_recorded():
    repo_root = _repo_root()
    specification_version = _load_yaml(
        repo_root / "records/versions/VER-000000013.yaml"
    )
    ledger_version = _load_yaml(repo_root / "records/versions/VER-000000014.yaml")

    assert specification_version["entity_id"] == "SPEC-000000002"
    assert specification_version["previous_version"] is None
    assert specification_version["current_version"] == "1.0"
    assert specification_version["change_type"] == "INITIAL_ADMISSION"
    assert specification_version["source_decision_id"] == "DDR-000000005"
    assert specification_version["authority_id"] == "CAG-000000006"

    assert ledger_version["entity_id"] == "LDG-000000001"
    assert ledger_version["previous_version"] == "1.9"
    assert ledger_version["current_version"] == "1.10"
    assert ledger_version["source_decision_id"] == "DDR-000000005"
    assert ledger_version["authority_id"] == "CAG-000000002"


def test_identifier_ledger_contains_the_coherent_admission_unit():
    repo_root = _repo_root()
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )
    expected_unit = [
        "DDR-000000005",
        "SPEC-000000002",
        "VAL-000000013",
        "VAL-000000014",
        "VAL-000000015",
        "VAL-000000016",
        "VER-000000013",
        "VER-000000014",
    ]

    assert ledger["version"] == "1.10"
    start = ledger["entries"].index("DDR-000000005")
    assert ledger["entries"][start : start + len(expected_unit)] == expected_unit


def test_admission_decision_instrument_fixity_resolves():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000005.yaml")
    instrument_path = repo_root / decision["decision_instrument_path"]
    fixity = decision["fixity"]["decision_instrument"]

    assert instrument_path.is_file()
    assert fixity["target_path"] == decision["decision_instrument_path"]
    assert hashlib.sha256(instrument_path.read_bytes()).hexdigest() == fixity["digest"]


def test_engine_authority_specification_preserves_cognitive_stage_boundaries():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000005.yaml")
    non_authorizations = set(decision["non_authorizations"])
    specification = (
        repo_root
        / "specifications/000008_Inquiry_Engine_Authority_Specification_v1.0.md"
    ).read_text(encoding="utf-8")

    assert "No one function silently absorbs another." in specification
    assert "The Engine may not:" in specification
    assert "certify its own output;" in specification
    assert "alter an active run’s Manifest;" in specification
    assert "Does not designate HOC-000000001 as a Candidate Cognitive Component." in (
        non_authorizations
    )
    assert "Does not validate, certify, or cognitively integrate any component." in (
        non_authorizations
    )
    assert decision["next_governed_action"] == (
        "REVIEW_DOCUMENT_000009_FOR_NATIVE_ADMISSION"
    )
