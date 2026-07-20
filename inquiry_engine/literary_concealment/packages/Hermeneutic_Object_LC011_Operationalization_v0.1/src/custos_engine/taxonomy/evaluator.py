from __future__ import annotations

from .models import (
    LC011EvaluationInput,
    LC011EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded divergence between a "
    "surface proposition and a candidate nonliteral proposition. The current "
    "source names ironical remarks but does not classify their varieties, and "
    "this evaluator does not establish intended irony, hidden teaching, authorial "
    "intention, intended meaning, or doctrinal truth."
)


def evaluate_lc011(candidate: LC011EvaluationInput) -> LC011EvaluationResult:
    """Evaluate structured LC-011 evidence without generating irony from tone."""

    supporting_markers = [
        marker for marker in candidate.markers if marker.supports_divergence
    ]
    countermarkers = [
        marker for marker in candidate.markers if not marker.supports_divergence
    ]

    common = {
        "technique_key": "LC-011",
        "remark_id": candidate.remark_id,
        "surface": candidate.surface,
        "candidate_nonliteral": candidate.candidate_nonliteral,
        "supporting_markers": supporting_markers,
        "countermarkers": countermarkers,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.materially_distinct_propositions:
        trigger_failures.append(
            "The surface and candidate nonliteral propositions are not materially distinct."
        )
    if not supporting_markers:
        trigger_failures.append(
            "No documentary marker supports divergence from the surface proposition."
        )
    if not candidate.divergence_relation.strip():
        trigger_failures.append(
            "The relation between surface and candidate nonliteral propositions is not documented."
        )

    if trigger_failures:
        return LC011EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The remark's textual boundary is not securely established.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, narrator, quotation, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.target_or_object_review_complete:
        missing_evidence.append(
            "The possible target or object of the remark has not been reviewed."
        )
    if not candidate.literal_coherence_tested:
        missing_evidence.append(
            "The literal surface reading has not been tested for contextual coherence."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, punctuation, edition, and textual-variant review is incomplete."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through both proposition records is incomplete."
        )

    if missing_evidence:
        return LC011EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the remark, textual boundary, and witness.",
                "Complete local, architectonic, speaker, target, source-language, translation, punctuation, and variant review.",
                "Test literal coherence before advancing the nonliteral proposition.",
                "Complete the proposition and marker evidence path.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC011EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_IRONIC_DIVERGENCE,
            reasons=[
                "A surface/nonliteral divergence is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved literal, humorous, sarcastic, dramatic, lexical, textual, and compositional alternative.",
                "Preserve surface and nonliteral propositions without selecting intended meaning.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC011EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_IRONIC_DIVERGENCE,
            reasons=[
                "No ordinary explanation of the apparent nonliteral divergence has yet been tested."
            ],
            authorized_next_actions=[
                "Test literal statement, sarcasm, humor, parody, hyperbole, understatement, metaphor, ambiguity, quotation, dramatic characterization, scope change, translation, and ordinary inconsistency.",
                "Do not infer intended irony from contextual tension.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC011EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_IRONIC_DIVERGENCE,
            reasons=[
                "The divergence survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for explicit rejection, repeated ironic patterns, target reactions, architectonic convergence, source comparison, and independently reconstructed devices.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC011EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_IRONIC_DIVERGENCE,
        reasons=[
            "A bounded remark and literal surface proposition are documented.",
            "A materially distinct candidate nonliteral proposition is reconstructed without altering the wording.",
            "At least one documentary marker supports the divergence.",
            "Source integrity, boundary, context, architecture, voice, target review, literal-coherence testing, source language, translation, variants, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the divergence.",
            "At least one independent corroborating indicator is recorded.",
            "Intended meaning and authorial intention remain outside the adjudicated result.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to both proposition records and all markers.",
            "Search the work for parallel remarks, explicit corrections, reactions, and counterexamples.",
            "Evaluate adjacent literary techniques separately when independently triggered.",
            "Preserve countermarkers and rival explanations.",
            "Do not infer intended irony, hidden teaching, authorial position, or a canonical subtype.",
        ],
    )
