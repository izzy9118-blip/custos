import json
from pathlib import Path

import yaml

from custos_engine.repository.validators import validate_against_schema


def _root():
    return Path(__file__).resolve().parents[3]


def _yaml(path):
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_iar_preserves_ten_phases_thirty_seven_steps_and_opens_all_phases():
    root = _root()
    iar = _yaml(root / "records/inquiry-architecture/IAR-000000001.yaml")
    schema = json.loads((root / "inquiry_engine/src/custos_engine/schemas/procedure.schema.json").read_text(encoding="utf-8"))
    validate_against_schema(iar, schema)
    assert iar["version"] == "1.1"
    phases = iar["ordered_stages"]
    assert [phase["phase"] for phase in phases] == list(range(1, 11))
    assert [step["sequence"] for phase in phases for step in phase["steps"]] == list(range(1, 38))
    assert all(phase["inner_sanctum_access"] == "OPEN_PERCEPTUAL_CONSTITUTION" for phase in phases)
    assert iar["inner_sanctum_gate"]["constitutional_status"] == "ALWAYS_OPEN"
    assert iar["inner_sanctum_gate"]["required_completed_phases"] == []


def test_hoc_preserves_twenty_two_techniques_and_evidentiary_activation():
    root = _root()
    hoc = _yaml(root / "registers/hermeneutic-object-register/objects/HOC-000000001.yaml")
    assert hoc["version"] == "1.2"
    assert len(hoc["technique_inventory"]) == 22
    assert hoc["reconstruction_status"]["corpus_wide_verification"] == "NOT_YET_COMPLETE"
    assert "EVIDENCE_ALONE" in hoc["engine_use_authorization_state"]["activation_rule"]
    assert any("does not prove concealment" in item for item in hoc["uncertainty"]["findings"])


def test_constitutional_correction_does_not_fabricate_strauss_evidence():
    correction = _yaml(_root() / "records/corrections/COR-000000004.yaml")
    assert correction["epistemic_classification"]["owner_design_judgment"] == "CONSTITUTIONAL_CORRECTION"
    assert correction["epistemic_classification"]["source_derived_documentary_finding"] is False
    assert any("Does not establish" in item for item in correction["certified_limitations"])


def test_readme_states_the_permanent_rule():
    text = (_root() / "README.md").read_text(encoding="utf-8")
    assert "permanent feature of text analysis" in text
    assert "The Inner Sanctum is always open; evidence alone activates its techniques." in text
