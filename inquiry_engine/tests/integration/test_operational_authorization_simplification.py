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


def _amendment() -> dict:
    return _load_yaml(_repo_root() / "amendments/AMD-000000003.yaml")


def test_founder_ratification_makes_merge_the_authorizing_event():
    repo_root = _repo_root()
    ratification = (
        repo_root
        / "governance/foundational-ratifications/2026-07-20_Operational_Authorization_Simplification_Ratification.md"
    ).read_text(encoding="utf-8")

    assert "Ratifying Founder: Ismail Ibrahim" in ratification
    assert "Authenticated repository-owner merge" in ratification
    assert "a draft or unmerged branch has no constitutional effect" in ratification
    assert "One explicit owner decision" in ratification


def test_amendment_has_founder_and_constitutional_authority_basis():
    amendment = _amendment()

    assert amendment["decision_outcome"] == "ADOPTED"
    assert amendment["adopting_authority"]["authority_id"] == "CAG-000000005"
    assert amendment["higher_authority_basis"]["authority_type"] == (
        "FOUNDER_RATIFICATION"
    )
    assert amendment["effective_event"] == (
        "AUTHENTICATED_REPOSITORY_OWNER_MERGE_TO_MAIN"
    )
    assert amendment["current_resolution"]["retroactive_effect"] == "NONE"


def test_amendment_covers_the_full_burdensome_operational_chain():
    amendment = _amendment()
    affected_documents = {
        item["document_number"] for item in amendment["affected_specifications"]
    }

    assert affected_documents == {"000005", "000008", "000009", "000012"}
    assert amendment["affected_prior_amendments"] == [
        {
            "identifier": "AMD-000000002",
            "effect": "Routine final-admission and serial specialized-determination mandates are prospectively superseded.",
        }
    ]


def test_routine_lane_uses_one_owner_merge_with_ci_evidence():
    routine = _amendment()["routine_lane"]

    assert routine["final_authorization_event"] == (
        "AUTHENTICATED_REPOSITORY_OWNER_MERGE"
    )
    assert "Passing required CI" in routine["required_evidence"]
    assert routine["mandatory_candidate_stage"] is False
    assert routine["mandatory_separate_authority_records"] is False
    assert set(routine["combinable_actions"]) == {
        "ADMISSION",
        "VALIDATION",
        "CERTIFICATION_WHERE_REQUIRED",
        "INTEGRATION",
        "MANIFEST_RELEASE",
        "ACTIVATION_FOR_LATER_RUNS",
    }


def test_protected_lane_is_reserved_for_material_risk():
    triggers = set(_amendment()["protected_lane_triggers"])

    assert triggers == {
        "FOUNDATIONAL_OR_CONSTITUTIONAL_CHANGE",
        "ONTOLOGY_IDENTIFIER_PREDICATE_OR_VOCABULARY_DEFINITION_CHANGE",
        "EVIDENCE_EPISTEMIC_OR_SAFEGUARD_CHANGE",
        "DESTRUCTIVE_HISTORY_OR_IDENTIFIER_REUSE",
        "SECURITY_PERMISSION_OR_EXTERNAL_PRODUCTION_EFFECT",
        "INTERPRETATION_AS_DOCUMENTARY_FACT",
        "OWNER_DESIGNATION",
    }


def test_epistemic_and_runtime_safeguards_survive_simplification():
    amendment = _amendment()
    non_authorizations = set(amendment["non_authorizations"])

    assert "Does not reuse canonical identifiers." in non_authorizations
    assert (
        "Does not permit interpretation or inference to be represented as documentary fact."
        in non_authorizations
    )
    assert "Does not permit engine or LLM self-authorization." in non_authorizations
    assert (
        "Does not treat CI success as historical or philosophical proof."
        in non_authorizations
    )
    assert "Does not mutate an active version-pinned run." in non_authorizations
    assert "Does not make Neo4j canonical." in non_authorizations


def test_amendment_text_defines_joint_but_explicit_authorization():
    repo_root = _repo_root()
    content = (
        repo_root
        / "amendments/AMD-000000003_Operational_Authorization_Simplification_Amendment_v1.0.md"
    ).read_text(encoding="utf-8")

    assert "The owner merge is the single final authorization event." in content
    assert "Evidence is not authority" in content or "EVIDENCE IS NOT AUTHORITY" in content
    assert "Joint authorization is not a silent conversion." in content
    assert "A Candidate Register is optional" in content
    assert "No Candidate Cognitive Component Register is required." in content


def test_amendment_fixity_resolves():
    repo_root = _repo_root()
    amendment = _amendment()
    content_path = repo_root / amendment["content_path"]

    assert content_path.is_file()
    assert amendment["fixity"]["target_path"] == amendment["content_path"]
    assert hashlib.sha256(content_path.read_bytes()).hexdigest() == (
        amendment["fixity"]["digest"]
    )


def test_existing_candidate_register_is_optional_not_mandatory():
    repo_root = _repo_root()
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )
    amendment_content = (
        repo_root
        / "amendments/AMD-000000003_Operational_Authorization_Simplification_Amendment_v1.0.md"
    ).read_text(encoding="utf-8")

    assert "REG-000000003" in ledger["entries"]
    assert (
        repo_root
        / "registers/candidate-cognitive-component-register/REG-000000003.yaml"
    ).is_file()
    assert "REG-000000003 remains preserved as optional infrastructure." in (
        amendment_content
    )
    assert _amendment()["routine_lane"]["mandatory_candidate_stage"] is False
    assert _amendment()["next_governed_action"] == (
        "DIRECT_ROUTINE_INTEGRATION_OF_HOC-000000001"
    )


def test_amendment_assignment_and_ledger_version_are_coherent():
    repo_root = _repo_root()
    amendment_assignment = _load_yaml(
        repo_root
        / "ledgers/identifier-assignment-ledger/assignments/AMD-000000003.yaml"
    )
    version_assignment = _load_yaml(
        repo_root
        / "ledgers/identifier-assignment-ledger/assignments/VER-000000019.yaml"
    )
    version = _load_yaml(repo_root / "records/versions/VER-000000019.yaml")
    ledger = _load_yaml(
        repo_root / "ledgers/identifier-assignment-ledger/LDG-000000001.yaml"
    )

    assert amendment_assignment["assignment_authority"]["authority_id"] == (
        "CAG-000000002"
    )
    assert version_assignment["assignment_authority"]["authority_id"] == (
        "CAG-000000002"
    )
    assert version["previous_version"] == "1.12"
    assert version["current_version"] == "1.13"
    assert version["source_decision_id"] == "AMD-000000003"
    assert ledger["version"] == "1.13"
    assert ledger["entries"][-2:] == ["AMD-000000003", "VER-000000019"]
