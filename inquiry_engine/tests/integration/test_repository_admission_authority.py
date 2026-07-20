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


def test_repository_admission_authority_is_separately_established():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000001.yaml")
    authority = _load_yaml(
        repo_root
        / "registers/authority-register/authorities/CAG-000000006.yaml"
    )

    assert decision["decision_type"] == "AUTHORITY_ESTABLISHMENT"
    assert decision["decision_outcome"] == "ESTABLISHED"
    assert decision["responsible_authority"]["authority_id"] == "CAG-000000005"
    assert decision["subject_authority"]["authority_id"] == "CAG-000000006"
    assert authority["authority_role_label"] == "Repository Admission Authority"
    assert authority["establishment_decision_id"] == "DDR-000000001"
    assert authority["lifecycle_status"]["label"] == "ACTIVE"


def test_repository_admission_authority_has_exact_bounded_responsibilities():
    repo_root = _repo_root()
    authority = _load_yaml(
        repo_root
        / "registers/authority-register/authorities/CAG-000000006.yaml"
    )

    assert set(authority["responsibilities"]) == {
        "Conduct final admission review under Document 000005 as amended.",
        "Verify the completeness and resolution of required specialized-authority determinations.",
        "Issue one authorized admission outcome.",
        "Require coherent object, register, ledger, lifecycle, version, and audit recording.",
        "Preserve reasons for rejection or return for correction.",
        "Preserve historical objects and decisions during supersession.",
        "Refuse admission when authority, evidence, identity, or referential integrity is unresolved.",
    }
    assert set(authority["jurisdiction"]["permitted_outcomes"]) == {
        "ADMITTED",
        "REJECTED",
        "RETURNED FOR CORRECTION",
        "SUPERSEDED",
    }
    assert authority["jurisdiction"]["exclusive_after_establishment"] is True


def test_repository_admission_authority_has_exact_separation_limits():
    repo_root = _repo_root()
    authority = _load_yaml(
        repo_root
        / "registers/authority-register/authorities/CAG-000000006.yaml"
    )

    assert set(authority["limitations"]) == {
        "May not create or redefine ontology classes.",
        "May not create identifier families or allocate identifiers.",
        "May not define predicates.",
        "May not approve controlled vocabulary.",
        "May not amend constitutional specifications.",
        "May not perform substantive documentary validation for another authorized role.",
        "May not certify cognitive components.",
        "May not issue cognitive-integration decisions.",
        "May not release Cognitive Memory Manifests.",
        "May not activate production engine components.",
        "May not silently correct candidate objects or historical records.",
        "May not retroactively cure earlier procedural defects.",
    }
    assert (
        authority["identifier_allocation_authority"]["authority_id"]
        == "CAG-000000002"
    )
    assert authority["establishing_authority"]["authority_id"] == "CAG-000000005"


def test_establishment_decision_instrument_and_fixity_resolve():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000001.yaml")
    instrument = repo_root / decision["decision_instrument_path"]

    assert instrument.is_file()
    assert decision["fixity"]["algorithm"] == "SHA-256"
    assert decision["fixity"]["target_path"] == decision["decision_instrument_path"]
    assert hashlib.sha256(instrument.read_bytes()).hexdigest() == decision["fixity"]["digest"]


def test_authority_and_decision_identifiers_preserve_power_separation():
    repo_root = _repo_root()
    assignments_dir = repo_root / "ledgers/identifier-assignment-ledger/assignments"

    for identifier in ("CAG-000000006", "DDR-000000001"):
        assignment = _load_yaml(assignments_dir / f"{identifier}.yaml")
        assert assignment["assignment_authority"]["authority_id"] == "CAG-000000002"
        assert assignment["source_decision_id"] == "DDR-000000001"

    decision = _load_yaml(repo_root / "records/decisions/DDR-000000001.yaml")
    assert decision["responsible_authority"]["authority_id"] == "CAG-000000005"
    assert decision["identifier_allocation_authority"]["authority_id"] == "CAG-000000002"


def test_register_and_ledger_versions_record_one_coherent_unit():
    repo_root = _repo_root()
    authority_register = _load_yaml(
        repo_root / "registers/authority-register/AUR-000000001.yaml"
    )
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )
    register_version = _load_yaml(repo_root / "records/versions/VER-000000004.yaml")
    ledger_version = _load_yaml(repo_root / "records/versions/VER-000000005.yaml")

    assert "CAG-000000006" in authority_register["authority_entries"]
    assert register_version["entity_id"] == "AUR-000000001"
    assert register_version["previous_version"] == "1.1"
    assert register_version["current_version"] == "1.2"
    assert register_version["source_decision_id"] == "DDR-000000001"
    assert ledger_version["entity_id"] == "LDG-000000001"
    assert ledger_version["previous_version"] == "1.5"
    assert ledger_version["current_version"] == "1.6"
    assert ledger_version["source_decision_id"] == "DDR-000000001"

    authority_index = ledger["entries"].index("CAG-000000006")
    assert ledger["entries"][authority_index : authority_index + 4] == [
        "CAG-000000006",
        "DDR-000000001",
        "VER-000000004",
        "VER-000000005",
    ]


def test_establishment_expressly_withholds_all_downstream_actions():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000001.yaml")
    non_authorizations = set(decision["non_authorizations"])

    assert "Does not admit Document 000010." in non_authorizations
    assert "Does not create the Hermeneutic Object Register." in non_authorizations
    assert (
        "Does not admit Strauss's Taxonomy of Literary Concealment."
        in non_authorizations
    )
    assert "Does not validate or certify any cognitive component." in non_authorizations
    assert "Does not issue a cognitive-integration decision." in non_authorizations
    assert "Does not release a Cognitive Memory Manifest." in non_authorizations
    assert (
        "Does not authorize production engine use or Neo4j projection."
        in non_authorizations
    )
    assert decision["next_governed_action"] == (
        "CONSTITUTIONAL_ADMISSION_REVIEW_OF_DOCUMENT_000010"
    )
