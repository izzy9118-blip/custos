"""Cognition-layer access to repository-integrated LC development runtimes."""

from typing import Any, Mapping

from pydantic import BaseModel

from custos_engine.literary_concealment import (
    SUPPORTED_COMPONENT_IDS,
    evaluate_component as evaluate_technical_component,
    get_component_runtime,
    load_component_schema,
    load_technique,
)

from .hermeneutic_gate import HermeneuticGateContext, require_inner_sanctum_access


def evaluate_component(
    component_id: str,
    candidate: BaseModel | Mapping[str, Any],
    *,
    gate_context: HermeneuticGateContext,
) -> BaseModel:
    """Evaluate one LC component only after the Outer Process opens the gate.

    The lower-level literary_concealment package remains a technically certified
    implementation surface. Production cognition enters it only through this
    gate-enforcing cognition-layer function.
    """

    require_inner_sanctum_access(gate_context)
    return evaluate_technical_component(component_id, candidate)

__all__ = [
    "SUPPORTED_COMPONENT_IDS",
    "evaluate_component",
    "evaluate_technical_component",
    "get_component_runtime",
    "load_component_schema",
    "load_technique",
]
