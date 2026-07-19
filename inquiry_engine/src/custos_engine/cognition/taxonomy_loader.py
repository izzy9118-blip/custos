from __future__ import annotations

import json
from pathlib import Path

import yaml

from custos_engine.models.taxonomy import TaxonomyComponent
from custos_engine.repository.validators import validate_against_schema


def load_taxonomy_components(
    source_path: Path,
    schema_path: Path,
) -> list[TaxonomyComponent]:
    text = source_path.read_text(encoding="utf-8")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if source_path.suffix.lower() == ".json":
        raw = json.loads(text)
    elif source_path.suffix.lower() in {".yaml", ".yml"}:
        raw = yaml.safe_load(text)
    else:
        raise ValueError("Taxonomy source must be JSON or YAML")

    if not isinstance(raw, list):
        raise ValueError("Taxonomy source must contain an array of components")

    components: list[TaxonomyComponent] = []
    for item in raw:
        validate_against_schema(item, schema)
        components.append(TaxonomyComponent.model_validate(item))
    return sorted(components, key=lambda component: component.component_id)
