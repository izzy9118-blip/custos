from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Iterator

import yaml

from custos_engine.repository.github_reader import LocalGitReader

from .projector import ProjectionEdge, ProjectionNode, ProjectionPlan


DEFAULT_PROJECTION_PREFIXES = (
    "amendments",
    "governance",
    "ledgers/identifier-assignment-ledger/assignments",
    "manifests",
    "records",
    "registers",
)

_IDENTIFIER_KEYS = ("canonical_id", "identifier", "id", "manifest_id")
_CLASS_KEYS = ("canonical_class", "class", "assigned_class")
_CANONICAL_IDENTIFIER = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]{3,9}[a-z]?$")
_RELATIONSHIP_BY_FIELD = {
    "dependencies": "DEPENDS_ON",
    "dependency_graph": "DEPENDS_ON",
    "governing_specification_ids": "GOVERNED_BY",
    "governing_references": "GOVERNED_BY",
    "certification_record_id": "CERTIFIED_BY",
    "certification_record_identifier": "CERTIFIED_BY",
    "integration_decision_id": "INTEGRATED_BY",
    "integration_decision_identifier": "INTEGRATED_BY",
    "admission_decision_id": "ADMITTED_BY",
    "decision_id": "DECIDED_BY",
    "source_decision_id": "ASSIGNED_BY",
    "validation_record_id": "VALIDATED_BY",
    "validation_record_ids": "VALIDATED_BY",
    "validation_record_identifiers": "VALIDATED_BY",
    "authority_id": "RESPONSIBLE_AUTHORITY",
    "responsible_authority_id": "RESPONSIBLE_AUTHORITY",
}


class ProjectionBuildError(ValueError):
    pass


@dataclass(frozen=True)
class _SourceRecord:
    canonical_id: str
    canonical_class: str
    path: str
    text: str
    data: dict[str, Any]


