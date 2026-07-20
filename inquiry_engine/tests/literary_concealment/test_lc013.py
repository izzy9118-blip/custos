import json
from pathlib import Path

from jsonschema import Draft202012Validator

from custos_engine.literary_concealment.lc013 import (
    AllusiveRelationRecord,
    LC013EvaluationInput,
    LiteraryConcealmentTechnique,
    LocalEvaluationOutcome,
    MottoRecord,
    MottoSourceRecord,
    evaluate_lc013,
)

ROOT = Path(__file__).resolve().parents[2] / "src" / "custos_engine" / "literary_concealment" / "lc013"


def load_projection():
    return json.loads((ROOT / "techniques" / "LC-013.json").read_text())


def source_record(**overrides):
    values = dict(
        attribution="Source Author",
        source_text="A path through darkness.",
        source_location="Source Work 1.1",
        source_context="The source passage concerns difficult guidance.",
        source_recovered=True,
        source_context_recovered=True,
    )
    values.update(overrides)
    return MottoSourceRecord(**values)


def motto(**overrides):
    values = dict(
        motto_text="A path through darkness.",
        witness_location="before Part II",
        placement_type="PART",
        governed_scope="Part II",
        governed_scope_documented=True,
        present_in_authorially_relevant_witness=True,
        provenance_status="AUTHORIAL",
        provenance_evidence=["first edition witness"],
        source=source_record(),
        surface_function="announces the theme of guidance",
        surface_function_documented=True,
    )
    values.update(overrides)
    return MottoRecord(**values)


def relation(**overrides):
    values = dict(
        relation_id="REL-LOCAL-1",
        relation_type_local_noncanonical="SOURCE_CONTEXT_KEY",
        description="The source context supplies a sequence reproduced in Part II.",
        motto_support=["path", "darkness"],
        governed_scope_support=["Part II sections 1-3 reproduce the sequence"],
        materially_specific_beyond_theme=True,
        relation_documented=True,
    )
    values.update(overrides)
    return AllusiveRelationRecord(**values)


def base_input(**overrides):
    values = dict(
        motto_id="MOTTO-1",
        motto=motto(),
        relation=relation(),
        source_integrity_confirmed=True,
        textual_boundary_confirmed=True,
        governed_scope_boundary_confirmed=True,
        local_context_reconstructed=True,
        architectonic_context_reconstructed=True,
        source_language_review_complete=True,
        translation_and_variant_review_complete=True,
        editorial_provenance_review_complete=True,
        comparison_index_complete_for_claimed_scope=True,
        evidence_path_complete=True,
    )
    values.update(overrides)
    return LC013EvaluationInput(**values)


def test_projection_validates_against_pydantic_and_schema():
    projection = load_projection()
    model = LiteraryConcealmentTechnique.model_validate(projection)
    assert model.technique_key == "LC-013"
    assert model.canonical_identifier is None
    assert model.source.source_pages == [75]

    schema = json.loads(
        (ROOT / "schemas" / "literary_concealment_technique.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(projection)


def test_editorial_epigraph_does_not_trigger():
    result = evaluate_lc013(
        base_input(
            motto=motto(
                provenance_status="EDITORIAL",
                provenance_evidence=["modern editor note"],
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_absent_from_authorial_witness_does_not_trigger():
    result = evaluate_lc013(
        base_input(motto=motto(present_in_authorially_relevant_witness=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_undocumented_governed_scope_does_not_trigger():
    result = evaluate_lc013(
        base_input(motto=motto(governed_scope_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_broad_theme_only_does_not_trigger():
    result = evaluate_lc013(
        base_input(relation=relation(materially_specific_beyond_theme=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_no_documented_relation_does_not_trigger():
    result = evaluate_lc013(
        base_input(relation=relation(relation_documented=False))
    )
    assert result.outcome == LocalEvaluationOutcome.NOT_TRIGGERED


def test_missing_provenance_evidence_blocks():
    result = evaluate_lc013(
        base_input(motto=motto(provenance_evidence=[]))
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_recovered_source_requires_location():
    result = evaluate_lc013(
        base_input(
            motto=motto(
                source=source_record(source_location=None)
            )
        )
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_incomplete_editorial_review_blocks():
    result = evaluate_lc013(
        base_input(editorial_provenance_review_complete=False)
    )
    assert result.outcome == LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE


def test_unresolved_alternative_preserves_candidate_status():
    result = evaluate_lc013(
        base_input(
            ordinary_alternatives_tested=["decorative epigraph"],
            unresolved_ordinary_alternatives=["general thematic summary"],
            corroborating_indicators=["distinctive sequence recurs in governed part"],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_MOTTO_ALLUSION
    assert result.unresolved_alternatives == ["general thematic summary"]


def test_tested_but_uncorroborated_relation_remains_candidate():
    result = evaluate_lc013(
        base_input(
            ordinary_alternatives_tested=[
                "decorative epigraph",
                "thematic summary",
                "devotional formula",
                "dedication",
                "genre convention",
                "editorial addition",
                "source acknowledgment",
                "style",
                "common vocabulary",
                "scope overextension",
            ]
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CANDIDATE_MOTTO_ALLUSION


def test_corroborated_result_preserves_noninterpretive_boundaries():
    result = evaluate_lc013(
        base_input(
            ordinary_alternatives_tested=[
                "decorative epigraph",
                "thematic summary",
                "devotional formula",
                "dedication",
                "genre convention",
                "editorial addition",
                "source acknowledgment",
                "style",
                "common vocabulary",
                "scope overextension",
            ],
            unresolved_ordinary_alternatives=[],
            corroborating_indicators=[
                "the governed unit reproduces the source passage's sequence"
            ],
        )
    )
    assert result.outcome == LocalEvaluationOutcome.CORROBORATED_MOTTO_ALLUSION
    assert result.concealment_proven is False
    assert result.hidden_key_declared is False
    assert result.intended_meaning_selected is False
    assert result.intended_audience_inferred is False
    assert result.authorial_intention_inferred is False
    assert result.doctrinal_truth_selected is False
