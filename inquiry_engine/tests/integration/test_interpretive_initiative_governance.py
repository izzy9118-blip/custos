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


SUCCESSOR_SOURCE_HASHES = {
    "candidates/chatgpt-project/v1.2/Custos_ChatGPT_Project_Instructions_v1.2.txt":
        "15f876ab0d04ad2dd4eacf42f98f0c95bb65bddc5c3c235676436996f3584d90",
    "candidates/chatgpt-project/v1.2/Custos_Codex_Amendment_002_Interpretive_Initiative_v1.0.txt":
        "fc658f3ac54f9a91efebae0e2537a7437ea0ee7425a2dc1eb4541f310a3ea018",
    "candidates/chatgpt-project/v1.2/Custos_Project_Startup_Procedure_v1.2.txt":
        "31b52e47c8cf8f046ce93e2c875b627401f160357038545af7df525cc5f9eca5",
    "candidates/citation-objects/chapter-01-citation-01-interpretive-initiative-correction-v1.1.md":
        "a97f7fb4c6a5341bd6f7a47f4cf389778460a2412350cd64562e882f1082a0a0",
}

PREDECESSOR_SOURCE_HASHES = {
    "candidates/chatgpt-project/v1.1/Custos_ChatGPT_Project_Instructions_v1.1.txt":
        "eaaf448674958c58d8be655adeefe20aad56906096f3be831cbebb3d0c8ceef1",
    "candidates/chatgpt-project/v1.1/Custos_Codex_Amendment_001_Shared_Textual_Examination_v1.0.txt":
        "10bd08794dbe40f88cd8af5731ac8c4b19f0bda8211cc31bf19550ac3c8bd18f",
    "candidates/chatgpt-project/v1.1/Custos_Project_Startup_Procedure_v1.1.txt":
        "2a979119ea0fbad48fc63e63ee00815cb27ff7f5078be977a016c087cf1de190",
    "candidates/citation-objects/chapter-01-citation-01-shared-examination-correction-v1.0.md":
        "26bc10e6b0d3d9ce7e399af0e23b594be94a19591b3ebc9dd5cb137b4d817712",
}


def test_successor_and_predecessor_source_fixity():
    root = _repo_root()
    for relative_path, expected_digest in {
        **SUCCESSOR_SOURCE_HASHES,
        **PREDECESSOR_SOURCE_HASHES,
    }.items():
        path = root / relative_path
        assert path.is_file(), relative_path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_digest


def test_active_instructions_require_initiative_without_user_polling():
    root = _repo_root()
    path = (
        root
        / "candidates/chatgpt-project/v1.2/"
        / "Custos_ChatGPT_Project_Instructions_v1.2.txt"
    )
    text = path.read_text(encoding="utf-8")
    block = text.split("\nBEGIN PROJECT INSTRUCTIONS\n", 1)[1].split(
        "\nEND PROJECT INSTRUCTIONS\n", 1
    )[0]

    assert len(block) < 8000
    assert "The AI bears responsibility for advancing the inquiry." in block
    assert "Do not ask the user to choose among interpretations" in block
    assert "Begin the examination in the same turn." in block
    assert "Silence neither blocks progress nor counts as agreement" in block
    assert "One opening question for the user's judgment" not in block
    assert "A required pause for the user's response" not in block
    assert "end a shared-reading turn with the live textual question" not in block


def test_startup_procedure_executes_the_reading_instead_of_assigning_it():
    root = _repo_root()
    text = (
        root
        / "candidates/chatgpt-project/v1.2/"
        / "Custos_Project_Startup_Procedure_v1.2.txt"
    ).read_text(encoding="utf-8")

    assert "begin the interpretation in the same turn" in text
    assert "Comparative Questions are research objects. Work them" in text
    assert "Do not end with a question assigned to the user." in text
    assert "One opening question addressed to the user" not in text
    assert "Waiting for the user's answer is a required active stage" not in text


