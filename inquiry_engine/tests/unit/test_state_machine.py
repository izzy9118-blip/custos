from custos_engine.models.base import EngineMode, InquiryState
from custos_engine.models.inquiry import InquiryRun
from custos_engine.runtime.state_machine import InquiryStateMachine


def test_state_machine_terminates_deterministically():
    run = InquiryRun(
        run_id="RUN-1",
        mode=EngineMode.DEVELOPMENT,
        initiating_question="Question",
        documentary_boundary="Boundary",
        repository_full_name="izzy9118-blip/custos",
        git_commit="1234567",
        cognitive_memory_manifest_id="MAN-1",
        governing_specification_ids=["SPEC-1"],
    )
    InquiryStateMachine().run_to_termination(run)
    assert run.current_state == InquiryState.TERMINATED
    assert len(run.state_history) == 11


def test_production_state_machine_accepts_absent_optional_projection():
    run = InquiryRun(
        run_id="RUN-PRODUCTION-NO-PROJECTION",
        mode=EngineMode.PRODUCTION,
        initiating_question="Question",
        documentary_boundary="Boundary",
        repository_full_name="izzy9118-blip/custos",
        git_commit="1234567",
        cognitive_memory_manifest_id="MAN-000000001",
        governing_specification_ids=["SPEC-000000002", "SPEC-000000003"],
    )

    InquiryStateMachine().run_to_termination(run)

    assert run.current_state == InquiryState.TERMINATED
    assert run.projection_manifest_id is None
