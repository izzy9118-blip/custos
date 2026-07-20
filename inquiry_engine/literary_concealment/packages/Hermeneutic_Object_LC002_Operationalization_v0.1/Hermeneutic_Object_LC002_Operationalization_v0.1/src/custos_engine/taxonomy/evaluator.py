from __future__ import annotations

from .models import (
    LC002EvaluationInput,
    LC002EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded contradiction pair with "
    "recorded unequal prominence. It does not establish deliberate concealment, "
    "hidden teaching, authorial intention, the truth of either statement, or the "
    "superiority of the incidental statement."
)


def evaluate_lc002(candidate: LC002EvaluationInput) -> LC002EvaluationResult:
    """Evaluate structured LC-002 evidence without interpreting raw prose.

    The evaluator does not discover contradiction, incidentality, prominence, or
    proposition identity. Those judgments must arrive as explicit, auditable inputs.
    """

    common = {
        "technique_key": "LC-002",
        "incidental_statement_id": candidate.incidental_statement_id,
        "prominent_statement_id": candidate.prominent_statement_id,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.same_work:
        trigger_failures.append("The statements do not belong to the same work.")
    if not candidate.same_subject:
        trigger_failures.append("Identity of subject has not been established.")
    if not candidate.mutually_incompatible:
        trigger_failures.append("Mutual incompatibility has not been established.")
    if not candidate.incidental_placement_observed:
        trigger_failures.append("No statement has been shown to occur incidentally or in passing.")
    if not candidate.other_statement_prominent:
        trigger_failures.append("The comparison statement has not been shown to receive greater prominence.")

    if trigger_failures:
        return LC002EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append("The complete local contexts of both statements are not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append("Speaker, cited voice, objection, or dramatic attribution is unresolved.")
    if not candidate.prominence_basis_documented:
        missing_evidence.append(
            "The basis for classifying one statement as incidental and the other as prominent is not documented."
        )

    if missing_evidence:
        return LC002EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Recover and verify both passages in their witnesses.",
                "Reconstruct the complete local rhetorical and syntactic context of each statement.",
                "Document the features establishing incidental and prominent placement.",
                "Resolve speaker, quotation, objection, and attribution before comparison.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC002EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_UNEQUAL_PROMINENCE_PAIR,
            reasons=[
                "The pair satisfies the documentary trigger, but ordinary explanations of the prominence asymmetry remain unresolved."
            ],
            authorized_next_actions=[
                "Test each remaining alternative against both passages and their rhetorical settings.",
                "Preserve the pair as a working hypothesis, not a documented finding.",
                "Search the work for recurrence of either proposition in comparable placements.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC002EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_UNEQUAL_PROMINENCE_PAIR,
            reasons=["No ordinary explanation of unequal prominence has yet been tested."],
            authorized_next_actions=[
                "Test qualification, exception, genre, quotation, objection, speaker difference, textual corruption, translation variation, and ordinary error.",
                "Do not infer concealment or doctrinal preference from incidentality alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC002EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_UNEQUAL_PROMINENCE_PAIR,
            reasons=[
                "The contradiction and unequal prominence remain after ordinary alternatives were tested, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for repeated low-prominence formulations, lexical recurrence, audience differentiation, structural placement, or another independently reconstructed device.",
                "Maintain the result as a bounded candidate pair.",
            ],
        )

    return LC002EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_UNEQUAL_PROMINENCE_CONTRADICTION,
        reasons=[
            "The statements concern the same subject within the same work.",
            "Their mutual incompatibility is documented.",
            "One statement is documentarily established as incidental and the other as more prominent.",
            "Source integrity, contexts, voice attribution, and prominence basis are resolved.",
            "Ordinary alternatives were tested without dissolving the contradiction or asymmetry.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to both passage records and the prominence evidence.",
            "Compare every occurrence of both propositions across the work.",
            "Test whether LC-001, LC-018, LC-019, or another technique also applies, but record each separately.",
            "Preserve rival explanations and the complete evidence path.",
            "Do not prefer the incidental statement without a separate source-governed rule and inquiry.",
        ],
    )