def test_specification_versions_the_package_and_preserves_history():
    root = _repo_root()
    spec = _yaml(root / "records/specifications/SPEC-000000004.yaml")
    artifacts = {item["path"]: item for item in spec["constituent_artifacts"]}

    assert spec["version"] == "1.1"
    assert spec["authority_basis"]["decision_id"] == "DDR-000000010"
    assert spec["authority_basis"]["lane"] == "PROTECTED_GOVERNANCE_LANE"
    assert set(SUCCESSOR_SOURCE_HASHES).intersection(artifacts) == {
        path for path in SUCCESSOR_SOURCE_HASHES if "chatgpt-project" in path
    }
    assert artifacts[
        "candidates/chatgpt-project/v1.2/Custos_ChatGPT_Project_Instructions_v1.2.txt"
    ]["disposition"] == "ACTIVE"
    assert artifacts[
        "candidates/chatgpt-project/v1.2/Custos_Project_Startup_Procedure_v1.2.txt"
    ]["disposition"] == "ACTIVE"
    assert artifacts[
        "candidates/chatgpt-project/v1.1/Custos_ChatGPT_Project_Instructions_v1.1.txt"
    ]["disposition"] == "SUPERSEDED_HISTORY"
    assert artifacts[
        "candidates/chatgpt-project/v1.1/Custos_Project_Startup_Procedure_v1.1.txt"
    ]["disposition"] == "SUPERSEDED_HISTORY"


def test_correction_changes_procedure_without_adopting_an_answer():
    root = _repo_root()
    correction = _yaml(root / "records/corrections/COR-000000003.yaml")

    assert correction["source_record"]["sha256"] == SUCCESSOR_SOURCE_HASHES[
        correction["source_record"]["path"]
    ]
    assert any(
        "research problems Custos must investigate" in item
        for item in correction["correction_scope"]
    )
    assert any(
        "adopts no answer" in item
        for item in correction["certified_limitations"]
    )
    assert any(
        "does not certify Chapter I" in item
        for item in correction["certified_limitations"]
    )


def test_decision_validation_and_certification_are_scope_coherent():
    root = _repo_root()
    decision = _yaml(root / "records/decisions/DDR-000000010.yaml")
    validation = _yaml(root / "records/validations/VAL-000000027.yaml")
    certification = _yaml(root / "records/certifications/CER-000000003.yaml")

    assert decision["authority_basis"]["lane"] == "PROTECTED_GOVERNANCE_LANE"
    assert decision["decision_outcome"] == (
        "VERSION_ADMIT_AND_CERTIFY_BOUNDED_SCOPE"
    )
    assert validation["validated_objects"] == [
        "SPEC-000000004",
        "COR-000000003",
    ]
    assert all(
        finding == "PASS" for finding in validation["validation_findings"].values()
    )
    assert certification["validation_record_ids"] == ["VAL-000000027"]
    assert certification["decision_record_id"] == "DDR-000000010"
    assert {item["identifier"] for item in certification["certified_objects"]} == {
        "SPEC-000000004",
        "COR-000000003",
    }
    assert any(
        "Chapter I, Citation 1 as a completed" in exclusion
        for exclusion in certification["expressly_not_certified"]
    )
    assert any(
        "Any answer to whether Chapter 8" in exclusion
        for exclusion in certification["expressly_not_certified"]
    )


def test_identifier_ledger_records_the_complete_successor_unit():
    root = _repo_root()
    ledger = _yaml(root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml")
    expected = [
        "DDR-000000010",
        "COR-000000003",
        "VAL-000000027",
        "CER-000000003",
        "VER-000000029",
        "VER-000000030",
    ]

    assert ledger["version"] == "1.16"
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
        assert assignment["source_decision_id"] == "DDR-000000010"


def test_readme_directs_ai_led_examination_and_resolves_links():
    root = _repo_root()
    text = (root / "README.md").read_text(encoding="utf-8")

    assert "questionnaire for the user" in text
    assert "forced-choice" in text
    assert "and begin with the live question" not in text
    for relative_path in [
        "records/certifications/CER-000000003.yaml",
        "records/corrections/COR-000000003.yaml",
        "candidates/chatgpt-project/v1.2/Custos_Codex_Amendment_002_Interpretive_Initiative_v1.0.txt",
        "candidates/chatgpt-project/v1.2/Custos_ChatGPT_Project_Instructions_v1.2.txt",
        "candidates/chatgpt-project/v1.2/Custos_Project_Startup_Procedure_v1.2.txt",
        "candidates/citation-objects/chapter-01-citation-01-interpretive-initiative-correction-v1.1.md",
    ]:
        assert (root / relative_path).is_file(), relative_path
