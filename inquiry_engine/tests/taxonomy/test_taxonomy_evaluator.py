import json
from pathlib import Path

from custos_engine.models.taxonomy import TaxonomyComponent
from custos_engine.cognition.taxonomy_evaluator import evaluate_taxonomy_component


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "taxonomy.json"


def load_component():
    return TaxonomyComponent.model_validate(json.loads(FIXTURE.read_text())[0])


def test_trigger_requires_corroboration():
    result = evaluate_taxonomy_component(
        load_component(),
        {"apparent_repetition", "minute_variation"},
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
    )
    assert not result.triggered
    assert result.disqualifier_present
