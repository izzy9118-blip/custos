from __future__ import annotations

from custos_engine.models.base import InquiryState
from custos_engine.models.inquiry import InquiryRun, StateResult


EXPECTED_STATE = InquiryState.HORIZON_AUDIT
NEXT_STATE = InquiryState.INDEPENDENT_RECONSTRUCTION


def execute(run: InquiryRun) -> StateResult:
    if run.current_state != EXPECTED_STATE:
        raise ValueError(
            f"Stage expects {EXPECTED_STATE}, received {run.current_state}"
        )
    return StateResult(
        completed=True,
        next_state=NEXT_STATE,
        notes={"stage_purpose": "Record the investigator's inherited assumptions and unavailable evidence."},
    )
