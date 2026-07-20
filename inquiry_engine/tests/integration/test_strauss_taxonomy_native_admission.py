import hashlib
import json
from pathlib import Path

import yaml


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"Expected mapping document: {path}")
    return data


def test_taxonomy_is_an_admitted_open_native_hoc_record():
    repo_root = _repo_root()
    hoc = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    )

    assert hoc["identifier"] == "HOC-000000001"
    assert hoc["class"] == "Hermeneutic Object C"
    assert hoc["title"] == "Strauss's Taxonomy of Literary Concealment"
    assert hoc["admission_status"] == "ADMITTED"
    assert hoc["reconstruction_status"]["label"] == (
        "ACTIVE — OPEN DOCUMENTARY RECONSTRUCTION"
    )
    assert hoc["reconstruction_status"]["corpus_wide_verification"] == (
        "NOT_YET_COMPLETE"
    )
    assert hoc["certification_eligibility"]["status"] == "NOT_YET_ELIGIBLE"
    assert hoc["engine_use_authorization_state"]["status"] == "NOT_AUTHORIZED"
    assert hoc["admission_record_reference"] == "DDR-000000004"


def test_hoc_record_contains_every_required_canonical_datum():
    repo_root = _repo_root()
    hoc = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    )
    required_fields = {
        "identifier",
        "class",
        "title",
        "bounded_inquiry_scope",
        "source_inquiry",
        "documentary_basis",
        "claims",
        "questions",
        "provenance",
        "reconstruction_status",
        "uncertainty",
        "lifecycle_status",
        "responsible_authority",
        "governing_references",
        "version_history",
        "audit_history",
        "admission_record_reference",
        "certification_eligibility",
        "engine_use_authorization_state",
    }

    assert required_fields <= set(hoc)
    assert hoc["bounded_inquiry_scope"]["current_primary_source_range"] == (
        "pp. 70–77"
    )
    assert hoc["responsible_authority"]["authority_id"] == "CAG-000000006"


def test_authoritative_reconstruction_content_is_single_and_fixity_verified():
    repo_root = _repo_root()
    hoc = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    )
    content = hoc["documentary_basis"]["authoritative_reconstruction_content"]
    content_path = repo_root / content["path"]

    assert content_path.is_file()
    assert hoc["provenance"]["candidate_source_path"] == content["path"]
    assert hoc["provenance"]["candidate_source_sha256"] == content["digest"]
    assert hashlib.sha256(content_path.read_bytes()).hexdigest() == content["digest"]
    assert content["role"] == "ACTIVE_HUMAN_READABLE_DOCUMENTARY_RECONSTRUCTION"


def test_technique_inventory_preserves_exactly_lc001_through_lc022():
    repo_root = _repo_root()
    hoc = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    )
    techniques = hoc["technique_inventory"]

    assert hoc["documentary_basis"]["technique_count"] == 22
    assert [item["technique_key"] for item in techniques] == [
        f"LC-{number:03d}" for number in range(1, 23)
    ]
    assert len({item["name"] for item in techniques}) == 22
    assert all(item["source_location"] for item in techniques)
    assert all(item["documentary_status"] for item in techniques)


def test_taxonomic_groupings_and_uncertainty_remain_explicit():
    repo_root = _repo_root()
    hoc = _load_yaml(
        repo_root
        / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    )
    grouped_keys = {
        key
        for grouping in hoc["taxonomy_groupings"]
        for key in grouping["technique_keys"]
    }

    assert grouped_keys == {f"LC-{number:03d}" for number in range(1, 23)}
    assert len(hoc["questions"]) == 7
    assert hoc["uncertainty"]["status"] == "OPEN"
    assert any(
        "does not prove concealment" in finding
        for finding in hoc["uncertainty"]["findings"]
    )


def test_admission_decision_is_final_and_authority_legible():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000004.yaml")

    assert decision["decision_type"] == "NATIVE_OBJECT_ADMISSION"
    assert decision["decision_outcome"] == "ADMITTED"
    assert decision["candidate"]["identifier"] == "HOC-000000001"
    assert decision["candidate"]["declared_class"] == "Hermeneutic Object C"
    assert decision["responsible_admission_authority"]["authority_id"] == (
        "CAG-000000006"
    )
    assert decision["identifier_allocation_authority"]["authority_id"] == (
        "CAG-000000002"
    )
    assert all(value == "PASS" for value in decision["validation_findings"].values())


def test_specialized_determinations_remain_distinct_and_consistent():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000004.yaml")
    expected_authorities = {
        "VAL-000000009": "CAG-000000001",
        "VAL-000000010": "CAG-000000002",
        "VAL-000000011": "CAG-000000003",
        "VAL-000000012": "CAG-000000004",
    }
    actual_authorities = {
        item["validation_record_id"]: item["authority_id"]
        for item in decision["specialized_determinations"]
    }

    assert actual_authorities == expected_authorities
    expected_digest = decision["fixity"]["canonical_object_record"]["digest"]
    for validation_id, authority_id in expected_authorities.items():
        validation = _load_yaml(
            repo_root / f"records/validations/{validation_id}.yaml"
        )
        assert validation["subject_id"] == "HOC-000000001"
        assert validation["validation_outcome"] == "PASS"
        assert validation["responsible_authority"]["authority_id"] == authority_id
        assert validation["subject_fixity"]["digest"] == expected_digest