def _raw_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _root_string(data: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _load_mapping(path: str, text: str) -> dict[str, Any] | None:
    try:
        if path.endswith(".json"):
            value = json.loads(text)
        else:
            value = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ProjectionBuildError(f"Unable to parse projection source {path}: {exc}") from exc
    return value if isinstance(value, dict) else None


def _path_priority(path: str) -> tuple[int, str]:
    if path.startswith("records/"):
        return (0, path)
    if "/objects/" in path:
        return (1, path)
    if path.startswith("registers/"):
        return (2, path)
    if path.startswith("manifests/"):
        return (3, path)
    if path.startswith("amendments/"):
        return (4, path)
    if path.startswith("governance/"):
        return (5, path)
    return (9, path)


def _safe_label(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", " ", value).strip()
    label = "".join(part[:1].upper() + part[1:] for part in normalized.split())
    return label or "CanonicalEntity"


def _iter_references(value: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _iter_references(child, (*path, str(key)))
    elif isinstance(value, list):
        for child in value:
            yield from _iter_references(child, path)
    elif isinstance(value, str) and _CANONICAL_IDENTIFIER.fullmatch(value):
        yield (value, ".".join(path))


def _relationship_type(field_path: str) -> str:
    leaf = field_path.rsplit(".", 1)[-1]
    return _RELATIONSHIP_BY_FIELD.get(leaf, "REFERENCES")


class RepositoryProjectionBuilder:
    """Compile assigned canonical repository records into a derived graph plan."""

    def __init__(
        self,
        reader: LocalGitReader,
        prefixes: tuple[str, ...] = DEFAULT_PROJECTION_PREFIXES,
    ) -> None:
        if not prefixes:
            raise ProjectionBuildError("At least one projection prefix is required")
        self.reader = reader
        self.prefixes = tuple(dict.fromkeys(prefixes))

    def _assigned_identifiers(self) -> set[str]:
        prefix = "ledgers/identifier-assignment-ledger/assignments"
        assigned: set[str] = set()
        for path in self.reader.list_files(prefix):
            if not path.endswith((".yaml", ".yml", ".json")):
                continue
            data = _load_mapping(path, self.reader.read_text(path))
            if not data or data.get("assignment_status") != "ASSIGNED":
                continue
            identifier = _root_string(data, _IDENTIFIER_KEYS)
            if identifier and _CANONICAL_IDENTIFIER.fullmatch(identifier):
                assigned.add(identifier)
        if not assigned:
            raise ProjectionBuildError("No assigned canonical identifiers were found")
        return assigned

    def _source_records(self, assigned: set[str]) -> dict[str, _SourceRecord]:
        candidates: dict[str, list[_SourceRecord]] = {}
        paths: set[str] = set()
        for prefix in self.prefixes:
            paths.update(self.reader.list_files(prefix))

        for path in sorted(paths):
            if PurePosixPath(path).suffix.lower() not in {".json", ".yaml", ".yml"}:
                continue
            text = self.reader.read_text(path)
            data = _load_mapping(path, text)
            if not data:
                continue
            canonical_id = _root_string(data, _IDENTIFIER_KEYS)
            if canonical_id not in assigned:
                continue
            canonical_class = _root_string(data, _CLASS_KEYS)
            if canonical_class is None:
                canonical_class = str(data.get("register_type") or data.get("family") or "Canonical Entity")
            candidates.setdefault(canonical_id, []).append(
                _SourceRecord(canonical_id, canonical_class, path, text, data)
            )

        return {
            canonical_id: sorted(records, key=lambda item: _path_priority(item.path))[0]
            for canonical_id, records in candidates.items()
        }

    def build(self, cognitive_memory_manifest_id: str) -> ProjectionPlan:
        assigned = self._assigned_identifiers()
        sources = self._source_records(assigned)
        if not sources:
            raise ProjectionBuildError("No canonical source records were projectable")

        nodes: list[ProjectionNode] = []
        for source in sources.values():
            title = source.data.get("title")
            source_role = source.data.get("source_role", "REPOSITORY_CONTEXT")
            if source_role not in {"PRIMARY", "SECONDARY", "REPOSITORY_CONTEXT"}:
                raise ProjectionBuildError(
                    f"Invalid source_role in canonical record {source.path}: {source_role}"
                )
            properties: dict[str, object] = {
                "projection_source": "GIT_CANONICAL_RECORD",
                "github_path": source.path,
                "git_commit": self.reader.resolved_commit,
                "cognitive_memory_manifest_id": cognitive_memory_manifest_id,
                "source_fixity_sha256": _raw_sha256(source.text),
                "source_role": source_role,
            }
            if isinstance(title, str) and title.strip():
                properties["title"] = title.strip()
            version = source.data.get("version")
            if isinstance(version, (str, int, float)):
                properties["version"] = str(version)
            nodes.append(
                ProjectionNode(
                    canonical_id=source.canonical_id,
                    canonical_class=source.canonical_class,
                    labels=["CanonicalEntity", _safe_label(source.canonical_class)],
                    properties=properties,
                )
            )

        node_ids = set(sources)
        edges: list[ProjectionEdge] = []
        seen_edges: set[str] = set()
        for source in sources.values():
            for target_id, field_path in _iter_references(source.data):
                if target_id == source.canonical_id or target_id not in node_ids:
                    continue
                relationship_type = _relationship_type(field_path)
                material = f"{source.canonical_id}\0{relationship_type}\0{target_id}\0{field_path}"
                edge_key = hashlib.sha256(material.encode("utf-8")).hexdigest()
                if edge_key in seen_edges:
                    continue
                seen_edges.add(edge_key)
                edges.append(
                    ProjectionEdge(
                        edge_key=edge_key,
                        subject_id=source.canonical_id,
                        relationship_type=relationship_type,
                        object_id=target_id,
                        derivative=True,
                        properties={"source_field": field_path},
                    )
                )

        return ProjectionPlan(
            git_commit=self.reader.resolved_commit,
            cognitive_memory_manifest_id=cognitive_memory_manifest_id,
            source_file_count=len({source.path for source in sources.values()}),
            nodes=nodes,
            edges=edges,
        ).deterministic()
