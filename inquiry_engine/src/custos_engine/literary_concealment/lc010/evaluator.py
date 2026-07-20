from __future__ import annotations

from .models import (
    LC010EvaluationInput,
    LC010EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded sophistic argument "
    "structure. The current source names intentional sophisms but does not classify "
    "their subtypes, and this v0.1 evaluator does not establish intention, concealment, "
    "hidden teaching, or the author's true position."
)


def evaluate_lc010(candidate: LC010EvaluationInput) -> LC010EvaluationResult:
    """Evaluate a reconstructed argument without inferring intentional deception."""

    common = {
        "technique_key": "LC-010",
        "argument_id": candidate.argument_id,
        "defect": candidate.defect,
        "preserved_intentionality_evidence": candidate.direct_intentionality_evidence,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.bounded_argument_reconstructed:
        trigger_failures.append("No bounded argument has been reconstructed.")
    if not candidate.premises:
        trigger_failures.append("No premise records are present.")
    if not candidate.inference_steps:
        trigger_failures.append("No ordered inference steps are present.")
    if not candidate.defect.defect_documented:
        trigger_failures.append(
            "No specific argumentative defect is documented under an explicit standard."
        )
    if not candidate.defect.materially_affects_support:
        trigger_failures.append(
            "The alleged defect does not materially affect support for the conclusion."
        )
    if not candidate.defect.correction_changes_support:
        trigger_failures.append(
            "Correcting the alleged defect does not change the argument's support."
        )

    if trigger_failures:
        return LC010EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The argument's textual boundary is not securely established.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, quotation, objection, hypothetical, or reported-opinion attribution is unresolved."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, punctuation, and textual-variant review is incomplete."
        )
    if not candidate.counterfactual_analysis_complete:
        missing_evidence.append(
            "The corrected counterfactual argument has not been fully analyzed."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through argument reconstruction is incomplete."
        )

    reconstructed_without_basis = [
        premise.premise_id
        for premise in candidate.premises
        if premise.status == "RECONSTRUCTED" and not premise.reconstruction_basis
    ]
    if reconstructed_without_basis:
        missing_evidence.append(
            "Reconstruction bases are absent for premises: "
            + ", ".join(reconstructed_without_basis)
            + "."
        )

    if missing_evidence:
        return LC010EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the argument and its witness.",
                "Complete premise, inference-step, and conclusion reconstruction.",
                "Resolve voice, quotation, objection, hypothetical, and source attribution.",
                "Complete source-language, translation, punctuation, variant, and counterfactual review.",
                "Preserve explicit and reconstructed premises separately.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC010EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SOPHISTIC_STRUCTURE,
            reasons=[
                "A material argumentative defect is documented, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved error, compression, pedagogy, rhetoric, textual, attribution, and reconstruction alternative.",
                "Preserve intentionality evidence without adjudicating it.",
                "Do not classify a canonical subtype.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC010EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SOPHISTIC_STRUCTURE,
            reasons=[
                "No ordinary explanation of the defective argument has yet been tested."
            ],
            authorized_next_actions=[
                "Test unintentional error, unstated premise, pedagogical simplification, rhetorical abbreviation, translation, corruption, speaker change, scope change, revision, and investigator misreconstruction.",
                "Do not infer intention from the defect.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC010EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_SOPHISTIC_STRUCTURE,
            reasons=[
                "The defect survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for repeated defect patterns, explicit corrections, source alterations, authorial competence, and convergence with independently reconstructed devices.",
                "Maintain the result as a bounded candidate sophistic structure.",
            ],
        )

    return LC010EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_SOPHISTIC_STRUCTURE,
        reasons=[
            "A bounded argument with premises, inference steps, and conclusion is reconstructed.",
            "A specific defect is documented under an explicit standard.",
            "The defect materially affects support for the conclusion.",
            "A corrected counterfactual changes the argument's support.",
            "Source integrity, boundary, context, architecture, voice, source language, translation, variants, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the defect.",
            "At least one independent corroborating indicator is recorded.",
            "Intentionality remains outside the adjudicated result.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the argument reconstruction and defect record.",
            "Search the work for corrections, repetitions, parallel arguments, and counterexamples.",
            "Evaluate adjacent literary techniques separately when independently triggered.",
            "Preserve all direct intentionality evidence for later documentary review.",
            "Do not infer intention, concealment, hidden teaching, authorial position, or a canonical subtype.",
        ],
    )
