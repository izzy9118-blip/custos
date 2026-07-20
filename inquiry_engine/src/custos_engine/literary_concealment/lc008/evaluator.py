from __future__ import annotations

from .models import (
    LC008EvaluationInput,
    LC008EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded common-word signal: "
    "an ordinary word in a low-prominence setting whose material effect is "
    "independently documented. It does not establish a secret, hidden meaning, "
    "authorial intention, audience, or doctrinal truth."
)


def evaluate_lc008(candidate: LC008EvaluationInput) -> LC008EvaluationResult:
    """Evaluate structured LC-008 evidence without searching raw prose for secrets."""

    signal = candidate.signal
    common = {
        "technique_key": "LC-008",
        "passage_id": candidate.passage_id,
        "signal": signal,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not signal.common_in_relevant_horizon:
        trigger_failures.append(
            "The selected word is not established as common in the relevant horizon."
        )
    if not signal.commonness_evidence:
        trigger_failures.append(
            "No documentary evidence supports the word's ordinary or common status."
        )
    if not signal.sentence_low_prominence:
        trigger_failures.append(
            "The containing sentence is not established as low prominence."
        )
    if not signal.word_low_prominence:
        trigger_failures.append(
            "The word is not placed unobtrusively within the sentence."
        )
    if not signal.independent_trigger_documented:
        trigger_failures.append(
            "No independent documentary trigger justifies attention to the word."
        )
    if not signal.effect_documented:
        trigger_failures.append(
            "The word's semantic, propositional, structural, or doctrinal effect is undocumented."
        )
    if not signal.counterfactual_material_change:
        trigger_failures.append(
            "Removing or replacing the word produces no documented material change."
        )

    if trigger_failures:
        return LC008EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The sentence or passage boundary is not securely established.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, quotation, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.morphology_and_syntax_review_complete:
        missing_evidence.append("Morphology and syntax review is incomplete.")
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, punctuation, and textual-variant review is incomplete."
        )
    if not candidate.prominence_assessment_documented:
        missing_evidence.append(
            "The sentence and word prominence assessments are undocumented."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through prominence and effect analysis is incomplete."
        )

    if missing_evidence:
        return LC008EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the word, sentence, and witness.",
                "Complete source-language, morphology, syntax, translation, punctuation, and variant review.",
                "Document commonness, sentence prominence, word placement, and the independent trigger.",
                "Complete the counterfactual and proposition-level effect analysis.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC008EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_COMMON_WORD_SIGNAL,
            reasons=[
                "The bounded common-word structure is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved grammatical, stylistic, translational, editorial, and witness alternative.",
                "Preserve the word-level signal without inferring hidden meaning.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC008EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_COMMON_WORD_SIGNAL,
            reasons=[
                "No ordinary explanation of the word's apparent significance has yet been tested."
            ],
            authorized_next_actions=[
                "Test insignificance, grammar, idiom, style, translation, punctuation, quotation, formulaic use, anachronism, and witness variation.",
                "Do not infer a secret from commonness or placement.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC008EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_COMMON_WORD_SIGNAL,
            reasons=[
                "The word-level signal survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for stable recurrence, architectonic placement, source comparison, explicit commentary, and convergence with independently reconstructed devices.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC008EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_COMMON_WORD_SIGNAL,
        reasons=[
            "The word is common in the relevant linguistic horizon.",
            "It is placed unobtrusively within an unobtrusive sentence.",
            "An independent documentary trigger justified examining it.",
            "Its semantic, propositional, structural, or doctrinal effect is documented.",
            "A counterfactual rendering shows a material change when the word is removed or replaced.",
            "Source integrity, context, architecture, voice, source language, syntax, translation, variants, prominence, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the signal.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded word-level inquiry linked to the passage and trigger.",
            "Search the work for every occurrence and positional pattern of the word.",
            "Evaluate LC-006, LC-009, LC-002, and LC-020 separately when independently warranted.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer a secret, hidden meaning, authorial intention, audience, or doctrinal truth.",
        ],
    )
