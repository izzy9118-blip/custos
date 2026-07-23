from __future__ import annotations

from pydantic import Field

from custos_engine.models.base import InquiryState, StrictModel


CANONICAL_PROCEDURE_ID = "IAR-000000001"
CANONICAL_TAXONOMY_ID = "HOC-000000001"
CANONICAL_MANIFEST_IDS = frozenset({"MAN-000000001", "MAN-000000002"})


class HermeneuticGateContext(StrictModel):
    """Auditable binding for the always-open Inner Sanctum.

    The procedural evidence fields are retained for backward-compatible inquiry
    records. They govern whether a named Taxonomy component is evidentially
    triggered; they no longer govern whether the Taxonomy is available to text
    analysis.
    """

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


def evaluate_inner_sanctum_gate(
    context: HermeneuticGateContext,
) -> HermeneuticGateDecision:
    """Confirm the canonical binding through which the always-open Sanctum runs.

    This function retains the historical ``gate`` API so existing inquiry records
    remain readable. Under the corrected constitution, phase completion and the
    presence of a prior documentary difficulty never close the Inner Sanctum.
    """

    failures: list[str] = []

    if context.procedure_id != CANONICAL_PROCEDURE_ID:
        failures.append(
            f"The canonical inquiry procedure {CANONICAL_PROCEDURE_ID} is not selected."
        )
    if context.taxonomy_id != CANONICAL_TAXONOMY_ID:
        failures.append(
            f"The canonical Inner Sanctum {CANONICAL_TAXONOMY_ID} is not selected."
        )
    if context.cognitive_memory_manifest_id not in CANONICAL_MANIFEST_IDS:
        failures.append(
            "A released Cognitive Memory Manifest authorizing the canonical pair "
            "is not selected."
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
            "The canonical inquiry procedure, Taxonomy, and released Manifest are selected.",
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
            "Inner Sanctum initialization failed: " + " ".join(decision.reasons)
        )
