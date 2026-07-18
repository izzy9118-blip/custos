from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from custos_engine.models.base import InquiryState
from custos_engine.models.inquiry import InquiryRun, StateResult, StateTransition

from . import (
    adversarial_testing,
    architectural_mapping,
    authorial_authorization,
    horizon_audit,
    independent_reconstruction,
    intake,
    problem_formation,
    progressive_disclosure,
    purpose_audience_function,
    synthesis,
    termination,
)


Stage = Callable[[InquiryRun], StateResult]


STAGES: dict[InquiryState, Stage] = {
    InquiryState.DOCUMENTARY_INTAKE: intake.execute,
    InquiryState.HORIZON_AUDIT: horizon_audit.execute,
    InquiryState.INDEPENDENT_RECONSTRUCTION: independent_reconstruction.execute,
    InquiryState.AUTHORIAL_AUTHORIZATION: authorial_authorization.execute,
    InquiryState.PURPOSE_AUDIENCE_FUNCTION: purpose_audience_function.execute,
    InquiryState.ARCHITECTURAL_MAPPING: architectural_mapping.execute,
    InquiryState.PROBLEM_FORMATION: problem_formation.execute,
    InquiryState.ADVERSARIAL_TESTING: adversarial_testing.execute,
    InquiryState.PROGRESSIVE_DISCLOSURE: progressive_disclosure.execute,
    InquiryState.SYNTHESIS_LIMITATION: synthesis.execute,
    InquiryState.CERTIFICATION_PREPARATION: termination.execute,
}


class InquiryStateMachine:
    def step(self, run: InquiryRun) -> StateResult:
        if run.current_state == InquiryState.TERMINATED:
            raise ValueError("InquiryRun is already terminated")

        stage = STAGES[run.current_state]
        result = stage(run)

        if not result.completed or result.next_state is None:
            return result

        prior = run.current_state
        if result.next_state == InquiryState.TERMINATED:
            run.termination_reason = result.termination_reason
        run.current_state = result.next_state
        run.state_history.append(
            StateTransition(
                from_state=prior,
                to_state=result.next_state,
                reason=result.notes.get("stage_purpose", "Stage completed."),
            )
        )
        run.observation_ids.extend(result.observations_created)
        run.evidence_chain_ids.extend(result.evidence_added)
        run.hypothesis_ids.extend(result.hypotheses_created)
        run.unresolved_questions.extend(result.unresolved_questions)
        run.updated_at = datetime.now(timezone.utc)

        return result

    def run_to_termination(
        self,
        run: InquiryRun,
        maximum_steps: int = 32,
    ) -> InquiryRun:
        for _ in range(maximum_steps):
            if run.current_state == InquiryState.TERMINATED:
                return run
            self.step(run)
        raise RuntimeError(
            f"Inquiry did not terminate within {maximum_steps} deterministic steps"
        )
