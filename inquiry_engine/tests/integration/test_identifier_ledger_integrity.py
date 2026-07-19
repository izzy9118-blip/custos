from pathlib import Path

import yaml


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"Expected mapping document: {path}")
    return data


def test_identifier_assignment_ledger_entries_match_assignment_records_exactly():
    repo_root = _repo_root()
    ledger_path = repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    assignments_dir = repo_root / "ledgers/identifier-assignment-ledger/assignments"

    ledger = _load_yaml(ledger_path)
    ledger_entries = ledger.get("entries")
    assert isinstance(ledger_entries, list)

    assignment_paths = sorted(
        list(assignments_dir.glob("*.yaml")) + list(assignments_dir.glob("*.yml"))
    )
    assignment_ids: list[str] = []
    assignment_dates: dict[str, str] = {}

    for path in assignment_paths:
        record = _load_yaml(path)
        identifier = record.get("identifier")
        assert isinstance(identifier, str) and identifier
        assignment_ids.append(identifier)

        assignment_date = record.get("assignment_date")
        assert isinstance(assignment_date, str) and assignment_date
        assignment_dates[identifier] = assignment_date

    assert len(ledger_entries) == len(set(ledger_entries)), "Duplicate ledger entries detected"
    assert len(assignment_ids) == len(set(assignment_ids)), "Duplicate assignment identifiers detected"

    ledger_set = set(ledger_entries)
    assignment_set = set(assignment_ids)

    missing_in_ledger = sorted(assignment_set - ledger_set)
    extra_in_ledger = sorted(ledger_set - assignment_set)

    assert not missing_in_ledger, f"Assignments missing in ledger entries: {missing_in_ledger}"
    assert not extra_in_ledger, f"Ledger entries missing assignment records: {extra_in_ledger}"

    assert ledger_entries == sorted(
        ledger_entries,
        key=lambda identifier: (assignment_dates[identifier], identifier),
    ), "Ledger entries are not ordered by assignment_date_then_identifier"
