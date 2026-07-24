from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import shlex
import subprocess

from .config import load_config, load_yaml
from .validation import validate_inquiry, validate_repository


READER_MODES = ("close", "sweep")


class ReaderError(RuntimeError):
    pass


class ReaderReasonerRequired(ReaderError):
    pass


def git_head(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception:
        return "UNAVAILABLE"


def _source_record(source: Path) -> dict[str, Any]:
    path = source.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Source file does not exist: {path}")
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    return {
        "kind": "source",
        "path": str(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "character_count": len(text),
        "text": text,
    }


def _inquiry_record(root: Path, inquiry: Path | str) -> dict[str, Any]:
    checked = validate_inquiry(root, inquiry)
    inquiry_dir = root / checked["path"]
    evidence_manifest = load_yaml(inquiry_dir / "evidence.yaml")
    excerpts = []
    for item in evidence_manifest.get("evidence", []):
        excerpts.append({**item, "text": (root / item["path"]).read_text(encoding="utf-8")})
    return {
        "kind": "inquiry",
        "path": checked["path"],
        "status": checked["status"],
        "text": (inquiry_dir / "inquiry.md").read_text(encoding="utf-8"),
        "evidence": excerpts,
    }


def _required_response(mode: str) -> dict[str, str]:
    common = {
        "contract": "custos.reader-response.v1",
        "mode": mode,
        "examination_markdown": "nonempty string",
        "documented_findings": "array",
        "supported_inferences": "array",
        "working_hypotheses": "array",
        "uncertainties": "array",
        "inner_gate_evaluations": "array",
        "status": "string",
    }
    if mode == "close":
        return {
            **common,
            "bounded_inquiry": "object defining passage, context, question, and boundary",
            "strongest_alternative": "string or null",
            "next_textual_act": "nonempty string",
        }
    return {
        **common,
        "whole_text_map": "object describing divisions, citations, terms, architecture, and anomalies",
        "outer_gate_passes": "array recording the whole-text procedural sweep",
        "candidate_inquiries": "array of bounded inquiries for later close reading",
        "next_textual_act": "nonempty string naming the first warranted close-reading act",
    }


def build_reader_request(
    root: Path,
    *,
    mode: str,
    source: Path | None = None,
    inquiry: Path | str | None = None,
) -> dict[str, Any]:
    if mode not in READER_MODES:
        raise ValueError(f"Unknown Reader mode: {mode}")
    if (source is None) == (inquiry is None):
        raise ValueError("Supply exactly one Reader input: --source or --inquiry")

    validation = validate_repository(root, inquiry=inquiry)
    config = load_config(root)
    reader_input = _source_record(source) if source is not None else _inquiry_record(root, inquiry)  # type: ignore[arg-type]
    protocol = load_yaml(root / config["reading_protocol"])
    taxonomy = load_yaml(root / config["literary_techniques"])

    mode_instruction = (
        "Complete one slow, bounded textual act. Preserve the next act so the examination can continue with the user."
        if mode == "close"
        else "Sweep the complete supplied text. Compile documentary architecture and candidate problems through the outer procedural gate and evaluate the inner literary gate only where fixed evidence activates it. A sweep maps and prioritizes; it does not pretend to complete every close reading."
    )

    return {
        "contract": "custos.reader-request.v1",
        "repository_commit": git_head(root),
        "instructions_path": config["instructions"],
        "reader_mode": mode,
        "mode_instruction": mode_instruction,
        "gates": {
            "outer": {
                "name": "documentary inquiry sequence",
                "source": config["reading_protocol"],
                "protocol": protocol,
            },
            "inner": {
                "name": "literary-technique discernment",
                "source": config["literary_techniques"],
                "taxonomy": taxonomy,
                "rule": "Availability is not presence; evidence alone activates a technique evaluation.",
            },
        },
        "input": reader_input,
        "validation": validation,
        "required_response": _required_response(mode),
    }


def _create_output(output: Path, request: dict[str, Any]) -> None:
    output.mkdir(parents=True, exist_ok=False)
    (output / "reader-request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def prepare_reader(
    root: Path,
    output: Path,
    *,
    mode: str,
    source: Path | None = None,
    inquiry: Path | str | None = None,
) -> Path:
    request = build_reader_request(root, mode=mode, source=source, inquiry=inquiry)
    _create_output(output, request)
    run = {
        "status": "PREPARED_FOR_REASONER",
        "reader_mode": mode,
        "repository_commit": request["repository_commit"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (output / "run.json").write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    return output


def _validate_reader_response(response: Any, mode: str) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise ValueError("Reader response must be a JSON object")
    if response.get("contract") != "custos.reader-response.v1":
        raise ValueError("Reader response must use contract custos.reader-response.v1")
    if response.get("mode") != mode:
        raise ValueError(f"Reader response mode must be {mode}")
    examination = response.get("examination_markdown")
    if not isinstance(examination, str) or not examination.strip():
        raise ValueError("Reader response requires substantive examination_markdown")
    if not isinstance(response.get("status"), str) or not response["status"].strip():
        raise ValueError("Reader response requires a nonempty status")
    required_arrays = (
        "documented_findings",
        "supported_inferences",
        "working_hypotheses",
        "uncertainties",
        "inner_gate_evaluations",
    )
    for key in required_arrays:
        if not isinstance(response.get(key), list):
            raise ValueError(f"Reader response field must be an array: {key}")
    if mode == "close":
        if not isinstance(response.get("bounded_inquiry"), dict):
            raise ValueError("Close Reader response requires bounded_inquiry")
    else:
        for key in ("whole_text_map",):
            if not isinstance(response.get(key), dict):
                raise ValueError(f"Sweep Reader response requires object: {key}")
        for key in ("outer_gate_passes", "candidate_inquiries"):
            if not isinstance(response.get(key), list):
                raise ValueError(f"Sweep Reader response requires array: {key}")
    if not isinstance(response.get("next_textual_act"), str) or not response["next_textual_act"].strip():
        raise ValueError("Reader response requires next_textual_act")
    return response


def execute_reader(
    root: Path,
    output: Path,
    *,
    mode: str,
    reasoner_command: str | None,
    source: Path | None = None,
    inquiry: Path | str | None = None,
) -> Path:
    if not reasoner_command:
        raise ReaderReasonerRequired(
            "custos read requires --reasoner-command and must produce substantive analysis; "
            "use custos prepare only when a request package is the intended result"
        )

    request = build_reader_request(root, mode=mode, source=source, inquiry=inquiry)
    _create_output(output, request)
    proc = subprocess.run(
        shlex.split(reasoner_command),
        input=json.dumps(request, ensure_ascii=False),
        capture_output=True,
        text=True,
        timeout=1800 if mode == "sweep" else 600,
    )
    if proc.returncode != 0:
        raise ReaderError(f"Reasoner failed ({proc.returncode}): {proc.stderr.strip()}")
    try:
        response = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Reasoner did not return valid JSON: {exc}") from exc
    response = _validate_reader_response(response, mode)

    (output / "reader-response.json").write_text(
        json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "examination.md").write_text(
        response["examination_markdown"].rstrip() + "\n", encoding="utf-8"
    )
    run = {
        "status": "CLOSE_READING_ACT_COMPLETE" if mode == "close" else "WHOLE_TEXT_SWEEP_COMPLETE",
        "reader_mode": mode,
        "repository_commit": request["repository_commit"],
        "reader_response_status": response.get("status"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (output / "run.json").write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    return output


def sanctum_report(root: Path, inquiry: Path | str, envelope_path: Path, output: Path) -> Path:
    """Temporary provenance adapter retained until the Strauss Minister is rebuilt."""
    request = build_reader_request(root, mode="close", inquiry=inquiry)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    reader_input = request["input"]
    if (
        not isinstance(envelope, dict)
        or not envelope.get("question")
        or envelope.get("inquiry_id") != reader_input["status"]["inquiry_id"]
    ):
        raise ValueError("Envelope must name the selected inquiry_id and a nonempty question")
    report = {
        "contract": "custos.sanctum-report.v1",
        "inquiry_id": envelope["inquiry_id"],
        "question": envelope["question"],
        "repository_commit": request["repository_commit"],
        "governing_instruction": "CUSTOS.md",
        "reading_protocol": request["gates"]["outer"]["source"],
        "evidence": [
            {
                "id": item["id"],
                "path": item["path"],
                "sha256": item["sha256"],
                "limitations": item.get("limitations", []),
            }
            for item in reader_input["evidence"]
        ],
        "current_state": reader_input["status"],
        "report_status": "CANDIDATE_NOT_CERTIFIED",
        "limitations": [
            "This temporary adapter does not constitute the Strauss Minister.",
            "Custos retains its corpus and internal inquiry record.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output
