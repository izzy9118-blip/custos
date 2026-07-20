import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc011 import (
    IronyMarker,
    LC011EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    PropositionRecord,
    evaluate_lc011,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc011"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-011.json").read_text())


def surface():
    return PropositionRecord(
        proposition_id="P-S",
        layer="SURFACE",
        proposition="The policy is admirable.",
        textual_support=["exact wording"],
    )


def nonliteral():
    return PropositionRecord(
        proposition_id="P-N",
        layer="CANDIDATE_NONLITERAL",
        proposition="The policy is blameworthy.",
        textual_support=["contextual conflict", "later explicit criticism"],
        reconstruction_basis="praise conflicts with the documented object and later judgment",
    )


def marker(marker_id="M-1", supports=True):
    return IronyMarker(
        marker_id=marker_id,
        marker_type="PRAISE_OR_BLAME_MISMATCH",
        description="Praise conflicts with the documented defects of the object.",
        documentary_support=["context record 1"],
        supports_divergence=supports,
    )


def base_input(**overrides):
    values = dict(
        remark_id="R-1",
        remark_text="What an admirable policy.",
        surface=surface(),
        candidate_nonliteral=nonliteral(),
        divergence_relation="surface praise versus candidate blame",
        materially_distinct_propositions=True,
        markers=[marker()],
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        target_or_object_review_complete=True,
        literal_coherence_tested=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC011EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-011"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_nonliteral_proposition_requires_reconstruction_basis():
    with pytest.raises(ValidationError):
        PropositionRecord(
            proposition_id="P-X",
            layer="CANDIDATE_NONLITERAL",
            proposition="different meaning",
            textual_support=["context"],
        )


def test_surface_proposition_cannot_have_reconstruction_basis():
    with pytest.raises(ValidationError):
        PropositionRecord(
            proposition_id="P-X",
            layer="SURFACE",
            proposition="literal meaning",
            textual_support=["text"],
            reconstruction_basis="not allowed",
        )


def test_proposition_identifiers_must_differ():
    with pytest.raises(ValidationError):
        base_input(
            surface=PropositionRecord(
                proposition_id="P-X",
                layer="SURFACE",
                proposition="surface",
                textual_support=["text"],
            ),
            candidate_nonliteral=PropositionRecord(
                proposition_id="P-X",
                layer="CANDIDATE_NONLITERAL",
                proposition="nonliteral",
                textual_support=["context"],
                reconstruction_basis="context",
            ),
        )


def test_no_material_divergence_does_not_trigger():
    result = evaluate_lc011(
        base_input(materially_distinct_propositions=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_tone_without_documentary_marker_does_not_trigger():
    result = evaluate_lc011(base_input(markers=[]))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_countermarker_alone_does_not_trigger():
    result = evaluate_lc011(base_input(markers=[marker(supports=False)]))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unresolved_voice_blocks_evaluation():
    result = evaluate_lc011(base_input(speaker_or_voice_resolved=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_literal_coherence_must_be_tested():
    result = evaluate_lc011(base_input(literal_coherence_tested=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc011(
        base_input(
            ordinary_alternatives_tested=["literal statement"],
            unresolved_ordinary_alternatives=["comic exaggeration"],
            corroborating_indicators=["later explicit rejection"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_IRONIC_DIVERGENCE
    assert result.unresolved_alternatives == ["comic exaggeration"]


def test_tested_but_uncorroborated_divergence_remains_candidate():
    result = evaluate_lc011(
        base_input(
            ordinary_alternatives_tested=[
                "literal statement",
                "sarcasm",
                "humor",
                "parody",
                "hyperbole",
                "understatement",
                "metaphor",
                "ambiguity",
                "quotation",
                "dramatic characterization",
                "scope change",
                "translation",
                "ordinary inconsistency",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_IRONIC_DIVERGENCE


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc011(
        base_input(
            markers=[marker(), marker("M-2", supports=False)],
            ordinary_alternatives_tested=[
                "literal statement",
                "sarcasm",
                "humor",
                "parody",
                "hyperbole",
                "understatement",
                "metaphor",
                "ambiguity",
                "quotation",
                "dramatic characterization",
                "scope change",
                "translation",
                "ordinary inconsistency",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the speaker explicitly rejects the surface proposition elsewhere"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_IRONIC_DIVERGENCE
    assert len(result.supporting_markers) == 1
    assert len(result.countermarkers) == 1
    assert result.irony_intended_proven is False
    assert result.authorial_intention_inferred is False
    assert result.hidden_teaching_inferred is False
    assert result.intended_meaning_selected is False
    assert result.authorial_position_selected is False
    assert result.canonical_subtype_assigned is False
