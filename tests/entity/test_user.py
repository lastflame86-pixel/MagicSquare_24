"""Unit tests for magicsquare.entity.user.User."""

from __future__ import annotations

import pytest

from magicsquare.entity.user import User, UserRole, UserValidationError


class TestUserCreate:
    """Tests for User.create factory and invariants."""

    def test_create_user_with_valid_fields_returns_user(self) -> None:
        """Given valid id, name, role, email — When create — Then User is returned."""
        # Arrange
        user_id = "user-100"
        display_name = "  Learner One  "
        role = UserRole.LEARNER
        email = "learner@example.com"

        # Act
        user = User.create(
            user_id=user_id,
            display_name=display_name,
            role=role,
            email=email,
        )

        # Assert
        assert user.user_id == "user-100"
        assert user.display_name == "Learner One"
        assert user.role is UserRole.LEARNER
        assert user.email == "learner@example.com"

    def test_create_user_without_email_sets_email_none(self) -> None:
        """Given no email — When create — Then email is None."""
        # Arrange & Act
        user = User.create(user_id="u-2", display_name="No Email")

        # Assert
        assert user.email is None
        assert user.role is UserRole.LEARNER

    def test_create_user_rejects_empty_user_id(self) -> None:
        """Given blank user_id — When create — Then UserValidationError."""
        # Arrange
        user_id = "   "

        # Act & Assert
        with pytest.raises(UserValidationError, match="user_id"):
            User.create(user_id=user_id, display_name="Name")

    def test_create_user_rejects_empty_display_name(self) -> None:
        """Given blank display_name — When create — Then UserValidationError."""
        # Arrange
        display_name = ""

        # Act & Assert
        with pytest.raises(UserValidationError, match="display_name"):
            User.create(user_id="u-3", display_name=display_name)

    def test_create_user_rejects_invalid_email(self) -> None:
        """Given malformed email — When create — Then UserValidationError."""
        # Arrange
        email = "not-an-email"

        # Act & Assert
        with pytest.raises(UserValidationError, match="invalid email"):
            User.create(
                user_id="u-4",
                display_name="Bad Email",
                email=email,
            )


class TestUserWithRole:
    """Tests for immutable role updates."""

    def test_with_role_returns_new_instance_with_updated_role(
        self, sample_user: User
    ) -> None:
        """Given QA user — When with_role(LEARNER) — Then new User has learner role."""
        # Arrange
        original_role = sample_user.role

        # Act
        updated = sample_user.with_role(UserRole.LEARNER)

        # Assert
        assert original_role is UserRole.QA
        assert updated.role is UserRole.LEARNER
        assert updated.user_id == sample_user.user_id
        assert sample_user.role is UserRole.QA

    def test_user_is_frozen(self, sample_user: User) -> None:
        """Given frozen User — When setattr — Then FrozenInstanceError."""
        # Arrange & Act & Assert
        with pytest.raises(AttributeError):
            sample_user.display_name = "Changed"  # type: ignore[misc]
