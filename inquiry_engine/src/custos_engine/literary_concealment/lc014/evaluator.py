from __future__ import annotations

from .models import (
    LC014EvaluationInput,
    LC014EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded significant omission: "
    "an item independently expected within a confirmed scope, absent from the "
    "relevant witness, and materially consequential. It does not establish "
    "deliberate silence, authorial intention, intended readership, exoteric status, "
    "a missing teaching, or doctrinal truth."
)


def evaluate_lc014(candidate: LC014EvaluationInput) -> LC014EvaluationResult:
    """Evaluate structured LC-014 evidence without turning absence into proof."""

    baseline = candidate.baseline
    omission = candidate.omission
    common = {
        "technique_key": "LC-014",
        "omission_id": candidate.omission_id,
        "baseline": baseline,
        "omission": omission,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not baseline.historically_appropriate:
        trigger_failures.append(
            "The expectation baseline is not historically appropriate."
        )
    if not baseline.scope_relevant:
        trigger_failures.append(
            "The expectation baseline does not apply to the declared textual or doctrinal scope."
        )
    if not baseline.documentary_support:
        trigger_failures.append(
            "No independent documentary support establishes the expectation."
        )
    if not omission.item_absent_in_relevant_witness:
        trigger_failures.append(
            "The expected item is not absent from the relevant witness."
        )
    if not omission.absence_verification:
        trigger_failures.append(
            "The claimed absence has not been documentarily verified."
        )
    if not omission.material_effect_documented:
        trigger_failures.append(
            "No material effect of the omission is documented."
        )
    if not omission.counterfactual_changes_passage:
        trigger_failures.append(
            "Counterfactual inclusion does not materially alter the passage."
        )

    if trigger_failures:
        return LC014EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The bounded unit's textual boundary is not securely established.")
    if not candidate.doctrinal_scope_confirmed:
        missing_evidence.append("The relevant doctrinal or enumerative scope is not securely established.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, quotation, objection, hypothetical, or reported-opinion attribution is unresolved."
        )
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, punctuation, edition, witness, and textual-variant review is incomplete."
        )
    if not candidate.negative_search_complete_within_scope:
        missing_evidence.append(
            "The search for the expected item elsewhere within the declared scope is incomplete."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from expectation baseline through absence verification and material effect is incomplete."
        )

    if missing_evidence:
        return LC014EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the bounded unit, witness, and scope.",
                "Complete the expectation-baseline record before evaluating the absence.",
                "Resolve voice, source language, translation, variants, and textual damage.",
                "Search the declared scope for the allegedly missing item.",
                "Complete the counterfactual and documentary evidence path.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC014EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SIGNIFICANT_OMISSION,
            reasons=[
                "A documentarily expected and materially significant absence is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved scope, abbreviation, genre, pedagogy, translation, damage, source-version, attribution, revision, and boundary alternative.",
                "Preserve the omission without inferring deliberate silence.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC014EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SIGNIFICANT_OMISSION,
            reasons=[
                "No ordinary explanation of the absence has yet been tested."
            ],
            authorized_next_actions=[
                "Test scope, summary, genre, pedagogy, supply elsewhere, translation, textual loss, source version, speaker change, revision, mistaken baseline, and mistaken boundary.",
                "Do not infer intention or exotericism from absence alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC014EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SIGNIFICANT_OMISSION,
            reasons=[
                "The significant absence survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for recovered sources, parallel passages, explicit enumerations, repeated omissions, indirect supply, status changes, authorial knowledge, and witness comparison.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC014EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_SIGNIFICANT_OMISSION,
        reasons=[
            "A specific expected item is defined.",
            "An independent, historically appropriate, scope-relevant documentary baseline supports the expectation.",
            "The item is verified as absent from the relevant witness and bounded unit.",
            "The omission has a documented material effect on completeness, status, scope, attribution, or doctrinal force.",
            "Counterfactual inclusion materially changes the passage.",
            "Source integrity, boundaries, scope, voice, contexts, source language, translation, variants, negative search, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the omission.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded omission inquiry linked to the baseline, bounded unit, and counterfactual record.",
            "Search the work for the missing item, parallel treatments, and counterexamples.",
            "Evaluate LC-015 separately when a quotation is altered by omission.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer deliberate silence, intention, intended readership, exoteric status, missing teaching, or doctrinal truth.",
        ],
    )
