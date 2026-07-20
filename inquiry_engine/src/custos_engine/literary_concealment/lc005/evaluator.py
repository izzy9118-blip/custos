from __future__ import annotations

from .models import (
    LC005EvaluationInput,
    LC005EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded three-stage sequence "
    "in which a final altered repetition of an intermediary assertion contradicts "
    "an earlier statement. It does not establish deliberate concealment, hidden "
    "teaching, authorial intention, or the truth of any statement."
)


def evaluate_lc005(candidate: LC005EvaluationInput) -> LC005EvaluationResult:
    """Evaluate structured LC-005 evidence without interpreting raw prose."""

    common = {
        "technique_key": "LC-005",
        "first_statement_id": candidate.first_statement_id,
        "intermediary_statement_id": candidate.intermediary_statement_id,
        "final_statement_id": candidate.final_statement_id,
        "recorded_differences": candidate.differences,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.same_work:
        trigger_failures.append("The three passages do not belong to the same work.")
    if not candidate.same_subject:
        trigger_failures.append("The three passages do not concern the same subject.")
    if not candidate.sequence_order_confirmed:
        trigger_failures.append("The first-intermediary-final order is not established.")
    if not candidate.intermediary_compatible_with_first:
        trigger_failures.append(
            "The intermediary assertion is not compatible with the first statement."
        )
    if not candidate.final_repeats_intermediary:
        trigger_failures.append(
            "The final statement does not present itself as a repetition or near-repetition of the intermediary."
        )
    if not candidate.differences:
        trigger_failures.append(
            "No addition or omission is recorded between intermediary and final statements."
        )
    elif not any(d.minute_relative_to_shared_text for d in candidate.differences):
        trigger_failures.append(
            "No recorded addition or omission is minute relative to the repeated text."
        )
    elif not any(
        d.minute_relative_to_shared_text and d.semantic_effect_documented
        for d in candidate.differences
    ):
        trigger_failures.append(
            "No minute difference has a documented semantic effect."
        )
    if not candidate.final_contradicts_first:
        trigger_failures.append(
            "The final proposition has not been shown to contradict the first proposition."
        )

    if trigger_failures:
        return LC005EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append(
            "The complete local contexts of the three passages are not reconstructed."
        )
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, cited voice, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.intermediary_final_alignment_complete:
        missing_evidence.append(
            "The intermediary and final passages have not been fully aligned."
        )
    if not candidate.proposition_normalization_documented:
        missing_evidence.append(
            "The propositions expressed by all three passages are not documented."
        )
    if not candidate.transition_sequence_reconstructed:
        missing_evidence.append(
            "The transition from first statement through intermediary to final statement is not reconstructed."
        )
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, and textual-variant effects have not been reviewed."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path preserving the complete three-stage sequence is incomplete."
        )

    undocumented = [
        d.expression
        for d in candidate.differences
        if d.minute_relative_to_shared_text and not d.semantic_effect_documented
    ]
    if undocumented:
        missing_evidence.append(
            "Semantic effects remain undocumented for minute differences: "
            + ", ".join(undocumented)
            + "."
        )

    if missing_evidence:
        return LC005EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Recover and verify all three passages in their witnesses.",
                "Reconstruct the local contexts, voices, and sequence order.",
                "Align intermediary and final passages word by word.",
                "Document the semantic effect of each addition or omission.",
                "Normalize all three propositions and complete the evidence path.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC005EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE,
            reasons=[
                "The three-stage structure is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved contextual, grammatical, textual, and compositional alternative.",
                "Preserve the sequence as a working hypothesis rather than a documented finding.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC005EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE,
            reasons=[
                "No ordinary explanation of the three-stage sequence has yet been tested."
            ],
            authorized_next_actions=[
                "Test development of thought, speaker change, scope shift, grammar, translation, witness variation, revision, and ordinary inconsistency.",
                "Do not infer concealment or doctrinal priority.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC005EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE,
            reasons=[
                "The sequence remains structurally intact after ordinary alternatives were tested, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for repeated three-stage patterns, stable technical wording, explicit differentiation, source confirmation, or an independently reconstructed literary device.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC005EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_CREEPING_CONTRADICTION_SEQUENCE,
        reasons=[
            "Three distinct passages occur in the same work and concern the same subject.",
            "Their first-intermediary-final order is documented.",
            "The intermediary proposition remains compatible with the first proposition.",
            "The final passage presents itself as a repetition of the intermediary.",
            "A complete alignment records a minute addition or omission with documented semantic effect.",
            "The final proposition contradicts the first proposition.",
            "Source integrity, contexts, voice, transition sequence, proposition normalization, translation review, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the sequence.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the three passages and their alignment record.",
            "Search the work for additional intermediary sequences and counterexamples.",
            "Evaluate LC-004 separately for the intermediary-final pair when warranted.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer concealment, intention, hidden teaching, or which statement is true.",
        ],
    )
