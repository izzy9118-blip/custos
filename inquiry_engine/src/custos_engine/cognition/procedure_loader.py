from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_procedure(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        value = json.loads(text)
    elif path.suffix.lower() in {".yaml", ".yml"}:
        value = yaml.safe_load(text)
    else:
        raise ValueError("Procedure must be JSON or YAML")
    if not isinstance(value, dict):
        raise ValueError("Procedure must be an object")
    return value
