from __future__ import annotations

from .models import (
    LC013EvaluationInput,
    LC013EvaluationResult,
    LocalEvaluationOutcome,
)


EPISTEMIC_LIMIT = (
    "This result identifies only a documentarily bounded relation between an "
    "authentic prefixed motto and the work or part it governs. It does not "
    "establish concealment, a hidden interpretive key, intended meaning, "
    "intended audience, authorial intention, or doctrinal truth."
)


def evaluate_lc013(candidate: LC013EvaluationInput) -> LC013EvaluationResult:
    """Evaluate structured LC-013 evidence without inventing an interpretive key."""

    motto = candidate.motto
    relation = candidate.relation
    common = {
        "technique_key": "LC-013",
        "motto_id": candidate.motto_id,
        "motto": motto,
        "relation": relation,
        "epistemic_limit": EPISTEMIC_LIMIT,
    }

    trigger_failures: list[str] = []
    if not motto.present_in_authorially_relevant_witness:
        trigger_failures.append(
            "The prefixed text is not present in an authorially relevant witness."
        )
    if motto.provenance_status in {
        "EDITORIAL",
        "PUBLISHER_SUPPLIED",
        "TRANSLATOR_SUPPLIED",
        "LATER_HAND",
    }:
        trigger_failures.append(
            "The prefixed text is not authorial or authorially adopted."
        )
    if not motto.governed_scope_documented:
        trigger_failures.append("The governed scope is not documented.")
    if not motto.surface_function_documented:
        trigger_failures.append("The motto's ordinary surface function is undocumented.")
    if not relation.relation_documented:
        trigger_failures.append(
            "No specific relation between the motto and governed unit is documented."
        )
    if not relation.materially_specific_beyond_theme:
        trigger_failures.append(
            "The proposed relation does not exceed broad thematic resemblance."
        )

    if trigger_failures:
        return LC013EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.NOT_TRIGGERED,
            reasons=trigger_failures,
        )

    missing_evidence: list[str] = []
    if not candidate.source_integrity_confirmed:
        missing_evidence.append("Source or witness integrity is unresolved.")
    if not candidate.textual_boundary_confirmed:
        missing_evidence.append("The motto's textual boundary is not securely established.")
    if not candidate.governed_scope_boundary_confirmed:
        missing_evidence.append(
            "The boundary of the governed work or part is not securely established."
        )
    if not candidate.local_context_reconstructed:
        missing_evidence.append("The local prefatory context is not reconstructed.")
    if not candidate.architectonic_context_reconstructed:
        missing_evidence.append(
            "The motto's architectonic relation to the governed unit is not reconstructed."
        )
    if not candidate.source_language_review_complete:
        missing_evidence.append("Source-language review is incomplete.")
    if not candidate.translation_and_variant_review_complete:
        missing_evidence.append(
            "Translation, edition, punctuation, and textual-variant review is incomplete."
        )
    if not candidate.editorial_provenance_review_complete:
        missing_evidence.append(
            "Editorial, publisher, translator, and later-hand provenance review is incomplete."
        )
    if not candidate.comparison_index_complete_for_claimed_scope:
        missing_evidence.append(
            "The comparison index of other mottoes is incomplete for the claimed scope."
        )
    if not candidate.evidence_path_complete:
        missing_evidence.append(
            "The evidence path from witness placement and source recovery to the allusive relation is incomplete."
        )
    if not motto.provenance_evidence:
        missing_evidence.append("No evidence supports the motto's provenance status.")
    if motto.source.source_recovered and not motto.source.source_location:
        missing_evidence.append(
            "The recovered motto source lacks a source location."
        )
    if motto.source.source_context_recovered and not motto.source.source_context:
        missing_evidence.append(
            "The recovered source context is not recorded."
        )

    if missing_evidence:
        return LC013EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.BLOCKED_MISSING_EVIDENCE,
            reasons=missing_evidence,
            authorized_next_actions=[
                "Verify the motto, witness, provenance, placement, and governed scope.",
                "Recover and preserve the source text and original context where possible.",
                "Complete local, architectonic, source-language, translation, variant, and editorial review.",
                "Complete the comparison index and documentary evidence path.",
                "Preserve the surface function separately from the candidate allusive relation.",
            ],
        )

    if candidate.unresolved_ordinary_alternatives:
        return LC013EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_MOTTO_ALLUSION,
            reasons=[
                "A specific motto-to-scope relation is present, but ordinary alternatives remain unresolved."
            ],
            authorized_next_actions=[
                "Test every unresolved decorative, thematic, devotional, generic, editorial, translational, and attribution alternative.",
                "Preserve the relation as a working hypothesis rather than a hidden key.",
            ],
            unresolved_alternatives=candidate.unresolved_ordinary_alternatives,
        )

    if not candidate.ordinary_alternatives_tested:
        return LC013EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_MOTTO_ALLUSION,
            reasons=[
                "No ordinary explanation of the motto's placement and relation has yet been tested."
            ],
            authorized_next_actions=[
                "Test decoration, thematic summary, invocation, dedication, genre convention, editorial addition, source acknowledgment, style, common vocabulary, and scope overextension.",
                "Do not infer an interpretive key from prefatory placement alone.",
            ],
        )

    if not candidate.corroborating_indicators:
        return LC013EvaluationResult(
            **common,
            outcome=LocalEvaluationOutcome.CANDIDATE_MOTTO_ALLUSION,
            reasons=[
                "The motto-to-scope relation survives ordinary alternatives, but no independent corroborating indicator is recorded."
            ],
            authorized_next_actions=[
                "Search for distinctive repetitions, structural sequence, source-context clarification, systematic motto patterns, architectonic placement, source alteration, and convergence with other devices.",
                "Maintain the result as a bounded candidate.",
            ],
        )

    return LC013EvaluationResult(
        **common,
        outcome=LocalEvaluationOutcome.CORROBORATED_MOTTO_ALLUSION,
        reasons=[
            "An authentic or authorially adopted prefixed text is documented.",
            "Its governed work or part is securely bounded.",
            "The motto's source and original context are preserved to the extent recoverable.",
            "Its ordinary surface function is documented.",
            "A specific relation beyond broad thematic resemblance links it to the governed unit.",
            "Source integrity, boundaries, context, architecture, language, translation, variants, provenance, comparison, and evidence path are complete.",
            "Ordinary alternatives were tested without dissolving the relation.",
            "At least one independent corroborating indicator is recorded.",
        ],
        authorized_next_actions=[
            "Open a bounded inquiry linked to the motto, source, governed scope, and allusive-relation records.",
            "Search the governed unit and other mottoes for confirming and disconfirming patterns.",
            "Evaluate adjacent techniques separately when independently triggered.",
            "Preserve rival explanations and the complete documentary path.",
            "Do not infer a hidden key, intended meaning, audience, intention, or doctrinal truth.",
        ],
    )
