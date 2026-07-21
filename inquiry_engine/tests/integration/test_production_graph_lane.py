import hashlib
import json
import sys
from pathlib import Path

from custos_engine import cli
from custos_engine.cli import build_parser
from custos_engine.models.artifacts import ProjectionManifest
from custos_engine.repository.github_reader import LocalGitReader


GOVERNED_COMMIT = "55a9a75a7857a91f6db19a323668d20da3c83af3"
MANIFEST_COMMIT = "55d6f7ad16f3f3de5ea237c3c718bd42d81f3534"


class FakeNeo4jClient:
    def __init__(self):
        self.writes = []
        self.transactions = []
        self.metadata = None
        self.documentary_rows = []
        self.closed = False

    def verify_connectivity(self):
        pass

    def close(self):
        self.closed = True

    def execute_write(self, query, parameters):
        self.writes.append((query, parameters))

    def execute_write_transaction(self, statements):
        self.transactions.append(list(statements))

    def execute_read(self, query, parameters):
        if "ProjectionSnapshot" in query:
            return [self.metadata] if self.metadata else []
        if "relationship_types" in parameters:
            return []
        return self.documentary_rows


def test_project_neo4j_builds_real_pinned_repository_plan(monkeypatch, tmp_path):
    repo_root = Path(__file__).resolve().parents[3]
    fake = FakeNeo4jClient()
    monkeypatch.setattr(cli, "_neo4j_client", lambda args: fake)
    output = tmp_path / "PRJ-TEST.json"
    args = build_parser().parse_args(
        [
            "project-neo4j",
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
            "--projection-id",
            "PRJ-TEST",
            "--manifest-output",
            str(output),
            "--neo4j-uri",
            "neo4j://example.invalid",
            "--neo4j-username",
            "neo4j",
        ]
    )

    assert args.handler(args) == 0

    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["git_commit"] == GOVERNED_COMMIT
    assert manifest["cognitive_memory_manifest_id"] == "MAN-000000001"
    assert manifest["source_file_count"] > 0
    assert manifest["node_counts"]
    assert len(fake.transactions) == 1
    node_rows = fake.transactions[0][1][1]["nodes"]
    assert any(row["canonical_id"] == "HOC-000000001" for row in node_rows)
    assert fake.closed is True


def test_field_reasoning_uses_graph_selected_git_verified_evidence(
    monkeypatch,
    tmp_path,
):
    repo_root = Path(__file__).resolve().parents[3]
    reader = LocalGitReader(repo_root, GOVERNED_COMMIT)
    source_path = "registers/hermeneutic-object-register/objects/HOC-000000001.yaml"
    source_text = reader.read_text(source_path)
    source_digest = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    projection = ProjectionManifest(
        projection_id="PRJ-FIELD",
        repository_full_name="izzy9118-blip/custos",
        git_commit=GOVERNED_COMMIT,
        cognitive_memory_manifest_id="MAN-000000001",
        projector_version="1.0.0",
        schema_versions={"projection_manifest": "1.0.0"},
        source_file_count=1,
        node_counts={"Hermeneutic Object C": 1},
        relationship_counts={},
        validation_status="PASS",
        integrity_sha256="f" * 64,
    )
    monkeypatch.setattr(
        cli.ProjectionManifestLoader,
        "load_repository",
        lambda self, manifest_path, schema_path: projection,
    )
    fake = FakeNeo4jClient()
    fake.metadata = {
        "projection_id": "PRJ-FIELD",
        "repository_full_name": "izzy9118-blip/custos",
        "git_commit": GOVERNED_COMMIT,
        "cognitive_memory_manifest_id": "MAN-000000001",
        "integrity_sha256": "f" * 64,
        "projector_version": "1.0.0",
    }
    fake.documentary_rows = [
        {
            "requested_id": "HOC-000000001",
            "canonical_id": "HOC-000000001",
            "canonical_class": "Hermeneutic Object C",
            "github_path": source_path,
            "git_commit": GOVERNED_COMMIT,
            "cognitive_memory_manifest_id": "MAN-000000001",
            "source_fixity_sha256": source_digest,
            "source_role": "REPOSITORY_CONTEXT",
            "title": "Strauss's Taxonomy of Literary Concealment",
        }
    ]
    monkeypatch.setattr(cli, "_neo4j_client", lambda args: fake)

    question = tmp_path / "question.json"
    question.write_text(
        json.dumps(
            {
                "run_id": "RUN-GRAPH-FIELD",
                "initiating_question": "What does this fixed record support?",
                "documentary_boundary": "One graph-selected canonical record.",
                "source_entity_ids": ["HOC-000000001"],
            }
        ),
        encoding="utf-8",
    )
    reasoner = tmp_path / "reasoner.py"
    reasoner.write_text(
        """import json, sys
request = json.load(sys.stdin)
print(json.dumps({
    "run_id": request["run_id"],
    "state": request["state"],
    "completed": True,
    "summary": "Completed over graph-selected, Git-verified evidence.",
    "candidate_statements": [{
        "candidate_id": f"CAND-GRAPH-{request['phase_number']:02d}",
        "text": "Bounded candidate.",
        "epistemic_classification": "SUPPORTED_INFERENCE",
        "evidence_record_ids": ["HOC-000000001"],
    }],
}))
""",
        encoding="utf-8",
    )
    output = tmp_path / "RUN-GRAPH-FIELD"
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
            "--projection-git-commit",
            MANIFEST_COMMIT,
            "--projection-manifest",
            "projections/PRJ-FIELD.json",
            "--projection-manifest-schema",
            "inquiry_engine/src/custos_engine/schemas/projection_manifest.schema.json",
            "--neo4j-uri",
            "neo4j://example.invalid",
            "--neo4j-username",
            "neo4j",
            "--question",
            str(question),
            "--output",
            str(output),
            "--reasoner-command",
            f"{sys.executable} {reasoner}",
        ]
    )

    assert args.handler(args) == 0

    receipt = json.loads(
        (output / "graph_retrieval_receipt.json").read_text(encoding="utf-8")
    )
    records = json.loads(
        (output / "phase_reasoning_records.json").read_text(encoding="utf-8")
    )
    assert receipt["requested_canonical_ids"] == ["HOC-000000001"]
    assert receipt["retrieved_items"][0]["source_role"] == "REPOSITORY_CONTEXT"
    assert records[0]["request"]["documentary_inputs"][0]["text"] == source_text
    assert records[0]["request"]["documentary_inputs"][0][
        "source_fixity_sha256"
    ] == source_digest
