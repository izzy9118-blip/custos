import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from custos_engine.literary_concealment.lc018 import (
    ContradictionRecord,
    LC018EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    PropositionFamily,
    StatementOccurrence,
    evaluate_lc018,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc018"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-018.json").read_text())


def family(family_id, classification, **overrides):
    values = dict(
        family_id=family_id,
        normalized_proposition=(
            "Providence applies equally to all beings."
            if classification == "CONVENTIONAL"
            else "Providence varies by kind of being."
        ),
        classification=classification,
        classification_basis=[
            "historical doctrinal baseline",
            "intra-work audience attribution",
        ],
        classification_independent_of_frequency=True,
    )
    values.update(overrides)
    return PropositionFamily(**values)


def contradiction(**overrides):
    values = dict(
        relation_id="CR-1",
        family_a_id="F-CONV",
        family_b_id="F-UNCONV",
        governing_scope="same subject, time, modality, and authorial voice",
        contradiction_description="equal application contradicts differentiated application",
        contradiction_documented=True,
        qualification_scope_and_modality_aligned=True,
    )
    values.update(overrides)
    return ContradictionRecord(**values)


def occurrence(index, family_id, occurrence_type="DIRECT_STATEMENT", **overrides):
    values = dict(
        occurrence_id=f"O-{index}",
        family_id=family_id,
        witness_location=f"chapter {index}",
        passage_text=f"statement {index}",
        occurrence_type=occurrence_type,
        speaker_or_source="authorial exposition",
        normalized_scope="same subject and conditions",
        modality_and_qualification="assertoric, unqualified",
        family_link_documented=True,
    )
    values.update(overrides)
    return StatementOccurrence(**values)


def occurrence_set():
    return [
        occurrence(1, "F-CONV"),
        occurrence(2, "F-CONV"),
        occurrence(3, "F-CONV"),
        occurrence(4, "F-CONV"),
        occurrence(5, "F-UNCONV"),
    ]


def base_input(**overrides):
    values = dict(
        pattern_id="PAT-18-1",
        declared_scope="Work A",
        families=[
            family("F-CONV", "CONVENTIONAL"),
            family("F-UNCONV", "UNCONVENTIONAL"),
        ],
        contradiction=contradiction(),
        occurrences=occurrence_set(),
        occurrence_index_complete_for_scope=True,
        inclusion_exclusion_rules_documented=True,
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
    return LC018EvaluationInput(**values)


def test_projection_validates_against_model_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-018"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [73, 74]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_requires_one_conventional_and_one_unconventional_family():
    with pytest.raises(ValidationError):
        base_input(
            families=[
                family("F-CONV", "CONVENTIONAL"),
                family("F-UNCONV", "CONVENTIONAL"),
            ]
        )


def test_occurrence_identifiers_must_be_unique():
    with pytest.raises(ValidationError):
        base_input(
            occurrences=[
                occurrence(1, "F-CONV"),
                occurrence(1, "F-UNCONV"),
            ]
        )


def test_no_documented_contradiction_does_not_trigger():
    result = evaluate_lc018(
        base_input(contradiction=contradiction(contradiction_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_scope_or_modality_misalignment_does_not_trigger():
    result = evaluate_lc018(
        base_input(
            contradiction=contradiction(
                qualification_scope_and_modality_aligned=False
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_equal_frequency_does_not_trigger():
    result = evaluate_lc018(
        base_input(
            occurrences=[
                occurrence(1, "F-CONV"),
                occurrence(2, "F-CONV"),
                occurrence(3, "F-UNCONV"),
                occurrence(4, "F-UNCONV"),
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_family_occurrence_does_not_trigger():
    result = evaluate_lc018(
        base_input(
            occurrences=[
                occurrence(1, "F-CONV"),
                occurrence(2, "F-CONV"),
            ]
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
        family("F-UNCONV", "UNCONVENTIONAL"),
    ]
    result = evaluate_lc018(base_input(families=families))
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_incomplete_occurrence_index_blocks():
    result = evaluate_lc018(
        base_input(occurrence_index_complete_for_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unlinked_implication_blocks():
    occurrences = occurrence_set()
    occurrences[-1] = occurrence(
        5,
        "F-UNCONV",
        occurrence_type="IMPLICATION",
        family_link_documented=False,
    )
    result = evaluate_lc018(base_input(occurrences=occurrences))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_presumption():
    result = evaluate_lc018(
        base_input(
            ordinary_alternatives_tested=["topic frequency"],
            unresolved_ordinary_alternatives=["quotation attribution"],
            corroborating_indicators=["LC-019 repetition pattern"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_RARITY_PRESUMPTION
    assert result.less_frequent_family_id == "F-UNCONV"
    assert result.straussian_presumption_applicable is True
    assert result.unresolved_alternatives == ["quotation attribution"]
    assert result.doctrinal_truth_selected is False


def test_structural_rule_applies_before_corroboration_but_remains_candidate():
    result = evaluate_lc018(
        base_input(
            ordinary_alternatives_tested=[
                "topic",
                "quotation",
                "scope",
                "genre",
                "pedagogy",
                "textual loss",
                "translation",
                "classification bias",
                "revision",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_RARITY_PRESUMPTION
    assert result.straussian_presumption_applicable is True
    assert "rebuttable" in result.presumption_statement


def test_corroborated_result_applies_presumption_without_selecting_truth():
    result = evaluate_lc018(
        base_input(
            ordinary_alternatives_tested=[
                "topic",
                "quotation",
                "objection",
                "scope",
                "modality",
                "incomplete index",
                "classification bias",
                "genre",
                "pedagogy",
                "witness loss",
                "translation",
                "conventionality error",
                "lexical recognizability",
                "revision",
                "topic importance",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the frequent family is attributed to common opinion",
                "LC-019 independently confirms repeated conventional teaching",
                "a hint converges on the rare statement",
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_RARITY_PRESUMPTION
    assert result.occurrence_counts == {"F-CONV": 4, "F-UNCONV": 1}
    assert result.less_frequent_family_id == "F-UNCONV"
    assert result.straussian_presumption_applicable is True
    assert "candidate the author considered true" in result.presumption_statement
    assert result.doctrinal_truth_selected is False
    assert result.final_authorial_preference_declared is False
    assert result.concealment_proven is False
    assert result.authorial_intention_inferred is False
    assert result.intended_audience_inferred is False
