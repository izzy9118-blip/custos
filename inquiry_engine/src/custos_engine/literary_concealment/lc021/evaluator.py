from __future__ import annotations

from .models import (
    LC021EvaluationInput,
    LC021EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a weak possible signal: a documentarily grounded "
    "expression mismatch that materially interrupts the surface reading and supports "
    "a bounded question. Strauss expressly permits the expression to be merely "
    "inappropriate. The evaluator does not infer hidden meaning, authorial intention, "
    "intended audience, concealment, or doctrinal truth."
)


def evaluate_lc021(candidate: LC021EvaluationInput) -> LC021EvaluationResult:
    """Evaluate LC-021 while preserving its weak and defeasible evidentiary force."""

    common = {
        "technique_key": "LC-021",
        "inquiry_id": candidate.inquiry_id,
        "baseline": candidate.baseline,
        "expression": candidate.expression,
        "question": candidate.question,
        "alternatives": candidate.alternatives,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.baseline.documentary_support:
        trigger_failures.append(
            "No independent documentary support establishes the fit baseline."
        )
    if not candidate.baseline.historically_appropriate:
        trigger_failures.append(
            "The fit baseline is not historically or linguistically appropriate."
        )
    if not candidate.baseline.scope_relevant:
        trigger_failures.append(
            "The fit baseline does not apply to the expression's context."
        )
    if not candidate.expression.mismatch_documented:
        trigger_failures.append(
            "No specific mismatch between expression and baseline is documented."
        )
    if not candidate.expression.materially_disrupts_surface_reading:
        trigger_failures.append(
            "The expression does not materially disrupt or complicate the surface reading."
        )
    if not candidate.expression.functions_as_stumbling_block:
        trigger_failures.append(
            "No documentary basis shows that the expression functions as a stumbling block."
        )
    if not candidate.expression.stumbling_block_support:
        trigger_failures.append(
            "No evidence supports the proposed stumbling-block function."
        )
    if not candidate.question.bounded_by_expression:
        trigger_failures.append(
            "The attention question is not bounded by the expression."
        )

    if trigger_failures:
        return LC021EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append(
            "The expression's textual boundary is not securely established."
        )
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, narrator, quotation, objection, hypothetical, or reported-opinion attribution is unresolved."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append(
            "Source-language grammar, semantic range, and morphology review is incomplete."
        )
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, punctuation, and textual-variant review is incomplete."
        )
    if not candidate.authorial_usage_review_complete:
        missing_evidence.append(
            "Comparable authorial usage and parallel passages have not been fully reviewed."
        )
    if not candidate.genre_and_technical_usage_review_complete:
        missing_evidence.append(
            "Genre, idiom, register, and technical-vocabulary review is incomplete."
        )
    if not candidate.adjacent_technique_review_complete:
        missing_evidence.append(
            "Adjacent literary techniques that may explain the feature have not been fully reviewed."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness through baseline and mismatch to question is incomplete."
        )

    untested = [
        item.alternative_id for item in candidate.alternatives if not item.tested
    ]
    if untested:
        missing_evidence.append(
            "Alternative explanations remain untested: " + ", ".join(untested) + "."
        )

    if missing_evidence:
        return LC021EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the expression, witness, boundary, speaker, and contexts.",
                "Complete source-language, translation, variant, authorial-usage, genre, and technical-vocabulary review.",
                "Test every ordinary repair and alternative explanation.",
                "Complete the evidence path while preserving only a bounded question.",
            ],
        )

    viable = [
        item.explanation for item in candidate.alternatives if item.remains_viable
    ]

    if viable:
        return LC021EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL,
            reasons=[
                "A documented expression mismatch functions as a possible stumbling block, but ordinary explanations remain viable."
            ],
            authorized_next_actions=[
                "Preserve the bounded question and test every remaining explanation.",
                "Retain explicitly the possibility that the expression is merely inappropriate.",
                "Do not escalate the signal to contradiction-level force.",
            ],
            unresolved_alternatives=viable,
        )

    if not candidate.alternatives:
        return LC021EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL,
            reasons=[
                "No ordinary repair or merely-inappropriate explanation has yet been tested."
            ],
            authorized_next_actions=[
                "Test idiom, archaic usage, technical vocabulary, translation, grammar, rhetoric, genre, speaker characterization, quoted source, textual variants, revision, mistaken baseline, and mere inappropriateness.",
                "Preserve the question without inferring an answer.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC021EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL,
            reasons=[
                "The mismatch survives ordinary explanations, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for comparable authorial usage, recurrence, parallel repair, contradiction or hint convergence, witness stability, source alteration, and architectonic placement.",
                "Maintain the result as a weak candidate signal.",
            ],
        )

    return LC021EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_INAPPROPRIATE_EXPRESSION_SIGNAL,
        reasons=[
            "An independent, historically appropriate, scope-relevant fit baseline is documented.",
            "The expression conflicts with that baseline in a specific and materially disruptive way.",
            "The expression has documentary support as a stumbling block.",
            "A bounded textual question is generated without asserting a hidden answer.",
            "Source integrity, boundary, contexts, voice, source language, translation, variants, authorial usage, genre, technical vocabulary, adjacent techniques, alternatives, and provenance are complete.",
            "Ordinary explanations were tested without dissolving the anomaly.",
            "At least one independent corroborating indicator is recorded.",
            "The signal remains weaker than a contradiction and the merely-inappropriate possibility is not excluded with certainty.",
        ],
        authorized_next_actions=[
            "Open a bounded attention review linked to the expression, fit baseline, mismatch, and question records.",
            "Search for confirming and disconfirming authorial usages and parallel passages.",
            "Evaluate adjacent techniques separately when independently triggered.",
            "Preserve all rival explanations and the merely-inappropriate possibility.",
            "Do not infer hidden meaning, intention, audience, concealment, or doctrinal truth.",
        ],
    )
