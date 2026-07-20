import json
from pathlib import Path

from jsonschema import Draft202012Validator

from custos_engine.literary_concealment.lc008 import (
    LC008EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    WordSignalRecord,
    evaluate_lc008,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc008"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-008.json").read_text())


def signal(**overrides):
    values = dict(
        word="only",
        source_language_form="term-x",
        sentence_text="The law applies only in this case.",
        word_location="middle of an otherwise incidental sentence",
        commonness_evidence=["corpus frequency record"],
        common_in_relevant_horizon=True,
        sentence_low_prominence=True,
        word_low_prominence=True,
        independent_trigger="parallel passage changes the scope",
        independent_trigger_documented=True,
        semantic_or_structural_effect="restricts the proposition's scope",
        effect_documented=True,
        counterfactual_rendering="The law applies in this case.",
        counterfactual_material_change=True,
    )
    values.update(overrides)
    return WordSignalRecord(**values)


def base_input(**overrides):
    values = dict(
        passage_id="P-1",
        signal=signal(),
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        morphology_and_syntax_review_complete=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        prominence_assessment_documented=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC008EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-008"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [72]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_noncommon_word_does_not_trigger():
    result = evaluate_lc008(
        base_input(signal=signal(common_in_relevant_horizon=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_independent_trigger_does_not_trigger():
    result = evaluate_lc008(
        base_input(signal=signal(independent_trigger_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_prominent_sentence_does_not_trigger():
    result = evaluate_lc008(
        base_input(signal=signal(sentence_low_prominence=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_material_counterfactual_change_does_not_trigger():
    result = evaluate_lc008(
        base_input(signal=signal(counterfactual_material_change=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_commonness_evidence_does_not_trigger():
    result = evaluate_lc008(
        base_input(signal=signal(commonness_evidence=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_source_language_review_blocks():
    result = evaluate_lc008(
        base_input(source_language_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_undocumented_prominence_blocks():
    result = evaluate_lc008(
        base_input(prominence_assessment_documented=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc008(
        base_input(
            ordinary_alternatives_tested=["grammar"],
            unresolved_ordinary_alternatives=["translation artifact"],
            corroborating_indicators=["same word has stable function elsewhere"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_COMMON_WORD_SIGNAL
    assert result.unresolved_alternatives == ["translation artifact"]


def test_tested_but_uncorroborated_signal_remains_candidate():
    result = evaluate_lc008(
        base_input(
            ordinary_alternatives_tested=[
                "insignificance",
                "grammar",
                "idiom",
                "style",
                "translation",
                "punctuation",
                "quotation",
                "formulaic use",
                "anachronism",
                "witness variation",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_COMMON_WORD_SIGNAL


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc008(
        base_input(
            ordinary_alternatives_tested=[
                "insignificance",
                "grammar",
                "idiom",
                "style",
                "translation",
                "punctuation",
                "quotation",
                "formulaic use",
                "anachronism",
                "witness variation",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the same word recurs at architectonically important locations"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_COMMON_WORD_SIGNAL
    assert result.concealment_proven is False
    assert result.hidden_meaning_inferred is False
    assert result.authorial_intention_inferred is False
    assert result.secret_audience_inferred is False
    assert result.doctrinal_truth_selected is False
