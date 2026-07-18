from __future__ import annotations

import json
from typing import Any

import yaml

from .github_reader import LocalGitReader


class ArtifactLoadError(ValueError):
    pass


class ArtifactLoader:
    def __init__(self, reader: LocalGitReader) -> None:
        self.reader = reader

    def load_text(self, repository_path: str) -> str:
        return self.reader.read_text(repository_path)

    def load_structured(self, repository_path: str) -> dict[str, Any] | list[Any]:
        text = self.reader.read_text(repository_path)
        suffix = repository_path.lower().rsplit(".", 1)[-1]
        try:
            if suffix == "json":
                value = json.loads(text)
            elif suffix in {"yaml", "yml"}:
                value = yaml.safe_load(text)
            else:
                raise ArtifactLoadError(
                    f"Unsupported structured artifact: {repository_path}"
                )
        except (json.JSONDecodeError, yaml.YAMLError) as exc:
            raise ArtifactLoadError(
                f"Unable to parse {repository_path}: {exc}"
            ) from exc

        if not isinstance(value, (dict, list)):
            raise ArtifactLoadError(
                f"Structured artifact must contain an object or array: {repository_path}"
            )
        return value
