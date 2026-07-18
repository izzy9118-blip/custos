from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def verify_edge_endpoints(node_ids: set[str], edges: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for edge in edges:
        if edge["subject_id"] not in node_ids:
            errors.append(f"Missing subject node: {edge['subject_id']}")
        if edge["object_id"] not in node_ids:
            errors.append(f"Missing object node: {edge['object_id']}")
    return errors
