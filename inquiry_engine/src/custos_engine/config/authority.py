from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Role(StrEnum):
    ENGINE = "ENGINE"
    INVESTIGATOR = "INVESTIGATOR"
    SECRETARY = "SECRETARY"
    VALIDATOR = "VALIDATOR"
    CERTIFIER = "CERTIFIER"
    RESPONSIBLE_AUTHORITY = "RESPONSIBLE_AUTHORITY"


class Action(StrEnum):
    READ_CANONICAL = "READ_CANONICAL"
    TRAVERSE_GRAPH = "TRAVERSE_GRAPH"
    CREATE_CANDIDATE = "CREATE_CANDIDATE"
    VALIDATE = "VALIDATE"
    PRESERVE_APPROVED = "PRESERVE_APPROVED"
    CERTIFY = "CERTIFY"
    ADMIT = "ADMIT"
    INTEGRATE_COGNITION = "INTEGRATE_COGNITION"


DEFAULT_PERMISSIONS: dict[Role, frozenset[Action]] = {
    Role.ENGINE: frozenset(
        {
            Action.READ_CANONICAL,
            Action.TRAVERSE_GRAPH,
            Action.CREATE_CANDIDATE,
        }
    ),
    Role.INVESTIGATOR: frozenset(
        {
            Action.READ_CANONICAL,
            Action.TRAVERSE_GRAPH,
            Action.CREATE_CANDIDATE,
        }
    ),
    Role.SECRETARY: frozenset(
        {
            Action.READ_CANONICAL,
            Action.PRESERVE_APPROVED,
        }
    ),
    Role.VALIDATOR: frozenset(
        {
            Action.READ_CANONICAL,
            Action.VALIDATE,
        }
    ),
    Role.CERTIFIER: frozenset(
        {
            Action.READ_CANONICAL,
            Action.CERTIFY,
        }
    ),
    Role.RESPONSIBLE_AUTHORITY: frozenset(
        {
            Action.READ_CANONICAL,
            Action.ADMIT,
            Action.INTEGRATE_COGNITION,
        }
    ),
}


class AuthorityPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    permissions: dict[Role, frozenset[Action]] = Field(
        default_factory=lambda: DEFAULT_PERMISSIONS.copy()
    )

    def allows(self, role: Role, action: Action) -> bool:
        return action in self.permissions.get(role, frozenset())

    def require(self, role: Role, action: Action) -> None:
        if not self.allows(role, action):
            raise PermissionError(f"{role} is not authorized to perform {action}")
