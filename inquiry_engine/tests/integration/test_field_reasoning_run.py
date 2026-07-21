import json
import sys
from pathlib import Path

from custos_engine.cli import build_parser
from custos_engine.graph.integrity import sha256_hex


GOVERNED_COMMIT = "55a9a75a7857a91f6db19a323668d20da3c83af3"
MANIFEST_COMMIT = "55d6f7ad16f3f3de5ea237c3c718bd42d81f3534"


def test_field_reasoner_executes_fixed_ten_phase_candidate_run(tmp_path):
    repo_root = Path(__file__).resolve().parents[3]
    question_path = tmp_path / "RUN-FIELD-INTEGRATION-question.json"
    output_dir = tmp_path / "RUN-FIELD-INTEGRATION"
    reasoner_path = tmp_path / "reasoner.py"

    question_path.write_text(
        json.dumps(
            {
                "run_id": "RUN-FIELD-INTEGRATION",
                "initiating_question": "What does the fixed excerpt support?",
                "documentary_boundary": "One neutral integration-test excerpt.",
                "source_entity_ids": [],
                "documentary_inputs": [
                    {
                        "evidence_id": "EVR-FIELD-INTEGRATION",
                        "source_role": "PRIMARY",
                        "citation": "Neutral integration fixture, line 1",
                        "text": "A fixed neutral documentary excerpt.",
                        "source_fixity_sha256": "a" * 64,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    reasoner_path.write_text(
        """import json
import sys

request = json.load(sys.stdin)
response = {
    "run_id": request["run_id"],
    "state": request["state"],
    "completed": True,
    "summary": f"Completed phase {request['phase_number']} over fixed evidence.",
    "candidate_statements": [
        {
            "candidate_id": f"CAND-FIELD-{request['phase_number']:02d}",
            "text": "A source-bounded candidate statement.",
            "epistemic_classification": "SUPPORTED_INFERENCE",
            "evidence_record_ids": ["EVR-FIELD-INTEGRATION"],
            "limitations": ["This integration fixture establishes no documentary truth."],
        }
    ],
}
print(json.dumps(response))
""",
        encoding="utf-8",
    )

    args = build_parser().parse_args(
        [
            "run",
            "--mode",
            "PRODUCTION",
            "--repo-root",
            str(repo_root),
            "--git-commit",
            GOVERNED_COMMIT,
            "--manifest-git-commit",
            MANIFEST_COMMIT,
            "--manifest",
            "manifests/cognitive-memory/MAN-000000001.json",
            "--manifest-schema",
            "inquiry_engine/src/custos_engine/schemas/cognitive_memory_manifest.schema.json",
            "--taxonomy-schema",
            "inquiry_engine/src/custos_engine/schemas/taxonomy_component.schema.json",
            "--procedure-schema",
            "inquiry_engine/src/custos_engine/schemas/procedure.schema.json",
            "--question",
            str(question_path),
            "--output",
            str(output_dir),
            "--reasoner-command",
            f"{sys.executable} {reasoner_path}",
        ]
    )

    assert args.handler(args) == 0

    run = json.loads((output_dir / "inquiry_run.json").read_text(encoding="utf-8"))
    records = json.loads(
        (output_dir / "phase_reasoning_records.json").read_text(encoding="utf-8")
    )
    package_manifest = json.loads(
        (output_dir / "package_manifest.json").read_text(encoding="utf-8")
    )
    assert run["current_state"] == "TERMINATED"
    assert run["termination_reason"] == "COMPLETED_AUTHORIZED_UNIT"
    assert len(records) == 10
    assert all(
        record["request"]["permitted_taxonomy_techniques"] == []
        for record in records
    )
    assert package_manifest["files"]["phase_reasoning_records.json"] == sha256_hex(
        records
    )
