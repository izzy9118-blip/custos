import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.taxonomy import (
    LC007EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    ReadingRecord,
    evaluate_lc007,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-007.json").read_text())


def reading(face, reading_id, **overrides):
    values = dict(
        reading_id=reading_id,
        face=face,
        reading_summary=f"{face.lower()} reading",
        normalized_proposition=f"{face.lower()} proposition",
        textual_support=[f"{face.lower()} textual support"],
        communicative_function=f"{face.lower()} communicative function",
        function_documented=True,
        audience_horizon=f"{face.lower()} audience horizon",
        audience_horizon_documented=True,
        same_verbal_surface_preserved=True,
    )
    values.update(overrides)
    return ReadingRecord(**values)


def base_input(**overrides):
    values = dict(
        passage_id="P-1",
        passage_text="the same speech",
        exterior_reading=reading("EXTERIOR", "R-EXT"),
        interior_reading=reading("INTERIOR", "R-INT"),
        materially_distinct_readings=True,
        distinct_functions=True,
        distinct_audience_horizons=True,
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        genre_and_pedagogy_review_complete=True,
        translation_and_variant_review_complete=True,
        audience_evidence_review_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC007EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-007"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [72]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_reading_roles_must_match_fields():
    with pytest.raises(ValidationError):
        base_input(exterior_reading=reading("INTERIOR", "R-EXT"))


def test_reading_identifiers_must_differ():
    with pytest.raises(ValidationError):
        base_input(
            exterior_reading=reading("EXTERIOR", "R-X"),
            interior_reading=reading("INTERIOR", "R-X"),
        )


def test_single_reading_structure_does_not_trigger():
    result = evaluate_lc007(base_input(materially_distinct_readings=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_same_function_does_not_trigger():
    result = evaluate_lc007(base_input(distinct_functions=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_rewritten_surface_does_not_trigger():
    result = evaluate_lc007(
        base_input(
            interior_reading=reading(
                "INTERIOR",
                "R-INT",
                same_verbal_surface_preserved=False,
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_audience_horizon_blocks():
    result = evaluate_lc007(
        base_input(
            interior_reading=reading(
                "INTERIOR",
                "R-INT",
                audience_horizon_documented=False,
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_incomplete_genre_review_blocks():
    result = evaluate_lc007(
        base_input(genre_and_pedagogy_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_ordinary_alternative_preserves_candidate_status():
    result = evaluate_lc007(
        base_input(
            ordinary_alternatives_tested=["ordinary pedagogy"],
            unresolved_ordinary_alternatives=["difference in expertise"],
            corroborating_indicators=["explicit reader distinction"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_TWO_FACED_SPEECH
    assert result.unresolved_alternatives == ["difference in expertise"]


def test_tested_but_uncorroborated_structure_remains_candidate():
    result = evaluate_lc007(
        base_input(
            ordinary_alternatives_tested=[
                "ordinary pedagogy",
                "difference in expertise",
                "genre",
                "rhetoric",
                "lexical ambiguity",
                "irony",
                "speaker change",
                "composition history",
                "translation",
                "ordinary inconsistency",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_TWO_FACED_SPEECH


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc007(
        base_input(
            ordinary_alternatives_tested=[
                "ordinary pedagogy",
                "difference in expertise",
                "genre",
                "rhetoric",
                "lexical ambiguity",
                "irony",
                "speaker change",
                "composition history",
                "translation",
                "ordinary inconsistency",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the author explicitly distinguishes levels of readers"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_TWO_FACED_SPEECH
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.persecution_inferred is False
    assert result.actual_reader_classification_inferred is False
    assert result.exterior_reading_rejected is False
    assert result.interior_reading_selected_as_true is False
