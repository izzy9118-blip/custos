from __future__ import annotations

from pydantic import Field

from .base import CanonicalReference, StrictModel


class TaxonomyComponent(StrictModel):
    component_id: str = Field(pattern=r"^LC-[0-9]{3}$")
    name: str = Field(min_length=1)
    source: CanonicalReference
    strauss_formulation: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    documentary_function: str = Field(min_length=1)
    investigative_requirement: str = Field(min_length=1)
    examples: list[str] = Field(default_factory=list)
    reconstruction_status: str = Field(min_length=1)
    related_technique_ids: list[str] = Field(default_factory=list)
    distinguished_from: list[str] = Field(default_factory=list)
    minimum_trigger_features: list[str] = Field(min_length=1)
    required_corroboration_features: list[str] = Field(default_factory=list)
    ordinary_alternatives: list[str] = Field(min_length=1)
    disqualifying_conditions: list[str] = Field(default_factory=list)
    authorized_engine_action: str = Field(min_length=1)
    prohibited_inferences: list[str] = Field(min_length=1)
    uncertainty_note: str = Field(min_length=1)


class TaxonomyEvaluation(StrictModel):
    component_id: str
    triggered: bool
    minimum_trigger_satisfied: bool
    corroboration_count: int = Field(ge=0)
    disqualifier_present: bool
    matched_features: list[str] = Field(default_factory=list)
    missing_features: list[str] = Field(default_factory=list)
    matched_disqualifiers: list[str] = Field(default_factory=list)
    authorized_action: str | None = None
    conclusion: str
