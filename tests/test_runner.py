from pathlib import Path
import json
import shlex
import sys

import pytest

from custos.runner import (
    ReaderReasonerRequired,
    build_reader_request,
    execute_reader,
    prepare_reader,
    sanctum_report,
)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def inquiry_path() -> Path:
    return Path("inquiries/thoughts-on-machiavelli/chapter-01-note-01")


def test_close_request_is_self_contained():
    request = build_reader_request(root(), mode="close", inquiry=inquiry_path())
    assert request["contract"] == "custos.reader-request.v1"
    assert request["reader_mode"] == "close"
    assert request["gates"]["outer"]["protocol"]["literary_attention"]["always_open"] is True
    assert len(request["gates"]["inner"]["taxonomy"]["techniques"]) == 22
    assert request["input"]["status"]["stage"] == "comparative_return"


def test_sweep_request_accepts_an_explicit_source(tmp_path):
    source = tmp_path / "book.txt"
    source.write_text("BOOK I\nBeginning.\n\nBOOK II\nEnding.\n", encoding="utf-8")
    request = build_reader_request(root(), mode="sweep", source=source)
    assert request["input"]["kind"] == "source"
    assert request["input"]["sha256"]
    assert request["required_response"]["whole_text_map"]
    assert request["required_response"]["candidate_inquiries"]


def test_prepare_is_explicitly_not_completed_analysis(tmp_path):
    output = prepare_reader(
        root(), tmp_path / "prepared", mode="close", inquiry=inquiry_path()
    )
    status = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert status["status"] == "PREPARED_FOR_REASONER"
    assert status["status"] != "READY_FOR_REASONER"
    assert not (output / "reader-response.json").exists()
    assert not (output / "examination.md").exists()


def test_read_refuses_to_claim_analysis_without_a_reasoner(tmp_path):
    output = tmp_path / "not-created"
    with pytest.raises(ReaderReasonerRequired, match="requires --reasoner-command"):
        execute_reader(
            root(),
            output,
            mode="close",
            reasoner_command=None,
            inquiry=inquiry_path(),
        )
    assert not output.exists()


def test_read_writes_substantive_close_examination(tmp_path):
    reasoner = tmp_path / "reasoner.py"
    response = {
        "contract": "custos.reader-response.v1",
        "mode": "close",
        "examination_markdown": "# Examination\n\nA substantive bounded reading.",
        "documented_findings": [],
        "supported_inferences": [],
        "working_hypotheses": [],
        "uncertainties": [],
        "inner_gate_evaluations": [],
        "bounded_inquiry": {"question": "What does the sequence establish?"},
        "strongest_alternative": None,
        "next_textual_act": "Recover the Italian wording.",
        "status": "BOUNDED_ACT_COMPLETE",
    }
    reasoner.write_text(
        "import json, sys\njson.load(sys.stdin)\nprint(json.dumps(" + repr(response) + "))\n",
        encoding="utf-8",
    )
    command = f"{shlex.quote(sys.executable)} {shlex.quote(str(reasoner))}"
    output = execute_reader(
        root(),
        tmp_path / "completed",
        mode="close",
        reasoner_command=command,
        inquiry=inquiry_path(),
    )
    run = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert run["status"] == "CLOSE_READING_ACT_COMPLETE"
    assert "substantive bounded reading" in (output / "examination.md").read_text()


def test_sanctum_adapter_requires_an_explicit_reader_inquiry(tmp_path):
    envelope = tmp_path / "envelope.json"
    envelope.write_text(
        json.dumps(
            {
                "inquiry_id": "TM-CH01-N01",
                "question": "What does the citation sequence establish?",
            }
        ),
        encoding="utf-8",
    )
    output = sanctum_report(
        root(), inquiry_path(), envelope, tmp_path / "report.json"
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["report_status"] == "CANDIDATE_NOT_CERTIFIED"
    assert report["limitations"][0].startswith("This temporary adapter")
