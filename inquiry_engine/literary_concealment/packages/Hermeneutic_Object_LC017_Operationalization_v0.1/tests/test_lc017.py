import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.taxonomy import (
    ChapterOpeningRecord,
    LC017EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    OpeningRelationRecord,
    evaluate_lc017,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-017.json").read_text())


def opening(index, **overrides):
    values = dict(
        chapter_id=f"CH-{index}",
        witness_location=f"chapter {index}, line 1",
        chapter_boundary_confirmed=True,
        boundary_basis=[f"authorial division marker {index}"],
        opening_text=f"Opening{index}",
        source_language_opening=f"SourceOpening{index}",
        extraction_unit_count=1,
        extraction_unit_type="WORD",
        first_authorial_expression_confirmed=True,
        editorial_paratext_excluded=True,
        local_context=f"chapter {index} local context",
        architectonic_location=f"part {index}",
        speaker_or_source="authorial exposition",
    )
    values.update(overrides)
    return ChapterOpeningRecord(**values)


def relation(**overrides):
    values = dict(
        relation_id="REL-LOCAL-1",
        target_chapter_id="CH-2",
        relation_type_local_noncanonical="DIVISION_SIGNAL",
        description="The opening marks the beginning of the work's second division.",
        opening_support=["distinctive opening term"],
        chapter_or_work_support=["structural transition at chapter 2"],
        initial_placement_material_to_relation=True,
        relation_documented=True,
    )
    values.update(overrides)
    return OpeningRelationRecord(**values)


def base_input(**overrides):
    values = dict(
        pattern_id="PAT-17-1",
        declared_scope="Work A",
        openings=[opening(1), opening(2), opening(3)],
        target_relation=relation(),
        opening_index_complete_for_scope=True,
        fixed_extraction_rule_documented=True,
        same_extraction_rule_applied=True,
        source_integrity_confirmed=True,
        chapter_boundaries_confirmed_for_scope=True,
        editorial_status_review_complete=True,
        local_contexts_reconstructed=True,
        architectonic_structure_reconstructed=True,
        speaker_and_source_attribution_complete=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        comparison_across_all_openings_complete=True,
        negative_cases_collected=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC017EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-017"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [77]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_chapter_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(openings=[opening(1), opening(1), opening(3)])


def test_target_relation_must_reference_indexed_chapter():
    with pytest.raises(ValidationError):
        base_input(target_relation=relation(target_chapter_id="CH-99"))


def test_declared_same_extraction_rule_must_be_consistent():
    with pytest.raises(ValidationError):
        base_input(
            openings=[
                opening(1),
                opening(2, extraction_unit_count=2),
                opening(3),
            ]
        )


def test_editorial_heading_does_not_trigger():
    openings = [opening(1), opening(2, editorial_paratext_excluded=False), opening(3)]
    result = evaluate_lc017(base_input(openings=openings))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_noninitial_expression_does_not_trigger():
    openings = [
        opening(1),
        opening(2, first_authorial_expression_confirmed=False),
        opening(3),
    ]
    result = evaluate_lc017(base_input(openings=openings))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_initial_position_without_material_relation_does_not_trigger():
    result = evaluate_lc017(
        base_input(
            target_relation=relation(initial_placement_material_to_relation=False)
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_relation_does_not_trigger():
    result = evaluate_lc017(
        base_input(target_relation=relation(relation_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_opening_index_blocks():
    result = evaluate_lc017(
        base_input(opening_index_complete_for_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_missing_boundary_basis_blocks():
    openings = [opening(1), opening(2, boundary_basis=[]), opening(3)]
    result = evaluate_lc017(base_input(openings=openings))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_missing_negative_cases_blocks():
    result = evaluate_lc017(base_input(negative_cases_collected=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate():
    result = evaluate_lc017(
        base_input(
            ordinary_alternatives_tested=["grammatical necessity"],
            unresolved_ordinary_alternatives=["formulaic opening"],
            corroborating_indicators=["systematic contrast with adjacent chapters"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_CHAPTER_OPENING_SIGNAL
    assert result.unresolved_alternatives == ["formulaic opening"]


def test_corroborated_result_preserves_epistemic_limits():
    result = evaluate_lc017(
        base_input(
            ordinary_alternatives_tested=[
                "grammar",
                "transition",
                "formula",
                "genre",
                "editorial division",
                "translator wording",
                "heading",
                "scribal segmentation",
                "coincidence",
                "obvious topic summary",
                "arbitrary extraction",
                "incomplete index",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "chapter openings form a recoverable sequence",
                "the target opening predicts a verified structural division",
            ],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_CHAPTER_OPENING_SIGNAL
    )
    assert result.hidden_meaning_inferred is False
    assert result.intended_meaning_selected is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
    assert result.doctrinal_truth_selected is False
    assert result.editorial_heading_treated_as_authorial is False
    assert result.arbitrary_extraction_rule_used is False
