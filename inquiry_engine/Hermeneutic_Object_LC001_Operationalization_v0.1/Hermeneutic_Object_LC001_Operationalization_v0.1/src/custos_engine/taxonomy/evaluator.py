from __future__ import annotations

from .models import (
    LC001EvaluationInput,
    LC001EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded contradiction pair. "
    "It does not establish deliberate concealment, hidden teaching, authorial intention, "
    "or which statement the author regarded as true."
)


def evaluate_lc001(candidate: LC001EvaluationInput) -> LC001EvaluationResult:
    """Evaluate a structured passage pair under LC-001 without interpreting the text.

    The evaluator does not discover propositions or infer contradiction from raw prose.
    Those judgments must enter as explicit, auditable inputs with their evidence paths.
    """

    trigger_failures: list[str] = []
    if not candidate.same_work:
        trigger_failures.append("The statements do not belong to the same work.")
    if not candidate.same_subject:
        trigger_failures.append("Identity of subject has not been established.")
    if not candidate.mutually_incompatible:
        trigger_failures.append("Mutual incompatibility has not been established.")
    if not candidate.positionally_separated:
        trigger_failures.append("No positive positional separation has been recorded.")

    if trigger_failures:
        return LC001EvaluationResult(
            technique_key="LC-001",
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
            epistemic_limit=EPISTEMIC_LIMIT,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append("The local contexts of both statements are not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append("Speaker, cited voice, or dramatic attribution is unresolved.")

    if missing_evidence:
        return LC001EvaluationResult(
            technique_key="LC-001",
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Recover and verify both passages in their witnesses.",
                "Reconstruct the complete local context of each statement.",
                "Resolve speaker, quotation, and attribution before interpretation.",
            ],
            epistemic_limit=EPISTEMIC_LIMIT,
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC001EvaluationResult(
            technique_key="LC-001",
            outcome=LocalEvaluationOutcome.CANDIDATE_PAIR,
            reasons=[
                "The pair satisfies the documentary trigger, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test each remaining ordinary alternative against both passages.",
                "Preserve the pair as a working hypothesis, not a documented finding.",
                "Search the whole work for additional statements on the same subject.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
            epistemic_limit=EPISTEMIC_LIMIT,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC001EvaluationResult(
            technique_key="LC-001",
            outcome=LocalEvaluationOutcome.CANDIDATE_PAIR,
            reasons=["No ordinary alternative explanation has yet been tested."],
            authorized_next_actions=[
                "Test contextual qualification, change over time, multiple voices, textual corruption, translation variation, and ordinary error.",
                "Do not infer concealment from contradiction and distance alone.",
            ],
            epistemic_limit=EPISTEMIC_LIMIT,
        )

    if not candidate.corroborating_indicators:
        return LC001EvaluationResult(
            technique_key="LC-001",
            outcome=LocalEvaluationOutcome.CANDIDATE_PAIR,
            reasons=[
                "The contradiction remains after ordinary alternatives were tested, but no independent corroborating indicator has been recorded."
            ],
            authorized_next_actions=[
                "Search for recurrence, exact lexical correspondence, explicit authorial care, structural placement, or related literary devices.",
                "Maintain the result as a bounded candidate contradiction pair.",
            ],
            epistemic_limit=EPISTEMIC_LIMIT,
        )

    return LC001EvaluationResult(
        technique_key="LC-001",
        outcome=LocalEvaluationOutcome.CORROBORATED_CONTRADICTION,
        reasons=[
            "The statements concern the same subject within the same work.",
            "Their mutual incompatibility and positional separation are documented.",
            "Source integrity, local contexts, and voice attribution are resolved.",
            "Ordinary alternatives were tested without resolving the contradiction.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded interpretive inquiry linked to both passage records and the corroborating evidence.",
            "Compare the pair with other statements on the same subject across the whole work.",
            "Preserve rival explanations and the complete evidence path.",
            "Do not select a true statement until a separate, source-governed inquiry warrants that judgment.",
        ],
        epistemic_limit=EPISTEMIC_LIMIT,
    )
