from __future__ import annotations

from pydantic import Field

from custos_engine.models.base import InquiryState, StrictModel


CANONICAL_PROCEDURE_ID = "IAR-000000001"
CANONICAL_TAXONOMY_ID = "HOC-000000001"
LEGACY_MANIFEST_ID = "MAN-000000001"
ALWAYS_OPEN_MANIFEST_ID = "MAN-000000002"
LEGACY_AUTHORIZED_STATES = frozenset(
    {
        InquiryState.ADVERSARIAL_TESTING,
        InquiryState.PROGRESSIVE_DISCLOSURE,
        InquiryState.SYNTHESIS_LIMITATION,
        InquiryState.CERTIFICATION_PREPARATION,
    }
)


class HermeneuticGateContext(StrictModel):
    """Auditable binding for versioned Inner-Sanctum operation."""

    procedure_id: str = Field(pattern=r"^IAR-[0-9]{9}$")
    taxonomy_id: str = Field(pattern=r"^HOC-[0-9]{9}$")
    cognitive_memory_manifest_id: str = Field(pattern=r"^MAN-[0-9]{9}$")
    current_state: InquiryState = InquiryState.DOCUMENTARY_INTAKE
    completed_phase_numbers: list[int] = Field(default_factory=list)
    documentary_difficulty_identified: bool = False
    historical_admissibility_established: bool = False
    authorial_authorization_established: bool = False
    ordinary_explanations_considered: bool = False
    evidence_record_ids: list[str] = Field(default_factory=list)


class HermeneuticGateDecision(StrictModel):
    authorized: bool
    reasons: list[str] = Field(min_length=1)
    epistemic_limit: str = Field(min_length=1)


EPISTEMIC_LIMIT = (
    "The Inner Sanctum is a standing perceptual constitution of text analysis. "
    "Its availability does not establish that any literary mechanism is present "
    "and does not establish concealment, hidden teaching, authorial intention, "
    "intended audience, or doctrinal truth. A named Taxonomy component becomes "
    "operative only when its documentary trigger, corroboration, ordinary-"
    "alternative, and disqualifier rules are satisfied and preserved."
)

LEGACY_EPISTEMIC_LIMIT = (
    "Historical MAN-000000001 authorizes only a bounded investigation of a named "
    "literary mechanism after its phase gate. It does not establish concealment, "
    "hidden teaching, authorial intention, intended audience, or doctrinal truth."
)


def _canonical_binding_failures(context: HermeneuticGateContext) -> list[str]:
    failures: list[str] = []
    if context.procedure_id != CANONICAL_PROCEDURE_ID:
        failures.append(
            f"The canonical inquiry procedure {CANONICAL_PROCEDURE_ID} is not selected."
        )
    if context.taxonomy_id != CANONICAL_TAXONOMY_ID:
        failures.append(
            f"The canonical Inner Sanctum {CANONICAL_TAXONOMY_ID} is not selected."
        )
    return failures


def _evaluate_legacy_gate(
    context: HermeneuticGateContext,
) -> HermeneuticGateDecision:
    failures = _canonical_binding_failures(context)
    if context.current_state not in LEGACY_AUTHORIZED_STATES:
        failures.append(
            "The historical inquiry has not reached a phase eligible for "
            "Inner-Sanctum invocation."
        )
    if not set(range(1, 8)).issubset(context.completed_phase_numbers):
        failures.append("Historical Outer-Process phases 1 through 7 are not complete.")
    if not context.documentary_difficulty_identified:
        failures.append("No genuine documentary difficulty has been identified.")
    if not context.historical_admissibility_established:
        failures.append("Historical admissibility has not been established.")
    if not context.authorial_authorization_established:
        failures.append("Authorial authorization has not been established.")
    if not context.ordinary_explanations_considered:
        failures.append("Ordinary explanations have not been considered.")
    if not context.evidence_record_ids:
        failures.append("No auditable evidence record supports the historical gate request.")

    if failures:
        return HermeneuticGateDecision(
            authorized=False,
            reasons=failures,
            epistemic_limit=LEGACY_EPISTEMIC_LIMIT,
        )
    return HermeneuticGateDecision(
        authorized=True,
        reasons=[
            "Historical MAN-000000001 reached adversarial testing or later.",
            "The predecessor gate evidence is complete and auditable.",
        ],
        epistemic_limit=LEGACY_EPISTEMIC_LIMIT,
    )


def evaluate_inner_sanctum_gate(
    context: HermeneuticGateContext,
) -> HermeneuticGateDecision:
    """Evaluate the manifest-pinned constitution without rewriting history.

    MAN-000000001 remains reproducibly gated. MAN-000000002 and its successors
    establish the always-open Inner Sanctum as the active text-analysis design.
    """

    if context.cognitive_memory_manifest_id == LEGACY_MANIFEST_ID:
        return _evaluate_legacy_gate(context)

    failures = _canonical_binding_failures(context)
    if context.cognitive_memory_manifest_id != ALWAYS_OPEN_MANIFEST_ID:
        failures.append(
            "The always-open Cognitive Memory Manifest MAN-000000002 is not selected."
        )
    if failures:
        return HermeneuticGateDecision(
            authorized=False,
            reasons=failures,
            epistemic_limit=EPISTEMIC_LIMIT,
        )

    return HermeneuticGateDecision(
        authorized=True,
        reasons=[
            "The canonical inquiry procedure, Taxonomy, and always-open Manifest are selected.",
            "The Inner Sanctum is constitutionally open from documentary intake "
            "through synthesis and limitation.",
            "Individual Taxonomy components remain evidence-governed and may return "
            "not triggered, disqualified, or underdetermined.",
        ],
        epistemic_limit=EPISTEMIC_LIMIT,
    )


def require_inner_sanctum_access(context: HermeneuticGateContext) -> None:
    decision = evaluate_inner_sanctum_gate(context)
    if not decision.authorized:
        raise PermissionError(
            "Inner Sanctum initialization or historical gate failed: "
            + " ".join(decision.reasons)
        )
