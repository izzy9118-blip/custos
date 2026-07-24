from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

class ConfigError(ValueError):
    pass

def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "custos.yaml").is_file():
            return candidate
    raise ConfigError("Could not locate custos.yaml in this directory or its parents")

def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ConfigError(f"Expected a YAML mapping: {path}")
    return value

def load_config(root: Path) -> dict[str, Any]:
    config = load_yaml(root / "custos.yaml")
    required = {"instructions", "reading_protocol", "literary_techniques", "active_inquiry", "sources_root", "runs_root"}
    missing = sorted(required.difference(config))
    if missing:
        raise ConfigError("custos.yaml is missing: " + ", ".join(missing))
    return config
