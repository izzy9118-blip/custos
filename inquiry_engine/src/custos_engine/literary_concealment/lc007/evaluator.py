from __future__ import annotations

from .models import (
    LC007EvaluationInput,
    LC007EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded dual-reading structure "
    "with distinct communicative functions and audience horizons. It does not "
    "establish deliberate concealment, persecution, actual audience reception, "
    "or that the interior reading is true."
)


def evaluate_lc007(candidate: LC007EvaluationInput) -> LC007EvaluationResult:
    """Evaluate structured LC-007 evidence without inventing readings or audiences."""

    common = {
        "technique_key": "LC-007",
        "passage_id": candidate.passage_id,
        "exterior_reading": candidate.exterior_reading,
        "interior_reading": candidate.interior_reading,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.materially_distinct_readings:
        trigger_failures.append(
            "The exterior and interior records do not yield materially distinct readings."
        )
    if not candidate.distinct_functions:
        trigger_failures.append(
            "The proposed readings do not have distinct communicative functions."
        )
    if not candidate.distinct_audience_horizons:
        trigger_failures.append(
            "The proposed readings do not have distinct audience horizons."
        )
    if not candidate.exterior_reading.same_verbal_surface_preserved:
        trigger_failures.append(
            "The exterior reading does not preserve the same verbal surface."
        )
    if not candidate.interior_reading.same_verbal_surface_preserved:
        trigger_failures.append(
            "The interior reading does not preserve the same verbal surface."
        )
    if not candidate.exterior_reading.textual_support:
        trigger_failures.append("The exterior reading lacks textual support.")
    if not candidate.interior_reading.textual_support:
        trigger_failures.append("The interior reading lacks textual support.")

    if trigger_failures:
        return LC007EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The bounded textual unit is not securely established.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, narrator, quotation, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.genre_and_pedagogy_review_complete:
        missing_evidence.append("Genre and pedagogical alternatives are not fully reviewed.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, and textual-variant effects are not fully reviewed."
        )
    if not candidate.audience_evidence_review_complete:
        missing_evidence.append("Audience-horizon evidence is incomplete.")
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through both reading reconstructions is incomplete."
        )
    if not candidate.exterior_reading.function_documented:
        missing_evidence.append("The exterior reading's communicative function is undocumented.")
    if not candidate.interior_reading.function_documented:
        missing_evidence.append("The interior reading's communicative function is undocumented.")
    if not candidate.exterior_reading.audience_horizon_documented:
        missing_evidence.append("The exterior audience horizon is undocumented.")
    if not candidate.interior_reading.audience_horizon_documented:
        missing_evidence.append("The interior audience horizon is undocumented.")

    if missing_evidence:
        return LC007EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the textual unit and its witness.",
                "Complete local, architectonic, speaker, genre, pedagogical, translation, and variant review.",
                "Document the textual support, proposition, function, and audience horizon of each reading.",
                "Complete the evidence path without selecting a true reading.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC007EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_TWO_FACED_SPEECH,
            reasons=[
                "Two readings, functions, and audience horizons are present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved pedagogical, generic, rhetorical, lexical, dramatic, and textual alternative.",
                "Preserve both readings and all rival explanations.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC007EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_TWO_FACED_SPEECH,
            reasons=[
                "No ordinary explanation of the dual-reading structure has yet been tested."
            ],
            authorized_next_actions=[
                "Test pedagogy, expertise differences, genre, rhetoric, ambiguity, irony, speaker change, composition history, translation, and ordinary inconsistency.",
                "Do not infer concealment or audience intention.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC007EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_TWO_FACED_SPEECH,
            reasons=[
                "The dual-reading structure survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for explicit reader distinctions, prefaces, addresses, parallel structures, reception evidence, and independently reconstructed literary devices.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC007EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_TWO_FACED_SPEECH,
        reasons=[
            "The same bounded verbal surface supports two materially distinct readings.",
            "Each reading has independent textual support.",
            "The readings have distinct documented communicative functions.",
            "The readings have distinct documented audience horizons.",
            "Source integrity, boundary, context, architecture, voice, genre, pedagogy, translation, variants, and provenance are complete.",
            "Ordinary alternatives were tested without collapsing the readings into one.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the textual unit and both reading records.",
            "Search the work for explicit audience distinctions, parallel dual-reading structures, and counterexamples.",
            "Evaluate LC-006, LC-008, LC-009, LC-011, and LC-012 separately when warranted.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer concealment, persecution, actual reception, or that the interior reading is true.",
        ],
    )
