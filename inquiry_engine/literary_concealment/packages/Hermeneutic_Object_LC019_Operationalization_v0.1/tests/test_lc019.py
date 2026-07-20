import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.taxonomy import (
    ContradictionRecord,
    LC019EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    PropositionFamily,
    RepetitionOpportunity,
    StatementOccurrence,
    evaluate_lc019,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-019.json").read_text())


def family(family_id, classification, **overrides):
    values = dict(
        family_id=family_id,
        normalized_proposition=(
            "Providence applies equally to all beings."
            if classification == "CONVENTIONAL"
            else "Providence varies by kind of being."
        ),
        classification=classification,
        classification_basis=(
            ["historical convention", "attributed to common opinion"]
            if classification == "CONVENTIONAL"
            else ["documented contradictory counterpart"]
        ),
        classification_independent_of_frequency=True,
    )
    values.update(overrides)
    return PropositionFamily(**values)


def contradiction(**overrides):
    values = dict(
        relation_id="CR-1",
        conventional_family_id="F-CONV",
        counterpart_family_id="F-COUNTER",
        governing_scope="same subject, time, modality, and voice",
        contradiction_description="equal application contradicts differentiated application",
        contradiction_documented=True,
        qualification_scope_and_modality_aligned=True,
    )
    values.update(overrides)
    return ContradictionRecord(**values)


def occurrence(index, family_id, **overrides):
    values = dict(
        occurrence_id=f"O-{index}",
        family_id=family_id,
        witness_location=f"chapter {index}",
        passage_text=f"statement {index}",
        occurrence_type="DIRECT_STATEMENT",
        speaker_or_source="authorial exposition",
        local_context=f"context {index}",
        architectonic_location=f"part {index}",
        normalized_scope="same subject and conditions",
        modality_and_qualification="assertoric, unqualified",
        family_link_documented=True,
    )
    values.update(overrides)
    return StatementOccurrence(**values)


def opportunity(index, occupied, occurrence_id=None, relevant=True):
    return RepetitionOpportunity(
        opportunity_id=f"OP-{index}",
        witness_or_structural_location=f"chapter {index}",
        opportunity_basis=f"relevant treatment {index}",
        relevant_to_conventional_family=relevant,
        conventional_family_repeated_here=occupied,
        occurrence_id=occurrence_id,
    )


def occurrences():
    return [
        occurrence(1, "F-CONV"),
        occurrence(2, "F-CONV"),
        occurrence(3, "F-CONV"),
        occurrence(4, "F-CONV"),
        occurrence(5, "F-COUNTER"),
    ]


def opportunities():
    return [
        opportunity(1, True, "O-1"),
        opportunity(2, True, "O-2"),
        opportunity(3, True, "O-3"),
        opportunity(4, True, "O-4"),
        opportunity(5, False),
    ]


def base_input(**overrides):
    values = dict(
        pattern_id="PAT-19-1",
        declared_scope="Work A",
        families=[
            family("F-CONV", "CONVENTIONAL"),
            family("F-COUNTER", "COUNTERPART"),
        ],
        contradiction=contradiction(),
        occurrences=occurrences(),
        opportunities=opportunities(),
        occurrence_index_complete_for_scope=True,
        inclusion_exclusion_rules_documented=True,
        opportunity_map_complete_for_scope=True,
        opportunity_rules_documented=True,
        distributed_across_multiple_contexts=True,
        source_integrity_confirmed=True,
        occurrence_witnesses_confirmed=True,
        speaker_and_source_attribution_complete=True,
        proposition_family_classification_complete=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        negative_search_complete_within_scope=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC019EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-019"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_requires_one_conventional_and_one_counterpart_family():
    with pytest.raises(ValidationError):
        base_input(
            families=[
                family("F-CONV", "CONVENTIONAL"),
                family("F-COUNTER", "CONVENTIONAL"),
            ]
        )


def test_occupied_opportunity_requires_occurrence_id():
    with pytest.raises(ValidationError):
        opportunity(1, True, None)


def test_occupied_opportunity_must_reference_indexed_occurrence():
    bad = opportunities()
    bad[0] = opportunity(1, True, "O-999")
    with pytest.raises(ValidationError):
        base_input(opportunities=bad)


def test_no_contradiction_does_not_trigger():
    result = evaluate_lc019(
        base_input(contradiction=contradiction(contradiction_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_equal_or_lower_frequency_does_not_trigger():
    result = evaluate_lc019(
        base_input(
            occurrences=[
                occurrence(1, "F-CONV"),
                occurrence(2, "F-COUNTER"),
                occurrence(3, "F-COUNTER"),
            ],
            opportunities=[
                opportunity(1, True, "O-1"),
                opportunity(2, False),
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_frequency_based_conventionality_does_not_trigger():
    families = [
        family(
            "F-CONV",
            "CONVENTIONAL",
            classification_independent_of_frequency=False,
        ),
        family("F-COUNTER", "COUNTERPART"),
    ]
    result = evaluate_lc019(base_input(families=families))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_single_context_does_not_trigger():
    result = evaluate_lc019(
        base_input(distributed_across_multiple_contexts=False)
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_repetition_opportunities_does_not_trigger():
    result = evaluate_lc019(
        base_input(
            opportunities=[
                opportunity(1, False, relevant=False),
                opportunity(2, False, relevant=False),
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_only_one_occupied_opportunity_does_not_trigger():
    result = evaluate_lc019(
        base_input(
            opportunities=[
                opportunity(1, True, "O-1"),
                opportunity(2, False),
                opportunity(3, False),
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_opportunity_map_blocks():
    result = evaluate_lc019(
        base_input(opportunity_map_complete_for_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate():
    result = evaluate_lc019(
        base_input(
            ordinary_alternatives_tested=["pedagogical repetition"],
            unresolved_ordinary_alternatives=["topic centrality"],
            corroborating_indicators=["LC-018 unequal-frequency pair"],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CANDIDATE_CONVENTIONAL_REPETITION_PATTERN
    )
    assert result.unresolved_alternatives == ["topic centrality"]
    assert result.frequent_view_declared_false is False


def test_corroborated_result_preserves_epistemic_limits():
    result = evaluate_lc019(
        base_input(
            ordinary_alternatives_tested=[
                "topic centrality",
                "pedagogy",
                "genre",
                "law",
                "scholastic convention",
                "repeated quotation",
                "historical narration",
                "family conflation",
                "missed paraphrases",
                "speaker differences",
                "translation normalization",
                "editorial duplication",
                "opportunity bias",
                "revision",
                "topic importance",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the frequent family is attributed to common opinion",
                "LC-018 independently confirms the unequal-frequency pair",
                "the pattern survives across authoritative witnesses",
            ],
        )
    )
    assert (
        result.outcome
        == LocalEvaluationOutcome.CORROBORATED_CONVENTIONAL_REPETITION_PATTERN
    )
    assert result.occurrence_counts == {"F-CONV": 4, "F-COUNTER": 1}
    assert result.relevant_opportunity_count == 5
    assert result.occupied_relevant_opportunity_count == 4
    assert result.repetition_opportunity_coverage == 0.8
    assert result.frequent_view_declared_false is False
    assert result.frequent_view_declared_exoteric is False
    assert result.insincerity_inferred is False
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
    assert result.counterpart_declared_true is False
