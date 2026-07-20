import json
from pathlib import Path

from jsonschema import Draft202012Validator

from custos_engine.taxonomy import (
    LC012EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    ReaderAddressRecord,
    evaluate_lc012,
)

ROOT = Path(__file__).resolve().parents[1]


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-012.json").read_text())


def address(**overrides):
    values = dict(
        address_text="Know, reader, that this matter requires care.",
        source_language_form="source-language address",
        grammatical_form="DIRECT_NOMINAL_ADDRESS",
        resolved_addressee="the reader of the work",
        addressee_is_reader=True,
        addressee_evidence=["explicit noun reader"],
        placement="opening of a restricted discussion",
        placement_documented=True,
        local_function_label_noncanonical="warning",
        communicative_effect="marks a transition and warns the reader to attend",
        communicative_effect_documented=True,
        modifies_surrounding_exposition=True,
    )
    values.update(overrides)
    return ReaderAddressRecord(**values)


def base_input(**overrides):
    values = dict(
        address_id="A-1",
        address=address(),
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        speaker_or_voice_resolved=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        genre_convention_review_complete=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        comparison_index_complete_for_claimed_scope=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC012EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-012"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [75]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_nonreader_apostrophe_does_not_trigger():
    result = evaluate_lc012(
        base_input(
            address=address(
                resolved_addressee="a city",
                addressee_is_reader=False,
                addressee_evidence=["vocative city"],
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_second_person_without_addressee_evidence_does_not_trigger():
    result = evaluate_lc012(
        base_input(address=address(addressee_evidence=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_placement_does_not_trigger():
    result = evaluate_lc012(
        base_input(address=address(placement_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_communicative_effect_does_not_trigger():
    result = evaluate_lc012(
        base_input(address=address(communicative_effect_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_modification_of_exposition_does_not_trigger():
    result = evaluate_lc012(
        base_input(address=address(modifies_surrounding_exposition=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_unresolved_voice_blocks_evaluation():
    result = evaluate_lc012(base_input(speaker_or_voice_resolved=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_incomplete_genre_review_blocks_evaluation():
    result = evaluate_lc012(base_input(genre_convention_review_complete=False))
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_incomplete_comparison_index_blocks_claim():
    result = evaluate_lc012(
        base_input(comparison_index_complete_for_claimed_scope=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc012(
        base_input(
            ordinary_alternatives_tested=["generic rhetoric"],
            unresolved_ordinary_alternatives=["ordinary pedagogy"],
            corroborating_indicators=["explicit reader distinction elsewhere"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_READER_ADDRESS_SIGNAL
    assert result.unresolved_alternatives == ["ordinary pedagogy"]


def test_tested_but_uncorroborated_signal_remains_candidate():
    result = evaluate_lc012(
        base_input(
            ordinary_alternatives_tested=[
                "generic rhetoric",
                "ordinary pedagogy",
                "preface convention",
                "nonreader apostrophe",
                "dramatic interlocution",
                "quotation",
                "translation convention",
                "style",
                "editorial intervention",
                "broad inclusive language",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_READER_ADDRESS_SIGNAL


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc012(
        base_input(
            ordinary_alternatives_tested=[
                "generic rhetoric",
                "ordinary pedagogy",
                "preface convention",
                "nonreader apostrophe",
                "dramatic interlocution",
                "quotation",
                "translation convention",
                "style",
                "editorial intervention",
                "broad inclusive language",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the work repeats different reader addresses at marked locations"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_READER_ADDRESS_SIGNAL
    assert result.concealment_proven is False
    assert result.intended_reader_identified is False
    assert result.differentiated_audience_inferred is False
    assert result.hidden_instruction_inferred is False
    assert result.authorial_intention_inferred is False
    assert result.canonical_subtype_assigned is False
