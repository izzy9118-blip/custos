import json
from pathlib import Path

from custos_engine.models.taxonomy import TaxonomyComponent
from custos_engine.models.base import InquiryState
from custos_engine.cognition.hermeneutic_gate import HermeneuticGateContext
from custos_engine.cognition.taxonomy_evaluator import evaluate_taxonomy_component


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "taxonomy.json"


def load_component():
    return TaxonomyComponent.model_validate(json.loads(FIXTURE.read_text())[0])


def gate_context() -> HermeneuticGateContext:
    return HermeneuticGateContext(
        procedure_id="IAR-000000001",
        taxonomy_id="HOC-000000001",
        cognitive_memory_manifest_id="MAN-000000001",
        current_state=InquiryState.ADVERSARIAL_TESTING,
        completed_phase_numbers=list(range(1, 8)),
        documentary_difficulty_identified=True,
        historical_admissibility_established=True,
        authorial_authorization_established=True,
        ordinary_explanations_considered=True,
        evidence_record_ids=["EVR-000000001"],
    )


def test_trigger_requires_corroboration():
    result = evaluate_taxonomy_component(
        load_component(),
        {"apparent_repetition", "minute_variation"},
        gate_context=gate_context(),
    )
    assert not result.triggered
    assert "corroboration" in result.conclusion.lower()


def test_trigger_succeeds_with_corroboration():
    result = evaluate_taxonomy_component(
        load_component(),
        {
            "apparent_repetition",
            "minute_variation",
            "repeated_pattern_elsewhere",
        },
        gate_context=gate_context(),
    )
    assert result.triggered
    assert result.authorized_action


def test_disqualifier_blocks_trigger():
    result = evaluate_taxonomy_component(
        load_component(),
        {
            "apparent_repetition",
            "minute_variation",
            "repeated_pattern_elsewhere",
            "witness_corruption",
        },
        gate_context=gate_context(),
    )
    assert not result.triggered
    assert result.disqualifier_present