def test_register_contains_a_complete_append_only_hoc_entry():
    repo_root = _repo_root()
    register = _load_yaml(
        repo_root / "registers/hermeneutic-object-register/REG-000000002.yaml"
    )
    entry = next(
        item
        for item in register["entries"]
        if item["canonical_identifier"] == "HOC-000000001"
    )

    assert register["entry_count"] == len(register["entries"])
    assert register["append_only"] is True
    assert register["ordering_rule"] == "admission_date_then_identifier"
    assert set(register["entry_schema"]["required_fields"]) <= set(entry)
    assert entry["ontology_class"] == "Hermeneutic Object C"
    assert entry["identifier_family"] == "HOC"
    assert entry["admission_record_reference"] == "DDR-000000004"
    assert entry["canonical_record_path"].endswith("HOC-000000001.yaml")


def test_admission_unit_allocations_preserve_separate_jurisdiction():
    repo_root = _repo_root()
    assignments_dir = repo_root / "ledgers/identifier-assignment-ledger/assignments"
    identifiers = [
        "DDR-000000004",
        "HOC-000000001",
        "VAL-000000009",
        "VAL-000000010",
        "VAL-000000011",
        "VAL-000000012",
        "VER-000000010",
        "VER-000000011",
        "VER-000000012",
    ]

    for identifier in identifiers:
        assignment = _load_yaml(assignments_dir / f"{identifier}.yaml")
        assert assignment["assignment_authority"]["authority_id"] == (
            "CAG-000000002"
        )
        assert assignment["source_decision_id"] == "DDR-000000004"

    decision = _load_yaml(repo_root / "records/decisions/DDR-000000004.yaml")
    assert decision["responsible_admission_authority"]["authority_id"] == (
        "CAG-000000006"
    )


def test_object_register_and_ledger_versions_are_recorded():
    repo_root = _repo_root()
    object_version = _load_yaml(repo_root / "records/versions/VER-000000010.yaml")
    register_version = _load_yaml(repo_root / "records/versions/VER-000000011.yaml")
    ledger_version = _load_yaml(repo_root / "records/versions/VER-000000012.yaml")

    assert object_version["entity_id"] == "HOC-000000001"
    assert object_version["previous_version"] is None
    assert object_version["current_version"] == "1.0"
    assert object_version["source_decision_id"] == "DDR-000000004"
    assert object_version["authority_id"] == "CAG-000000006"

    assert register_version["entity_id"] == "REG-000000002"
    assert register_version["previous_version"] == "1.0"
    assert register_version["current_version"] == "1.1"
    assert register_version["authority_id"] == "CAG-000000006"

    assert ledger_version["entity_id"] == "LDG-000000001"
    assert ledger_version["previous_version"] == "1.8"
    assert ledger_version["current_version"] == "1.9"
    assert ledger_version["authority_id"] == "CAG-000000002"


def test_ledger_manifest_fixity_and_nonauthorizations_form_one_unit():
    repo_root = _repo_root()
    decision = _load_yaml(repo_root / "records/decisions/DDR-000000004.yaml")
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )
    expected_unit = [
        "DDR-000000004",
        "HOC-000000001",
        "VAL-000000009",
        "VAL-000000010",
        "VAL-000000011",
        "VAL-000000012",
        "VER-000000010",
        "VER-000000011",
        "VER-000000012",
    ]
    start = ledger["entries"].index("DDR-000000004")
    assert ledger["entries"][start : start + len(expected_unit)] == expected_unit

    manifest_path = (
        repo_root / "inquiry_engine/literary_concealment/INTEGRATION_MANIFEST.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    canonical_record = manifest["authoritative_taxonomy"]["canonical_record"]
    assert canonical_record["identifier"] == "HOC-000000001"
    assert canonical_record["admission_decision"] == "DDR-000000004"

    instrument_path = repo_root / decision["decision_instrument_path"]
    assert hashlib.sha256(instrument_path.read_bytes()).hexdigest() == (
        decision["fixity"]["decision_instrument"]["digest"]
    )
    non_authorizations = set(decision["non_authorizations"])
    assert "Does not designate a Candidate Cognitive Component." in non_authorizations
    assert (
        "Does not validate or certify HOC-000000001 as a cognitive component."
        in non_authorizations
    )
    assert "Does not authorize Neo4j projection." in non_authorizations
    assert decision["next_governed_action"] == (
        "SELECT_SEPARATE_COGNITIVE_GOVERNANCE_PATH"
    )
