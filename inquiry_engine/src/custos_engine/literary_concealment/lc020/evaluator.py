from __future__ import annotations

from .models import (
    LC020EvaluationInput,
    LC020EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a finite, documentarily supported path by which "
    "a small textual cue materially directs inquiry toward an independently "
    "documented contradiction or contradictory-statement discernment problem. "
    "It does not establish hidden teaching, doctrinal truth, authorial intention, "
    "intended audience, or concealment."
)


def evaluate_lc020(candidate: LC020EvaluationInput) -> LC020EvaluationResult:
    """Evaluate a bounded cue-to-target discovery path without free association."""

    unsupported_steps = [
        step.step_id for step in candidate.discovery_steps if not step.supported
    ]

    common = {
        "technique_key": "LC-020",
        "inquiry_id": candidate.inquiry_id,
        "cue": candidate.cue,
        "target": candidate.target,
        "discovery_steps": candidate.discovery_steps,
        "alternative_paths": candidate.alternative_paths,
        "unsupported_step_ids": unsupported_steps,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if candidate.cue.directly_states_result:
        trigger_failures.append(
            "The cue states the proposed result directly rather than hinting."
        )
    if not candidate.cue.materially_guides_inquiry:
        trigger_failures.append(
            "The cue does not materially narrow, redirect, or structure inquiry."
        )
    if not candidate.target.independently_documented:
        trigger_failures.append(
            "The contradiction or discernment target is not independently documented."
        )
    if not candidate.target.independent_evidence:
        trigger_failures.append(
            "No independent evidence supports the target problem."
        )
    if not candidate.discovery_steps:
        trigger_failures.append(
            "No finite discovery path connects cue and target."
        )
    if unsupported_steps:
        trigger_failures.append(
            "One or more discovery steps lack documentary support."
        )

    if trigger_failures:
        return LC020EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The cue's textual boundary is not securely established.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The cue's local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The cue's architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, narrator, quotation, objection, hypothetical, or reported-opinion attribution is unresolved."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, punctuation, and textual-variant review is incomplete."
        )
    if not candidate.adjacent_technique_review_complete:
        missing_evidence.append(
            "Adjacent literary techniques that may explain the cue have not been fully reviewed."
        )
    if not candidate.alternative_target_testing_complete:
        missing_evidence.append(
            "Alternative targets and cue-to-target paths have not been fully tested."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from cue through discovery steps to target is incomplete."
        )

    step_support_missing = [
        step.step_id
        for step in candidate.discovery_steps
        if not step.documentary_support
    ]
    if step_support_missing:
        missing_evidence.append(
            "Documentary support is not recorded for discovery steps: "
            + ", ".join(step_support_missing)
            + "."
        )

    untested_alternatives = [
        item.alternative_id
        for item in candidate.alternative_paths
        if not item.tested
    ]
    if untested_alternatives:
        missing_evidence.append(
            "Alternative paths remain untested: "
            + ", ".join(untested_alternatives)
            + "."
        )

    if missing_evidence:
        return LC020EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the cue, witness, boundary, voice, and contexts.",
                "Document every discovery step and its evidence.",
                "Complete source-language, translation, and variant review.",
                "Test alternative targets and adjacent literary techniques.",
                "Complete the finite evidence path without adding associative steps.",
            ],
        )

    viable_alternative_paths = [
        item.alternative_target_or_explanation
        for item in candidate.alternative_paths
        if item.remains_viable
    ]
    unresolved = list(dict.fromkeys(
        candidate.unresolved_ordinary_alternatives + viable_alternative_paths
    ))

    if unresolved:
        return LC020EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_HINT_PATH,
            reasons=[
                "A bounded cue-to-target discovery path is present, but rival explanations or targets remain viable."
            ],
            authorized_next_actions=[
                "Test every remaining syntactic, referential, topical, rhetorical, pedagogical, translational, textual, and alternative-target explanation.",
                "Preserve every supported path step and do not select truth.",
            ],
            unresolved_alternatives=unresolved,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC020EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_HINT_PATH,
            reasons=[
                "No ordinary explanation of the cue-to-target relation has yet been tested."
            ],
            authorized_next_actions=[
                "Test ordinary syntax, cross-reference, transition, emphasis, pedagogy, ambiguity, common-word usage, editorial intervention, translation, corruption, coincidence, explicit statement, hindsight, and unbounded association.",
                "Do not infer a hint from suggestiveness alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC020EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_HINT_PATH,
            reasons=[
                "The discovery path survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for independently established contradictions, LC-018 or LC-019 convergence, parallel cues, later confirmation, architectonic placement, source alteration, and device convergence.",
                "Maintain the result as a bounded candidate hint path.",
            ],
        )

    return LC020EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_HINT_PATH,
        reasons=[
            "A small bounded textual cue is recoverable in a stable witness.",
            "The contradiction or discernment problem is independently documented.",
            "A finite consecutive discovery path connects cue and target.",
            "Every discovery step has documentary support.",
            "The cue materially narrows, redirects, or structures inquiry without stating the result directly.",
            "Source integrity, boundary, contexts, voice, source language, translation, variants, adjacent-technique review, alternative-target testing, and provenance are complete.",
            "Ordinary explanations and rival paths were tested without dissolving the cue-to-target relation.",
            "At least one independent corroborating indicator is recorded.",
            "No hidden teaching or truth judgment is made.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the cue, target, and complete discovery-path record.",
            "Preserve all alternative paths and counterevidence.",
            "Evaluate adjacent techniques separately when independently triggered.",
            "Use the hint only to direct further documentary inquiry.",
            "Do not infer hidden teaching, doctrinal truth, authorial intention, intended audience, or concealment.",
        ],
    )
