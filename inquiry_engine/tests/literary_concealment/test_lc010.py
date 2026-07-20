import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc010 import (
    DefectRecord,
    InferenceStep,
    LC010EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    PremiseRecord,
    evaluate_lc010,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc010"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-010.json").read_text())


def explicit_premise():
    return PremiseRecord(
        premise_id="P-1",
        text="All A are B.",
        status="EXPLICIT",
        witness_support=["line 1"],
    )


def reconstructed_premise():
    return PremiseRecord(
        premise_id="P-2",
        text="All B are C.",
        status="RECONSTRUCTED",
        witness_support=["line 2 implication"],
        reconstruction_basis="required to connect the explicit premise to the conclusion",
    )


def inference_step():
    return InferenceStep(
        step_id="I-1",
        from_ids=["P-1", "P-2"],
        result_text="All A are C.",
        rule_or_relation="purported transitive inference",
        textually_explicit=False,
    )


def defect(**overrides):
    values = dict(
        local_label_noncanonical="equivocal middle term",
        description="B changes meaning between the two premises.",
        governing_standard="the middle term must retain the same meaning",
        documentary_support=["lexical record 1", "context record 2"],
        defect_documented=True,
        materially_affects_support=True,
        corrected_argument_summary="With a stable meaning of B, the conclusion no longer follows.",
        correction_changes_support=True,
    )
    values.update(overrides)
    return DefectRecord(**values)


def base_input(**overrides):
    values = dict(
        argument_id="ARG-1",
        argument_text="All A are B; all B are C; therefore all A are C.",
        premises=[explicit_premise(), reconstructed_premise()],
        inference_steps=[inference_step()],
        conclusion_text="All A are C.",
        defect=defect(),
        bounded_argument_reconstructed=True,
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        counterfactual_analysis_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC010EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-010"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_reconstructed_premise_requires_basis():
    with pytest.raises(ValidationError):
        PremiseRecord(
            premise_id="P-X",
            text="unstated premise",
            status="RECONSTRUCTED",
            witness_support=[],
        )


def test_explicit_premise_must_not_have_reconstruction_basis():
    with pytest.raises(ValidationError):
        PremiseRecord(
            premise_id="P-X",
            text="explicit premise",
            status="EXPLICIT",
            witness_support=["line 1"],
            reconstruction_basis="not allowed",
        )


def test_argument_record_ids_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(
            premises=[explicit_premise(), explicit_premise()]
        )


def test_no_documented_defect_does_not_trigger():
    result = evaluate_lc010(
        base_input(defect=defect(defect_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_nonmaterial_defect_does_not_trigger():
    result = evaluate_lc010(
        base_input(defect=defect(materially_affects_support=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_correction_that_changes_nothing_does_not_trigger():
    result = evaluate_lc010(
        base_input(defect=defect(correction_changes_support=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unresolved_voice_blocks_evaluation():
    result = evaluate_lc010(
        base_input(speaker_or_voice_resolved=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc010(
        base_input(
            ordinary_alternatives_tested=["unintentional error"],
            unresolved_ordinary_alternatives=["unstated premise"],
            corroborating_indicators=["same defect pattern elsewhere"],
            direct_intentionality_evidence=["separate evidence record"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_SOPHISTIC_STRUCTURE
    assert result.unresolved_alternatives == ["unstated premise"]
    assert result.preserved_intentionality_evidence == ["separate evidence record"]
    assert result.authorial_intention_inferred is False


def test_tested_but_uncorroborated_structure_remains_candidate():
    result = evaluate_lc010(
        base_input(
            ordinary_alternatives_tested=[
                "unintentional error",
                "unstated premise",
                "pedagogical simplification",
                "rhetorical abbreviation",
                "translation",
                "textual corruption",
                "speaker change",
                "scope change",
                "ordinary revision",
                "investigator misreconstruction",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_SOPHISTIC_STRUCTURE


def test_corroborated_result_never_declares_intentionality():
    result = evaluate_lc010(
        base_input(
            ordinary_alternatives_tested=[
                "unintentional error",
                "unstated premise",
                "pedagogical simplification",
                "rhetorical abbreviation",
                "translation",
                "textual corruption",
                "speaker change",
                "scope change",
                "ordinary revision",
                "investigator misreconstruction",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the author supplies the governing distinction elsewhere"
            ],
            direct_intentionality_evidence=[
                "separately preserved direct evidence record"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_SOPHISTIC_STRUCTURE
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.intentional_sophism_declared is False
    assert result.hidden_teaching_inferred is False
    assert result.authorial_position_selected is False
    assert result.canonical_subtype_assigned is False
    assert result.preserved_intentionality_evidence == [
        "separately preserved direct evidence record"
    ]
