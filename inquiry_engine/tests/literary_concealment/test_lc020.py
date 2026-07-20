import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc020 import (
    AlternativePathRecord,
    DiscoveryStep,
    HintCueRecord,
    HintTargetRecord,
    LC020EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    evaluate_lc020,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc020"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-020.json").read_text())


def cue(**overrides):
    values = dict(
        cue_id="CUE-1",
        cue_text="consider this distinction",
        witness_location="chapter 10, line 4",
        textual_boundary="one clause",
        source_language_form="source-language clause",
        cue_type_local_noncanonical="REFERENTIAL",
        directly_states_result=False,
        materially_guides_inquiry=True,
        material_guidance_description=(
            "redirects the reader from the local assertion to the earlier contradictory pair"
        ),
    )
    values.update(overrides)
    return HintCueRecord(**values)


def target(**overrides):
    values = dict(
        target_id="TARGET-1",
        target_type="CONTRADICTORY_STATEMENT_DISCERNMENT",
        target_description="which of two contradictory statements should be weighed more strongly",
        independently_documented=True,
        independent_evidence=[
            "contradiction record CR-1",
            "frequency records for both statements",
        ],
        target_scope="Work A",
    )
    values.update(overrides)
    return HintTargetRecord(**values)


def step(index, supported=True, support=None):
    if support is None:
        support = [f"documentary support {index}"]
    return DiscoveryStep(
        step_id=f"STEP-{index}",
        sequence_number=index,
        from_element="cue" if index == 1 else f"intermediate-{index-1}",
        to_element=f"intermediate-{index}" if index < 3 else "target",
        inference_description=f"bounded inference {index}",
        documentary_support=support,
        supported=supported,
    )


def alternative(index=1, tested=True, viable=False):
    return AlternativePathRecord(
        alternative_id=f"ALT-{index}",
        alternative_target_or_explanation="ordinary cross-reference",
        documentary_support=["comparison record"],
        tested=tested,
        remains_viable=viable,
    )


def base_input(**overrides):
    values = dict(
        inquiry_id="INQ-20-1",
        cue=cue(),
        target=target(),
        discovery_steps=[step(1), step(2), step(3)],
        alternative_paths=[alternative()],
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        adjacent_technique_review_complete=True,
        alternative_target_testing_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC020EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-020"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_discovery_steps_must_be_consecutive():
    with pytest.raises(ValidationError):
        base_input(discovery_steps=[step(1), step(3)])


def test_step_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(discovery_steps=[step(1), step(1)])


def test_direct_statement_is_not_a_hint():
    result = evaluate_lc020(base_input(cue=cue(directly_states_result=True)))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_suggestiveness_without_material_guidance_does_not_trigger():
    result = evaluate_lc020(
        base_input(cue=cue(materially_guides_inquiry=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_target_must_be_independently_documented():
    result = evaluate_lc020(
        base_input(
            target=target(
                independently_documented=False,
                independent_evidence=[],
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unsupported_discovery_step_does_not_trigger():
    result = evaluate_lc020(
        base_input(discovery_steps=[step(1), step(2, supported=False), step(3)])
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED
    assert result.unsupported_step_ids == ["STEP-2"]


def test_step_without_recorded_support_blocks():
    result = evaluate_lc020(
        base_input(discovery_steps=[step(1), step(2, support=[]), step(3)])
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_incomplete_adjacent_technique_review_blocks():
    result = evaluate_lc020(
        base_input(adjacent_technique_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_untested_alternative_path_blocks():
    result = evaluate_lc020(
        base_input(alternative_paths=[alternative(tested=False)])
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_viable_alternative_preserves_candidate():
    result = evaluate_lc020(
        base_input(
            alternative_paths=[alternative(viable=True)],
            ordinary_alternatives_tested=["ordinary syntax"],
            corroborating_indicators=["LC-018 convergence"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_HINT_PATH
    assert "ordinary cross-reference" in result.unresolved_alternatives


def test_no_ordinary_alternative_testing_remains_candidate():
    result = evaluate_lc020(base_input())
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_HINT_PATH


def test_tested_but_uncorroborated_path_remains_candidate():
    result = evaluate_lc020(
        base_input(
            ordinary_alternatives_tested=[
                "syntax",
                "cross-reference",
                "transition",
                "emphasis",
                "pedagogy",
                "ambiguity",
                "common-word usage",
                "editorial intervention",
                "translation",
                "corruption",
                "coincidence",
                "explicit statement",
                "hindsight",
                "unbounded association",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_HINT_PATH


def test_corroborated_result_preserves_epistemic_limits():
    result = evaluate_lc020(
        base_input(
            ordinary_alternatives_tested=[
                "syntax",
                "cross-reference",
                "transition",
                "emphasis",
                "pedagogy",
                "ambiguity",
                "common-word usage",
                "editorial intervention",
                "translation",
                "corruption",
                "coincidence",
                "explicit statement",
                "hindsight",
                "unbounded association",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the cue points to an independently established contradiction",
                "LC-018 and LC-019 converge on the same target",
                "removing the cue weakens the discovery path",
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_HINT_PATH
    assert result.hidden_teaching_inferred is False
    assert result.doctrinal_truth_selected is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
    assert result.concealment_proven is False
    assert result.unlimited_association_used is False
