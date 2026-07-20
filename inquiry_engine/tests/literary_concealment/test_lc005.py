import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc005 import (
    LC005EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    TextualDifference,
    evaluate_lc005,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc005"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-005.json").read_text())


def minute_difference(**overrides):
    values = dict(
        operation="ADDITION",
        expression="only",
        intermediary_form="citizens may speak",
        final_form="only citizens may speak",
        alignment_location="before citizens",
        minute_relative_to_shared_text=True,
        semantic_effect="restricts the subject class",
        semantic_effect_documented=True,
    )
    values.update(overrides)
    return TextualDifference(**values)


def base_input(**overrides):
    values = dict(
        first_statement_id="S-A",
        intermediary_statement_id="S-B",
        final_statement_id="S-C",
        first_text="all persons may speak",
        intermediary_text="citizens may speak",
        final_text="only citizens may speak",
        first_proposition="all persons may speak",
        intermediary_proposition="citizens may speak",
        final_proposition="only citizens may speak",
        same_work=True,
        same_subject=True,
        sequence_order_confirmed=True,
        intermediary_compatible_with_first=True,
        final_repeats_intermediary=True,
        differences=[minute_difference()],
        final_contradicts_first=True,
        source_integrity_confirmed=True,
        local_contexts_reconstructed=True,
        speaker_or_voice_resolved=True,
        intermediary_final_alignment_complete=True,
        proposition_normalization_documented=True,
        transition_sequence_reconstructed=True,
        translation_and_variant_review_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC005EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-005"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [71]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_three_statement_identifiers_must_be_distinct():
    with pytest.raises(ValidationError):
        base_input(final_statement_id="S-B")


def test_missing_intermediary_compatibility_does_not_trigger():
    result = evaluate_lc005(
        base_input(intermediary_compatible_with_first=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_three_stage_order_does_not_trigger():
    result = evaluate_lc005(base_input(sequence_order_confirmed=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_final_must_repeat_intermediary():
    result = evaluate_lc005(base_input(final_repeats_intermediary=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_final_must_contradict_first():
    result = evaluate_lc005(base_input(final_contradicts_first=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_alignment_blocks_evaluation():
    result = evaluate_lc005(
        base_input(intermediary_final_alignment_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc005(
        base_input(
            ordinary_alternatives_tested=["ordinary revision"],
            unresolved_ordinary_alternatives=["different speaker"],
            corroborating_indicators=["parallel sequence elsewhere"],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE
    )
    assert result.unresolved_alternatives == ["different speaker"]


def test_tested_but_uncorroborated_sequence_remains_candidate():
    result = evaluate_lc005(
        base_input(
            ordinary_alternatives_tested=[
                "ordinary development",
                "speaker change",
                "scope shift",
                "grammar",
                "translation variation",
                "witness variation",
                "ordinary inconsistency",
            ]
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE
    )


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc005(
        base_input(
            ordinary_alternatives_tested=[
                "ordinary development",
                "speaker change",
                "scope shift",
                "grammar",
                "translation variation",
                "witness variation",
                "ordinary revision",
                "ordinary inconsistency",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "another three-stage sequence reproduces the pattern"
            ],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_CREEPING_CONTRADICTION_SEQUENCE
    )
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.intermediary_rejected is False
    assert result.first_statement_rejected is False
    assert result.final_statement_rejected is False
    assert result.true_statement_selected is None
