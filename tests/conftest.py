"""Shared pytest fixtures for MagicSquare."""

from __future__ import annotations

import pytest

from magicsquare.entity.user import User, UserRole


@pytest.fixture
def sample_user() -> User:
    """Provide a valid QA user for Arrange sections."""
    return User.create(
        user_id="user-001",
        display_name="QA Operator",
        role=UserRole.QA,
        email="qa@example.com",
    )
