"""Entity-track grid fixtures (G0~G3) — RED skeleton placeholders only.

PRD §16.4 representative matrices (0-index). Uncomment when implementing Arrange.
"""

from __future__ import annotations

# import pytest

# G0 — complete valid magic square (no zeros)
# G0_GRID: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — Step A success (exactly two zeros)
# G1_GRID: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2 — Step B success (TBD confirmation in D-SOL-02 GREEN)
# G2_GRID: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 0, 12],
#     [4, 14, 15, 0],
# ]

# G3 — unsolvable (both Step A and B fail)
# G3_GRID: list[list[int]] = [
#     [1, 2, 3, 0],
#     [5, 6, 0, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16],
# ]

# @pytest.fixture
# def g0_grid() -> list[list[int]]:
#     return [row[:] for row in G0_GRID]
#
# @pytest.fixture
# def g1_grid() -> list[list[int]]:
#     return [row[:] for row in G1_GRID]
#
# @pytest.fixture
# def g2_grid() -> list[list[int]]:
#     return [row[:] for row in G2_GRID]
#
# @pytest.fixture
# def g3_grid() -> list[list[int]]:
#     return [row[:] for row in G3_GRID]
