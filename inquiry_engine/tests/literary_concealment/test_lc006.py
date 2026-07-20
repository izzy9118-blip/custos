import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc006 import (
    LC006EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    SenseCandidate,
    evaluate_lc006,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc006"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-006.json").read_text())


def sense(
    sense_id,
    gloss,
    proposition,
    *,
    attested=True,
    source_supported=True,
    syntax=True,
    local=True,
):
    return SenseCandidate(
        sense_id=sense_id,
        gloss=gloss,
        documentary_attestation=["lexicon:1"] if attested else [],
        source_language_supported=source_supported,
        syntactically_viable=syntax,
        locally_viable=local,
        rendered_passage=f"rendered with {gloss}",
        normalized_proposition=proposition,
    )


def base_input(**overrides):
    values = dict(
        passage_id="P-1",
        passage_text="the statement is an addition",
        lexical_item="addition",
        source_language_form="term-x",
        senses=[
            sense("S1", "true addition to an untruth", "truth is appended to falsehood"),
            sense("S2", "untrue addition to the truth", "falsehood is appended to truth"),
        ],
        materially_distinct_propositions=True,
        source_integrity_confirmed=True,
        local_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        morphology_and_syntax_review_complete=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        contextual_disambiguation_tested=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC006EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-006"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [71, 72]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_sense_identifiers_must_be_unique():
    duplicate = sense("S1", "other", "other proposition")
    with pytest.raises(ValidationError):
        base_input(
            senses=[
                sense("S1", "first", "first proposition"),
                duplicate,
            ]
        )


def test_only_one_viable_sense_does_not_trigger():
    result = evaluate_lc006(
        base_input(
            senses=[
                sense("S1", "first", "first proposition"),
                sense(
                    "S2",
                    "second",
                    "second proposition",
                    syntax=False,
                ),
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_equivalent_propositions_do_not_trigger():
    result = evaluate_lc006(
        base_input(materially_distinct_propositions=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unattested_dictionary_sense_is_rejected():
    result = evaluate_lc006(
        base_input(
            senses=[
                sense("S1", "first", "first proposition"),
                sense("S2", "invented", "second proposition", attested=False),
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED
    assert len(result.rejected_senses) == 1


def test_missing_source_language_review_blocks():
    result = evaluate_lc006(
        base_input(source_language_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_missing_contextual_disambiguation_blocks():
    result = evaluate_lc006(
        base_input(contextual_disambiguation_tested=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc006(
        base_input(
            ordinary_alternatives_tested=["translation artifact"],
            unresolved_ordinary_alternatives=["technical usage"],
            corroborating_indicators=["same two senses elsewhere"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_LEXICAL_AMBIGUITY
    assert result.unresolved_alternatives == ["technical usage"]


def test_tested_but_uncorroborated_ambiguity_remains_candidate():
    result = evaluate_lc006(
        base_input(
            ordinary_alternatives_tested=[
                "dominant contextual meaning",
                "translation artifact",
                "metaphor",
                "idiom",
                "technical usage",
                "vagueness",
                "textual corruption",
                "ordinary imprecision",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_LEXICAL_AMBIGUITY


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc006(
        base_input(
            ordinary_alternatives_tested=[
                "dominant contextual meaning",
                "translation artifact",
                "metaphor",
                "idiom",
                "technical usage",
                "vagueness",
                "textual corruption",
                "ordinary imprecision",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the same word bears both senses elsewhere in the work"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_LEXICAL_AMBIGUITY
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.audience_differentiation_inferred is False
    assert result.secret_terminology_inferred is False
    assert result.true_sense_selected is None
