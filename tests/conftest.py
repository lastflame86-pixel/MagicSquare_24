"""Shared pytest fixtures for MagicSquare."""

from __future__ import annotations

import pytest

from magicsquare.entity.demo_grids import G0_GRID, G1_GRID, G2_GRID, G3_GRID
from magicsquare.entity.user import User, UserRole


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register Golden Master approve flags."""
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Regenerate tests/golden_master_expected.txt from current output",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers (also declared in pyproject.toml)."""
    config.addinivalue_line(
        "markers",
        "golden_master: GM-2 Golden Master approve regression",
    )


@pytest.fixture
def g0_grid() -> list[list[int]]:
    """Complete valid magic square (no zeros)."""
    return [row[:] for row in G0_GRID]


@pytest.fixture
def g1_grid() -> list[list[int]]:
    """Partial grid — FR-05 Step B success for G1 (two zeros)."""
    return [row[:] for row in G1_GRID]


@pytest.fixture
def g2_grid() -> list[list[int]]:
    """Partial grid — Step B success (G2)."""
    return [row[:] for row in G2_GRID]


@pytest.fixture
def g3_grid() -> list[list[int]]:
    """Partial grid — unsolvable (both steps fail)."""
    return [row[:] for row in G3_GRID]


@pytest.fixture
def sample_user() -> User:
    """Provide a valid QA user for Arrange sections."""
    return User.create(
        user_id="user-001",
        display_name="QA Operator",
        role=UserRole.QA,
        email="qa@example.com",
    )
