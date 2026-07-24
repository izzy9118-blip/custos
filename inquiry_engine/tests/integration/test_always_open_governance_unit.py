from pathlib import Path

import yaml


def _root() -> Path:
    return Path(__file__).resolve().parents[3]


def _yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_always_open_governance_identifiers_are_append_only_and_assigned():
    root = _root()
    ledger = _yaml(root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml")
    expected = [
        "DDR-000000011",
        "COR-000000004",
        "MAN-000000002",
        "VAL-000000028",
        "CER-000000004",
        "VER-000000031",
        "VER-000000032",
        "VER-000000033",
        "VER-000000034",
        "VER-000000035",
    ]
    assert ledger["version"] == "1.17"
    assert ledger["entries"][-len(expected):] == expected
    for identifier in expected:
        assignment = _yaml(
            root
            / "ledgers/identifier-assignment-ledger/assignments"
            / f"{identifier}.yaml"
        )
        assert assignment["identifier"] == identifier
        assert assignment["source_decision_id"] == "DDR-000000011"
        assert assignment["assignment_authority"]["authority_id"] == "CAG-000000002"


def test_version_records_match_corrected_objects_and_ledger():
    root = _root()
    expected = {
        "VER-000000031": ("COR-000000004", None, "1.0"),
        "VER-000000032": ("MAN-000000002", None, "1.0"),
        "VER-000000033": ("IAR-000000001", "1.0", "1.1"),
        "VER-000000034": ("HOC-000000001", "1.1", "1.2"),
        "VER-000000035": ("LDG-000000001", "1.16", "1.17"),
    }
    for identifier, (entity, previous, current) in expected.items():
        record = _yaml(root / "records/versions" / f"{identifier}.yaml")
        assert record["entity_id"] == entity
        assert record["previous_version"] == previous
        assert record["current_version"] == current
        assert record["source_decision_id"] == "DDR-000000011"


def test_certification_preserves_manifest_one_and_activates_manifest_two_only_on_merge():
    root = _root()
    correction = _yaml(root / "records/corrections/COR-000000004.yaml")
    certification = _yaml(root / "records/certifications/CER-000000004.yaml")
    assert any("MAN-000000001" in item for item in correction["correction_scope"])
    assert certification["certification_status"] == "CERTIFIED_UPON_OWNER_MERGE"
    assert any("MAN-000000001" in item for item in certification["certified_principles"])
    assert certification["effective_condition"].startswith("Authenticated repository-owner merge")
