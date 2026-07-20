from __future__ import annotations

from .models import (
    LC012EvaluationInput,
    LC012EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded reader-address signal "
    "with a resolved addressee, placement, and communicative effect. The source "
    "names various kinds of apostrophe without reconstructing their subtypes. "
    "The evaluator does not establish concealment, intended readership, "
    "differentiated audiences, hidden instruction, or authorial intention."
)


def evaluate_lc012(candidate: LC012EvaluationInput) -> LC012EvaluationResult:
    """Evaluate structured LC-012 evidence without inventing an intended audience."""

    address = candidate.address
    common = {
        "technique_key": "LC-012",
        "address_id": candidate.address_id,
        "address": address,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not address.addressee_is_reader:
        trigger_failures.append(
            "The direct address is not established as addressed to the reader."
        )
    if not address.addressee_evidence:
        trigger_failures.append(
            "No documentary evidence identifies the addressee as the reader."
        )
    if not address.placement_documented:
        trigger_failures.append(
            "The address's placement within the exposition is undocumented."
        )
    if not address.communicative_effect_documented:
        trigger_failures.append(
            "No communicative effect is documented."
        )
    if not address.modifies_surrounding_exposition:
        trigger_failures.append(
            "The address does not documentably modify, frame, redirect, or qualify the surrounding exposition."
        )

    if trigger_failures:
        return LC012EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The address's textual boundary is not securely established.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, narrator, quotation, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The architectonic context is not reconstructed.")
    if not candidate.genre_convention_review_complete:
        missing_evidence.append(
            "Ordinary genre and pedagogical conventions have not been fully reviewed."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language grammatical review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, punctuation, edition, and textual-variant review is incomplete."
        )
    if not candidate.comparison_index_complete_for_claimed_scope:
        missing_evidence.append(
            "The comparison index of other reader addresses is incomplete for the claimed scope."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through addressee, placement, and function analysis is incomplete."
        )

    if missing_evidence:
        return LC012EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the address and its witness.",
                "Resolve addressee, speaker, quotation, and dramatic attribution.",
                "Complete local, architectonic, genre, source-language, translation, punctuation, and variant review.",
                "Complete the comparison index for the declared scope.",
                "Preserve the function label as local and noncanonical.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC012EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_READER_ADDRESS_SIGNAL,
            reasons=[
                "A reader-address structure is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved rhetorical, pedagogical, generic, dramatic, translational, and editorial alternative.",
                "Preserve the reader address without identifying an intended reader.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC012EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_READER_ADDRESS_SIGNAL,
            reasons=[
                "No ordinary explanation of the reader address has yet been tested."
            ],
            authorized_next_actions=[
                "Test generic rhetoric, pedagogy, preface convention, nonreader apostrophe, dramatic interlocution, quotation, translation, style, editorial intervention, and broad inclusive language.",
                "Do not infer differentiated audiences from the address alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC012EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_READER_ADDRESS_SIGNAL,
            reasons=[
                "The reader-address signal survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for repeated address patterns, explicit reader distinctions, restrictions, warnings, invitations, architectonic placement, and source alterations.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC012EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_READER_ADDRESS_SIGNAL,
        reasons=[
            "A bounded direct address is recoverable in a stable witness.",
            "The addressee is documentarily resolved as the reader.",
            "The address's placement is documented.",
            "Its communicative effect on the surrounding exposition is documented.",
            "Source integrity, boundary, attribution, context, architecture, genre, source language, translation, variants, comparison index, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the signal.",
            "At least one independent corroborating indicator is recorded.",
            "Intended readership and concealed instruction remain outside the adjudicated result.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the address, addressee, placement, and function records.",
            "Search the work for all other reader addresses and counterexamples.",
            "Evaluate adjacent techniques separately when independently triggered.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer concealment, intended reader, differentiated audience, hidden instruction, or a canonical subtype.",
        ],
    )
