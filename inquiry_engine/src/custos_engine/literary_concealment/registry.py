from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import import_module
from importlib.resources import files
from typing import Any, Callable, Mapping

from pydantic import BaseModel


SUPPORTED_COMPONENT_IDS = tuple(f"LC-{number:03d}" for number in range(1, 23))


@dataclass(frozen=True)
class ComponentRuntime:
    """The isolated runtime contract for one development-only LC component."""

    component_id: str
    module_name: str
    technique_model: type[BaseModel]
    input_model: type[BaseModel]
    result_model: type[BaseModel]
    evaluator: Callable[[BaseModel], BaseModel]


def _normalize_component_id(component_id: str) -> str:
    normalized = component_id.strip().upper()
    if normalized not in SUPPORTED_COMPONENT_IDS:
        raise KeyError(
            f"Unsupported Literary Concealment component {component_id!r}; "
            f"expected one of {SUPPORTED_COMPONENT_IDS[0]} through "
            f"{SUPPORTED_COMPONENT_IDS[-1]}"
        )
    return normalized


def _module_name(component_id: str) -> str:
    digits = component_id.removeprefix("LC-")
    return f"custos_engine.literary_concealment.lc{digits}"


def get_component_runtime(component_id: str) -> ComponentRuntime:
    """Resolve one LC component without importing neighboring implementations."""

    normalized = _normalize_component_id(component_id)
    digits = normalized.removeprefix("LC-")
    module_name = _module_name(normalized)
    module = import_module(module_name)

    return ComponentRuntime(
        component_id=normalized,
        module_name=module_name,
        technique_model=getattr(module, "LiteraryConcealmentTechnique"),
        input_model=getattr(module, f"LC{digits}EvaluationInput"),
        result_model=getattr(module, f"LC{digits}EvaluationResult"),
        evaluator=getattr(module, f"evaluate_lc{digits}"),
    )


def _resource_text(component_id: str, directory: str, filename: str) -> str:
    module_name = _module_name(component_id)
    return files(module_name).joinpath(directory, filename).read_text(encoding="utf-8")


def load_technique(component_id: str) -> BaseModel:
    """Load and validate one repository-integrated technique projection."""

    normalized = _normalize_component_id(component_id)
    runtime = get_component_runtime(normalized)
    payload = json.loads(
        _resource_text(normalized, "techniques", f"{normalized}.json")
    )
    technique = runtime.technique_model.model_validate(payload)
    if getattr(technique, "technique_key", None) != normalized:
        raise ValueError(
            f"Technique resource identity mismatch for {normalized}: "
            f"{getattr(technique, 'technique_key', None)!r}"
        )
    return technique


def load_component_schema(component_id: str) -> dict[str, Any]:
    """Load the component-specific JSON Schema preserved with one LC package."""

    normalized = _normalize_component_id(component_id)
    schema = json.loads(
        _resource_text(
            normalized,
            "schemas",
            "literary_concealment_technique.schema.json",
        )
    )
    if not isinstance(schema, dict):
        raise ValueError(f"Schema for {normalized} must be a JSON object")
    return schema


def evaluate_component(
    component_id: str,
    candidate: BaseModel | Mapping[str, Any],
) -> BaseModel:
    """Validate and evaluate a structured candidate through its own LC runtime.

    This dispatcher performs no semantic extraction from raw prose and grants
    no authority beyond the development-only result defined by the component.
    """

    runtime = get_component_runtime(component_id)
    validated = (
        candidate
        if isinstance(candidate, runtime.input_model)
        else runtime.input_model.model_validate(candidate)
    )
    result = runtime.evaluator(validated)
    if not isinstance(result, runtime.result_model):
        raise TypeError(
            f"Evaluator for {runtime.component_id} returned "
            f"{type(result).__name__}, expected {runtime.result_model.__name__}"
        )
    return result
