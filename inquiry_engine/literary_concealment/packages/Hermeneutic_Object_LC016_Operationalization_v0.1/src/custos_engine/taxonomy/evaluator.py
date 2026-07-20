from __future__ import annotations

from .models import (
    LC016EvaluationInput,
    LC016EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded four-or-more-occurrence "
    "quotation-family recurrence pattern. Exact, altered, and incomplete forms remain "
    "separate evidence. The evaluator does not establish hidden significance, authorial "
    "intention, intended audience, concealed teaching, or doctrinal meaning."
)


def evaluate_lc016(candidate: LC016EvaluationInput) -> LC016EvaluationResult:
    """Evaluate an indexed quotation recurrence without interpreting the motif."""

    common = {
        "technique_key": "LC-016",
        "pattern_id": candidate.pattern_id,
        "declared_scope": candidate.declared_scope,
        "source_quotation": candidate.source_quotation,
        "occurrences": candidate.occurrences,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if len(candidate.occurrences) < 4:
        trigger_failures.append(
            "Fewer than four distinct occurrences are recoverable."
        )
    if not candidate.same_work_or_scope:
        trigger_failures.append(
            "The occurrences do not belong to the same declared work or scope."
        )
    if not candidate.express_quotation_relation_confirmed:
        trigger_failures.append(
            "The express quotation or quotation-family relation is not confirmed."
        )
    if any(
        not occurrence.quotation_family_link_documented
        for occurrence in candidate.occurrences
    ):
        trigger_failures.append(
            "At least one occurrence lacks a documented quotation-family link."
        )
    if not candidate.distributed_across_multiple_contexts:
        trigger_failures.append(
            "The occurrences are not distributed across multiple contexts or locations."
        )
    if not candidate.recurrence_nontrivial_beyond_frequency:
        trigger_failures.append(
            "The proposed pattern does not exceed mere frequency or mechanical repetition."
        )

    if trigger_failures:
        return LC016EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.occurrence_index_complete_for_scope:
        missing_evidence.append(
            "The occurrence index is incomplete for the declared scope."
        )
    if not candidate.collation_complete:
        missing_evidence.append(
            "Occurrence-to-source collation is incomplete."
        )
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source quotation integrity is unresolved.")
    if not candidate.occurrence_witnesses_confirmed:
        missing_evidence.append("One or more occurrence witnesses are unresolved.")
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append("Local contexts are not fully reconstructed.")
    if not candidate.architectonic_distribution_reconstructed:
        missing_evidence.append(
            "Architectonic distribution is not fully reconstructed."
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
    if not candidate.negative_search_complete_within_scope:
        missing_evidence.append(
            "The negative search for additional occurrences is incomplete."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from source quotation through occurrence index is incomplete."
        )

    unresolved_forms = [
        occurrence.occurrence_id
        for occurrence in candidate.occurrences
        if occurrence.form_type == "UNRESOLVED"
    ]
    if unresolved_forms:
        missing_evidence.append(
            "Occurrence form remains unresolved for: "
            + ", ".join(unresolved_forms)
            + "."
        )

    undocumented_differences = [
        difference.difference_id
        for occurrence in candidate.occurrences
        for difference in occurrence.differences
        if not difference.material_effect_documented
    ]
    if undocumented_differences:
        missing_evidence.append(
            "Material effects remain undocumented for differences: "
            + ", ".join(undocumented_differences)
            + "."
        )

    if missing_evidence:
        return LC016EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Complete the occurrence index and negative search.",
                "Verify source and occurrence witnesses.",
                "Collate every occurrence against the source quotation.",
                "Preserve exact, altered, incomplete, and unresolved forms separately.",
                "Complete context, distribution, attribution, language, translation, and provenance review.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC016EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_LEITMOTIF_PATTERN,
            reasons=[
                "A four-or-more-occurrence quotation pattern is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved formulaic, generic, thematic, translational, editorial, witness, stock-phrase, and sampling alternative.",
                "Preserve the pattern without interpreting its significance.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC016EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_LEITMOTIF_PATTERN,
            reasons=[
                "No ordinary explanation of the recurrence has yet been tested."
            ],
            authorized_next_actions=[
                "Test formula, liturgy, law, scholastic convention, theme frequency, citation necessity, memory quotation, translation normalization, editorial duplication, contamination, proverb, family conflation, and selective scope.",
                "Do not infer importance or hidden significance from repetition alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC016EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_LEITMOTIF_PATTERN,
            reasons=[
                "The recurrence survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for architectonic distribution, patterned variation, source commentary, source alteration, device convergence, and independently verified predictions.",
                "Maintain the result as a bounded candidate leitmotif pattern.",
            ],
        )

    return LC016EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_LEITMOTIF_PATTERN,
        reasons=[
            "At least four distinct occurrences are documented within one declared work or scope.",
            "Each occurrence is linked to the same express quotation or quotation-family.",
            "The occurrences are distributed across multiple contexts or architectonic locations.",
            "Exact, altered, and incomplete forms remain separately preserved.",
            "Complete collation records every addition, omission, substitution, and reordering.",
            "Source integrity, occurrence witnesses, contexts, distribution, attribution, language, translation, variants, negative search, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the recurrence pattern.",
            "At least one independent corroborating indicator is recorded.",
            "The motif's significance remains outside the adjudicated result.",
        ],
        authorized_next_actions=[
            "Open a bounded recurrence inquiry linked to the source quotation and complete occurrence index.",
            "Search for additional occurrences, counterexamples, and unrelated repetition families.",
            "Evaluate LC-004, LC-015, LC-009, LC-017, and LC-020 separately when independently warranted.",
            "Preserve all occurrence variants and rival explanations.",
            "Do not infer hidden significance, intention, audience, concealed teaching, or doctrinal meaning.",
        ],
    )
