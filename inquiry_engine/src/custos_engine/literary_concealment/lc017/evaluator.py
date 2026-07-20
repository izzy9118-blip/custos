from __future__ import annotations

from .models import (
    LC017EvaluationInput,
    LC017EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded relation between the "
    "first authorial word or words of a chapter and the chapter or work's structure. "
    "It does not establish hidden meaning, intended meaning, authorial intention, "
    "intended audience, or doctrinal truth."
)


def evaluate_lc017(candidate: LC017EvaluationInput) -> LC017EvaluationResult:
    """Evaluate an indexed chapter-opening relation without manufacturing a pattern."""

    target = next(
        item
        for item in candidate.openings
        if item.chapter_id == candidate.target_relation.target_chapter_id
    )

    common = {
        "technique_key": "LC-017",
        "pattern_id": candidate.pattern_id,
        "declared_scope": candidate.declared_scope,
        "openings": candidate.openings,
        "target_relation": candidate.target_relation,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not target.chapter_boundary_confirmed:
        trigger_failures.append("The target chapter boundary is not confirmed.")
    if not target.first_authorial_expression_confirmed:
        trigger_failures.append(
            "The target expression is not confirmed as the first authorial word or words."
        )
    if not target.editorial_paratext_excluded:
        trigger_failures.append(
            "Editorial headings, numerals, running heads, or supplied titles are not excluded."
        )
    if not candidate.target_relation.relation_documented:
        trigger_failures.append(
            "No lexical, grammatical, structural, or doctrinal relation is documented."
        )
    if not candidate.target_relation.initial_placement_material_to_relation:
        trigger_failures.append(
            "Initial chapter placement does not materially contribute to the proposed relation."
        )

    if trigger_failures:
        return LC017EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.opening_index_complete_for_scope:
        missing_evidence.append(
            "The chapter-opening index is incomplete for the declared scope."
        )
    if not candidate.fixed_extraction_rule_documented:
        missing_evidence.append(
            "The rule for extracting the first word or words is undocumented."
        )
    if not candidate.same_extraction_rule_applied:
        missing_evidence.append(
            "The same extraction rule was not applied to every chapter."
        )
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.chapter_boundaries_confirmed_for_scope:
        missing_evidence.append(
            "Chapter boundaries are not confirmed across the declared scope."
        )
    if not candidate.editorial_status_review_complete:
        missing_evidence.append(
            "Editorial headings, titles, numerals, and later segmentation have not been fully reviewed."
        )
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append("Local contexts are not fully reconstructed.")
    if not candidate.architectonic_structure_reconstructed:
        missing_evidence.append(
            "The work's architectonic structure is not fully reconstructed."
        )
    if not candidate.speaker_and_source_attribution_complete:
        missing_evidence.append(
            "Speaker, quotation, objection, hypothetical, or source attribution is incomplete."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, punctuation, and textual-variant review is incomplete."
        )
    if not candidate.comparison_across_all_openings_complete:
        missing_evidence.append(
            "Comparison across all indexed chapter openings is incomplete."
        )
    if not candidate.negative_cases_collected:
        missing_evidence.append(
            "Negative cases and nonconforming openings have not been collected."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness boundaries through the opening index is incomplete."
        )

    unresolved_boundaries = [
        item.chapter_id
        for item in candidate.openings
        if not item.chapter_boundary_confirmed or not item.boundary_basis
    ]
    if unresolved_boundaries:
        missing_evidence.append(
            "Boundary evidence remains incomplete for chapters: "
            + ", ".join(unresolved_boundaries)
            + "."
        )

    unresolved_paratext = [
        item.chapter_id
        for item in candidate.openings
        if not item.first_authorial_expression_confirmed
        or not item.editorial_paratext_excluded
    ]
    if unresolved_paratext:
        missing_evidence.append(
            "Authorial-opening status remains incomplete for chapters: "
            + ", ".join(unresolved_paratext)
            + "."
        )

    if missing_evidence:
        return LC017EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify every chapter boundary and exclude editorial paratext.",
                "Apply one documented extraction rule to all chapters.",
                "Complete the opening index, source-language mapping, context records, and architectonic comparison.",
                "Collect negative cases and complete the documentary evidence path.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC017EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CHAPTER_OPENING_SIGNAL,
            reasons=[
                "A chapter-opening relation is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved grammatical, transitional, formulaic, generic, editorial, translational, segmentation, coincidence, and sampling alternative.",
                "Preserve the relation without assigning intended meaning.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC017EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CHAPTER_OPENING_SIGNAL,
            reasons=[
                "No ordinary explanation of the opening relation has yet been tested."
            ],
            authorized_next_actions=[
                "Test grammar, transition, formula, genre, editorial division, translator wording, headings, scribal segmentation, coincidence, obvious topic summary, arbitrary extraction, and incomplete indexing.",
                "Do not infer significance from initial position alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC017EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CHAPTER_OPENING_SIGNAL,
            reasons=[
                "The chapter-opening relation survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for opening sequences, systematic contrasts, corresponding chapters, later development, source commentary, source alteration, and device convergence.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC017EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_CHAPTER_OPENING_SIGNAL,
        reasons=[
            "The target expression is the first authorial word or words of a securely bounded chapter.",
            "Editorial headings, numerals, running heads, and supplied titles are excluded.",
            "A fixed extraction rule is documented and applied across the complete chapter-opening index.",
            "The opening has a specific relation to subject, division, sequence, contrast, architectonic correspondence, or doctrinal relation.",
            "Initial placement materially contributes to the relation.",
            "Source integrity, boundaries, contexts, architecture, attribution, source language, translation, variants, comparison, negative cases, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the relation.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the target opening, chapter, complete index, and relation record.",
            "Search for confirming and disconfirming patterns across all chapter beginnings.",
            "Evaluate adjacent techniques separately when independently triggered.",
            "Preserve rival segmentations and explanations.",
            "Do not infer hidden meaning, intended meaning, authorial intention, audience, or doctrinal truth.",
        ],
    )
