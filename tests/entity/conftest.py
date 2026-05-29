"""Entity-track grid fixtures (G0~G3) — PRD §16.4 (0-index)."""

from __future__ import annotations

import pytest

G0_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G1_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

G2_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

G3_GRID: list[list[int]] = [
    [1, 2, 3, 0],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]


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
    """Partial grid — Step B success (TBD in D-SOL-02 GREEN)."""
    return [row[:] for row in G2_GRID]


@pytest.fixture
def g3_grid() -> list[list[int]]:
    """Partial grid — unsolvable (both steps fail)."""
    return [row[:] for row in G3_GRID]
