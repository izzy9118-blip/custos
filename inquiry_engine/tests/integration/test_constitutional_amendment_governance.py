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


def test_constitutional_amendment_procedure_is_adopted_by_bounded_authority():
    repo_root = _repo_root()
    amendment = _load_yaml(repo_root / "amendments/AMD-000000001.yaml")
    authority = _load_yaml(
        repo_root
        / "registers/authority-register/authorities/CAG-000000005.yaml"
    )

    assert amendment["decision_outcome"] == "ADOPTED"
    assert amendment["adopting_authority"]["authority_id"] == "CAG-000000005"
    assert amendment["adopted_specification"]["document_number"] == "000012"
    assert amendment["adopted_specification"]["status"] == "ADOPTED — ACTIVE"

    limitations = set(authority["limitations"])
    assert "May not perform ordinary native-object admission." in limitations
    assert (
        "May not authorize cognitive integration, production-engine use, or activation."
        in limitations
    )


def test_amendment_identifier_allocation_preserves_authority_separation():
    repo_root = _repo_root()
    assignment = _load_yaml(
        repo_root
        / "ledgers/identifier-assignment-ledger/assignments/AMD-000000001.yaml"
    )

    assert assignment["family"] == "AMD"
    assert assignment["assignment_authority"]["authority_id"] == "CAG-000000002"
    assert assignment["source_decision_id"] == "AMD-000000001"


def test_amendment_adoption_and_ledger_version_records_resolve():
    repo_root = _repo_root()
    amendment = _load_yaml(repo_root / "amendments/AMD-000000001.yaml")
    adopted_path = repo_root / amendment["adopted_specification"]["path"]
    version = _load_yaml(repo_root / "records/versions/VER-000000002.yaml")
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )

    assert adopted_path.is_file()
    assert amendment["fixity"]["algorithm"] == "SHA-256"
    assert amendment["fixity"]["target_path"] == amendment["adopted_specification"]["path"]
    assert (
        hashlib.sha256(adopted_path.read_bytes()).hexdigest()
        == amendment["fixity"]["digest"]
    )
    assert version["entity_id"] == ledger["id"]
    assert version["previous_version"] == "1.3"
    assert version["current_version"] == ledger["version"] == "1.4"
    assert version["source_decision_id"] == "AMD-000000001"
    assert ledger["entries"][-2:] == ["AMD-000000001", "VER-000000002"]


def test_adoption_expressly_withholds_downstream_authority():
    repo_root = _repo_root()
    amendment = _load_yaml(repo_root / "amendments/AMD-000000001.yaml")
    non_authorizations = set(amendment["non_authorizations"])

    assert "Does not amend Document 000005." in non_authorizations
    assert "Does not establish the Repository Admission Authority." in non_authorizations
    assert "Does not admit Document 000010." in non_authorizations
    assert (
        "Does not admit Strauss's Taxonomy of Literary Concealment."
        in non_authorizations
    )
    assert (
        "Does not validate, certify, integrate, or activate any cognitive component."
        in non_authorizations
    )
