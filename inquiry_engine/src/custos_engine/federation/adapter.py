from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from custos_engine import __version__ as ENGINE_VERSION
from custos_engine.graph.integrity import sha256_hex
from custos_engine.repository.github_reader import LocalGitReader


ADAPTER_MANIFEST_PATH = (
    "inquiry_engine/src/custos_engine/federation/adapter-manifest.json"
)
ADAPTER_MANIFEST_SCHEMA_PATH = (
    "inquiry_engine/src/custos_engine/federation/schemas/"
    "adapter-manifest.schema.json"
)
REPORT_FILENAME = "ministerial-report.json"
MAX_EXCERPT_BYTES = 200_000
MAX_DOCUMENTARY_INPUT_BYTES = 1_000_000


class FederationContractError(ValueError):
    """The supplied federation input or pinned interface is not trustworthy."""


@dataclass(frozen=True)
class FederationRunConfig:
    repo_root: Path
    release_commit: str
    envelope_path: Path
    evidence_bundle_path: Path
    output_dir: Path
    reasoner_command: str
    reasoner_timeout_seconds: float
    reasoner_provider: str
    reasoner_model: str
    reasoner_model_revision: str | None
    prompt_id: str
    prompt_version: str


@dataclass(frozen=True)
class _AdapterSnapshot:
    release_commit: str
    manifest: dict[str, Any]
    envelope_schema: dict[str, Any]
    report_schema: dict[str, Any]
    evidence_bundle_schema: dict[str, Any]


@dataclass(frozen=True)
class _VerifiedEvidence:
    documentary_input: dict[str, Any]
    report_record: dict[str, Any]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso8601(value: datetime) -> str:
    return value.isoformat()


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise FederationContractError(f"JSON object repeats key: {key}")
        value[key] = item
    return value


def _reject_nonfinite(value: str) -> None:
    raise FederationContractError(f"JSON contains non-finite number: {value}")


