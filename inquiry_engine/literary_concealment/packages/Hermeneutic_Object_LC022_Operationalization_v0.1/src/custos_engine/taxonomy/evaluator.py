from __future__ import annotations

from .models import (
    LC022EvaluationInput,
    LC022EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a weak possible signal: a documentarily grounded "
    "transition mismatch that materially interrupts expected continuity and supports "
    "a bounded question about relation or structural break. Strauss expressly permits "
    "the transition to be mere clumsiness. The evaluator does not infer a concealed "
    "relation, final structural break, authorial intention, intended audience, "
    "concealment, or doctrinal truth."
)


def evaluate_lc022(candidate: LC022EvaluationInput) -> LC022EvaluationResult:
    """Evaluate LC-022 while preserving its weak and defeasible force."""

    common = {
        "technique_key": "LC-022",
        "inquiry_id": candidate.inquiry_id,
        "before_unit": candidate.before_unit,
        "after_unit": candidate.after_unit,
        "baseline": candidate.baseline,
        "transition": candidate.transition,
        "question": candidate.question,
        "alternatives": candidate.alternatives,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.transition.adjacency_or_explicit_link_confirmed:
        trigger_failures.append(
            "The two textual units are not confirmed as adjacent or explicitly linked."
        )
    if not candidate.before_unit.reconstruction_support:
        trigger_failures.append(
            "The pre-transition subject or argumentative task lacks documentary support."
        )
    if not candidate.after_unit.reconstruction_support:
        trigger_failures.append(
            "The post-transition subject or argumentative task lacks documentary support."
        )
    if not candidate.baseline.documentary_support:
        trigger_failures.append(
            "No independent documentary support establishes the transition-coherence baseline."
        )
    if not candidate.baseline.historically_appropriate:
        trigger_failures.append(
            "The transition-coherence baseline is not historically or linguistically appropriate."
        )
    if not candidate.baseline.scope_relevant:
        trigger_failures.append(
            "The transition-coherence baseline does not apply to the units."
        )
    if not candidate.transition.mismatch_documented:
        trigger_failures.append(
            "No specific transition mismatch is documented."
        )
    if not candidate.transition.materially_interrupts_continuity:
        trigger_failures.append(
            "The transition does not materially interrupt expected continuity."
        )
    if not candidate.transition.structural_effect_documented:
        trigger_failures.append(
            "No material structural effect is documented."
        )
    if not candidate.transition.functions_as_attention_directing_anomaly:
        trigger_failures.append(
            "No documentary basis shows that the transition directs attention."
        )
    if not candidate.transition.attention_function_support:
        trigger_failures.append(
            "No evidence supports the attention-directing function."
        )
    if not candidate.question.bounded_by_transition:
        trigger_failures.append(
            "The structural question is not bounded by the transition."
        )

    if trigger_failures:
        return LC022EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.transition_boundary_confirmed:
        missing_evidence.append(
            "The transition boundary is not securely established."
        )
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.speaker_and_source_attribution_complete:
        missing_evidence.append(
            "Speaker, narrator, quotation, objection, hypothetical, or source attribution is incomplete."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append(
            "Source-language syntax, discourse markers, and semantic review is incomplete."
        )
    if not candidate.translation_paragraphing_and_variant_review_complete:
        missing_evidence.append(
            "Translation, punctuation, paragraphing, edition, and textual-variant review is incomplete."
        )
    if not candidate.authorial_transition_practice_review_complete:
        missing_evidence.append(
            "Comparable authorial transition practice and parallel passages have not been fully reviewed."
        )
    if not candidate.adjacent_technique_review_complete:
        missing_evidence.append(
            "Adjacent literary techniques that may explain the transition have not been fully reviewed."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from both units through baseline and mismatch to question is incomplete."
        )

    untested = [
        item.alternative_id for item in candidate.alternatives if not item.tested
    ]
    if untested:
        missing_evidence.append(
            "Alternative explanations remain untested: " + ", ".join(untested) + "."
        )

    if missing_evidence:
        return LC022EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify both units, the transition boundary, witnesses, speakers, and contexts.",
                "Complete source-language, discourse-marker, translation, paragraphing, and variant review.",
                "Compare authorial transition practice and parallel passages.",
                "Test every ordinary repair and alternative explanation.",
                "Complete the evidence path while preserving only a bounded structural question.",
            ],
        )

    viable = [
        item.explanation for item in candidate.alternatives if item.remains_viable
    ]

    if viable:
        return LC022EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CLUMSY_TRANSITION_SIGNAL,
            reasons=[
                "A documented transition mismatch directs attention to a possible relation or break, but ordinary explanations remain viable."
            ],
            authorized_next_actions=[
                "Preserve the bounded structural question and test every remaining explanation.",
                "Retain explicitly the possibility that the transition is mere clumsiness.",
                "Do not escalate the signal to contradiction-level force.",
            ],
            unresolved_alternatives=viable,
        )

    if not candidate.alternatives:
        return LC022EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CLUMSY_TRANSITION_SIGNAL,
            reasons=[
                "No ordinary continuity repair or mere-clumsiness explanation has yet been tested."
            ],
            authorized_next_actions=[
                "Test topic change, ellipsis, pedagogy, summary, genre, speaker shift, rhetorical acceleration, translation, editorial segmentation, textual damage, composite source, revision, mistaken baseline, and mistaken boundary.",
                "Preserve the question without inferring a concealed relation.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC022EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_CLUMSY_TRANSITION_SIGNAL,
            reasons=[
                "The transition mismatch survives ordinary explanations, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for later clarification, smoother parallels, corresponding juxtapositions, device convergence, witness stability, source alteration, and marked placement.",
                "Maintain the result as a weak candidate signal.",
            ],
        )

    return LC022EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_CLUMSY_TRANSITION_SIGNAL,
        reasons=[
            "The adjacent or explicitly linked textual units are securely bounded.",
            "The subject or argumentative task on each side is independently reconstructed.",
            "An independent, historically appropriate, scope-relevant transition-coherence baseline is documented.",
            "The actual movement conflicts with that baseline in a specific and materially disruptive way.",
            "The transition has a documented structural effect and attention-directing function.",
            "A bounded question is generated without asserting a concealed relation or final structural break.",
            "Source integrity, boundary, contexts, attribution, source language, translation, paragraphing, variants, authorial practice, adjacent techniques, alternatives, and provenance are complete.",
            "Ordinary explanations were tested without dissolving the anomaly.",
            "At least one independent corroborating indicator is recorded.",
            "The signal remains weaker than a contradiction and mere clumsiness is not excluded with certainty.",
        ],
        authorized_next_actions=[
            "Open a bounded structural review linked to both units, the baseline, mismatch, effect, and question records.",
            "Search for confirming and disconfirming transitions and parallel structures.",
            "Evaluate adjacent techniques separately when independently triggered.",
            "Preserve all rival explanations and the mere-clumsiness possibility.",
            "Do not infer a concealed relation, final structural break, intention, audience, concealment, or doctrinal truth.",
        ],
    )
