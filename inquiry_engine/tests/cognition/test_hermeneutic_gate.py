import pytest

from custos_engine.cognition.hermeneutic_gate import (
    HermeneuticGateContext,
    evaluate_inner_sanctum_gate,
    require_inner_sanctum_access,
)
from custos_engine.models.base import InquiryState


def _context(**changes) -> HermeneuticGateContext:
    values = {
        "procedure_id": "IAR-000000001",
        "taxonomy_id": "HOC-000000001",
        "cognitive_memory_manifest_id": "MAN-000000001",
        "current_state": InquiryState.ADVERSARIAL_TESTING,
        "completed_phase_numbers": list(range(1, 8)),
        "documentary_difficulty_identified": True,
        "historical_admissibility_established": True,
        "authorial_authorization_established": True,
        "ordinary_explanations_considered": True,
        "evidence_record_ids": ["EVR-000000001"],
    }
    values.update(changes)
    return HermeneuticGateContext(**values)


def test_outer_process_opens_inner_sanctum_only_after_phase_seven():
    decision = evaluate_inner_sanctum_gate(_context())

    assert decision.authorized is True
    assert "does not establish concealment" in decision.epistemic_limit


@pytest.mark.parametrize(
    ("changes", "expected_reason"),
    [
        (
            {"current_state": InquiryState.DOCUMENTARY_INTAKE},
            "not reached an Outer-Process state",
        ),
        (
            {"completed_phase_numbers": [1, 2, 3, 4, 5, 6]},
            "phases 1 through 7",
        ),
        (
            {"documentary_difficulty_identified": False},
            "No genuine documentary difficulty",
        ),
        (
            {"historical_admissibility_established": False},
            "Historical admissibility",
        ),
        (
            {"authorial_authorization_established": False},
            "Authorial authorization",
        ),
        (
            {"ordinary_explanations_considered": False},
            "Ordinary explanations",
        ),
        ({"evidence_record_ids": []}, "No auditable evidence record"),
    ],
)
def test_missing_outer_process_requirement_closes_gate(changes, expected_reason):
    decision = evaluate_inner_sanctum_gate(_context(**changes))

    assert decision.authorized is False
    assert any(expected_reason in reason for reason in decision.reasons)
    with pytest.raises(PermissionError, match="IAR-000000001"):
        require_inner_sanctum_access(_context(**changes))


def test_noncanonical_pair_cannot_open_gate():
    decision = evaluate_inner_sanctum_gate(
        _context(procedure_id="IAR-999999999", taxonomy_id="HOC-999999999")
    )

    assert decision.authorized is False
    assert len(decision.reasons) == 2
