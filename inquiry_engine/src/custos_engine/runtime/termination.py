from __future__ import annotations

from custos_engine.models.base import InquiryState, TerminationReason
from custos_engine.models.inquiry import InquiryRun, StateResult


EXPECTED_STATE = InquiryState.CERTIFICATION_PREPARATION


def execute(run: InquiryRun) -> StateResult:
    if run.current_state != EXPECTED_STATE:
        raise ValueError(
            f"Termination stage expects {EXPECTED_STATE}, received {run.current_state}"
        )
    return StateResult(
        completed=True,
        next_state=InquiryState.TERMINATED,
        termination_reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
        notes={
            "stage_purpose": (
                "Close the authorized candidate package without conferring "
                "certification or Repository admission."
            )
        },
    )
