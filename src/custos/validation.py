from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib

from .config import load_config, load_yaml


class ValidationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_inquiry(root: Path, inquiries_root: str, inquiry: Path | str) -> Path:
    candidate = Path(inquiry)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    allowed_root = (root / inquiries_root).resolve()
    if candidate != allowed_root and allowed_root not in candidate.parents:
        raise ValidationError(f"Inquiry must be inside {inquiries_root}: {candidate}")
    return candidate


def validate_inquiry(root: Path, inquiry: Path | str) -> dict[str, Any]:
    config = load_config(root)
    inquiry_dir = _resolve_inquiry(root, config["inquiries_root"], inquiry)
    if not inquiry_dir.is_dir():
        raise ValidationError(f"Inquiry directory does not exist: {inquiry_dir}")
    for name in ("inquiry.md", "evidence.yaml", "status.yaml"):
        if not (inquiry_dir / name).is_file():
            raise ValidationError(f"Inquiry is missing {name}: {inquiry_dir}")

    evidence = load_yaml(inquiry_dir / "evidence.yaml")
    checked: list[dict[str, str]] = []
    for item in evidence.get("evidence", []):
        if not isinstance(item, dict) or not all(k in item for k in ("id", "path", "sha256")):
            raise ValidationError(f"Malformed evidence entry in {inquiry_dir / 'evidence.yaml'}")
        path = root / item["path"]
        if not path.is_file():
            raise ValidationError(f"Missing evidence file: {item['path']}")
        actual = sha256_file(path)
        if actual != item["sha256"]:
            raise ValidationError(f"Evidence hash mismatch: {item['path']}")
        checked.append({"id": item["id"], "path": item["path"], "sha256": actual})

    return {
        "path": str(inquiry_dir.relative_to(root)),
        "evidence": checked,
        "status": load_yaml(inquiry_dir / "status.yaml"),
    }


def validate_repository(root: Path, inquiry: Path | str | None = None) -> dict[str, Any]:
    config = load_config(root)
    file_paths = [
        config["instructions"],
        config["reading_protocol"],
        config["literary_techniques"],
    ]
    for relative in file_paths:
        if not (root / relative).is_file():
            raise ValidationError(f"Missing configured file: {relative}")
    for key in ("inquiries_root", "sources_root"):
        relative = config[key]
        if not (root / relative).is_dir():
            raise ValidationError(f"Missing configured directory: {relative}")
    runs_path = root / config["runs_root"]
    if runs_path.exists() and not runs_path.is_dir():
        raise ValidationError(f"Configured runs root is not a directory: {config['runs_root']}")

    protocol = load_yaml(root / config["reading_protocol"])
    stages = protocol.get("stages")
    if not isinstance(stages, list) or [stage.get("id") for stage in stages] != [1, 2, 3, 4, 5]:
        raise ValidationError("Reading protocol must contain exactly stages 1 through 5")
    if protocol.get("literary_attention", {}).get("always_open") is not True:
        raise ValidationError("Literary attention must be always open")

    taxonomy = load_yaml(root / config["literary_techniques"])
    techniques = taxonomy.get("techniques")
    expected = [f"LC-{i:03d}" for i in range(1, 23)]
    if not isinstance(techniques, list) or [item.get("id") for item in techniques] != expected:
        raise ValidationError(
            "Literary inventory must contain LC-001 through LC-022 exactly once and in order"
        )

    result: dict[str, Any] = {
        "valid": True,
        "stages": 5,
        "techniques": 22,
        "roots": {
            "inquiries": config["inquiries_root"],
            "sources": config["sources_root"],
            "runs": config["runs_root"],
        },
    }
    if inquiry is not None:
        result["inquiry"] = validate_inquiry(root, inquiry)
    return result
