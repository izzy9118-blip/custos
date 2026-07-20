import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.taxonomy import (
    ExpectationBaseline,
    LC014EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    OmissionRecord,
    evaluate_lc014,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-014.json").read_text())


def baseline(**overrides):
    values = dict(
        baseline_id="BASE-1",
        baseline_type="RECOVERED_SOURCE",
        expected_item="qualification that the statement is common opinion",
        basis_description="the cited source contains the qualification",
        documentary_support=["source passage line 10"],
        historically_appropriate=True,
        scope_relevant=True,
    )
    values.update(overrides)
    return ExpectationBaseline(**values)


def omission(**overrides):
    values = dict(
        bounded_unit_id="UNIT-1",
        bounded_unit_text="The cited proposition without the qualification.",
        textual_scope="the complete quotation",
        expected_item="qualification that the statement is common opinion",
        item_absent_in_relevant_witness=True,
        absence_verification=["witness collation record"],
        omission_effect_type="STATUS",
        material_effect="the proposition appears to be Aristotle's teaching rather than common opinion",
        material_effect_documented=True,
        counterfactual_inclusion="The proposition is common opinion.",
        counterfactual_changes_passage=True,
    )
    values.update(overrides)
    return OmissionRecord(**values)


def base_input(**overrides):
    values = dict(
        omission_id="OM-1",
        baseline=baseline(),
        omission=omission(),
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        doctrinal_scope_confirmed=True,
        speaker_or_voice_resolved=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        negative_search_complete_within_scope=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC014EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-014"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [75, 76, 77]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_expected_item_must_match_between_records():
    with pytest.raises(ValidationError):
        base_input(
            omission=omission(expected_item="different item")
        )


def test_no_documentary_baseline_does_not_trigger():
    result = evaluate_lc014(
        base_input(baseline=baseline(documentary_support=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_ahistorical_baseline_does_not_trigger():
    result = evaluate_lc014(
        base_input(baseline=baseline(historically_appropriate=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_scope_irrelevant_baseline_does_not_trigger():
    result = evaluate_lc014(
        base_input(baseline=baseline(scope_relevant=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_item_present_does_not_trigger():
    result = evaluate_lc014(
        base_input(omission=omission(item_absent_in_relevant_witness=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unverified_absence_does_not_trigger():
    result = evaluate_lc014(
        base_input(omission=omission(absence_verification=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_material_effect_does_not_trigger():
    result = evaluate_lc014(
        base_input(omission=omission(material_effect_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_negative_search_blocks():
    result = evaluate_lc014(
        base_input(negative_search_complete_within_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_scope_blocks():
    result = evaluate_lc014(base_input(doctrinal_scope_confirmed=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc014(
        base_input(
            ordinary_alternatives_tested=["ordinary abbreviation"],
            unresolved_ordinary_alternatives=["different source version"],
            corroborating_indicators=["parallel passage includes the item"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_SIGNIFICANT_OMISSION
    assert result.unresolved_alternatives == ["different source version"]


def test_tested_but_uncorroborated_omission_remains_candidate():
    result = evaluate_lc014(
        base_input(
            ordinary_alternatives_tested=[
                "scope",
                "summary",
                "genre",
                "pedagogy",
                "supplied elsewhere",
                "translation",
                "textual loss",
                "different source version",
                "speaker change",
                "revision",
                "mistaken baseline",
                "mistaken boundary",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_SIGNIFICANT_OMISSION


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc014(
        base_input(
            ordinary_alternatives_tested=[
                "scope",
                "summary",
                "genre",
                "pedagogy",
                "supplied elsewhere",
                "translation",
                "textual loss",
                "different source version",
                "speaker change",
                "revision",
                "mistaken baseline",
                "mistaken boundary",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the recovered source contains the omitted qualification"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_SIGNIFICANT_OMISSION
    assert result.deliberate_silence_proven is False
    assert result.authorial_intention_inferred is False
    assert result.missing_teaching_supplied is False
    assert result.intended_reader_identified is False
    assert result.exoteric_status_declared is False
    assert result.doctrinal_truth_selected is False
