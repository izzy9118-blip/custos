import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.taxonomy import (
    LC015EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    OmittedExpression,
    PropositionStatusRecord,
    QuotationRecord,
    SourceWitnessRecord,
    evaluate_lc015,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-015.json").read_text())


def source():
    return SourceWitnessRecord(
        source_id="SRC-1",
        source_author="Aristotle",
        source_work="Source Work",
        source_location="1.1",
        source_text="It is commonly held that the sense of touch is base.",
        source_version="critical edition A",
        source_language="Greek",
        witness_support=["edition A, line 10"],
    )


def quotation(**overrides):
    values = dict(
        quotation_id="Q-1",
        quotation_text="The sense of touch is base.",
        witness_location="Guide, passage 1",
        presents_as="DIRECT_QUOTATION",
        quotation_status_documented=True,
        speaker_or_source="authorial citation of Aristotle",
    )
    values.update(overrides)
    return QuotationRecord(**values)


def omission(**overrides):
    values = dict(
        omission_id="OM-1",
        source_expression="It is commonly held that",
        source_location_within_passage="opening qualification",
        quotation_location_after_omission="before 'the sense of touch'",
        effect_type="STATUS",
        material_effect="changes common opinion into an apparently unqualified assertion",
        material_effect_documented=True,
    )
    values.update(overrides)
    return OmittedExpression(**values)


def proposition(layer):
    if layer == "FULL_SOURCE":
        return PropositionStatusRecord(
            layer=layer,
            normalized_proposition="Common opinion holds that touch is base.",
            attribution_status="reported common opinion",
            epistemic_or_rhetorical_status="qualified report",
        )
    return PropositionStatusRecord(
        layer=layer,
        normalized_proposition="Touch is base.",
        attribution_status="apparently attributed to Aristotle",
        epistemic_or_rhetorical_status="unqualified assertion",
    )


def base_input(**overrides):
    values = dict(
        case_id="CASE-1",
        source=source(),
        quotation=quotation(),
        omissions=[omission()],
        full_source_record=proposition("FULL_SOURCE"),
        shortened_quotation_record=proposition("SHORTENED_QUOTATION"),
        source_relation_confirmed=True,
        collation_complete=True,
        material_difference_established=True,
        source_integrity_confirmed=True,
        quotation_witness_integrity_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        speaker_or_voice_resolved=True,
        source_language_review_complete=True,
        alternate_source_versions_review_complete=True,
        translation_and_variant_review_complete=True,
        quotation_boundary_confirmed=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC015EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-015"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [75, 76]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_proposition_layers_must_match_fields():
    with pytest.raises(ValidationError):
        base_input(full_source_record=proposition("SHORTENED_QUOTATION"))


def test_omission_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(omissions=[omission(), omission()])


def test_no_quotation_status_does_not_trigger():
    result = evaluate_lc015(
        base_input(quotation=quotation(quotation_status_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unconfirmed_source_relation_does_not_trigger():
    result = evaluate_lc015(base_input(source_relation_confirmed=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_omission_does_not_trigger():
    result = evaluate_lc015(base_input(omissions=[]))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_material_difference_does_not_trigger():
    result = evaluate_lc015(base_input(material_difference_established=False))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_effect_does_not_trigger():
    result = evaluate_lc015(
        base_input(omissions=[omission(material_effect_documented=False)])
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_collation_blocks():
    result = evaluate_lc015(base_input(collation_complete=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unreviewed_source_versions_block():
    result = evaluate_lc015(
        base_input(alternate_source_versions_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate():
    result = evaluate_lc015(
        base_input(
            ordinary_alternatives_tested=["ordinary abbreviation"],
            unresolved_ordinary_alternatives=["alternate source version"],
            corroborating_indicators=["author quotes source fully elsewhere"],
            direct_intentionality_evidence=["separate evidence record"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_QUOTATION_OMISSION
    assert result.unresolved_alternatives == ["alternate source version"]
    assert result.preserved_intentionality_evidence == ["separate evidence record"]
    assert result.authorial_intention_inferred is False


def test_tested_but_uncorroborated_case_remains_candidate():
    result = evaluate_lc015(
        base_input(
            ordinary_alternatives_tested=[
                "abbreviation",
                "memory quotation",
                "paraphrase",
                "alternate source version",
                "intermediary citation",
                "grammar",
                "ellipsis convention",
                "translator omission",
                "editor omission",
                "textual corruption",
                "redundancy",
                "mistaken source",
                "mistaken boundary",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_QUOTATION_OMISSION


def test_corroborated_result_preserves_epistemic_limits():
    result = evaluate_lc015(
        base_input(
            ordinary_alternatives_tested=[
                "abbreviation",
                "memory quotation",
                "paraphrase",
                "alternate source version",
                "intermediary citation",
                "grammar",
                "ellipsis convention",
                "translator omission",
                "editor omission",
                "textual corruption",
                "redundancy",
                "mistaken source",
                "mistaken boundary",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the author quotes the same source fully elsewhere"
            ],
            direct_intentionality_evidence=["separately preserved evidence"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_QUOTATION_OMISSION
    assert result.deliberate_misquotation_proven is False
    assert result.authorial_intention_inferred is False
    assert result.concealment_proven is False
    assert result.hidden_teaching_inferred is False
    assert result.intended_reader_identified is False
    assert result.fuller_source_selected_as_authorial_truth is False
    assert result.shortened_quotation_rejected_as_false is False
