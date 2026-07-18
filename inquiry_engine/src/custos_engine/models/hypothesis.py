from __future__ import annotations

from pydantic import Field, model_validator

from .base import EpistemicClassification, StrictModel


class Hypothesis(StrictModel):
    hypothesis_id: str
    canonical_class: str = "Hypothesis"
    proposition: str = Field(min_length=1)
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    contrary_evidence_ids: list[str] = Field(default_factory=list)
    rival_hypothesis_ids: list[str] = Field(default_factory=list)
    historical_admissibility_note: str = Field(min_length=1)
    epistemic_classification: EpistemicClassification = (
        EpistemicClassification.WORKING_HYPOTHESIS
    )
    scope: str = Field(min_length=1)
    unresolved_requirements: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def must_remain_hypothesis(self) -> "Hypothesis":
        if self.epistemic_classification != EpistemicClassification.WORKING_HYPOTHESIS:
            raise ValueError("Hypothesis must be classified WORKING_HYPOTHESIS")
        return self
