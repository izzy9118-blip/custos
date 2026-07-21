import json

from custos_engine.graph.integrity import sha256_hex
from custos_engine.models.base import EngineMode, InquiryState, TerminationReason
from custos_engine.models.inquiry import InquiryRun, TerminationRecord
from custos_engine.outputs.inquiry_package import InquiryPackageWriter


def test_package_records_and_hashes_inner_sanctum_gate_decision(tmp_path):
    run = InquiryRun(
        run_id="RUN-1",
        mode=EngineMode.PRODUCTION,
        initiating_question="Does the bounded difficulty satisfy the gate?",
        documentary_boundary="One declared passage pair.",
        repository_full_name="izzy9118-blip/custos",
        git_commit="1234567",
        cognitive_memory_manifest_id="MAN-000000001",
        governing_specification_ids=["SPEC-000000002"],
        current_state=InquiryState.TERMINATED,
        termination_reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
    )
    termination = TerminationRecord(
        run_id=run.run_id,
        reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
        explanation="The bounded gate determination is complete.",
        evidence_exhausted=False,
        authorized_unit_completed=True,
    )
    gate_decision = {
        "authorized": False,
        "reasons": ["No genuine documentary difficulty has been identified."],
        "epistemic_limit": "No concealment conclusion is authorized.",
    }
    output_dir = tmp_path / "RUN-1"

    InquiryPackageWriter(output_dir).write(
        run,
        {"run_id": "RUN-1"},
        termination,
        gate_decision=gate_decision,
    )

    persisted = json.loads(
        (output_dir / "inner_sanctum_gate_decision.json").read_text(
            encoding="utf-8"
        )
    )
    package_manifest = json.loads(
        (output_dir / "package_manifest.json").read_text(encoding="utf-8")
    )
    assert persisted == gate_decision
    assert package_manifest["files"]["inner_sanctum_gate_decision.json"] == (
        sha256_hex(gate_decision)
    )


def test_package_records_and_hashes_phase_reasoning_records(tmp_path):
    run = InquiryRun(
        run_id="RUN-FIELD-1",
        mode=EngineMode.PRODUCTION,
        initiating_question="What does the fixed evidence support?",
        documentary_boundary="One declared source excerpt.",
        repository_full_name="izzy9118-blip/custos",
        git_commit="1234567",
        cognitive_memory_manifest_id="MAN-000000001",
        governing_specification_ids=["SPEC-000000002"],
        current_state=InquiryState.TERMINATED,
        termination_reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
        reasoning_record_ids=["RUN-FIELD-1-PHASE-01"],
    )
    termination = TerminationRecord(
        run_id=run.run_id,
        reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
        explanation="The candidate inquiry unit is complete.",
        evidence_exhausted=False,
        authorized_unit_completed=True,
    )
    reasoning_records = [
        {
            "record_id": "RUN-FIELD-1-PHASE-01",
            "adapter_id": "SUBPROCESS_JSON_V1",
            "request": {"phase_number": 1},
            "response": {"completed": True},
        }
    ]
    output_dir = tmp_path / run.run_id

    InquiryPackageWriter(output_dir).write(
        run,
        {"run_id": run.run_id},
        termination,
        phase_reasoning_records=reasoning_records,
    )

    persisted = json.loads(
        (output_dir / "phase_reasoning_records.json").read_text(encoding="utf-8")
    )
    package_manifest = json.loads(
        (output_dir / "package_manifest.json").read_text(encoding="utf-8")
    )
    assert persisted == reasoning_records
    assert package_manifest["files"]["phase_reasoning_records.json"] == sha256_hex(
        reasoning_records
    )


def test_package_records_and_hashes_graph_retrieval_receipt(tmp_path):
    run = InquiryRun(
        run_id="RUN-GRAPH-1",
        mode=EngineMode.PRODUCTION,
        initiating_question="What does the graph-selected evidence support?",
        documentary_boundary="One graph-selected canonical record.",
        repository_full_name="izzy9118-blip/custos",
        git_commit="1234567",
        cognitive_memory_manifest_id="MAN-000000001",
        projection_manifest_id="PRJ-000000001",
        governing_specification_ids=["SPEC-000000002"],
        current_state=InquiryState.TERMINATED,
        termination_reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
    )
    termination = TerminationRecord(
        run_id=run.run_id,
        reason=TerminationReason.COMPLETED_AUTHORIZED_UNIT,
        explanation="The graph retrieval record is fixed.",
        evidence_exhausted=False,
        authorized_unit_completed=True,
    )
    receipt = {
        "projection_id": "PRJ-000000001",
        "projection_integrity_sha256": "a" * 64,
        "requested_canonical_ids": ["SPEC-000000001"],
    }
    output_dir = tmp_path / run.run_id

    InquiryPackageWriter(output_dir).write(
        run,
        {"run_id": run.run_id},
        termination,
        graph_retrieval_receipt=receipt,
    )

    package_manifest = json.loads(
        (output_dir / "package_manifest.json").read_text(encoding="utf-8")
    )
    assert package_manifest["files"]["graph_retrieval_receipt.json"] == sha256_hex(
        receipt
    )
