from __future__ import annotations

from typing import Any, Mapping

from jsonschema import Draft202012Validator


class SchemaValidationError(ValueError):
    pass


def validate_against_schema(instance: Any, schema: Mapping[str, Any]) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        raise SchemaValidationError(f"Invalid JSON schema: {exc}") from exc

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if not errors:
        return

    messages: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.path) or "<root>"
        messages.append(f"{location}: {error.message}")
    raise SchemaValidationError("; ".join(messages))
