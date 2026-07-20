import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc002 import (
    LC002EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    evaluate_lc002,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc002"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-002.json").read_text())


def base_input(**overrides):
    values = dict(
        statement_a_id="S-A",
        statement_b_id="S-B",
        incidental_statement_id="S-B",
        prominent_statement_id="S-A",
        same_work=True,
        same_subject=True,
        mutually_incompatible=True,
        incidental_placement_observed=True,
        other_statement_prominent=True,
        prominence_basis_documented=True,
        source_integrity_confirmed=True,
        local_contexts_reconstructed=True,
        speaker_or_voice_resolved=True,
    )
    values.update(overrides)
    return LC002EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-002"
    assert model.canonical_identifier is None

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_pair_roles_must_resolve_to_different_statements():
    with pytest.raises(ValidationError):
        base_input(prominent_statement_id="S-B")


def test_no_incidental_placement_does_not_trigger():
    result = evaluate_lc002(base_input(incidental_placement_observed=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_prominence_basis_blocks_evaluation():
    result = evaluate_lc002(base_input(prominence_basis_documented=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_ordinary_alternative_preserves_candidate_status():
    result = evaluate_lc002(
        base_input(
            ordinary_alternatives_tested=["different speaker"],
            unresolved_ordinary_alternatives=["general rule and special exception"],
            corroborating_indicators=["lexical recurrence"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_UNEQUAL_PROMINENCE_PAIR
    assert result.unresolved_alternatives == ["general rule and special exception"]


def test_tested_but_uncorroborated_pair_remains_candidate():
    result = evaluate_lc002(
        base_input(
            ordinary_alternatives_tested=[
                "different speaker",
                "general rule and special exception",
                "translation variation",
                "ordinary error",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_UNEQUAL_PROMINENCE_PAIR


def test_corroborated_result_does_not_prove_concealment_or_prefer_incidental_statement():
    result = evaluate_lc002(
        base_input(
            ordinary_alternatives_tested=[
                "different speaker",
                "general rule and special exception",
                "genre or syntax",
                "textual variant",
                "ordinary error",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=["repeated low-prominence formulation"],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_UNEQUAL_PROMINENCE_CONTRADICTION
    )
    assert result.concealment_proven is False
    assert result.incidental_statement_preferred is False
    assert result.true_statement_selected is None
