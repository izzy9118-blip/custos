from __future__ import annotations

from .models import (
    LC015EvaluationInput,
    LC015EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded quotation omission "
    "whose material effect survives source-version and ordinary-alternative review. "
    "The technique name preserves Strauss's reconstruction, but this evaluator does "
    "not establish deliberate misquotation, concealment, authorial intention, hidden "
    "teaching, intended readership, or doctrinal truth."
)


def evaluate_lc015(candidate: LC015EvaluationInput) -> LC015EvaluationResult:
    """Evaluate source-to-quotation omission without inferring deliberateness."""

    common = {
        "technique_key": "LC-015",
        "case_id": candidate.case_id,
        "source": candidate.source,
        "quotation": candidate.quotation,
        "omissions": candidate.omissions,
        "full_source_record": candidate.full_source_record,
        "shortened_quotation_record": candidate.shortened_quotation_record,
        "preserved_intentionality_evidence": candidate.direct_intentionality_evidence,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.quotation.quotation_status_documented:
        trigger_failures.append(
            "The passage is not documentarily established as quotation or citation."
        )
    if not candidate.source_relation_confirmed:
        trigger_failures.append(
            "The relation between quotation and proposed source is not confirmed."
        )
    if not candidate.omissions:
        trigger_failures.append(
            "No source expression is recorded as omitted from the quotation."
        )
    elif not any(item.material_effect_documented for item in candidate.omissions):
        trigger_failures.append(
            "No omitted expression has a documented material effect."
        )
    if not candidate.material_difference_established:
        trigger_failures.append(
            "The full source and shortened quotation are not shown to differ materially."
        )

    if trigger_failures:
        return LC015EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.collation_complete:
        missing_evidence.append(
            "Source and quotation collation is incomplete."
        )
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source witness integrity is unresolved.")
    if not candidate.quotation_witness_integrity_confirmed:
        missing_evidence.append("Quotation witness integrity is unresolved.")
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The quotation's local context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append("The quotation's architectonic context is not reconstructed.")
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, narrator, objection, hypothetical, or reported-opinion attribution is unresolved."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.alternate_source_versions_review_complete:
        missing_evidence.append(
            "Alternate source editions, recensions, and intermediary versions are not fully reviewed."
        )
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, punctuation, edition, and textual-variant review is incomplete."
        )
    if not candidate.quotation_boundary_confirmed:
        missing_evidence.append("The quotation boundary is not securely established.")
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from source witness through collation and semantic effect is incomplete."
        )

    undocumented = [
        item.omission_id
        for item in candidate.omissions
        if not item.material_effect_documented
    ]
    if undocumented:
        missing_evidence.append(
            "Material effects remain undocumented for omissions: "
            + ", ".join(undocumented)
            + "."
        )

    if missing_evidence:
        return LC015EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify both source and quotation witnesses.",
                "Confirm quotation status, boundary, source identity, and source-version family.",
                "Complete word- or phrase-level collation.",
                "Document the effect of every omitted expression.",
                "Complete source-language, translation, variant, context, and attribution review.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC015EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_QUOTATION_OMISSION,
            reasons=[
                "A materially altered quotation by omission is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved abbreviation, paraphrase, memory, source-version, intermediary-source, translation, grammar, editorial, and witness alternative.",
                "Preserve direct intentionality evidence without adjudicating it.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC015EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_QUOTATION_OMISSION,
            reasons=[
                "No ordinary explanation of the shortened quotation has yet been tested."
            ],
            authorized_next_actions=[
                "Test abbreviation, memory quotation, paraphrase, alternate source version, intermediary citation, grammar, ellipsis convention, translator or editor omission, corruption, redundancy, mistaken source, and mistaken boundary.",
                "Do not infer deliberateness from omission alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC015EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_QUOTATION_OMISSION,
            reasons=[
                "The material quotation alteration survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for fuller quotations, repeated omissions, evidence of source knowledge, status changes, source alterations, and convergence with independently reconstructed devices.",
                "Maintain the result as a bounded candidate quotation omission.",
            ],
        )

    return LC015EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_QUOTATION_OMISSION,
        reasons=[
            "The passage is documentarily established as quotation or citation.",
            "The source relation and relevant source-version family are confirmed.",
            "Complete collation records at least one omitted source expression.",
            "The omission materially changes proposition, scope, qualification, attribution, status, or doctrinal force.",
            "Full-source and shortened-quotation proposition-status records remain separate.",
            "Source integrity, quotation integrity, boundaries, contexts, voice, source language, alternate versions, translation, variants, and provenance are complete.",
            "Ordinary alternatives were tested without dissolving the alteration.",
            "At least one independent corroborating indicator is recorded.",
            "Deliberateness remains outside the adjudicated result.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to source, quotation, collation, omission, and proposition-status records.",
            "Search the work for other quotations of the same source and counterexamples.",
            "Evaluate LC-014 and LC-004 separately when independently warranted.",
            "Preserve intentionality evidence and rival explanations.",
            "Do not infer deliberate misquotation, concealment, hidden teaching, intended readership, or doctrinal truth.",
        ],
    )
