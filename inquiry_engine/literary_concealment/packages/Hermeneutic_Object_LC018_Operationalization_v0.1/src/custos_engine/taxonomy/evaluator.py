from __future__ import annotations

from collections import Counter

from .models import (
    LC018EvaluationInput,
    LC018EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result applies Strauss's rebuttable rule of discernment only to a "
    "documented contradictory pair with complete occurrence inventories and "
    "independent conventionality classifications. Applicability of the presumption "
    "does not establish doctrinal truth, final authorial preference, concealment, "
    "authorial intention, or intended audience."
)


def evaluate_lc018(candidate: LC018EvaluationInput) -> LC018EvaluationResult:
    """Evaluate LC-018 frequency evidence without converting presumption into truth."""

    counts = Counter(item.family_id for item in candidate.occurrences)
    family_ids = [family.family_id for family in candidate.families]
    occurrence_counts = {family_id: counts.get(family_id, 0) for family_id in family_ids}

    conventional = next(
        family for family in candidate.families
        if family.classification == "CONVENTIONAL"
    )
    unconventional = next(
        family for family in candidate.families
        if family.classification == "UNCONVENTIONAL"
    )

    common = {
        "technique_key": "LC-018",
        "pattern_id": candidate.pattern_id,
        "declared_scope": candidate.declared_scope,
        "families": candidate.families,
        "contradiction": candidate.contradiction,
        "occurrences": candidate.occurrences,
        "occurrence_counts": occurrence_counts,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.contradiction.contradiction_documented:
        trigger_failures.append("The contradictory relation is not documented.")
    if not candidate.contradiction.qualification_scope_and_modality_aligned:
        trigger_failures.append(
            "Scope, qualification, or modality is not aligned across the two statements."
        )
    if any(count == 0 for count in occurrence_counts.values()):
        trigger_failures.append(
            "Both contradictory proposition families must occur at least once."
        )
    if len(set(occurrence_counts.values())) == 1:
        trigger_failures.append("The two proposition families occur equally often.")
    if not conventional.classification_independent_of_frequency:
        trigger_failures.append(
            "The conventional classification depends on frequency rather than independent evidence."
        )
    if not unconventional.classification_independent_of_frequency:
        trigger_failures.append(
            "The unconventional classification depends on frequency rather than independent evidence."
        )
    if not conventional.classification_basis:
        trigger_failures.append(
            "No independent evidence supports the conventional classification."
        )
    if not unconventional.classification_basis:
        trigger_failures.append(
            "No independent evidence supports the unconventional classification."
        )

    if trigger_failures:
        return LC018EvaluationResult(
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
            "The evidence path from passages through counting and classification is incomplete."
        )

    unlinked = [
        item.occurrence_id
        for item in candidate.occurrences
        if not item.family_link_documented
    ]
    if unlinked:
        missing_evidence.append(
            "Proposition-family links remain undocumented for occurrences: "
            + ", ".join(unlinked)
            + "."
        )

    if missing_evidence:
        return LC018EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Complete both proposition-family occurrence inventories.",
                "Document counting and classification rules before recalculation.",
                "Resolve every speaker, quotation, implication, scope, modality, and witness record.",
                "Complete source-language, translation, variant, negative-search, and provenance review.",
                "Preserve conventionality evidence independently of frequency.",
            ],
        )

    less_frequent_family_id = min(occurrence_counts, key=occurrence_counts.get)
    presumption_statement = (
        "Under Strauss's LC-018 rule, the less frequent contradictory statement-family "
        f"({less_frequent_family_id}) is presumptively the candidate the author considered true. "
        "This is a rebuttable procedural presumption, not an adjudication of truth."
    )

    if candidate.unresolved_ordinary_alternatives:
        return LC018EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_RARITY_PRESUMPTION,
            less_frequent_family_id=less_frequent_family_id,
            straussian_presumption_applicable=True,
            presumption_statement=presumption_statement,
            reasons=[
                "The LC-018 structural conditions are present, but ordinary explanations of the frequency difference remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved topic, attribution, scope, genre, pedagogy, textual, translation, classification, and revision alternative.",
                "Preserve the presumption as rebuttable and do not select doctrinal truth.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC018EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_RARITY_PRESUMPTION,
            less_frequent_family_id=less_frequent_family_id,
            straussian_presumption_applicable=True,
            presumption_statement=presumption_statement,
            reasons=[
                "Strauss's frequency presumption is structurally applicable, but ordinary explanations have not yet been tested."
            ],
            authorized_next_actions=[
                "Test topic, quotation, objection, scope, modality, incomplete indexing, classification bias, genre, pedagogy, witness loss, translation, conventionality error, lexical recognizability, revision, and topic importance.",
                "Do not convert the presumption into a truth judgment.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC018EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_RARITY_PRESUMPTION,
            less_frequent_family_id=less_frequent_family_id,
            straussian_presumption_applicable=True,
            presumption_statement=presumption_statement,
            reasons=[
                "The frequency presumption survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for hints, low-prominence placement, common-opinion attribution, LC-019 repetition, parallel distinctions, and convergence with other devices.",
                "Maintain the result as a rebuttable candidate presumption.",
            ],
        )

    return LC018EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_RARITY_PRESUMPTION,
        less_frequent_family_id=less_frequent_family_id,
        straussian_presumption_applicable=True,
        presumption_statement=presumption_statement,
        reasons=[
            "Two proposition-families contradict one another under aligned scope, qualification, modality, and attribution.",
            "Both families occur within the declared scope and their counts are unequal.",
            "The more frequent family is independently documented as conventional.",
            "The less frequent family is independently documented as unconventional.",
            "The occurrence inventories, counting rules, witnesses, attribution, classifications, source language, translation, variants, negative search, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the frequency pattern.",
            "At least one independent corroborating indicator is recorded.",
            "Strauss's rebuttable presumption therefore applies to the less frequent family.",
            "No doctrinal truth or final authorial preference is adjudicated.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to both proposition families, the contradiction record, and complete occurrence inventories.",
            "Evaluate LC-019 separately for the frequent conventional family.",
            "Search for hints, placement signals, source relations, and counterexamples.",
            "Preserve all disputed occurrences and rival classifications.",
            "Do not convert the presumption into doctrinal truth, final authorial preference, concealment, intention, or audience.",
        ],
    )
