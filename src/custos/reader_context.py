"""Expose the active Reader authority to callers outside the Custos checkout."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import subprocess

from .config import load_config, load_yaml
from .validation import validate_repository


CONTEXT_CONTRACT = "custos.reader-context.v1"
REPOSITORY = "izzy9118-blip/custos"


def git_head(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "UNAVAILABLE"


def build_reader_context(root: Path) -> dict[str, Any]:
    """Load current instructions and both gates without selecting an inquiry.

    Full wording and byte hashes travel with the context. A filename in a different
    repository is insufficient to convey governing instructions to a reasoner.
    """
    root = root.resolve()
    validation = validate_repository(root)
    config = load_config(root)
    documents = []
    for key, relative in (
        ("configuration", "custos.yaml"),
        ("instructions", config["instructions"]),
        ("reading_protocol", config["reading_protocol"]),
        ("literary_techniques", config["literary_techniques"]),
    ):
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"Reader authority path escapes Custos: {relative}")
        raw = path.read_bytes()
        documents.append({
            "role": key,
            "path": relative,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "text": raw.decode("utf-8"),
        })
    instructions = next(item["text"] for item in documents if item["role"] == "instructions")
    return {
        "contract": CONTEXT_CONTRACT,
        "repository": REPOSITORY,
        "repository_commit": git_head(root),
        "instructions_path": config["instructions"],
        "instructions": instructions,
        "authority_documents": documents,
        "configuration": config,
        "reader_modes": ["close", "sweep"],
        "gates": {
            "outer": {
                "name": "documentary inquiry sequence",
                "source": config["reading_protocol"],
                "protocol": load_yaml(root / config["reading_protocol"]),
            },
            "inner": {
                "name": "literary-technique discernment",
                "source": config["literary_techniques"],
                "taxonomy": load_yaml(root / config["literary_techniques"]),
                "rule": "Availability is not presence; evidence alone activates a technique evaluation.",
            },
        },
        "validation": validation,
        "activation_status": "READER_CONTEXT_LOADED_NOT_ANALYSIS",
    }
