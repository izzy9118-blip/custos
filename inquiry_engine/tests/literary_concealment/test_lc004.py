import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc004 import (
    LC004EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    TextualDifference,
    evaluate_lc004,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc004"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-004.json").read_text())


def minute_difference(**overrides):
    values = dict(
        operation="ADDITION",
        expression="only",
        earlier_form="all citizens may speak",
        later_form="only citizens may speak",
        alignment_location="before citizens",
        minute_relative_to_shared_text=True,
        semantic_effect="restricts the subject class",
        semantic_effect_documented=True,
    )
    values.update(overrides)
    return TextualDifference(**values)


def base_input(**overrides):
    values = dict(
        earlier_statement_id="S-A",
        later_statement_id="S-B",
        earlier_text="all citizens may speak",
        later_text="only citizens may speak",
        earlier_proposition="all citizens may speak",
        later_proposition="only citizens may speak",
        same_work=True,
        same_subject=True,
        parallel_relation_documented=True,
        later_presents_as_repetition=True,
        differences=[minute_difference()],
        substantive_contradiction_established=True,
        source_integrity_confirmed=True,
        local_contexts_reconstructed=True,
        speaker_or_voice_resolved=True,
        word_alignment_complete=True,
        proposition_normalization_documented=True,
        translation_and_variant_review_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC004EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-004"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [71]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_statement_identifiers_must_differ():
    with pytest.raises(ValidationError):
        base_input(later_statement_id="S-A")


def test_nonparallel_passages_do_not_trigger_lc004():
    result = evaluate_lc004(base_input(parallel_relation_documented=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_addition_or_omission_does_not_trigger_lc004():
    result = evaluate_lc004(base_input(differences=[]))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_wording_difference_without_contradiction_does_not_trigger():
    result = evaluate_lc004(
        base_input(substantive_contradiction_established=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_alignment_blocks_evaluation():
    result = evaluate_lc004(base_input(word_alignment_complete=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_undocumented_semantic_effect_does_not_trigger():
    result = evaluate_lc004(
        base_input(
            differences=[
                minute_difference(
                    semantic_effect_documented=False,
                    semantic_effect="effect not yet established",
                )
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unresolved_ordinary_alternative_preserves_candidate_status():
    result = evaluate_lc004(
        base_input(
            ordinary_alternatives_tested=["stylistic variation"],
            unresolved_ordinary_alternatives=["translation variation"],
            corroborating_indicators=["repeated pattern elsewhere"],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_MINUTE_VARIATION_CONTRADICTION
    )
    assert result.unresolved_alternatives == ["translation variation"]


def test_tested_but_uncorroborated_pair_remains_candidate():
    result = evaluate_lc004(
        base_input(
            ordinary_alternatives_tested=[
                "stylistic variation",
                "grammar",
                "different voice",
                "scope change",
                "translation variation",
                "witness variation",
                "ordinary revision",
            ]
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_MINUTE_VARIATION_CONTRADICTION
    )


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc004(
        base_input(
            ordinary_alternatives_tested=[
                "stylistic variation",
                "grammar",
                "abbreviation",
                "different voice",
                "scope change",
                "translation variation",
                "witness variation",
                "ordinary revision",
                "ordinary imprecision",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the expression has a stable technical function elsewhere"
            ],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_MINUTE_VARIATION_CONTRADICTION
    )
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.wording_difference_alone_treated_as_contradiction is False
    assert result.earlier_statement_rejected is False
    assert result.later_statement_rejected is False
    assert result.true_statement_selected is None