def _parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite,
        )
    except json.JSONDecodeError as exc:
        raise FederationContractError(f"{label} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise FederationContractError(f"{label} must be a JSON object")
    return value


def _read_json_file(path: Path, label: str) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise FederationContractError(f"{label} does not exist: {resolved}")
    return _parse_json(resolved.read_text(encoding="utf-8"), label)


def _validate_schema(
    value: dict[str, Any],
    schema: dict[str, Any],
    label: str,
) -> None:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(value),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if not errors:
        return
    first = errors[0]
    location = ".".join(str(part) for part in first.absolute_path) or "<root>"
    raise FederationContractError(
        f"{label} failed schema validation at {location}: {first.message}"
    )


def _canonical_json_bytes(value: Any) -> bytes:
    """RFC 8785 bytes for the schemas' integer/string/boolean value domain."""

    def assert_supported(item: Any) -> None:
        if isinstance(item, float):
            raise FederationContractError(
                "Federation integrity values must not contain floating-point numbers"
            )
        if isinstance(item, dict):
            for key, nested in item.items():
                if not isinstance(key, str):
                    raise FederationContractError(
                        "Federation integrity object keys must be strings"
                    )
                assert_supported(nested)
        elif isinstance(item, list):
            for nested in item:
                assert_supported(nested)
        elif item is not None and not isinstance(item, (str, int, bool)):
            raise FederationContractError(
                f"Unsupported federation integrity value: {type(item).__name__}"
            )

    assert_supported(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _object_sha256_without_integrity(value: dict[str, Any]) -> str:
    hashed = dict(value)
    hashed.pop("integrity", None)
    return hashlib.sha256(_canonical_json_bytes(hashed)).hexdigest()


def _verify_integrity(
    value: dict[str, Any],
    digest_field: str,
    label: str,
) -> None:
    integrity = value["integrity"]
    supplied = integrity[digest_field]
    computed = _object_sha256_without_integrity(value)
    if supplied != computed:
        raise FederationContractError(
            f"{label} integrity mismatch: {supplied} != {computed}"
        )


def _raw_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _run_git(
    repo_root: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if check and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise FederationContractError(message or f"Git command failed: {args}")
    return completed


def _verify_runtime_checkout(repo_root: Path, release_commit: str) -> str:
    reader = LocalGitReader(repo_root, release_commit)
    head = _run_git(repo_root, "rev-parse", "HEAD^{commit}").stdout.strip()
    if head != reader.resolved_commit:
        raise FederationContractError(
            "Federation execution requires the checkout HEAD to equal the "
            f"selected minister release commit: {head} != {reader.resolved_commit}"
        )
    status = _run_git(
        repo_root,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ).stdout
    if status.strip():
        raise FederationContractError(
            "Federation execution requires a clean release checkout"
        )
    return reader.resolved_commit


def _load_snapshot_from_git(
    repo_root: Path,
    release_commit: str,
) -> _AdapterSnapshot:
    reader = LocalGitReader(repo_root, release_commit)
    manifest = _parse_json(
        reader.read_text(ADAPTER_MANIFEST_PATH),
        "Pinned adapter manifest",
    )
    manifest_schema = _parse_json(
        reader.read_text(ADAPTER_MANIFEST_SCHEMA_PATH),
        "Pinned adapter-manifest schema",
    )
    _validate_schema(manifest, manifest_schema, "Pinned adapter manifest")
    return _build_snapshot(reader.resolved_commit, manifest, reader.read_text)


def _load_working_snapshot(
    repo_root: Path,
    release_commit: str,
) -> _AdapterSnapshot:
    """Load uncommitted interface files only for repository tests."""

    root = repo_root.expanduser().resolve()

    def read_text(repository_path: str) -> str:
        return (root / repository_path).read_text(encoding="utf-8")

    manifest = _parse_json(
        read_text(ADAPTER_MANIFEST_PATH),
        "Working adapter manifest",
    )
    manifest_schema = _parse_json(
        read_text(ADAPTER_MANIFEST_SCHEMA_PATH),
        "Working adapter-manifest schema",
    )
    _validate_schema(manifest, manifest_schema, "Working adapter manifest")
    return _build_snapshot(release_commit, manifest, read_text)


def _build_snapshot(
    release_commit: str,
    manifest: dict[str, Any],
    read_text: Any,
) -> _AdapterSnapshot:
    if manifest["engine"]["version"] != ENGINE_VERSION:
        raise FederationContractError(
            "Adapter manifest engine version does not match the executing package: "
            f"{manifest['engine']['version']} != {ENGINE_VERSION}"
        )
    contract_values: dict[str, dict[str, Any]] = {}
    for name in ("inquiry_envelope", "ministerial_report"):
        declaration = manifest["contracts"][name]
        text = read_text(declaration["vendored_path"])
        digest = _raw_sha256(text)
        if digest != declaration["sha256"]:
            raise FederationContractError(
                f"Vendored {name} schema failed manifest fixity: "
                f"{digest} != {declaration['sha256']}"
            )
        schema = _parse_json(text, f"Vendored {name} schema")
        if schema.get("$id") != declaration["schema_id"]:
            raise FederationContractError(
                f"Vendored {name} schema identifier does not match the adapter manifest"
            )
        Draft202012Validator.check_schema(schema)
        contract_values[name] = schema

    evidence_declaration = manifest["evidence_bundle"]
    evidence_text = read_text(evidence_declaration["vendored_path"])
    evidence_digest = _raw_sha256(evidence_text)
    if evidence_digest != evidence_declaration["sha256"]:
        raise FederationContractError(
            "Vendored evidence-bundle schema failed manifest fixity: "
            f"{evidence_digest} != {evidence_declaration['sha256']}"
        )
    evidence_schema = _parse_json(evidence_text, "Vendored evidence-bundle schema")
    if evidence_schema.get("$id") != evidence_declaration["schema_id"]:
        raise FederationContractError(
            "Evidence-bundle schema identifier does not match the adapter manifest"
        )
    Draft202012Validator.check_schema(evidence_schema)

    return _AdapterSnapshot(
        release_commit=release_commit,
        manifest=manifest,
        envelope_schema=contract_values["inquiry_envelope"],
        report_schema=contract_values["ministerial_report"],
        evidence_bundle_schema=evidence_schema,
    )


def _selected_minister(
    envelope: dict[str, Any],
    snapshot: _AdapterSnapshot,
) -> dict[str, Any]:
    identity = snapshot.manifest["minister"]
    selections = [
        item
        for item in envelope["routing"]["selected_ministers"]
        if item["minister_id"] == identity["minister_id"]
    ]
    if len(selections) != 1:
        raise FederationContractError(
            "Inquiry Envelope must select the Custos minister exactly once"
        )
    selection = selections[0]
    expected = {
        "minister_id": identity["minister_id"],
        "manifest_id": identity["manifest_id"],
        "manifest_version": identity["manifest_version"],
        "repository_full_name": snapshot.manifest["repository"]["full_name"],
        "repository_commit": snapshot.release_commit,
    }
    mismatches = [
        key for key, value in expected.items() if selection.get(key) != value
    ]
    if mismatches:
        raise FederationContractError(
            "Inquiry Envelope Custos selection does not match the pinned "
            "adapter release: "
            + ", ".join(mismatches)
        )
    return selection


def _assert_ancestor(
    repo_root: Path,
    source_commit: str,
    release_commit: str,
) -> None:
    completed = _run_git(
        repo_root,
        "merge-base",
        "--is-ancestor",
        source_commit,
        release_commit,
        check=False,
    )
    if completed.returncode != 0:
        raise FederationContractError(
            f"Evidence commit is not reachable from the adapter release: {source_commit}"
        )


def _bounded(value: str, maximum: int, label: str) -> str:
    if len(value) > maximum:
        raise FederationContractError(
            f"{label} exceeds the federation contract limit of {maximum} characters"
        )
    return value


def _verify_evidence(
    repo_root: Path,
    release_commit: str,
    bundle: dict[str, Any],
) -> list[_VerifiedEvidence]:
    evidence_ids = [item["evidence_id"] for item in bundle["items"]]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise FederationContractError(
            "Evidence Bundle evidence identifiers must be unique"
        )

    readers: dict[str, LocalGitReader] = {}
    verified: list[_VerifiedEvidence] = []
    total_bytes = 0
    for item in bundle["items"]:
        start_line = item["start_line"]
        end_line = item["end_line"]
        if end_line < start_line:
            raise FederationContractError(
                f"Evidence line range is reversed for {item['evidence_id']}"
            )
        commit = item["git_commit"]
        _assert_ancestor(repo_root, commit, release_commit)
        if commit not in readers:
            readers[commit] = LocalGitReader(repo_root, commit)
        reader = readers[commit]
        source = reader.read_text(item["path"])
        lines = source.splitlines(keepends=True)
        if end_line > len(lines):
            raise FederationContractError(
                f"Evidence line range exceeds {item['path']} for "
                f"{item['evidence_id']}: {end_line} > {len(lines)}"
            )
        excerpt = "".join(lines[start_line - 1 : end_line])
        if not excerpt:
            raise FederationContractError(
                f"Evidence excerpt is empty for {item['evidence_id']}"
            )
        excerpt_bytes = excerpt.encode("utf-8")
        if len(excerpt_bytes) > MAX_EXCERPT_BYTES:
            raise FederationContractError(
                f"Evidence excerpt exceeds {MAX_EXCERPT_BYTES} bytes for "
                f"{item['evidence_id']}"
            )
        total_bytes += len(excerpt_bytes)
        if total_bytes > MAX_DOCUMENTARY_INPUT_BYTES:
            raise FederationContractError(
                "Evidence Bundle exceeds the total documentary-input byte limit"
            )
        digest = hashlib.sha256(excerpt_bytes).hexdigest()
        if digest != item["sha256"]:
            raise FederationContractError(
                f"Evidence excerpt failed Git fixity for {item['evidence_id']}: "
                f"{digest} != {item['sha256']}"
            )

        line_locator = (
            f"{item['citation']}; lines {start_line}-{end_line} "
            "(1-based, inclusive)"
        )
        _bounded(line_locator, 2000, "Evidence locator")
        verified.append(
            _VerifiedEvidence(
                documentary_input={
                    "evidence_id": item["evidence_id"],
                    "source_role": item["source_role"],
                    "citation": line_locator,
                    "text": excerpt,
                    "source_fixity_sha256": digest,
                    "source_entity_id": item["canonical_id"],
                    "note": (
                        "Selected by the content-addressed Custos federation "
                        "Evidence Bundle and re-read from canonical Git."
                    ),
                },
                report_record={
                    "evidence_id": item["evidence_id"],
                    "canonical_id": item["canonical_id"],
                    "repository_full_name": bundle["repository_full_name"],
                    "git_commit": reader.resolved_commit,
                    "path": item["path"],
                    "sha256": digest,
                    "locator": line_locator,
                    "direct_or_derived": item["direct_or_derived"],
                    "source_classification": item["source_classification"],
                    "support_summary": item["support_summary"],
                    "verified": True,
                },
            )
        )
    return verified


def _engine_question(
    envelope: dict[str, Any],
    verified_evidence: list[_VerifiedEvidence],
) -> dict[str, Any]:
    return {
        "run_id": (
            f"RUN-FED-{envelope['envelope_id']}-MIN-000000001"
        ),
        "initiating_question": envelope["question"]["text"],
        "documentary_boundary": envelope["scope"]["documentary_boundary"],
        "source_entity_ids": [],
        "documentary_inputs": [
            item.documentary_input for item in verified_evidence
        ],
        "federation_envelope": {
            "envelope_id": envelope["envelope_id"],
            "envelope_version": envelope["envelope_version"],
            "envelope_sha256": envelope["integrity"]["envelope_sha256"],
            "purpose": envelope["question"]["purpose"],
            "context": envelope["question"].get("context"),
            "as_of": envelope["question"].get("as_of"),
            "requested_deliverable": envelope["question"].get(
                "requested_deliverable"
            ),
            "scope": envelope["scope"],
        },
    }


def _engine_namespace(
    config: FederationRunConfig,
    snapshot: _AdapterSnapshot,
    question_path: Path,
    package_dir: Path,
) -> argparse.Namespace:
    engine = snapshot.manifest["engine"]
    return argparse.Namespace(
        mode="PRODUCTION",
        repo_root=str(config.repo_root),
        git_commit=engine["governed_commit"],
        manifest_git_commit=engine["manifest_git_commit"],
        manifest=engine["manifest_path"],
        manifest_schema=engine["manifest_schema_path"],
        taxonomy_schema=engine["taxonomy_schema_path"],
        procedure_schema=engine["procedure_schema_path"],
        projection_git_commit=None,
        projection_manifest=None,
        projection_manifest_schema=None,
        neo4j_uri=None,
        neo4j_username=None,
        neo4j_password_env="NEO4J_PASSWORD",
        question=str(question_path),
        output=str(package_dir),
        reasoner_command=config.reasoner_command,
        reasoner_timeout_seconds=config.reasoner_timeout_seconds,
    )


def _execute_engine(args: argparse.Namespace) -> None:
    # Lazy import avoids a module cycle when cli.py registers federation-run.
    from custos_engine.cli import run_command

    with contextlib.redirect_stdout(io.StringIO()):
        result = run_command(args)
    if result != 0:
        raise RuntimeError(f"Custos Inquiry Engine returned status {result}")


def _read_package_json(package_dir: Path, name: str) -> Any:
    path = package_dir / name
    if not path.is_file():
        raise FederationContractError(
            f"Custos inquiry package is missing required file: {name}"
        )
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite,
        )
    except json.JSONDecodeError as exc:
        raise FederationContractError(
            f"Custos inquiry package contains invalid JSON: {name}"
        ) from exc


def _manifest_provenance(
    repo_root: Path,
    snapshot: _AdapterSnapshot,
) -> tuple[dict[str, Any], dict[str, Any]]:
    engine = snapshot.manifest["engine"]
    reader = LocalGitReader(repo_root, engine["manifest_git_commit"])
    manifest_text = reader.read_text(engine["manifest_path"])
    manifest = _parse_json(manifest_text, "Governing Cognitive Memory Manifest")
    blob_sha = _run_git(
        repo_root,
        "rev-parse",
        f"{reader.resolved_commit}:{engine['manifest_path']}",
    ).stdout.strip()
    provenance = {
        "id": manifest["manifest_id"],
        "version": manifest["version"],
        "path": engine["manifest_path"],
        "sha256": _raw_sha256(manifest_text),
        "git_blob_sha": blob_sha,
        "declared_repository_commit": manifest["repository_commit"],
    }
    return manifest, provenance


def _new_uncertainty(
    uncertainties: list[dict[str, Any]],
    statement: str,
    effect: str,
    evidence_refs: list[str],
) -> str:
    uncertainty_id = f"UNC-{len(uncertainties) + 1:09d}"
    uncertainties.append(
        {
            "uncertainty_id": uncertainty_id,
            "statement": _bounded(statement, 10000, "Uncertainty statement"),
            "effect": effect,
            "resolvability": "UNKNOWN",
            "evidence_refs": sorted(set(evidence_refs)),
        }
    )
    return uncertainty_id


def _report_findings(
    reasoning_records: list[dict[str, Any]],
    evidence_ids: set[str],
    terminal_unresolved: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    uncertainties: list[dict[str, Any]] = []
    seen_finding_ids: set[str] = set()

    for record in reasoning_records:
        response = record["response"]
        for candidate in response["candidate_statements"]:
            candidate_id = candidate["candidate_id"]
            references = candidate["evidence_record_ids"]
            unknown = sorted(set(references).difference(evidence_ids))
            if unknown:
                raise FederationContractError(
                    f"Candidate {candidate_id} cites unknown report evidence: "
                    + ", ".join(unknown)
                )
            classification = candidate["epistemic_classification"]
            if classification == "UNRESOLVED_QUESTION":
                _new_uncertainty(
                    uncertainties,
                    candidate["text"],
                    "REQUIRES_FURTHER_INQUIRY",
                    references,
                )
                continue
            if classification not in {
                "SUPPORTED_INFERENCE",
                "WORKING_HYPOTHESIS",
            }:
                raise FederationContractError(
                    f"Candidate {candidate_id} has no lawful report mapping: "
                    f"{classification}"
                )
            if candidate_id in seen_finding_ids:
                raise FederationContractError(
                    f"Ministerial finding identifier is repeated: {candidate_id}"
                )
            seen_finding_ids.add(candidate_id)
            uncertainty_refs = [
                _new_uncertainty(
                    uncertainties,
                    limitation,
                    "LOWERS_CONFIDENCE",
                    references,
                )
                for limitation in candidate.get("limitations", [])
            ]
            findings.append(
                {
                    "finding_id": candidate_id,
                    "classification": classification,
                    "statement": _bounded(
                        candidate["text"],
                        10000,
                        "Finding statement",
                    ),
                    "rationale": _bounded(
                        response["summary"],
                        10000,
                        "Finding rationale",
                    ),
                    "confidence": (
                        "MODERATE"
                        if classification == "SUPPORTED_INFERENCE"
                        else "LOW"
                    ),
                    "evidence_refs": references,
                    "uncertainty_refs": uncertainty_refs,
                    "dissent_refs": [],
                }
            )
        for unresolved in response.get("unresolved_questions", []):
            _new_uncertainty(
                uncertainties,
                unresolved,
                "REQUIRES_FURTHER_INQUIRY",
                [],
            )

    known_statements = {item["statement"] for item in uncertainties}
    for unresolved in terminal_unresolved:
        if unresolved not in known_statements:
            _new_uncertainty(
                uncertainties,
                unresolved,
                "REQUIRES_FURTHER_INQUIRY",
                [],
            )
            known_statements.add(unresolved)
    return findings, uncertainties


def _termination(
    engine_reason: str,
    explanation: str,
    findings: list[dict[str, Any]],
    uncertainties: list[dict[str, Any]],
) -> dict[str, Any]:
    if engine_reason == "COMPLETED_AUTHORIZED_UNIT":
        if not findings:
            return {
                "status": "INSUFFICIENT_EVIDENCE",
                "code": "NO_REPORTABLE_FINDING",
                "reason": (
                    "Custos completed the authorized procedure but produced no "
                    "candidate statement that may lawfully enter a Ministerial Report."
                ),
                "retryable": True,
                "unresolved_items": [
                    "No reportable candidate finding was produced."
                ],
            }
        status = "COMPLETED_WITH_LIMITATIONS" if uncertainties else "COMPLETED"
        return {
            "status": status,
            "code": engine_reason,
            "reason": _bounded(explanation, 10000, "Termination reason"),
            "retryable": False,
            "unresolved_items": [
                item["uncertainty_id"] for item in uncertainties
            ],
        }

    if engine_reason in {
        "EVIDENCE_EXHAUSTED",
        "MISSING_SOURCE_BLOCK",
        "UNDERDETERMINED",
    }:
        status = "INSUFFICIENT_EVIDENCE"
        retryable = True
    elif engine_reason in {"SCOPE_EXCEEDED", "AUTHORITY_STOP"}:
        status = "OUT_OF_JURISDICTION"
        retryable = False
    else:
        status = "FAILED"
        retryable = True

    value = {
        "status": status,
        "code": engine_reason,
        "reason": _bounded(explanation, 10000, "Termination reason"),
        "retryable": retryable,
        "unresolved_items": [
            item["uncertainty_id"] for item in uncertainties
        ],
    }
    if status == "FAILED":
        value["error_code"] = engine_reason
    return value


def _execution_provenance(
    config: FederationRunConfig,
    snapshot: _AdapterSnapshot,
    run_id: str,
    procedure_id: str,
    started_at: datetime,
    completed_at: datetime,
) -> dict[str, Any]:
    execution: dict[str, Any] = {
        "run_id": run_id,
        "started_at": _iso8601(started_at),
        "completed_at": _iso8601(completed_at),
        "isolated_context": True,
        "engine": {
            "name": snapshot.manifest["engine"]["name"],
            "version": snapshot.manifest["engine"]["version"],
        },
        "procedure_ids": [procedure_id],
        "reasoner": {
            "provider": config.reasoner_provider,
            "model": config.reasoner_model,
            "prompt_id": config.prompt_id,
            "prompt_version": config.prompt_version,
        },
        "cache": {
            "status": "BYPASSED"
        },
    }
    if config.reasoner_model_revision:
        execution["reasoner"]["model_revision"] = config.reasoner_model_revision
    return execution


def _build_report(
    config: FederationRunConfig,
    snapshot: _AdapterSnapshot,
    envelope: dict[str, Any],
    verified_evidence: list[_VerifiedEvidence],
    package_dir: Path,
    started_at: datetime,
    completed_at: datetime,
) -> dict[str, Any]:
    inquiry_run = _read_package_json(package_dir, "inquiry_run.json")
    termination_record = _read_package_json(
        package_dir,
        "termination_record.json",
    )
    reasoning_records = _read_package_json(
        package_dir,
        "phase_reasoning_records.json",
    )
    if not isinstance(reasoning_records, list):
        raise FederationContractError(
            "phase_reasoning_records.json must contain an array"
        )
    evidence_records = [item.report_record for item in verified_evidence]
    evidence_ids = {item["evidence_id"] for item in evidence_records}
    findings, uncertainties = _report_findings(
        reasoning_records,
        evidence_ids,
        termination_record["unresolved_questions"],
    )
    manifest, manifest_provenance = _manifest_provenance(
        config.repo_root,
        snapshot,
    )
    execution = _execution_provenance(
        config,
        snapshot,
        inquiry_run["run_id"],
        manifest["procedure_source"]["canonical_id"],
        started_at,
        completed_at,
    )

    report: dict[str, Any] = {
        "contract_version": "1.0.0",
        "report_id": (
            f"MREP-{envelope['envelope_id']}-MIN-000000001"
        ),
        "report_status": "SUBMITTED",
        "secretary_validation_status": "NOT_YET_VALIDATED",
        "created_at": _iso8601(completed_at),
        "inquiry": {
            "envelope_id": envelope["envelope_id"],
            "envelope_version": envelope["envelope_version"],
            "envelope_sha256": envelope["integrity"]["envelope_sha256"],
            "question_sha256": hashlib.sha256(
                envelope["question"]["text"].encode("utf-8")
            ).hexdigest(),
        },
        "minister": snapshot.manifest["minister"],
        "repository": {
            "full_name": snapshot.manifest["repository"]["full_name"],
            "git_commit": snapshot.release_commit,
            "canonical_authority": "GIT",
        },
        "governing_manifest": manifest_provenance,
        "execution": execution,
        "evidence": evidence_records,
        "findings": findings,
        "uncertainties": uncertainties,
        "dissent": [],
        "termination": _termination(
            termination_record["reason"],
            termination_record["explanation"],
            findings,
            uncertainties,
        ),
    }
    report["integrity"] = {
        "hash_algorithm": "SHA-256",
        "canonicalization": "RFC8785",
        "report_sha256": hashlib.sha256(
            _canonical_json_bytes(report)
        ).hexdigest(),
    }
    _validate_report_references(report)
    _validate_schema(report, snapshot.report_schema, "Ministerial Report")
    return report


def _build_failed_report(
    config: FederationRunConfig,
    snapshot: _AdapterSnapshot,
    envelope: dict[str, Any],
    verified_evidence: list[_VerifiedEvidence],
    error: Exception,
    started_at: datetime,
    completed_at: datetime,
) -> dict[str, Any]:
    manifest, manifest_provenance = _manifest_provenance(
        config.repo_root,
        snapshot,
    )
    message = str(error).strip() or "Federation execution failed."
    message = _bounded(
        f"{type(error).__name__}: {message}",
        10000,
        "Federation failure reason",
    )
    uncertainty = {
        "uncertainty_id": "UNC-000000001",
        "statement": message,
        "effect": "PREVENTS_CONCLUSION",
        "resolvability": "UNKNOWN",
        "evidence_refs": [],
    }
    run_id = f"RUN-FED-{envelope['envelope_id']}-MIN-000000001"
    report: dict[str, Any] = {
        "contract_version": "1.0.0",
        "report_id": (
            f"MREP-{envelope['envelope_id']}-MIN-000000001"
        ),
        "report_status": "SUBMITTED",
        "secretary_validation_status": "NOT_YET_VALIDATED",
        "created_at": _iso8601(completed_at),
        "inquiry": {
            "envelope_id": envelope["envelope_id"],
            "envelope_version": envelope["envelope_version"],
            "envelope_sha256": envelope["integrity"]["envelope_sha256"],
            "question_sha256": hashlib.sha256(
                envelope["question"]["text"].encode("utf-8")
            ).hexdigest(),
        },
        "minister": snapshot.manifest["minister"],
        "repository": {
            "full_name": snapshot.manifest["repository"]["full_name"],
            "git_commit": snapshot.release_commit,
            "canonical_authority": "GIT",
        },
        "governing_manifest": manifest_provenance,
        "execution": _execution_provenance(
            config,
            snapshot,
            run_id,
            manifest["procedure_source"]["canonical_id"],
            started_at,
            completed_at,
        ),
        "evidence": [item.report_record for item in verified_evidence],
        "findings": [],
        "uncertainties": [uncertainty],
        "dissent": [],
        "termination": {
            "status": "FAILED",
            "code": "FEDERATION_EXECUTION_FAILED",
            "reason": message,
            "retryable": True,
            "unresolved_items": [uncertainty["uncertainty_id"]],
            "error_code": "FEDERATION_EXECUTION_FAILED",
        },
    }
    report["integrity"] = {
        "hash_algorithm": "SHA-256",
        "canonicalization": "RFC8785",
        "report_sha256": hashlib.sha256(
            _canonical_json_bytes(report)
        ).hexdigest(),
    }
    _validate_report_references(report)
    _validate_schema(report, snapshot.report_schema, "Failed Ministerial Report")
    return report


def _validate_report_references(report: dict[str, Any]) -> None:
    evidence_ids = {item["evidence_id"] for item in report["evidence"]}
    finding_ids = {item["finding_id"] for item in report["findings"]}
    uncertainty_ids = {
        item["uncertainty_id"] for item in report["uncertainties"]
    }
    dissent_ids = {item["dissent_id"] for item in report["dissent"]}
    for finding in report["findings"]:
        if not set(finding["evidence_refs"]).issubset(evidence_ids):
            raise FederationContractError(
                f"Finding {finding['finding_id']} has unresolved evidence references"
            )
        if not set(finding["uncertainty_refs"]).issubset(uncertainty_ids):
            raise FederationContractError(
                f"Finding {finding['finding_id']} has unresolved uncertainty references"
            )
        if not set(finding["dissent_refs"]).issubset(dissent_ids):
            raise FederationContractError(
                f"Finding {finding['finding_id']} has unresolved dissent references"
            )
    for uncertainty in report["uncertainties"]:
        if not set(uncertainty["evidence_refs"]).issubset(evidence_ids):
            raise FederationContractError(
                f"Uncertainty {uncertainty['uncertainty_id']} has unresolved evidence references"
            )
    for dissent in report["dissent"]:
        if not set(dissent["evidence_refs"]).issubset(evidence_ids):
            raise FederationContractError(
                f"Dissent {dissent['dissent_id']} has unresolved evidence references"
            )
        if not set(dissent["related_finding_refs"]).issubset(finding_ids):
            raise FederationContractError(
                f"Dissent {dissent['dissent_id']} has unresolved finding references"
            )


def _write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(
            value,
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")


def _bind_report_to_package(
    package_dir: Path,
    report: dict[str, Any],
    envelope: dict[str, Any],
    bundle: dict[str, Any],
) -> None:
    package_manifest_path = package_dir / "package_manifest.json"
    package_manifest = _read_package_json(
        package_dir,
        "package_manifest.json",
    )
    package_manifest["files"][REPORT_FILENAME] = sha256_hex(report)
    package_manifest["files"]["inquiry_envelope.json"] = sha256_hex(envelope)
    package_manifest["files"]["evidence_bundle.json"] = sha256_hex(bundle)
    package_manifest["federation"] = {
        "interface_id": "CUSTOS-SANCTUM-FEDERATION",
        "interface_version": "1.0.0",
        "report_sha256": report["integrity"]["report_sha256"],
    }
    package_manifest_path.write_text(
        json.dumps(
            package_manifest,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_failed_package(
    package_dir: Path,
    report: dict[str, Any],
    envelope: dict[str, Any],
    bundle: dict[str, Any] | None,
    snapshot: _AdapterSnapshot,
) -> None:
    package_dir.mkdir()
    _write_json(package_dir / REPORT_FILENAME, report)
    _write_json(package_dir / "inquiry_envelope.json", envelope)
    files = {
        REPORT_FILENAME: sha256_hex(report),
        "inquiry_envelope.json": sha256_hex(envelope),
    }
    if bundle is not None:
        _write_json(package_dir / "evidence_bundle.json", bundle)
        files["evidence_bundle.json"] = sha256_hex(bundle)
    package_manifest = {
        "run_id": report["execution"]["run_id"],
        "git_commit": snapshot.manifest["engine"]["governed_commit"],
        "cognitive_memory_manifest_id": report["governing_manifest"]["id"],
        "status": "FAILED",
        "files": files,
        "federation": {
            "interface_id": "CUSTOS-SANCTUM-FEDERATION",
            "interface_version": "1.0.0",
            "report_sha256": report["integrity"]["report_sha256"],
        },
    }
    _write_json(package_dir / "package_manifest.json", package_manifest)


def execute_federation_run(
    config: FederationRunConfig,
    *,
    snapshot_override: _AdapterSnapshot | None = None,
    verify_runtime_checkout: bool = True,
) -> Path:
    repo_root = config.repo_root.expanduser().resolve()
    if not config.reasoner_command.strip():
        raise FederationContractError("Federation run requires a reasoner command")
    if (
        config.reasoner_timeout_seconds <= 0
        or not math.isfinite(config.reasoner_timeout_seconds)
    ):
        raise FederationContractError(
            "Federation reasoner timeout must be positive"
        )
    required_labels = {
        "reasoner provider": config.reasoner_provider,
        "reasoner model": config.reasoner_model,
        "prompt identifier": config.prompt_id,
    }
    for label, value in required_labels.items():
        if not value.strip() or len(value) > 500:
            raise FederationContractError(
                f"Federation {label} must contain 1 to 500 characters"
            )
    if (
        config.reasoner_model_revision is not None
        and len(config.reasoner_model_revision) > 500
    ):
        raise FederationContractError(
            "Federation model revision exceeds 500 characters"
        )
    if not re.fullmatch(
        r"(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*)){1,2}",
        config.prompt_version,
    ):
        raise FederationContractError(
            "Federation prompt version must be a two- or three-part version"
        )
    output_dir = config.output_dir.expanduser().resolve()
    if output_dir.exists():
        raise FileExistsError(
            f"Federation output directory already exists: {output_dir}"
        )

    release_commit = (
        _verify_runtime_checkout(repo_root, config.release_commit)
        if verify_runtime_checkout
        else LocalGitReader(repo_root, config.release_commit).resolved_commit
    )
    snapshot = snapshot_override or _load_snapshot_from_git(
        repo_root,
        release_commit,
    )
    if snapshot.release_commit != release_commit:
        raise FederationContractError(
            "Adapter snapshot release does not match the selected repository commit"
        )

    envelope = _read_json_file(config.envelope_path, "Inquiry Envelope")
    _validate_schema(envelope, snapshot.envelope_schema, "Inquiry Envelope")
    _verify_integrity(envelope, "envelope_sha256", "Inquiry Envelope")
    _selected_minister(envelope, snapshot)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".custos-federation-",
        dir=output_dir.parent,
    ) as temporary:
        temporary_root = Path(temporary)
        package_dir = temporary_root / "package"
        bundle: dict[str, Any] | None = None
        verified_evidence: list[_VerifiedEvidence] = []
        started_at = _utc_now()
        try:
            bundle = _read_json_file(
                config.evidence_bundle_path,
                "Custos Evidence Bundle",
            )
            _validate_schema(
                bundle,
                snapshot.evidence_bundle_schema,
                "Custos Evidence Bundle",
            )
            _verify_integrity(
                bundle,
                "bundle_sha256",
                "Custos Evidence Bundle",
            )
            verified_evidence = _verify_evidence(
                repo_root,
                release_commit,
                bundle,
            )
            question = _engine_question(envelope, verified_evidence)
            question_path = temporary_root / "question.json"
            question_path.write_text(
                json.dumps(
                    question,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            _execute_engine(
                _engine_namespace(
                    config,
                    snapshot,
                    question_path,
                    package_dir,
                )
            )
            completed_at = _utc_now()
            report = _build_report(
                config,
                snapshot,
                envelope,
                verified_evidence,
                package_dir,
                started_at,
                completed_at,
            )
            _write_json(package_dir / REPORT_FILENAME, report)
            _write_json(package_dir / "inquiry_envelope.json", envelope)
            _write_json(package_dir / "evidence_bundle.json", bundle)
            _bind_report_to_package(
                package_dir,
                report,
                envelope,
                bundle,
            )
            os.replace(package_dir, output_dir)
        except (FederationContractError, RuntimeError, OSError, ValueError) as error:
            completed_at = _utc_now()
            failed_report = _build_failed_report(
                config,
                snapshot,
                envelope,
                verified_evidence,
                error,
                started_at,
                completed_at,
            )
            failure_dir = temporary_root / "failure-package"
            _write_failed_package(
                failure_dir,
                failed_report,
                envelope,
                bundle,
                snapshot,
            )
            os.replace(failure_dir, output_dir)
    return output_dir
