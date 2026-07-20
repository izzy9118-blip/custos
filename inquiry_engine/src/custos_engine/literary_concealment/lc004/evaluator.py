from __future__ import annotations

from .models import (
    LC004EvaluationInput,
    LC004EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded apparent repetition "
    "in which a minute addition or omission has a documented propositional "
    "effect. It does not establish deliberate concealment, hidden teaching, "
    "authorial intention, the truth of either statement, or the significance "
    "of wording difference without semantic and contextual evidence."
)


def evaluate_lc004(candidate: LC004EvaluationInput) -> LC004EvaluationResult:
    """Evaluate structured LC-004 evidence without interpreting raw prose.

    The evaluator does not discover parallelism, textual differences, semantic
    effect, contradiction, or intention. Those judgments must arrive as
    explicit, auditable inputs.
    """

    common = {
        "technique_key": "LC-004",
        "earlier_statement_id": candidate.earlier_statement_id,
        "later_statement_id": candidate.later_statement_id,
        "recorded_differences": candidate.differences,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.same_work:
        trigger_failures.append("The selected passages do not belong to the same work.")
    if not candidate.same_subject:
        trigger_failures.append("The selected passages do not concern the same subject.")
    if not candidate.parallel_relation_documented:
        trigger_failures.append(
            "No documentary basis establishes the passages as genuine parallels."
        )
    if not candidate.later_presents_as_repetition:
        trigger_failures.append(
            "The later passage does not present itself as a repetition or near-repetition."
        )
    if not candidate.differences:
        trigger_failures.append(
            "No addition or omission is recorded between the aligned passages."
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
            "No minute addition or omission has a documented semantic effect."
        )
    if not candidate.substantive_contradiction_established:
        trigger_failures.append(
            "The altered formulations have not been shown to express incompatible propositions."
        )

    if trigger_failures:
        return LC004EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append(
            "The complete local contexts of both passages are not reconstructed."
        )
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, cited voice, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.word_alignment_complete:
        missing_evidence.append(
            "The passages have not been aligned word by word or phrase by phrase."
        )
    if not candidate.proposition_normalization_documented:
        missing_evidence.append(
            "The propositions expressed by the two formulations are not documented."
        )
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, and textual-variant effects have not been reviewed."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through alignment and semantic analysis is incomplete."
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
        return LC004EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Recover and verify both passages in their witnesses.",
                "Reconstruct local context, voice, and argumentative function.",
                "Complete a word-by-word alignment and preserve each addition and omission separately.",
                "Document the semantic effect of each relevant minute expression.",
                "Normalize both propositions and complete the evidence path before further evaluation.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC004EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_MINUTE_VARIATION_CONTRADICTION,
            reasons=[
                "The altered-repetition structure is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test each unresolved alternative against the aligned passages and contexts.",
                "Preserve the result as a working hypothesis rather than a documented finding.",
                "Search for witness, translation, scope, voice, grammatical, and compositional explanations.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC004EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_MINUTE_VARIATION_CONTRADICTION,
            reasons=[
                "No ordinary explanation of the minute addition or omission has yet been tested."
            ],
            authorized_next_actions=[
                "Test stylistic variation, grammar, abbreviation, voice, scope, translation, witness variation, revision, and ordinary imprecision.",
                "Do not infer concealment or doctrinal priority from the textual difference.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC004EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_MINUTE_VARIATION_CONTRADICTION,
            reasons=[
                "The minute variation remains propositionally significant after ordinary alternatives were tested, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for stable technical use of the expression, repeated parallel patterns, explicit differentiation, source confirmation, or another independently reconstructed device.",
                "Maintain the result as a bounded candidate altered-repetition contradiction.",
            ],
        )

    return LC004EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_MINUTE_VARIATION_CONTRADICTION,
        reasons=[
            "The passages occur in the same work and concern the same subject.",
            "Their parallel relation and apparent repetition are documentarily established.",
            "A complete alignment records at least one minute addition or omission.",
            "The relevant expression has a documented semantic effect.",
            "The normalized formulations are substantively incompatible.",
            "Source integrity, contexts, voice, alignment, proposition normalization, translation review, and evidence provenance are complete.",
            "Ordinary alternatives were tested without dissolving the contradiction.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to both passages and the alignment record.",
            "Search the work for further parallel formulations, counterexamples, and stable uses of the minute expression.",
            "Evaluate LC-001, LC-002, LC-003, or LC-005 separately when their conditions are independently present.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer concealment, intention, hidden teaching, or which statement is true.",
        ],
    )
