import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.taxonomy import (
    LC016EvaluationInput,
    LeitmotifOccurrence,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    OccurrenceDifference,
    SourceQuotationRecord,
    evaluate_lc016,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-016.json").read_text())


def source_quote():
    return SourceQuotationRecord(
        source_id="SRC-1",
        source_text="The beginning of wisdom is wonder.",
        source_author="Source Author",
        source_work="Source Work",
        source_location="1.1",
        source_recovered=True,
        source_context_recovered=True,
        source_context="The source passage concerns inquiry.",
    )


def difference(diff_id="D-1", documented=True):
    return OccurrenceDifference(
        difference_id=diff_id,
        operation="OMISSION",
        expression="of wisdom",
        source_form="The beginning of wisdom is wonder.",
        occurrence_form="The beginning is wonder.",
        material_effect="removes the explicit relation to wisdom",
        material_effect_documented=documented,
    )


def occurrence(index, form="EXACT", differences=None, linked=True):
    if differences is None:
        differences = []
    text = (
        "The beginning of wisdom is wonder."
        if form == "EXACT"
        else "The beginning is wonder."
    )
    return LeitmotifOccurrence(
        occurrence_id=f"O-{index}",
        witness_location=f"chapter {index}",
        occurrence_text=text,
        form_type=form,
        quotation_family_link_documented=linked,
        local_context=f"context {index}",
        local_function=f"function {index}",
        architectonic_location=f"part {index}",
        speaker_or_source="authorial quotation",
        differences=differences,
    )


def four_occurrences():
    return [
        occurrence(1),
        occurrence(2),
        occurrence(3, "ALTERED", [difference("D-1")]),
        occurrence(4, "INCOMPLETE", [difference("D-2")]),
    ]


def base_input(**overrides):
    values = dict(
        pattern_id="PAT-1",
        declared_scope="Work A",
        source_quotation=source_quote(),
        occurrences=four_occurrences(),
        same_work_or_scope=True,
        express_quotation_relation_confirmed=True,
        distributed_across_multiple_contexts=True,
        recurrence_nontrivial_beyond_frequency=True,
        occurrence_index_complete_for_scope=True,
        collation_complete=True,
        source_integrity_confirmed=True,
        occurrence_witnesses_confirmed=True,
        local_contexts_reconstructed=True,
        architectonic_distribution_reconstructed=True,
        speaker_and_source_attribution_complete=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        negative_search_complete_within_scope=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC016EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-016"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [75]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_recovered_source_requires_location():
    with pytest.raises(ValidationError):
        SourceQuotationRecord(
            source_id="SRC-X",
            source_text="quotation",
            source_recovered=True,
            source_context_recovered=False,
        )


def test_occurrence_identifiers_must_be_unique():
    occurrences = four_occurrences()
    occurrences[1] = occurrence(1)
    with pytest.raises(ValidationError):
        base_input(occurrences=occurrences)


def test_difference_identifiers_must_be_unique_across_pattern():
    occurrences = [
        occurrence(1),
        occurrence(2),
        occurrence(3, "ALTERED", [difference("D-X")]),
        occurrence(4, "INCOMPLETE", [difference("D-X")]),
    ]
    with pytest.raises(ValidationError):
        base_input(occurrences=occurrences)


def test_fewer_than_four_occurrences_does_not_trigger():
    result = evaluate_lc016(base_input(occurrences=four_occurrences()[:3]))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unlinked_occurrence_does_not_trigger():
    occurrences = four_occurrences()
    occurrences[3] = occurrence(4, "INCOMPLETE", [difference("D-2")], linked=False)
    result = evaluate_lc016(base_input(occurrences=occurrences))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_frequency_alone_does_not_trigger():
    result = evaluate_lc016(
        base_input(recurrence_nontrivial_beyond_frequency=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_single_context_distribution_does_not_trigger():
    result = evaluate_lc016(
        base_input(distributed_across_multiple_contexts=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_occurrence_index_blocks():
    result = evaluate_lc016(
        base_input(occurrence_index_complete_for_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_occurrence_form_blocks():
    occurrences = four_occurrences()
    occurrences[3] = occurrence(4, "UNRESOLVED")
    result = evaluate_lc016(base_input(occurrences=occurrences))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_undocumented_difference_effect_blocks():
    occurrences = [
        occurrence(1),
        occurrence(2),
        occurrence(3, "ALTERED", [difference("D-1", documented=False)]),
        occurrence(4),
    ]
    result = evaluate_lc016(base_input(occurrences=occurrences))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate():
    result = evaluate_lc016(
        base_input(
            ordinary_alternatives_tested=["formulaic repetition"],
            unresolved_ordinary_alternatives=["citation convention"],
            corroborating_indicators=["architectonic distribution"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_LEITMOTIF_PATTERN
    assert result.unresolved_alternatives == ["citation convention"]


def test_corroborated_result_preserves_epistemic_limits():
    result = evaluate_lc016(
        base_input(
            ordinary_alternatives_tested=[
                "formula",
                "liturgy",
                "law",
                "scholastic convention",
                "theme frequency",
                "citation necessity",
                "memory quotation",
                "translation normalization",
                "editorial duplication",
                "witness contamination",
                "stock phrase",
                "quotation-family conflation",
                "selective scope",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the quotation recurs at four architectonically distinct locations",
                "altered forms display a consistent omission pattern",
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_LEITMOTIF_PATTERN
    assert result.hidden_significance_inferred is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
    assert result.concealed_teaching_inferred is False
    assert result.doctrinal_meaning_selected is False
    assert result.occurrence_variants_silently_normalized is False
