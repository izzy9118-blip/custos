from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from custos_engine.graph.integrity import sha256_hex
from custos_engine.models.inquiry import InquiryRun, TerminationRecord


class InquiryPackageWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=False)

    @staticmethod
    def _write_json(path: Path, value: Any) -> None:
        path.write_text(
            json.dumps(
                value,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )

    def write(
        self,
        run: InquiryRun,
        question: dict[str, Any],
        termination: TerminationRecord,
        gate_decision: dict[str, Any] | None = None,
        phase_reasoning_records: list[dict[str, Any]] | None = None,
    ) -> Path:
        run_data = run.model_dump(mode="json")
        termination_data = termination.model_dump(mode="json")

        self._write_json(self.output_dir / "inquiry_run.json", run_data)
        self._write_json(self.output_dir / "question_snapshot.json", question)
        self._write_json(self.output_dir / "termination_record.json", termination_data)

        package_files = {
            "inquiry_run.json": sha256_hex(run_data),
            "question_snapshot.json": sha256_hex(question),
            "termination_record.json": sha256_hex(termination_data),
        }
        if gate_decision is not None:
            self._write_json(
                self.output_dir / "inner_sanctum_gate_decision.json",
                gate_decision,
            )
            package_files["inner_sanctum_gate_decision.json"] = sha256_hex(
                gate_decision
            )
        if phase_reasoning_records is not None:
            self._write_json(
                self.output_dir / "phase_reasoning_records.json",
                phase_reasoning_records,
            )
            package_files["phase_reasoning_records.json"] = sha256_hex(
                phase_reasoning_records
            )

        package_manifest = {
            "run_id": run.run_id,
            "git_commit": run.git_commit,
            "cognitive_memory_manifest_id": run.cognitive_memory_manifest_id,
            "files": package_files,
        }
        self._write_json(self.output_dir / "package_manifest.json", package_manifest)
        return self.output_dir
