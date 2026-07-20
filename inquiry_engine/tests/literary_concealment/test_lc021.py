import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc021 import (
    AlternativeExplanationRecord,
    AttentionQuestionRecord,
    ExpressionMismatchRecord,
    FitBaselineRecord,
    LC021EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    evaluate_lc021,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc021"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-021.json").read_text())


def baseline(**overrides):
    values = dict(
        baseline_id="BASE-21-1",
        baseline_type="AUTHORIAL_USAGE",
        expected_fit="the author consistently uses term A for this technical distinction",
        documentary_support=["parallel passages 1-5"],
        historically_appropriate=True,
        scope_relevant=True,
    )
    values.update(overrides)
    return FitBaselineRecord(**values)


def expression(**overrides):
    values = dict(
        expression_id="EXP-21-1",
        expression_text="term B",
        witness_location="chapter 12, line 8",
        textual_boundary="one noun phrase",
        local_sentence_or_clause="The author unexpectedly uses term B here.",
        source_language_form="source-language term B",
        mismatch_type="TECHNICAL",
        mismatch_description="term B conflicts with the author's established technical usage",
        mismatch_documented=True,
        materially_disrupts_surface_reading=True,
        functions_as_stumbling_block=True,
        stumbling_block_support=[
            "the substitution reverses the local technical distinction"
        ],
    )
    values.update(overrides)
    return ExpressionMismatchRecord(**values)


def question(**overrides):
    values = dict(
        question_id="Q-21-1",
        question_text="Why is term B used here instead of the established term A?",
        target_textual_problem="unexpected technical substitution",
        bounded_by_expression=True,
        asserts_hidden_answer=False,
    )
    values.update(overrides)
    return AttentionQuestionRecord(**values)


def alternative(
    index=1,
    explanation_type="MERELY_INAPPROPRIATE",
    tested=True,
    viable=False,
):
    return AlternativeExplanationRecord(
        alternative_id=f"ALT-{index}",
        explanation_type=explanation_type,
        explanation="the wording may simply be imprecise",
        documentary_support=["usage comparison"],
        tested=tested,
        remains_viable=viable,
    )


def base_input(**overrides):
    values = dict(
        inquiry_id="INQ-21-1",
        baseline=baseline(),
        expression=expression(),
        question=question(),
        alternatives=[alternative()],
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        authorial_usage_review_complete=True,
        genre_and_technical_usage_review_complete=True,
        adjacent_technique_review_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC021EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-021"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_attention_question_cannot_assert_hidden_answer():
    with pytest.raises(ValidationError):
        base_input(question=question(asserts_hidden_answer=True))


def test_alternative_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(alternatives=[alternative(1), alternative(1)])


def test_no_fit_baseline_does_not_trigger():
    result = evaluate_lc021(
        base_input(baseline=baseline(documentary_support=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_ahistorical_baseline_does_not_trigger():
    result = evaluate_lc021(
        base_input(baseline=baseline(historically_appropriate=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_mismatch_does_not_trigger():
    result = evaluate_lc021(
        base_input(expression=expression(mismatch_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_nonmaterial_awkwardness_does_not_trigger():
    result = evaluate_lc021(
        base_input(
            expression=expression(materially_disrupts_surface_reading=False)
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_stumbling_block_function_does_not_trigger():
    result = evaluate_lc021(
        base_input(
            expression=expression(
                functions_as_stumbling_block=False,
                stumbling_block_support=[],
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unbounded_question_does_not_trigger():
    result = evaluate_lc021(
        base_input(question=question(bounded_by_expression=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_source_language_review_blocks():
    result = evaluate_lc021(
        base_input(source_language_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_untested_alternative_blocks():
    result = evaluate_lc021(
        base_input(alternatives=[alternative(tested=False)])
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_viable_merely_inappropriate_explanation_preserves_candidate():
    result = evaluate_lc021(
        base_input(
            alternatives=[alternative(viable=True)],
            corroborating_indicators=["parallel passage repair"],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL
    )
    assert "the wording may simply be imprecise" in result.unresolved_alternatives
    assert result.inquiry_compelled_as_contradiction is False


def test_tested_but_uncorroborated_signal_remains_candidate():
    result = evaluate_lc021(base_input())
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL
    )


def test_corroborated_result_preserves_weak_epistemic_limits():
    result = evaluate_lc021(
        base_input(
            alternatives=[
                alternative(1, "MERELY_INAPPROPRIATE", tested=True, viable=False),
                alternative(2, "TECHNICAL_USAGE", tested=True, viable=False),
                alternative(3, "TRANSLATION", tested=True, viable=False),
                alternative(
                    4,
                    "TEXTUAL_VARIANT_OR_CORRUPTION",
                    tested=True,
                    viable=False,
                ),
            ],
            corroborating_indicators=[
                "the author uses the expected term consistently elsewhere",
                "a parallel passage repairs the mismatch",
                "the anomaly converges with an independent contradiction",
            ],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_INAPPROPRIATE_EXPRESSION_SIGNAL
    )
    assert result.evidentiary_force == "WEAK_POSSIBLE_SIGNAL"
    assert result.inquiry_compelled_as_contradiction is False
    assert result.hidden_meaning_inferred is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
    assert result.concealment_proven is False
    assert result.doctrinal_truth_selected is False
    assert result.merely_inappropriate_excluded_with_certainty is False
