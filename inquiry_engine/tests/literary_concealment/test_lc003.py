import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc003 import (
    LC003EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    evaluate_lc003,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc003"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-003.json").read_text())


def base_input(**overrides):
    values = dict(
        anchor_statement_id="S-A",
        bridge_statement_ids=["S-B"],
        contrary_statement_id="S-C",
        anchor_proposition="a = b",
        bridge_propositions=["b = c"],
        derived_implication="a = c",
        contrary_proposition="a != c",
        implication_rule="transitive substitution over documented identity relations",
        same_work=True,
        bridge_chain_present=True,
        derived_implication_unpronounced=True,
        selected_contrary_directly_denies_anchor=False,
        contrary_denies_derived_implication=True,
        term_identity_or_equivalence_documented=True,
        implication_rule_validated=True,
        source_integrity_confirmed=True,
        local_contexts_reconstructed=True,
        speaker_or_voice_resolved=True,
        proposition_normalization_documented=True,
        derivation_provenance_complete=True,
    )
    values.update(overrides)
    return LC003EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-003"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [70, 71]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_chain_identifiers_must_be_distinct():
    with pytest.raises(ValidationError):
        base_input(bridge_statement_ids=["S-A"])


def test_each_bridge_requires_one_normalized_proposition():
    with pytest.raises(ValidationError):
        base_input(bridge_statement_ids=["S-B", "S-D"])


def test_direct_denial_does_not_trigger_lc003():
    result = evaluate_lc003(
        base_input(selected_contrary_directly_denies_anchor=True)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_pronounced_implication_does_not_trigger_lc003():
    result = evaluate_lc003(base_input(derived_implication_unpronounced=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_implication_validation_blocks_evaluation():
    result = evaluate_lc003(base_input(implication_rule_validated=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_ordinary_alternative_preserves_candidate_status():
    result = evaluate_lc003(
        base_input(
            ordinary_alternatives_tested=["different speaker"],
            unresolved_ordinary_alternatives=["equivocation in b"],
            corroborating_indicators=["explicit term definition"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_IMPLICATION_CONTRADICTION
    assert result.unresolved_alternatives == ["equivocation in b"]


def test_tested_but_uncorroborated_chain_remains_candidate():
    result = evaluate_lc003(
        base_input(
            ordinary_alternatives_tested=[
                "equivocation",
                "scope difference",
                "speaker difference",
                "invalid transitivity",
                "translation variation",
                "ordinary error",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_IMPLICATION_CONTRADICTION


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc003(
        base_input(
            ordinary_alternatives_tested=[
                "equivocation",
                "scope difference",
                "speaker difference",
                "invalid transitivity",
                "translation variation",
                "missing premise",
                "ordinary error",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=["explicit term definition elsewhere"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_IMPLICATION_CONTRADICTION
    assert result.concealment_proven is False
    assert result.derived_implication_treated_as_quote is False
    assert result.anchor_statement_rejected is False
    assert result.true_statement_selected is None
