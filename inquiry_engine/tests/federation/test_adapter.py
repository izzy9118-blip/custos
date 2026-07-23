import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from custos_engine.federation.adapter import (
    FederationContractError,
    FederationRunConfig,
    _load_working_snapshot,
    _object_sha256_without_integrity,
    _selected_minister,
    _validate_schema,
    _verify_evidence,
    _verify_integrity,
    execute_federation_run,
)
from custos_engine.graph.integrity import sha256_hex
from custos_engine.repository.github_reader import LocalGitReader


REPOSITORY_FULL_NAME = "izzy9118-blip/custos"
GOVERNED_COMMIT = "55a9a75a7857a91f6db19a323668d20da3c83af3"
EVIDENCE_PATH = "records/inquiry-architecture/IAR-000000001.yaml"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _head(repo_root: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _snapshot():
    repo_root = _repo_root()
    release_commit = _head(repo_root)
    return _load_working_snapshot(repo_root, release_commit)


def _envelope(release_commit: str) -> dict:
    value = {
        "contract_version": "1.0.0",
        "envelope_id": "INQ-000000001",
        "envelope_version": "1.0.0",
        "status": "ISSUED",
        "created_at": "2026-07-23T12:00:00-05:00",
        "created_by": {
            "office": "PRESIDENT",
            "actor_id": "SANCTUM-PRESIDENT",
        },
        "question": {
            "text": "What does this bounded documentary evidence support?",
            "purpose": "Exercise the first Custos-to-Sanctum federation lane.",
            "context": "A strict integration fixture.",
            "requested_deliverable": "A source-bounded Ministerial Report.",
        },
        "scope": {
            "documentary_boundary": (
                "Only the declared line range in the content-addressed "
                "Evidence Bundle."
            ),
            "included_topics": ["Political philosophy"],
            "excluded_topics": ["Unfixed evidence"],
            "constraints": ["Preserve epistemic classifications"],
            "preserve_uncertainty": True,
        },
        "routing": {
            "registry_snapshot": {
                "repository_full_name": "izzy9118-blip/Sanctum",
                "git_commit": "9" * 40,
                "path": "registry/ministers.yaml",
                "sha256": "8" * 64,
                "registry_version": "1.1.0",
            },
            "selected_ministers": [
                {
                    "minister_id": "MIN-000000001",
                    "manifest_id": "MNF-000000001",
                    "manifest_version": "1.1.0",
                    "repository_full_name": REPOSITORY_FULL_NAME,
                    "repository_commit": release_commit,
                    "selection_reason": (
                        "The bounded inquiry concerns political philosophy."
                    ),
                }
            ],
        },
        "dispatch_policy": {
            "same_envelope_for_all": True,
            "isolated_context_required": True,
            "parallel_execution": "PREFERRED_WHERE_AVAILABLE",
        },
        "report_contract": {
            "schema_id": (
                "urn:sanctum:federation:ministerial-report:1.0.0"
            ),
            "contract_version": "1.0.0",
        },
    }
    value["integrity"] = {
        "hash_algorithm": "SHA-256",
        "canonicalization": "RFC8785",
        "envelope_sha256": _object_sha256_without_integrity(value),
    }
    return value


def _evidence_bundle(repo_root: Path) -> dict:
    source = LocalGitReader(repo_root, GOVERNED_COMMIT).read_text(EVIDENCE_PATH)
    excerpt = "".join(source.splitlines(keepends=True)[:3])
    value = {
        "contract_version": "1.0.0",
        "bundle_id": "EVB-FEDERATION-INTEGRATION",
        "bundle_version": "1.0.0",
        "created_at": "2026-07-23T12:01:00-05:00",
        "repository_full_name": REPOSITORY_FULL_NAME,
        "items": [
            {
                "evidence_id": "EVR-FED-000000001",
                "canonical_id": "IAR-000000001",
                "git_commit": GOVERNED_COMMIT,
                "path": EVIDENCE_PATH,
                "start_line": 1,
                "end_line": 3,
                "sha256": hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
                "source_role": "REPOSITORY_CONTEXT",
                "source_classification": "REPOSITORY_GOVERNANCE",
                "direct_or_derived": "DIRECT",
                "citation": "IAR-000000001 identity and title",
                "support_summary": (
                    "Identifies the governing inquiry architecture used by "
                    "the bounded integration fixture."
                ),
            }
        ],
    }
    value["integrity"] = {
        "hash_algorithm": "SHA-256",
        "canonicalization": "RFC8785",
        "bundle_sha256": _object_sha256_without_integrity(value),
    }
    return value


def _write_json(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _reasoner(path: Path) -> None:
    path.write_text(
        """import json
import sys

request = json.load(sys.stdin)
phase = request["phase_number"]
candidate = {
    "candidate_id": f"CAND-FED-{phase:02d}",
    "text": f"A source-bounded candidate statement from phase {phase}.",
    "epistemic_classification": (
        "WORKING_HYPOTHESIS" if phase == 7 else "SUPPORTED_INFERENCE"
    ),
    "evidence_record_ids": ["EVR-FED-000000001"],
    "limitations": (
        ["The integration fixture establishes no documentary truth."]
        if phase == 10
        else []
    ),
}
print(json.dumps({
    "run_id": request["run_id"],
    "state": request["state"],
    "completed": True,
    "summary": f"Completed bounded federation phase {phase}.",
    "candidate_statements": [candidate],
}))
""",
        encoding="utf-8",
    )


def test_vendored_contracts_are_fixed_and_compile():
    snapshot = _snapshot()

    assert snapshot.envelope_schema["$id"] == (
        "urn:sanctum:federation:inquiry-envelope:1.0.0"
    )
    assert snapshot.report_schema["$id"] == (
        "urn:sanctum:federation:ministerial-report:1.0.0"
    )
    assert snapshot.evidence_bundle_schema["$id"] == (
        "urn:custos:federation:evidence-bundle:1.0.0"
    )


def test_envelope_integrity_and_release_selection_are_enforced():
    snapshot = _snapshot()
    envelope = _envelope(snapshot.release_commit)

    _validate_schema(envelope, snapshot.envelope_schema, "Inquiry Envelope")
    _verify_integrity(envelope, "envelope_sha256", "Inquiry Envelope")
    assert _selected_minister(envelope, snapshot)["minister_id"] == (
        "MIN-000000001"
    )

    envelope["question"]["text"] = "Tampered after issue."
    with pytest.raises(FederationContractError, match="integrity mismatch"):
        _verify_integrity(envelope, "envelope_sha256", "Inquiry Envelope")


def test_nonisolated_envelope_is_rejected_by_sanctum_contract():
    snapshot = _snapshot()
    envelope = _envelope(snapshot.release_commit)
    envelope["dispatch_policy"]["isolated_context_required"] = False
    envelope["integrity"]["envelope_sha256"] = (
        _object_sha256_without_integrity(envelope)
    )

    with pytest.raises(
        FederationContractError,
        match="failed schema validation",
    ):
        _validate_schema(envelope, snapshot.envelope_schema, "Inquiry Envelope")


def test_evidence_bundle_is_reread_from_reachable_git(tmp_path):
    repo_root = _repo_root()
    snapshot = _snapshot()
    bundle = _evidence_bundle(repo_root)

    _validate_schema(
        bundle,
        snapshot.evidence_bundle_schema,
        "Custos Evidence Bundle",
    )
    _verify_integrity(bundle, "bundle_sha256", "Custos Evidence Bundle")
    verified = _verify_evidence(repo_root, snapshot.release_commit, bundle)

    assert len(verified) == 1
    assert verified[0].documentary_input["text"].startswith(
        'id: "IAR-000000001"'
    )
    assert verified[0].report_record["verified"] is True
    assert "lines 1-3" in verified[0].report_record["locator"]

    bundle["items"][0]["sha256"] = "0" * 64
    with pytest.raises(FederationContractError, match="failed Git fixity"):
        _verify_evidence(repo_root, snapshot.release_commit, bundle)


def test_federation_round_trip_emits_valid_candidate_report(tmp_path):
    repo_root = _repo_root()
    snapshot = _snapshot()
    envelope = _envelope(snapshot.release_commit)
    bundle = _evidence_bundle(repo_root)
    envelope_path = tmp_path / "envelope.json"
    bundle_path = tmp_path / "evidence-bundle.json"
    reasoner_path = tmp_path / "reasoner.py"
    output_dir = tmp_path / "federation-run"
    _write_json(envelope_path, envelope)
    _write_json(bundle_path, bundle)
    _reasoner(reasoner_path)

    result = execute_federation_run(
        FederationRunConfig(
            repo_root=repo_root,
            release_commit=snapshot.release_commit,
            envelope_path=envelope_path,
            evidence_bundle_path=bundle_path,
            output_dir=output_dir,
            reasoner_command=f"{sys.executable} {reasoner_path}",
            reasoner_timeout_seconds=30.0,
            reasoner_provider="TEST",
            reasoner_model="STRICT-STUB",
            reasoner_model_revision="1",
            prompt_id="PROMPT-FEDERATION-INTEGRATION",
            prompt_version="1.0",
        ),
        snapshot_override=snapshot,
        verify_runtime_checkout=False,
    )

    report = json.loads(
        (result / "ministerial-report.json").read_text(encoding="utf-8")
    )
    package_manifest = json.loads(
        (result / "package_manifest.json").read_text(encoding="utf-8")
    )
    question_snapshot = json.loads(
        (result / "question_snapshot.json").read_text(encoding="utf-8")
    )
    reasoning_records = json.loads(
        (result / "phase_reasoning_records.json").read_text(encoding="utf-8")
    )

    _validate_schema(report, snapshot.report_schema, "Ministerial Report")
    _verify_integrity(report, "report_sha256", "Ministerial Report")
    assert report["repository"]["git_commit"] == snapshot.release_commit
    assert report["governing_manifest"]["declared_repository_commit"] == (
        GOVERNED_COMMIT
    )
    assert report["secretary_validation_status"] == "NOT_YET_VALIDATED"
    assert report["termination"]["status"] == "COMPLETED_WITH_LIMITATIONS"
    assert len(report["evidence"]) == 1
    assert len(report["findings"]) == 10
    assert len(report["uncertainties"]) == 1
    assert report["dissent"] == []
    assert "excerpt" not in report["evidence"][0]
    assert question_snapshot["initiating_question"] == (
        envelope["question"]["text"]
    )
    assert len(reasoning_records) == 10
    assert all(
        record["request"]["initiating_question"] == envelope["question"]["text"]
        for record in reasoning_records
    )
    assert package_manifest["files"]["ministerial-report.json"] == sha256_hex(
        report
    )
    assert package_manifest["files"]["inquiry_envelope.json"] == sha256_hex(
        envelope
    )
    assert package_manifest["files"]["evidence_bundle.json"] == sha256_hex(
        bundle
    )
    assert package_manifest["federation"]["report_sha256"] == (
        report["integrity"]["report_sha256"]
    )


def test_reasoner_failure_returns_a_conforming_failed_report(tmp_path):
    repo_root = _repo_root()
    snapshot = _snapshot()
    envelope = _envelope(snapshot.release_commit)
    bundle = _evidence_bundle(repo_root)
    envelope_path = tmp_path / "envelope.json"
    bundle_path = tmp_path / "evidence-bundle.json"
    reasoner_path = tmp_path / "failing-reasoner.py"
    output_dir = tmp_path / "failed-federation-run"
    _write_json(envelope_path, envelope)
    _write_json(bundle_path, bundle)
    reasoner_path.write_text(
        "raise SystemExit(7)\n",
        encoding="utf-8",
    )

    result = execute_federation_run(
        FederationRunConfig(
            repo_root=repo_root,
            release_commit=snapshot.release_commit,
            envelope_path=envelope_path,
            evidence_bundle_path=bundle_path,
            output_dir=output_dir,
            reasoner_command=f"{sys.executable} {reasoner_path}",
            reasoner_timeout_seconds=30.0,
            reasoner_provider="TEST",
            reasoner_model="FAILING-STUB",
            reasoner_model_revision=None,
            prompt_id="PROMPT-FEDERATION-FAILURE",
            prompt_version="1.0",
        ),
        snapshot_override=snapshot,
        verify_runtime_checkout=False,
    )

    report = json.loads(
        (result / "ministerial-report.json").read_text(encoding="utf-8")
    )
    package_manifest = json.loads(
        (result / "package_manifest.json").read_text(encoding="utf-8")
    )
    _validate_schema(report, snapshot.report_schema, "Ministerial Report")
    _verify_integrity(report, "report_sha256", "Ministerial Report")
    assert report["termination"]["status"] == "FAILED"
    assert report["termination"]["error_code"] == (
        "FEDERATION_EXECUTION_FAILED"
    )
    assert report["findings"] == []
    assert report["uncertainties"][0]["effect"] == "PREVENTS_CONCLUSION"
    assert package_manifest["status"] == "FAILED"
    assert package_manifest["files"]["ministerial-report.json"] == sha256_hex(
        report
    )


def test_federation_output_is_never_overwritten(tmp_path):
    snapshot = _snapshot()
    output_dir = tmp_path / "existing"
    output_dir.mkdir()

    with pytest.raises(FileExistsError, match="already exists"):
        execute_federation_run(
            FederationRunConfig(
                repo_root=_repo_root(),
                release_commit=snapshot.release_commit,
                envelope_path=tmp_path / "missing-envelope.json",
                evidence_bundle_path=tmp_path / "missing-bundle.json",
                output_dir=output_dir,
                reasoner_command="unused",
                reasoner_timeout_seconds=30.0,
                reasoner_provider="TEST",
                reasoner_model="STUB",
                reasoner_model_revision=None,
                prompt_id="PROMPT-TEST",
                prompt_version="1.0",
            ),
            snapshot_override=snapshot,
            verify_runtime_checkout=False,
        )
