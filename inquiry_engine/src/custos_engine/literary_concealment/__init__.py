"""Development-only executable projections of literary-concealment techniques.

LC-001 through LC-022 are repository-integrated here without granting
canonical admission, certification, Cognitive Memory integration, or
production authority.
"""

from .registry import (
    SUPPORTED_COMPONENT_IDS,
    ComponentRuntime,
    evaluate_component,
    get_component_runtime,
    load_component_schema,
    load_technique,
)

__all__ = [
    "SUPPORTED_COMPONENT_IDS",
    "ComponentRuntime",
    "evaluate_component",
    "get_component_runtime",
    "load_component_schema",
    "load_technique",
]
