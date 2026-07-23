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
        "cognitive_memory_manifest_id": "MAN-000000002",
        "current_state": InquiryState.DOCUMENTARY_INTAKE,
    }
    values.update(changes)
    return HermeneuticGateContext(**values)


def test_inner_sanctum_is_open_at_documentary_intake():
    decision = evaluate_inner_sanctum_gate(_context())
    assert decision.authorized is True
    assert any("open from documentary intake" in reason for reason in decision.reasons)
    assert "does not establish that any literary mechanism is present" in decision.epistemic_limit
    require_inner_sanctum_access(_context())


@pytest.mark.parametrize(
    "changes",
    [
        {"completed_phase_numbers": []},
        {"documentary_difficulty_identified": False},
        {"historical_admissibility_established": False},
        {"authorial_authorization_established": False},
        {"ordinary_explanations_considered": False},
        {"evidence_record_ids": []},
        {"current_state": InquiryState.HORIZON_AUDIT},
        {"current_state": InquiryState.SYNTHESIS_LIMITATION},
    ],
)
def test_procedural_thresholds_do_not_close_the_inner_sanctum(changes):
    assert evaluate_inner_sanctum_gate(_context(**changes)).authorized is True


@pytest.mark.parametrize(
    ("changes", "expected_reason"),
    [
        ({"cognitive_memory_manifest_id": "MAN-999999999"}, "released Cognitive Memory Manifest"),
        ({"procedure_id": "IAR-999999999"}, "IAR-000000001"),
        ({"taxonomy_id": "HOC-999999999"}, "HOC-000000001"),
    ],
)
def test_invalid_canonical_binding_fails_initialization(changes, expected_reason):
    decision = evaluate_inner_sanctum_gate(_context(**changes))
    assert decision.authorized is False
    assert any(expected_reason in reason for reason in decision.reasons)
    with pytest.raises(PermissionError, match="initialization failed"):
        require_inner_sanctum_access(_context(**changes))


def test_predecessor_manifest_remains_readable_under_versioned_runtime():
    assert evaluate_inner_sanctum_gate(
        _context(cognitive_memory_manifest_id="MAN-000000001")
    ).authorized
