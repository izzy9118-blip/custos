from pathlib import Path
import json
from custos.runner import build_request, analyze, sanctum_report

def root() -> Path:
    return Path(__file__).resolve().parents[1]

def test_request_is_self_contained():
    req=build_request(root())
    assert req["contract"] == "custos.analysis-request.v1"
    assert req["protocol"]["literary_attention"]["always_open"] is True
    assert len(req["literary_techniques"]["techniques"]) == 22
    assert req["inquiry"]["status"]["stage"] == "comparative_return"

def test_analyze_writes_auditable_request(tmp_path):
    out=analyze(root(),tmp_path/"run")
    assert (out/"analysis-request.json").is_file()
    status=json.loads((out/"run.json").read_text())
    assert status["status"] == "READY_FOR_REASONER"

def test_sanctum_report_is_bounded(tmp_path):
    env=tmp_path/"envelope.json"
    env.write_text(json.dumps({"inquiry_id":"TM-CH01-N01","question":"What does the citation sequence establish?"}))
    out=sanctum_report(root(),env,tmp_path/"report.json")
    report=json.loads(out.read_text())
    assert report["report_status"] == "CANDIDATE_NOT_CERTIFIED"
    assert report["governing_instruction"] == "CUSTOS.md"
