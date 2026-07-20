from __future__ import annotations

from .models import (
    LC009EvaluationInput,
    LC009EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded corpus-level terminology "
    "pattern. It does not establish concealment, hidden meaning, authorial intention, "
    "audience, or doctrinal truth."
)


def evaluate_lc009(candidate: LC009EvaluationInput) -> LC009EvaluationResult:
    """Evaluate a structured terminology index without generating secret terms."""

    common = {
        "technique_key": "LC-009",
        "terminology_label": candidate.terminology_label,
        "candidate_term": candidate.candidate_term,
        "declared_scope": candidate.declared_scope,
        "occurrences": candidate.occurrences,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if len(candidate.occurrences) < 2:
        trigger_failures.append(
            "The candidate term does not recur within the declared scope."
        )
    if not candidate.multiple_context_classes_present:
        trigger_failures.append(
            "The occurrence set does not include multiple context or usage classes."
        )
    if not candidate.stable_pattern_documented:
        trigger_failures.append(
            "No stable semantic, functional, positional, audience, or doctrinal pattern is documented."
        )
    if not candidate.pattern_nontrivial_beyond_frequency:
        trigger_failures.append(
            "The proposed pattern does not exceed mere frequency."
        )

    if trigger_failures:
        return LC009EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.occurrence_index_complete_for_scope:
        missing_evidence.append(
            "The occurrence index is incomplete for the declared scope."
        )
    if not candidate.variants_normalized:
        missing_evidence.append(
            "Inflectional, orthographic, or translational variants are not normalized."
        )
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, and textual-variant review is incomplete."
        )
    if not candidate.speaker_and_source_attribution_complete:
        missing_evidence.append(
            "Speaker, quotation, and source attribution are incomplete."
        )
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append("Local contexts are not fully reconstructed.")
    if not candidate.architectonic_distribution_reconstructed:
        missing_evidence.append(
            "Architectonic distribution across the declared scope is not reconstructed."
        )
    if not candidate.negative_cases_collected:
        missing_evidence.append(
            "Negative cases and counterexamples have not been collected."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from occurrences to the terminology-pattern claim is incomplete."
        )

    undocumented = [
        occ.occurrence_id for occ in candidate.occurrences
        if not occ.function_documented
    ]
    if undocumented:
        missing_evidence.append(
            "Candidate functions remain undocumented for occurrences: "
            + ", ".join(undocumented)
            + "."
        )

    if missing_evidence:
        return LC009EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Complete the occurrence index for the declared scope.",
                "Normalize variants while preserving original forms.",
                "Complete source-language, translation, witness, attribution, local-context, and architectonic review.",
                "Collect negative cases and document each occurrence's function.",
                "Complete the evidence path before evaluating terminology status.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC009EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SECRET_TERMINOLOGY_PATTERN,
            reasons=[
                "A recurrent terminology pattern is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved technical, generic, translational, editorial, thematic, and distributional alternative.",
                "Preserve the complete occurrence index and all negative cases.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC009EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SECRET_TERMINOLOGY_PATTERN,
            reasons=[
                "No ordinary explanation of the terminology pattern has yet been tested."
            ],
            authorized_next_actions=[
                "Test technical vocabulary, genre, subject matter, translation convention, semantic drift, speaker differences, editorial normalization, style, and index bias.",
                "Do not infer secret terminology from recurrence alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC009EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SECRET_TERMINOLOGY_PATTERN,
            reasons=[
                "The terminology pattern survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for explicit distinctions, complementary terms, architectonic clustering, source comparison, and independently verified predictions.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC009EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_SECRET_TERMINOLOGY_PATTERN,
        reasons=[
            "The candidate term recurs across the declared scope.",
            "The occurrence index is complete for that scope and variants are normalized.",
            "Multiple context or usage classes are represented.",
            "A stable nontrivial semantic, functional, positional, audience, or doctrinal pattern is documented.",
            "Source integrity, source language, translation, variants, attribution, local contexts, architectonic distribution, negative cases, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the pattern.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded terminology inquiry linked to the complete occurrence index.",
            "Test the pattern against additional works only after independent reconstruction.",
            "Evaluate LC-006 and LC-008 separately for individual occurrences when warranted.",
            "Preserve negative cases, rival explanations, and the complete documentary path.",
            "Do not infer concealment, hidden meaning, authorial intention, audience, or doctrinal truth.",
        ],
    )
