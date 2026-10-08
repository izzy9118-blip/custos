from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

import pytest

from custos.reader_context import build_reader_context
from custos.runner import build_reader_request


ROOT = Path(__file__).resolve().parents[1]


def test_activation_loads_full_current_authority_without_an_inquiry():
    context = build_reader_context(ROOT)
    assert context["contract"] == "custos.reader-context.v1"
    assert context["repository"] == "izzy9118-blip/custos"
    assert context["instructions"] == (ROOT / "CUSTOS.md").read_text(encoding="utf-8")
    assert len(context["gates"]["outer"]["protocol"]["stages"]) == 5
    assert len(context["gates"]["inner"]["taxonomy"]["techniques"]) == 22
    assert "input" not in context
    assert context["activation_status"] == "READER_CONTEXT_LOADED_NOT_ANALYSIS"
    assert len(context["authority_documents"]) == 4
    for document in context["authority_documents"]:
        raw = (ROOT / document["path"]).read_bytes()
        assert document["text"] == raw.decode("utf-8")
        assert document["sha256"] == hashlib.sha256(raw).hexdigest()


@pytest.mark.parametrize("mode", ["close", "sweep"])
def test_external_reasoner_gets_governing_instructions_in_each_mode(tmp_path, mode):
    source = tmp_path / "witness.txt"
    source.write_text("An explicit witness.", encoding="utf-8")
    context = build_reader_context(ROOT)
    request = build_reader_request(ROOT, mode=mode, source=source)
    assert request["instructions"] == context["instructions"]
    assert request["authority_documents"] == context["authority_documents"]
    assert request["gates"] == context["gates"]


def test_context_cli_is_usable_from_an_external_working_directory(tmp_path):
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    result = subprocess.run(
        [sys.executable, "-m", "custos.cli", "--repo-root", str(ROOT), "context"],
        cwd=tmp_path, env=env, capture_output=True, text=True, check=True,
    )
    assert json.loads(result.stdout)["instructions"] == (ROOT / "CUSTOS.md").read_text()
    assert list(tmp_path.iterdir()) == []
