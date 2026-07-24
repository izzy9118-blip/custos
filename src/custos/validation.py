from __future__ import annotations
from pathlib import Path
from typing import Any
import hashlib
from .config import load_config, load_yaml

class ValidationError(ValueError):
    pass

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_repository(root: Path) -> dict[str, Any]:
    config = load_config(root)
    required_paths = [config["instructions"], config["reading_protocol"], config["literary_techniques"], config["active_inquiry"]]
    for relative in required_paths:
        if not (root / relative).exists():
            raise ValidationError(f"Missing configured path: {relative}")
    inquiry_dir = root / config["active_inquiry"]
    for name in ("inquiry.md", "evidence.yaml", "status.yaml"):
        if not (inquiry_dir / name).is_file():
            raise ValidationError(f"Active inquiry is missing {name}")
    protocol = load_yaml(root / config["reading_protocol"])
    stages = protocol.get("stages")
    if not isinstance(stages, list) or [stage.get("id") for stage in stages] != [1,2,3,4,5]:
        raise ValidationError("Reading protocol must contain exactly stages 1 through 5")
    if protocol.get("literary_attention", {}).get("always_open") is not True:
        raise ValidationError("Literary attention must be always open")
    taxonomy = load_yaml(root / config["literary_techniques"])
    techniques = taxonomy.get("techniques")
    expected = [f"LC-{i:03d}" for i in range(1,23)]
    if not isinstance(techniques, list) or [item.get("id") for item in techniques] != expected:
        raise ValidationError("Literary inventory must contain LC-001 through LC-022 exactly once and in order")
    evidence = load_yaml(inquiry_dir / "evidence.yaml")
    checked=[]
    for item in evidence.get("evidence", []):
        path=root / item["path"]
        if not path.is_file():
            raise ValidationError(f"Missing evidence file: {item['path']}")
        actual=sha256_file(path)
        if actual != item["sha256"]:
            raise ValidationError(f"Evidence hash mismatch: {item['path']}")
        checked.append({"id":item["id"],"path":item["path"],"sha256":actual})
    return {"valid":True,"active_inquiry":config["active_inquiry"],"stages":5,"techniques":22,"evidence":checked}
