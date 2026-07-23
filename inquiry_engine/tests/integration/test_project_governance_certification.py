import hashlib
from pathlib import Path

import yaml


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"Expected mapping: {path}")
    return value


EXPECTED_SOURCE_HASHES = {
    "candidates/chatgpt-project/v1.0/Custos_ChatGPT_Project_Instructions_v1.0.txt":
        "7d9ad00196bf17cf26f9f3b14629ba1e8911167000eef5f06a47454bf2ee17cc",
    "candidates/chatgpt-project/v1.0/Custos_Codex_Complete_v1.0.txt":
        "b67cc89932d26bc50feae6b8c1ef8790ab997c96ed68737b290351db0ca9702a",
    "candidates/chatgpt-project/v1.0/Custos_Project_Startup_Procedure_v1.0.txt":
        "9ae7bc312ac632ef198d5a4d89ad7f7aaa289a6e35256fd915f76e5c1e885f07",
    "candidates/chatgpt-project/v1.1/Custos_ChatGPT_Project_Instructions_v1.1.txt":
        "eaaf448674958c58d8be655adeefe20aad56906096f3be831cbebb3d0c8ceef1",
    "candidates/chatgpt-project/v1.1/Custos_Codex_Amendment_001_Shared_Textual_Examination_v1.0.txt":
        "10bd08794dbe40f88cd8af5731ac8c4b19f0bda8211cc31bf19550ac3c8bd18f",
    "candidates/chatgpt-project/v1.1/Custos_Project_Startup_Procedure_v1.1.txt":
        "2a979119ea0fbad48fc63e63ee00815cb27ff7f5078be977a016c087cf1de190",
    "candidates/citation-objects/chapter-01-citation-01-documentary-anchor.md":
        "aeb79a4a7dac8323d0b24a661c54c2c59665c44af5db166563054540ba7b1c54",
    "candidates/citation-objects/chapter-01-citation-01-shared-examination-correction-v1.0.md":
        "26bc10e6b0d3d9ce7e399af0e23b594be94a19591b3ebc9dd5cb137b4d817712",
}


def test_all_eight_preserved_source_artifacts_match_certified_fixity():
    root = _repo_root()
    for relative_path, expected_digest in EXPECTED_SOURCE_HASHES.items():
        path = root / relative_path
        assert path.is_file(), relative_path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_digest


def test_project_governance_package_preserves_active_and_superseded_versions():
    root = _repo_root()
    spec = _yaml(root / "records/specifications/SPEC-000000004.yaml")
    artifacts = {item["path"]: item for item in spec["constituent_artifacts"]}

    assert spec["authority_basis"]["lane"] == "PROTECTED_GOVERNANCE_LANE"
    assert set(artifacts) == {
        path for path in EXPECTED_SOURCE_HASHES if "chatgpt-project" in path
    }
    assert artifacts[
        "candidates/chatgpt-project/v1.0/Custos_ChatGPT_Project_Instructions_v1.0.txt"
    ]["disposition"] == "SUPERSEDED_HISTORY"
    assert artifacts[
        "candidates/chatgpt-project/v1.1/Custos_ChatGPT_Project_Instructions_v1.1.txt"
    ]["disposition"] == "ACTIVE"
    assert artifacts[
        "candidates/chatgpt-project/v1.1/Custos_Project_Startup_Procedure_v1.1.txt"
    ]["disposition"] == "ACTIVE"
    assert any(
        "does not amend admitted Repository Documents" in boundary
        for boundary in spec["governance_boundaries"]
    )


def test_correction_is_forward_only_and_does_not_adopt_an_answer():
    root = _repo_root()
    correction = _yaml(root / "records/corrections/COR-000000002.yaml")

    assert correction["source_record"]["sha256"] == EXPECTED_SOURCE_HASHES[
        correction["source_record"]["path"]
    ]
    assert correction["qualified_record"]["triggering_commit"] == (
        "e93250739f516fd8227fc97d76e3d791f56f7334"
    )
    assert any(
        "adopts no answer" in limitation
        for limitation in correction["certified_limitations"]
    )


def test_evidence_record_does_not_promote_the_citation_object():
    root = _repo_root()
    evidence = _yaml(root / "records/evidence/EVR-000000001.yaml")

    assert evidence["source_artifact"]["sha256"] == EXPECTED_SOURCE_HASHES[
        evidence["source_artifact"]["path"]
    ]
    assert evidence["canonical_citation_object_identifier"] is None
    assert evidence["current_inquiry_state"] == (
        "DOCUMENTARY_PREPARATION_READY_FOR_SHARED_EXAMINATION"
    )
    excluded = " ".join(evidence["excluded_scope"])
    assert "Substantive completion" in excluded
    assert "Primary-language verification" in excluded
    assert "final Inner Sanctum" in excluded


def test_decision_validation_and_certification_are_scope_coherent():
    root = _repo_root()
    decision = _yaml(root / "records/decisions/DDR-000000009.yaml")
    validation = _yaml(root / "records/validations/VAL-000000026.yaml")
    certification = _yaml(root / "records/certifications/CER-000000002.yaml")

    assert decision["authority_basis"]["lane"] == "PROTECTED_GOVERNANCE_LANE"
    assert decision["decision_outcome"] == "ADMIT_AND_CERTIFY_BOUNDED_SCOPE"
    assert set(validation["validated_objects"]) == {
        "SPEC-000000004",
        "COR-000000002",
        "EVR-000000001",
    }
    assert all(
        finding == "PASS" for finding in validation["validation_findings"].values()
    )
    assert certification["validation_record_ids"] == ["VAL-000000026"]
    assert certification["decision_record_id"] == "DDR-000000009"
    assert {item["identifier"] for item in certification["certified_objects"]} == {
        "SPEC-000000004",
        "COR-000000002",
        "EVR-000000001",
    }
    assert any(
        "completed, admitted, or certified Citation Object" in exclusion
        for exclusion in certification["expressly_not_certified"]
    )


def test_identifier_ledger_records_the_complete_protected_unit():
    root = _repo_root()
    ledger = _yaml(root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml")
    expected = [
        "DDR-000000009",
        "SPEC-000000004",
        "COR-000000002",
        "EVR-000000001",
        "VAL-000000026",
        "CER-000000002",
        "VER-000000025",
        "VER-000000026",
        "VER-000000027",
        "VER-000000028",
    ]

    assert ledger["version"] == "1.15"
    assert ledger["entries"][-len(expected):] == expected
    for identifier in expected:
        assignment = _yaml(
            root
            / "ledgers/identifier-assignment-ledger/assignments"
            / f"{identifier}.yaml"
        )
        assert assignment["assignment_authority"]["authority_id"] == (
            "CAG-000000002"
        )
        assert assignment["source_decision_id"] == "DDR-000000009"
