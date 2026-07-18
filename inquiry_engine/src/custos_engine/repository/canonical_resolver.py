from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .artifact_loader import ArtifactLoader


class ResolutionEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_class: str
    repository_path: str
    version: str | None = None


class CanonicalResolver:
    """Resolve identifiers through a declared canonical index artifact."""

    def __init__(self, loader: ArtifactLoader, index_path: str) -> None:
        data = loader.load_structured(index_path)
        if not isinstance(data, dict) or "entries" not in data:
            raise ValueError("Canonical index must contain an entries object")
        raw_entries = data["entries"]
        if not isinstance(raw_entries, dict):
            raise ValueError("Canonical index entries must be an object")
        self._entries = {
            canonical_id: ResolutionEntry.model_validate(
                {"canonical_id": canonical_id, **entry}
            )
            for canonical_id, entry in raw_entries.items()
        }

    def resolve(self, canonical_id: str) -> ResolutionEntry:
        try:
            return self._entries[canonical_id]
        except KeyError as exc:
            raise KeyError(f"Canonical identifier does not resolve: {canonical_id}") from exc
