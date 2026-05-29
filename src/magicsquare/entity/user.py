"""User domain entity for MagicSquare learners and QA operators."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserRole(str, Enum):
    """Role of a user interacting with the MagicSquare system."""

    QA = "qa"
    LEARNER = "learner"


class UserValidationError(ValueError):
    """Raised when User invariants are violated."""


@dataclass(frozen=True, slots=True)
class User:
    """Immutable user identity in the MagicSquare domain.

    Represents a person who runs validations or TDD exercises. This entity
    holds no I/O, validation-of-grid, or framework dependencies.

    Attributes:
        user_id: Non-empty unique identifier.
        display_name: Non-empty human-readable name (leading/trailing space stripped).
        role: QA or learner role.
        email: Optional contact email; when set, must match a basic format.
    """

    user_id: str
    display_name: str
    role: UserRole = UserRole.LEARNER
    email: str | None = None

    def __post_init__(self) -> None:
        """Validate invariants after initialization."""
        normalized_id = self.user_id.strip()
        if not normalized_id:
            raise UserValidationError("user_id must not be empty")

        normalized_name = self.display_name.strip()
        if not normalized_name:
            raise UserValidationError("display_name must not be empty")

        if self.email is not None:
            normalized_email = self.email.strip()
            if not normalized_email:
                raise UserValidationError("email must not be blank when provided")
            if not _EMAIL_PATTERN.match(normalized_email):
                raise UserValidationError(f"invalid email format: {self.email!r}")

        if normalized_id != self.user_id:
            object.__setattr__(self, "user_id", normalized_id)
        if normalized_name != self.display_name:
            object.__setattr__(self, "display_name", normalized_name)
        if self.email is not None and self.email != self.email.strip():
            object.__setattr__(self, "email", self.email.strip())

    @classmethod
    def create(
        cls,
        user_id: str,
        display_name: str,
        role: UserRole = UserRole.LEARNER,
        email: str | None = None,
    ) -> User:
        """Build a validated User instance.

        Args:
            user_id: Unique identifier.
            display_name: Display name.
            role: User role; defaults to learner.
            email: Optional email address.

        Returns:
            A validated frozen User.

        Raises:
            UserValidationError: If any invariant fails.
        """
        return cls(
            user_id=user_id,
            display_name=display_name,
            role=role,
            email=email,
        )

    def with_role(self, role: UserRole) -> User:
        """Return a copy of this user with an updated role.

        Args:
            role: New role value.

        Returns:
            New User instance with the same identity fields and new role.
        """
        return User(
            user_id=self.user_id,
            display_name=self.display_name,
            role=role,
            email=self.email,
        )
