import pytest

from custos_engine.config.authority import Action, AuthorityPolicy, Role


def test_engine_can_create_candidate_but_not_certify():
    policy = AuthorityPolicy()
    assert policy.allows(Role.ENGINE, Action.CREATE_CANDIDATE)
    assert not policy.allows(Role.ENGINE, Action.CERTIFY)
    with pytest.raises(PermissionError):
        policy.require(Role.ENGINE, Action.CERTIFY)
