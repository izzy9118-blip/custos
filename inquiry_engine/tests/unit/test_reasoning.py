import json
import sys

import pytest
from pydantic import ValidationError

from custos_engine.models.base import EngineMode, EpistemicClassification, InquiryState, TerminationReason
from custos_engine.models.inquiry import InquiryRun
from custos_engine.models.reasoning import CandidateStatement, DocumentaryInput, PhaseInstruction, PhaseReasoningRequest, PhaseReasoningResponse
from custos_engine.models.taxonomy import TaxonomyComponent
from custos_engine.runtime.reasoning import InquiryReasoningExecutor, SubprocessPhaseReasoner
from custos_engine.cli import build_parser, reasoning_schema_command

PHASE_STATES = [InquiryState.DOCUMENTARY_INTAKE, InquiryState.HORIZON_AUDIT, InquiryState.INDEPENDENT_RECONSTRUCTION, InquiryState.AUTHORIAL_AUTHORIZATION, InquiryState.PURPOSE_AUDIENCE_FUNCTION, InquiryState.ARCHITECTURAL_MAPPING, InquiryState.PROBLEM_FORMATION, InquiryState.ADVERSARIAL_TESTING, InquiryState.PROGRESSIVE_DISCLOSURE, InquiryState.SYNTHESIS_LIMITATION]


def _procedure():
    return {"ordered_stages": [{"phase": n, "state": state.value, "name": f"Phase {n}", "steps": [{"sequence": n, "instruction": f"Execute bounded phase {n}."}]} for n, state in enumerate(PHASE_STATES, 1)]}


def _run():
    return InquiryRun(run_id="RUN-FIELD-1", mode=EngineMode.PRODUCTION, initiating_question="What does the fixed evidence support?", documentary_boundary="One declared source excerpt.", repository_full_name="izzy9118-blip/custos", git_commit="1234567", cognitive_memory_manifest_id="MAN-000000002", governing_specification_ids=["SPEC-000000002"])


def _documentary_input():
    return DocumentaryInput(evidence_id="EVR-FIELD-1", source_role="PRIMARY", citation="Declared witness, bounded passage", text="Fixed documentary text.", source_fixity_sha256="a" * 64)


def _taxonomy_component():
    return TaxonomyComponent(component_id="LC-001", name="Bounded Test Technique", source={"canonical_id": "HOC-000000001", "canonical_class": "Hermeneutic Object C", "github_path": "inquiry_engine/cognitive_memory/HOC-000000001.taxonomy.json", "git_commit": "1234567", "version": "1.2"}, strauss_formulation="A bounded documentary formulation.", mechanism="A bounded mechanism.", documentary_function="Direct attention to a named documentary relation.", investigative_requirement="Test the relation against the fixed evidence.", reconstruction_status="TECHNICALLY_CERTIFIED", minimum_trigger_features=["A named documentary feature."], ordinary_alternatives=["An ordinary textual explanation."], authorized_engine_action="Investigate the named mechanism only.", prohibited_inferences=["No concealment conclusion."], uncertainty_note="The result remains a candidate interpretation.")


class StubReasoner:
    adapter_id = "STUB_REASONER_V1"
    def __init__(self, stop_phase=None):
        self.stop_phase = stop_phase
        self.requests = []
    def reason(self, request):
        self.requests.append(request)
        if request.phase_number == self.stop_phase:
            return PhaseReasoningResponse(run_id=request.run_id, state=request.state, completed=False, summary="A required source is unavailable.", termination_reason=TerminationReason.MISSING_SOURCE_BLOCK)
        return PhaseReasoningResponse(run_id=request.run_id, state=request.state, completed=True, summary=f"Completed bounded phase {request.phase_number}.", candidate_statements=[CandidateStatement(candidate_id=f"CAND-{request.phase_number:02d}", text="A source-bounded candidate statement.", epistemic_classification=EpistemicClassification.SUPPORTED_INFERENCE, evidence_record_ids=["EVR-FIELD-1"])])


def _execute(reasoner, run=None):
    return InquiryReasoningExecutor(reasoner).run_to_termination(run or _run(), _procedure(), [_documentary_input()], permitted_taxonomy_techniques=[_taxonomy_component()])


def test_reasoning_executor_records_all_ten_phases_and_terminates():
    reasoner = StubReasoner(); run = _run(); records = _execute(reasoner, run)
    assert run.current_state == InquiryState.TERMINATED
    assert run.termination_reason == TerminationReason.COMPLETED_AUTHORIZED_UNIT
    assert len(records) == 10


def test_taxonomy_techniques_reach_every_phase():
    reasoner = StubReasoner(); _execute(reasoner)
    assert len(reasoner.requests) == 10
    assert all(r.inner_sanctum_status == "ALWAYS_OPEN" for r in reasoner.requests)
    assert all([c.component_id for c in r.permitted_taxonomy_techniques] == ["LC-001"] for r in reasoner.requests)


def test_reasoning_executor_rejects_closed_inner_sanctum():
    with pytest.raises(ValueError, match="cannot be closed"):
        InquiryReasoningExecutor(StubReasoner()).run_to_termination(_run(), _procedure(), [_documentary_input()], inner_sanctum_authorized=False, permitted_taxonomy_techniques=[_taxonomy_component()])


def test_reasoning_executor_requires_taxonomy():
    with pytest.raises(ValueError, match="requires the always-open"):
        InquiryReasoningExecutor(StubReasoner()).run_to_termination(_run(), _procedure(), [_documentary_input()])


def _request():
    return PhaseReasoningRequest(run_id="RUN-FIELD-1", repository_full_name="izzy9118-blip/custos", git_commit="1234567", cognitive_memory_manifest_id="MAN-000000002", governing_specification_ids=["SPEC-000000002"], state=InquiryState.DOCUMENTARY_INTAKE, phase_number=1, phase_name="Documentary Intake", instructions=[PhaseInstruction(sequence=1, instruction="Audit the source.")], initiating_question="Question", documentary_boundary="Boundary", documentary_inputs=[_documentary_input()], permitted_taxonomy_techniques=[_taxonomy_component()], epistemic_limit="No model output establishes documentary truth.")


def test_subprocess_reasoner_exchanges_strict_json_without_shell():
    script = "import json,sys; r=json.load(sys.stdin); print(json.dumps({'run_id':r['run_id'],'state':r['state'],'completed':True,'summary':'Bounded response.'}))"
    response = SubprocessPhaseReasoner([sys.executable, "-c", script]).reason(_request())
    assert response.completed is True


def test_phase_request_cannot_close_inner_sanctum():
    values = _request().model_dump(mode="json"); values["inner_sanctum_authorized"] = False
    with pytest.raises(ValidationError, match="mandatory always-open"):
        PhaseReasoningRequest.model_validate(values)


def test_field_reasoner_cannot_create_documented_finding():
    with pytest.raises(ValidationError, match="may not create documented findings"):
        CandidateStatement(candidate_id="CAND-01", text="Unsupported promotion.", epistemic_classification=EpistemicClassification.DOCUMENTED_FINDING, evidence_record_ids=["EVR-FIELD-1"])


def test_reasoning_schema_command_exposes_always_open_contract(capsys):
    args = build_parser().parse_args(["reasoning-schema", "--kind", "both"])
    assert reasoning_schema_command(args) == 0
    schemas = json.loads(capsys.readouterr().out)
    assert "permitted_taxonomy_techniques" in schemas["request"]["required"]
    assert schemas["request"]["properties"]["inner_sanctum_status"]["default"] == "ALWAYS_OPEN"
