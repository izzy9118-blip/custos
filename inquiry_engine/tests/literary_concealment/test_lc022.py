import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc022 import (
    AlternativeExplanationRecord,
    LC022EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    StructuralQuestionRecord,
    TextualUnitRecord,
    TransitionBaselineRecord,
    TransitionMismatchRecord,
    evaluate_lc022,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc022"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-022.json").read_text())


def unit(side, index, **overrides):
    values = dict(
        unit_id=f"UNIT-{index}",
        side=side,
        witness_location=f"chapter 8, paragraph {index}",
        unit_text=f"textual unit {index}",
        reconstructed_subject_or_task=(
            "discussion of law" if side == "BEFORE" else "discussion of prophecy"
        ),
        reconstruction_support=[f"subject analysis {index}"],
        speaker_or_source="authorial exposition",
    )
    values.update(overrides)
    return TextualUnitRecord(**values)


def baseline(**overrides):
    values = dict(
        baseline_id="BASE-22-1",
        baseline_type="AUTHORIAL_PRACTICE",
        expected_transition="a connective or intermediate step relating law to prophecy",
        documentary_support=["parallel transitions 1-4"],
        historically_appropriate=True,
        scope_relevant=True,
    )
    values.update(overrides)
    return TransitionBaselineRecord(**values)


def transition(**overrides):
    values = dict(
        transition_id="TR-22-1",
        boundary_location="between paragraphs 1 and 2",
        transition_expression="Now concerning prophecy",
        adjacency_or_explicit_link_confirmed=True,
        mismatch_type="MISSING_INTERMEDIATE_STEP",
        mismatch_description=(
            "the discourse moves from law to prophecy without the relation ordinarily supplied"
        ),
        mismatch_documented=True,
        materially_interrupts_continuity=True,
        material_structural_effect=(
            "the juxtaposition raises whether law and prophecy form a hidden division or relation"
        ),
        structural_effect_documented=True,
        functions_as_attention_directing_anomaly=True,
        attention_function_support=[
            "parallel passages supply an intermediate relation absent here"
        ],
    )
    values.update(overrides)
    return TransitionMismatchRecord(**values)


def question(**overrides):
    values = dict(
        question_id="Q-22-1",
        question_text=(
            "Why does the text move directly from law to prophecy at this boundary?"
        ),
        target_relation_or_break="possible relation or division between law and prophecy",
        bounded_by_transition=True,
        asserts_hidden_relation=False,
    )
    values.update(overrides)
    return StructuralQuestionRecord(**values)


def alternative(
    index=1,
    explanation_type="REVISION_OR_CLUMSINESS",
    tested=True,
    viable=False,
):
    return AlternativeExplanationRecord(
        alternative_id=f"ALT-{index}",
        explanation_type=explanation_type,
        explanation="the transition may simply be stylistically clumsy",
        documentary_support=["transition-practice comparison"],
        tested=tested,
        remains_viable=viable,
    )


def base_input(**overrides):
    values = dict(
        inquiry_id="INQ-22-1",
        before_unit=unit("BEFORE", 1),
        after_unit=unit("AFTER", 2),
        baseline=baseline(),
        transition=transition(),
        question=question(),
        alternatives=[alternative()],
        source_integrity_confirmed=True,
        transition_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_and_source_attribution_complete=True,
        source_language_review_complete=True,
        translation_paragraphing_and_variant_review_complete=True,
        authorial_transition_practice_review_complete=True,
        adjacent_technique_review_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC022EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-022"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_before_and_after_sides_are_enforced():
    with pytest.raises(ValidationError):
        base_input(before_unit=unit("AFTER", 1))


def test_structural_question_cannot_assert_hidden_relation():
    with pytest.raises(ValidationError):
        base_input(question=question(asserts_hidden_relation=True))


def test_alternative_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(alternatives=[alternative(1), alternative(1)])


def test_nonadjacent_units_do_not_trigger():
    result = evaluate_lc022(
        base_input(
            transition=transition(adjacency_or_explicit_link_confirmed=False)
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unreconstructed_subject_does_not_trigger():
    result = evaluate_lc022(
        base_input(
            before_unit=unit("BEFORE", 1, reconstruction_support=[])
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_transition_baseline_does_not_trigger():
    result = evaluate_lc022(
        base_input(baseline=baseline(documentary_support=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_mismatch_does_not_trigger():
    result = evaluate_lc022(
        base_input(transition=transition(mismatch_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_nonmaterial_abruptness_does_not_trigger():
    result = evaluate_lc022(
        base_input(
            transition=transition(materially_interrupts_continuity=False)
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_attention_directing_function_does_not_trigger():
    result = evaluate_lc022(
        base_input(
            transition=transition(
                functions_as_attention_directing_anomaly=False,
                attention_function_support=[],
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unbounded_question_does_not_trigger():
    result = evaluate_lc022(
        base_input(question=question(bounded_by_transition=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_source_language_review_blocks():
    result = evaluate_lc022(
        base_input(source_language_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_untested_alternative_blocks():
    result = evaluate_lc022(
        base_input(alternatives=[alternative(tested=False)])
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_viable_mere_clumsiness_preserves_candidate():
    result = evaluate_lc022(
        base_input(
            alternatives=[alternative(viable=True)],
            corroborating_indicators=["parallel transition clarifies relation"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_CLUMSY_TRANSITION_SIGNAL
    assert "the transition may simply be stylistically clumsy" in result.unresolved_alternatives
    assert result.inquiry_compelled_as_contradiction is False


def test_tested_but_uncorroborated_signal_remains_candidate():
    result = evaluate_lc022(base_input())
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_CLUMSY_TRANSITION_SIGNAL


def test_corroborated_result_preserves_weak_epistemic_limits():
    result = evaluate_lc022(
        base_input(
            alternatives=[
                alternative(1, "REVISION_OR_CLUMSINESS", tested=True, viable=False),
                alternative(2, "ELLIPSIS", tested=True, viable=False),
                alternative(3, "TRANSLATION", tested=True, viable=False),
                alternative(
                    4,
                    "EDITORIAL_SEGMENTATION",
                    tested=True,
                    viable=False,
                ),
            ],
            corroborating_indicators=[
                "a later passage supplies the missing relation",
                "a parallel passage uses a smoother transition",
                "the anomaly converges with an independent hint path",
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_CLUMSY_TRANSITION_SIGNAL
    assert result.evidentiary_force == "WEAK_POSSIBLE_SIGNAL"
    assert result.inquiry_compelled_as_contradiction is False
    assert result.concealed_relation_inferred is False
    assert result.structural_break_declared_final is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
    assert result.concealment_proven is False
    assert result.doctrinal_truth_selected is False
    assert result.mere_clumsiness_excluded_with_certainty is False
