"""Shared pytest fixtures for MagicSquare."""

from __future__ import annotations

import pytest

from magicsquare.entity.user import User, UserRole

# --- G0~G3 grid placeholders (PRD §16.4, Report/05) — RED skeleton only ---
# See tests/entity/conftest.py for full matrix literals when Track B Arrange is enabled.
# G0: complete 4x4 magic square (0 empty cells)
# G1: two zeros at (1,1),(2,2) 0-index — Step A NS-01
# G2: two zeros — Step B NS-02 (fixture TBD in D-SOL-02)
# G3: unsolvable partial grid


@pytest.fixture
def sample_user() -> User:
    """Provide a valid QA user for Arrange sections."""
    return User.create(
        user_id="user-001",
        display_name="QA Operator",
        role=UserRole.QA,
        email="qa@example.com",
    )
