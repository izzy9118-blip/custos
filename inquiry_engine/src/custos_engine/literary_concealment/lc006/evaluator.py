from __future__ import annotations

from .models import (
    LC006EvaluationInput,
    LC006EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded lexical ambiguity in "
    "which multiple materially distinct senses remain viable in the same passage. "
    "It does not establish concealment, audience differentiation, secret terminology, "
    "authorial intention, or which sense is true."
)


def evaluate_lc006(candidate: LC006EvaluationInput) -> LC006EvaluationResult:
    """Evaluate structured LC-006 evidence without generating senses from raw prose."""

    viable = [
        sense
        for sense in candidate.senses
        if sense.documentary_attestation
        and sense.syntactically_viable
        and sense.locally_viable
        and (
            sense.source_language_supported
            or candidate.source_language_form is None
        )
    ]
    rejected = [sense for sense in candidate.senses if sense not in viable]

    common = {
        "technique_key": "LC-006",
        "passage_id": candidate.passage_id,
        "lexical_item": candidate.lexical_item,
        "viable_senses": viable,
        "rejected_senses": rejected,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if len(viable) < 2:
        trigger_failures.append(
            "Fewer than two documentarily attested, syntactically viable, and locally viable senses remain."
        )
    if not candidate.materially_distinct_propositions:
        trigger_failures.append(
            "The surviving senses do not yield materially distinct propositions."
        )

    if trigger_failures:
        return LC006EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The complete local context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, quotation, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.morphology_and_syntax_review_complete:
        missing_evidence.append("Morphology and syntax review is incomplete.")
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, and textual-variant effects are not fully reviewed."
        )
    if not candidate.contextual_disambiguation_tested:
        missing_evidence.append(
            "Ordinary contextual disambiguation has not been fully tested."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness text through sense analysis is incomplete."
        )

    if missing_evidence:
        return LC006EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the passage and lexical item in the witness.",
                "Complete source-language, morphology, syntax, translation, and variant review.",
                "Document each sense and its attestation.",
                "Render the passage under each sense and normalize the resulting propositions.",
                "Test whether local context decisively eliminates any sense.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC006EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_LEXICAL_AMBIGUITY,
            reasons=[
                "Multiple senses remain viable, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved lexical, grammatical, textual, and contextual alternative.",
                "Preserve all viable senses without selecting an interior meaning.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC006EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_LEXICAL_AMBIGUITY,
            reasons=[
                "No ordinary explanation of the apparent ambiguity has yet been tested."
            ],
            authorized_next_actions=[
                "Test dominant contextual meaning, translation artifact, metaphor, idiom, technical usage, vagueness, textual corruption, and ordinary imprecision.",
                "Do not privilege the rarer or more esoteric sense.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC006EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_LEXICAL_AMBIGUITY,
            reasons=[
                "Multiple senses survive ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search the work for repeated uses, explicit distinctions, parallel passages, source-language confirmation, and independently reconstructed literary signals.",
                "Maintain all surviving senses as bounded candidates.",
            ],
        )

    return LC006EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_LEXICAL_AMBIGUITY,
        reasons=[
            "At least two senses are documentarily attested.",
            "Each surviving sense fits the same local syntax.",
            "Each surviving sense remains viable in context.",
            "The senses yield materially distinct propositions.",
            "Source integrity, context, voice, morphology, syntax, source language, translation, variants, and provenance are complete.",
            "Ordinary alternatives were tested without eliminating the ambiguity.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded lexical inquiry linked to the passage and all viable sense records.",
            "Search the work for every occurrence of the lexical item and its variants.",
            "Evaluate LC-007, LC-008, and LC-009 separately when their conditions are independently present.",
            "Preserve rival readings and the complete evidence path.",
            "Do not infer concealment, intended audience, secret terminology, or which sense is true.",
        ],
    )
