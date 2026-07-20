import json
from pathlib import Path

from jsonschema import Draft202012Validator

from custos_engine.taxonomy import (
    LC001EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    evaluate_lc001,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-001.json").read_text())


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-001"
    assert model.canonical_identifier is None

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_noncontradictory_pair_does_not_trigger():
    result = evaluate_lc001(
        LC001EvaluationInput(
            statement_a_id="S-A",
            statement_b_id="S-B",
            same_work=True,
            same_subject=True,
            mutually_incompatible=False,
            positionally_separated=True,
            source_integrity_confirmed=True,
            local_contexts_reconstructed=True,
            speaker_or_voice_resolved=True,
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_context_blocks_evaluation():
    result = evaluate_lc001(
        LC001EvaluationInput(
            statement_a_id="S-A",
            statement_b_id="S-B",
            same_work=True,
            same_subject=True,
            mutually_incompatible=True,
            positionally_separated=True,
            source_integrity_confirmed=True,
            local_contexts_reconstructed=False,
            speaker_or_voice_resolved=True,
        )
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_ordinary_alternative_preserves_candidate_status():
    result = evaluate_lc001(
        LC001EvaluationInput(
            statement_a_id="S-A",
            statement_b_id="S-B",
            same_work=True,
            same_subject=True,
            mutually_incompatible=True,
            positionally_separated=True,
            source_integrity_confirmed=True,
            local_contexts_reconstructed=True,
            speaker_or_voice_resolved=True,
            ordinary_alternatives_tested=["different senses"],
            unresolved_ordinary_alternatives=["different audiences"],
            corroborating_indicators=["lexical recurrence"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_PAIR
    assert result.unresolved_alternatives == ["different audiences"]


def test_corroborated_result_does_not_prove_concealment_or_select_truth():
    result = evaluate_lc001(
        LC001EvaluationInput(
            statement_a_id="S-A",
            statement_b_id="S-B",
            same_work=True,
            same_subject=True,
            mutually_incompatible=True,
            positionally_separated=True,
            source_integrity_confirmed=True,
            local_contexts_reconstructed=True,
            speaker_or_voice_resolved=True,
            ordinary_alternatives_tested=[
                "different senses",
                "different audiences",
                "change over time",
                "textual variant",
                "ordinary error",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=["exact lexical recurrence"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_CONTRADICTION
    assert result.concealment_proven is False
    assert result.true_statement_selected is None
