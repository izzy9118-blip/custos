from __future__ import annotations

from .models import (
    LC003EvaluationInput,
    LC003EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded implication-mediated "
    "contradiction. The derived implication is an analytical reconstruction, not "
    "a quotation. The result does not establish deliberate concealment, hidden "
    "teaching, authorial intention, the truth of any statement, or the rejection "
    "of the anchor statement."
)


def evaluate_lc003(candidate: LC003EvaluationInput) -> LC003EvaluationResult:
    """Evaluate structured LC-003 evidence without interpreting raw prose.

    The evaluator does not discover propositions, term identity, implication,
    contradiction, or authorial intention. Those judgments must arrive as
    explicit, auditable inputs.
    """

    common = {
        "technique_key": "LC-003",
        "anchor_statement_id": candidate.anchor_statement_id,
        "bridge_statement_ids": candidate.bridge_statement_ids,
        "contrary_statement_id": candidate.contrary_statement_id,
        "derived_implication": candidate.derived_implication,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not candidate.same_work:
        trigger_failures.append("The selected statements do not belong to the same work.")
    if not candidate.bridge_chain_present:
        trigger_failures.append("No bridge chain connects the anchor to a derived implication.")
    if not candidate.derived_implication_unpronounced:
        trigger_failures.append(
            "The alleged implication is pronounced directly in the selected path rather than reconstructed."
        )
    if candidate.selected_contrary_directly_denies_anchor:
        trigger_failures.append(
            "The selected contrary statement directly denies the anchor, so the relation is not LC-003."
        )
    if not candidate.contrary_denies_derived_implication:
        trigger_failures.append(
            "The contrary statement has not been shown to deny the derived implication."
        )

    if trigger_failures:
        return LC003EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.local_contexts_reconstructed:
        missing_evidence.append(
            "The complete local contexts of the anchor, bridge, and contrary statements are not reconstructed."
        )
    if not candidate.speaker_or_voice_resolved:
        missing_evidence.append(
            "Speaker, cited voice, objection, hypothetical, or dramatic attribution is unresolved."
        )
    if not candidate.proposition_normalization_documented:
        missing_evidence.append("Proposition normalization is not documented.")
    if not candidate.term_identity_or_equivalence_documented:
        missing_evidence.append(
            "Identity or controlled equivalence of terms carried through the chain is not documented."
        )
    if not candidate.implication_rule_validated:
        missing_evidence.append("The declared implication rule has not been validated.")
    if not candidate.derivation_provenance_complete:
        missing_evidence.append(
            "The derivation record does not preserve complete passage-to-proposition-to-implication provenance."
        )

    if missing_evidence:
        return LC003EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Recover and verify every pronounced passage in its witness.",
                "Reconstruct local context, voice, and proposition identity for every statement.",
                "Document term continuity and validate each inference step.",
                "Preserve the derived implication as an analytical reconstruction rather than a quotation.",
                "Complete the derivation evidence path before further evaluation.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC003EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_IMPLICATION_CONTRADICTION,
            reasons=[
                "The implication-mediated contradiction is structurally present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test each remaining alternative against every premise and inference step.",
                "Preserve the chain as a working hypothesis, not a documented finding.",
                "Search for term shifts, scope differences, missing conditions, and contrary evidence across the work.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC003EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_IMPLICATION_CONTRADICTION,
            reasons=["No ordinary explanation of the implication chain has yet been tested."],
            authorized_next_actions=[
                "Test equivocation, scope, condition, modality, speaker difference, invalid transitivity, translation variation, missing premises, and ordinary error.",
                "Do not infer concealment or truth from logical form alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC003EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_IMPLICATION_CONTRADICTION,
            reasons=[
                "The chain remains valid after ordinary alternatives were tested, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for explicit term definitions, repeated chains, direct parallel contradictions, source confirmation, or another separately reconstructed device.",
                "Maintain the result as a bounded candidate implication contradiction.",
            ],
        )

    return LC003EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_IMPLICATION_CONTRADICTION,
        reasons=[
            "The anchor, bridge, and contrary statements occur in the same work.",
            "The selected contradiction is indirect rather than a direct denial of the anchor.",
            "The unpronounced implication is explicitly reconstructed from documented bridge statements.",
            "The contrary statement denies the derived implication.",
            "Source integrity, contexts, voice, proposition normalization, term continuity, inference validity, and derivation provenance are resolved.",
            "Ordinary alternatives were tested without dissolving the chain.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to every passage and derivation record.",
            "Search the work for direct formulations, repeated implication chains, and counterexamples.",
            "Test whether LC-001, LC-002, or another technique also applies, but record each separately.",
            "Preserve rival explanations and the complete evidence path.",
            "Do not attribute the derived implication to the author as a quotation or select the true statement without separate evidence and authority.",
        ],
    )
