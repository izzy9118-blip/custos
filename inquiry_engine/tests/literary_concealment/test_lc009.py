import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc009 import (
    LC009EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    OccurrenceRecord,
    evaluate_lc009,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc009"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-009.json").read_text())


def occurrence(occurrence_id, usage_class="CANDIDATE_CODED", **overrides):
    values = dict(
        occurrence_id=occurrence_id,
        witness_location=f"chapter:{occurrence_id}",
        surface_form="the wise",
        normalized_form="wise",
        source_language_form="term-x",
        speaker_or_source="authorial voice",
        local_context=f"context {occurrence_id}",
        architectonic_location=f"part {occurrence_id}",
        usage_class=usage_class,
        normalized_proposition=f"proposition {occurrence_id}",
        candidate_function=f"function {occurrence_id}",
        function_documented=True,
    )
    values.update(overrides)
    return OccurrenceRecord(**values)


def base_input(**overrides):
    values = dict(
        terminology_label="wise terminology",
        candidate_term="the wise",
        declared_scope="Work A",
        occurrences=[
            occurrence("O-1", "ORDINARY"),
            occurrence("O-2", "CANDIDATE_CODED"),
            occurrence("O-3", "TECHNICAL"),
        ],
        occurrence_index_complete_for_scope=True,
        variants_normalized=True,
        multiple_context_classes_present=True,
        stable_pattern_documented=True,
        pattern_nontrivial_beyond_frequency=True,
        source_integrity_confirmed=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        speaker_and_source_attribution_complete=True,
        local_contexts_reconstructed=True,
        architectonic_distribution_reconstructed=True,
        negative_cases_collected=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC009EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-009"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74, 75]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_occurrence_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(
            occurrences=[
                occurrence("O-1"),
                occurrence("O-1"),
            ]
        )


def test_single_occurrence_does_not_trigger():
    result = evaluate_lc009(
        base_input(occurrences=[occurrence("O-1")])
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_frequency_alone_does_not_trigger():
    result = evaluate_lc009(
        base_input(pattern_nontrivial_beyond_frequency=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_stable_pattern_does_not_trigger():
    result = evaluate_lc009(
        base_input(stable_pattern_documented=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_occurrence_index_blocks():
    result = evaluate_lc009(
        base_input(occurrence_index_complete_for_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_missing_negative_cases_blocks():
    result = evaluate_lc009(
        base_input(negative_cases_collected=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_undocumented_occurrence_function_blocks():
    result = evaluate_lc009(
        base_input(
            occurrences=[
                occurrence("O-1"),
                occurrence("O-2", function_documented=False),
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc009(
        base_input(
            ordinary_alternatives_tested=["ordinary technical vocabulary"],
            unresolved_ordinary_alternatives=["subject-matter frequency"],
            corroborating_indicators=["complementary term distribution"],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_SECRET_TERMINOLOGY_PATTERN
    )
    assert result.unresolved_alternatives == ["subject-matter frequency"]


def test_tested_but_uncorroborated_pattern_remains_candidate():
    result = evaluate_lc009(
        base_input(
            ordinary_alternatives_tested=[
                "technical vocabulary",
                "genre",
                "subject matter",
                "translation convention",
                "semantic drift",
                "speaker differences",
                "editorial normalization",
                "style",
                "index bias",
            ]
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_SECRET_TERMINOLOGY_PATTERN
    )


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc009(
        base_input(
            ordinary_alternatives_tested=[
                "technical vocabulary",
                "genre",
                "subject matter",
                "translation convention",
                "semantic drift",
                "speaker differences",
                "editorial normalization",
                "style",
                "index bias",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the terminology predicts independently verified passage distinctions"
            ],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_SECRET_TERMINOLOGY_PATTERN
    )
    assert result.concealment_proven is False
    assert result.hidden_meaning_inferred is False
    assert result.authorial_intention_inferred is False
    assert result.audience_inferred is False
    assert result.doctrinal_truth_selected is False
