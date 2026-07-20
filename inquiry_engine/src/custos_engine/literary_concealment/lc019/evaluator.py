from __future__ import annotations

from collections import Counter

from .models import (
    LC019EvaluationInput,
    LC019EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded pattern in which an "
    "independently conventional proposition-family is repeated more frequently "
    "and across more relevant opportunities than its contradictory counterpart. "
    "It does not establish falsity, exotericism, insincerity, concealment, "
    "authorial intention, intended audience, or truth of the counterpart."
)


def evaluate_lc019(candidate: LC019EvaluationInput) -> LC019EvaluationResult:
    """Evaluate conventional-view repetition without selecting truth."""

    conventional = next(
        family
        for family in candidate.families
        if family.classification == "CONVENTIONAL"
    )
    counterpart = next(
        family
        for family in candidate.families
        if family.classification == "COUNTERPART"
    )

    counts = Counter(item.family_id for item in candidate.occurrences)
    occurrence_counts = {
        conventional.family_id: counts.get(conventional.family_id, 0),
        counterpart.family_id: counts.get(counterpart.family_id, 0),
    }

    relevant_opportunities = [
        item
        for item in candidate.opportunities
        if item.relevant_to_conventional_family
    ]
    occupied_relevant_opportunities = [
        item
        for item in relevant_opportunities
        if item.conventional_family_repeated_here
    ]
    relevant_count = len(relevant_opportunities)
    occupied_count = len(occupied_relevant_opportunities)
    coverage = occupied_count / relevant_count if relevant_count else 0.0

    common = {
        "technique_key": "LC-019",
        "pattern_id": candidate.pattern_id,
        "declared_scope": candidate.declared_scope,
        "families": candidate.families,
        "contradiction": candidate.contradiction,
        "occurrences": candidate.occurrences,
        "opportunities": candidate.opportunities,
        "occurrence_counts": occurrence_counts,
        "relevant_opportunity_count": relevant_count,
        "occupied_relevant_opportunity_count": occupied_count,
        "repetition_opportunity_coverage": coverage,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.contradiction.contradiction_documented:
        trigger_failures.append("The contradictory relation is not documented.")
    if not candidate.contradiction.qualification_scope_and_modality_aligned:
        trigger_failures.append(
            "Scope, qualification, or modality is not aligned across the proposition families."
        )
    if occurrence_counts[conventional.family_id] == 0:
        trigger_failures.append("The conventional family has no occurrence.")
    if occurrence_counts[counterpart.family_id] == 0:
        trigger_failures.append("The contradictory counterpart has no occurrence.")
    if occurrence_counts[conventional.family_id] <= occurrence_counts[counterpart.family_id]:
        trigger_failures.append(
            "The conventional family does not occur more frequently than its counterpart."
        )
    if not conventional.classification_independent_of_frequency:
        trigger_failures.append(
            "The conventional classification depends on frequency rather than independent evidence."
        )
    if not conventional.classification_basis:
        trigger_failures.append(
            "No independent evidence supports the conventional classification."
        )
    if not candidate.distributed_across_multiple_contexts:
        trigger_failures.append(
            "The conventional family is not distributed across multiple contexts or architectonic locations."
        )
    if relevant_count == 0:
        trigger_failures.append(
            "No relevant repetition opportunities are documented."
        )
    if occupied_count < 2:
        trigger_failures.append(
            "The conventional family is not repeated across at least two relevant opportunities."
        )

    if trigger_failures:
        return LC019EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.occurrence_index_complete_for_scope:
        missing_evidence.append(
            "The occurrence index is incomplete for the declared scope."
        )
    if not candidate.inclusion_exclusion_rules_documented:
        missing_evidence.append(
            "Occurrence inclusion and exclusion rules are undocumented."
        )
    if not candidate.opportunity_map_complete_for_scope:
        missing_evidence.append(
            "The repetition-opportunity map is incomplete for the declared scope."
        )
    if not candidate.opportunity_rules_documented:
        missing_evidence.append(
            "Rules for identifying relevant repetition opportunities are undocumented."
        )
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source integrity is unresolved.")
    if not candidate.occurrence_witnesses_confirmed:
        missing_evidence.append("One or more occurrence witnesses are unresolved.")
    if not candidate.speaker_and_source_attribution_complete:
        missing_evidence.append(
            "Speaker, quotation, objection, hypothetical, or reported-opinion attribution is incomplete."
        )
    if not candidate.proposition_family_classification_complete:
        missing_evidence.append(
            "Proposition-family classification is incomplete."
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
            "The evidence path from passages and opportunities to the repetition-pattern claim is incomplete."
        )

    unlinked_occurrences = [
        item.occurrence_id
        for item in candidate.occurrences
        if not item.family_link_documented
    ]
    if unlinked_occurrences:
        missing_evidence.append(
            "Proposition-family links remain undocumented for occurrences: "
            + ", ".join(unlinked_occurrences)
            + "."
        )

    occupied_ids = {
        item.occurrence_id
        for item in occupied_relevant_opportunities
        if item.occurrence_id is not None
    }
    conventional_occurrence_ids = {
        item.occurrence_id
        for item in candidate.occurrences
        if item.family_id == conventional.family_id
    }
    wrongly_linked = occupied_ids - conventional_occurrence_ids
    if wrongly_linked:
        missing_evidence.append(
            "Occupied conventional opportunities link to nonconventional occurrences: "
            + ", ".join(sorted(wrongly_linked))
            + "."
        )

    if missing_evidence:
        return LC019EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Complete both proposition-family occurrence inventories.",
                "Document counting and opportunity-identification rules before recalculation.",
                "Complete the repetition-opportunity map for the declared scope.",
                "Resolve every speaker, scope, modality, witness, source-language, and translation record.",
                "Preserve conventionality evidence independently of frequency.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC019EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CONVENTIONAL_REPETITION_PATTERN,
            reasons=[
                "A conventional-view repetition pattern is present, but ordinary explanations remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved topic, pedagogical, generic, legal, quotation, attribution, translation, witness, classification, opportunity-map, and revision alternative.",
                "Preserve the frequent view without declaring it false or exoteric.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC019EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CONVENTIONAL_REPETITION_PATTERN,
            reasons=[
                "No ordinary explanation of the frequent conventional recurrence has yet been tested."
            ],
            authorized_next_actions=[
                "Test topic centrality, pedagogy, genre, law, scholastic convention, repeated quotation, narration, family conflation, missed paraphrases, speaker differences, translation normalization, editorial duplication, opportunity bias, revision, and topic importance.",
                "Do not infer falsity, exotericism, or protection from frequency alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC019EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CONVENTIONAL_REPETITION_PATTERN,
            reasons=[
                "The conventional recurrence survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for common-opinion attribution, architectonic distribution, multiple formulations, LC-018 confirmation, hints, omissions, contradictions, and witness stability.",
                "Maintain the result as a bounded candidate pattern.",
            ],
        )

    return LC019EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_CONVENTIONAL_REPETITION_PATTERN,
        reasons=[
            "A conventional proposition-family and contradictory counterpart are documentarily reconstructed.",
            "The contradiction holds under aligned scope, qualification, modality, and attribution.",
            "The conventional family occurs more frequently than its counterpart.",
            "The conventional family is independently documented as conventional.",
            "The conventional family recurs across multiple contexts and relevant repetition opportunities.",
            "The occurrence inventories, opportunity map, counting rules, witnesses, attribution, classifications, source language, translation, variants, negative search, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the repetition pattern.",
            "At least one independent corroborating indicator is recorded.",
            "No falsity, exotericism, insincerity, concealment, or truth judgment is made.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to both proposition families, the contradiction record, occurrence inventories, and opportunity map.",
            "Evaluate LC-018 separately for the rarity presumption concerning the counterpart.",
            "Search for hints, omissions, placement signals, and counterexamples.",
            "Preserve all disputed occurrences and alternative opportunity maps.",
            "Do not declare the frequent view false, exoteric, insincere, intentionally protective, or concealment-producing.",
        ],
    )
