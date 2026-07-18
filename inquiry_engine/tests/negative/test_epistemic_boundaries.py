import pytest
from pydantic import ValidationError

from custos_engine.models.base import CanonicalReference, EpistemicClassification
from custos_engine.models.evidence import EvidenceRecord
from custos_engine.models.hypothesis import Hypothesis


def ref(identifier: str, klass: str):
    return CanonicalReference(canonical_id=identifier, canonical_class=klass)


def test_derived_evidence_cannot_be_documented_finding():
    with pytest.raises(ValidationError):
        EvidenceRecord(
            evidence_record_id="EVR-1",
            evidence_bearing_entity=ref("PSG-000000001", "Passage"),
            target_entity=ref("INT-000000001", "Interpretation"),
            relevance_statement="Derived relation.",
            direct_or_derived="DERIVED",
            epistemic_classification=EpistemicClassification.DOCUMENTED_FINDING,
            provenance_ids=["PRO-1"],
        )


def test_hypothesis_cannot_be_promoted_by_field_change():
    hypothesis = Hypothesis(
        hypothesis_id="HYP-1",
        proposition="Provisional proposition.",
        historical_admissibility_note="Historically possible.",
        scope="Bounded passage.",
    )
    with pytest.raises(ValidationError):
        hypothesis.epistemic_classification = (
            EpistemicClassification.DOCUMENTED_FINDING
        )
