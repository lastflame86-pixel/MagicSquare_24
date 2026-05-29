"""SC-CTL-002~004 (G-04) — SolvePartialMagicSquare.resolve() Control unit tests.

AC: FR-05 orchestration entry via Control; mirrors D-SOL-01~03 at Control boundary.
"""

from __future__ import annotations

import pytest

from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import UnsolvableDomainError

G1_EXPECTED = [2, 2, 10, 3, 3, 7]
G2_EXPECTED = [3, 3, 6, 4, 4, 1]


class TestSCCTL002G1Resolve:
    """SC-CTL-002 — G1 Step B success via Control.resolve()."""

    def test_sc_ctl_002_g1_resolve_returns_int_six(self, g1_grid: list[list[int]]) -> None:
        """Given G1 — When resolve — Then [2,2,10,3,3,7] 1-index coords."""
        # SC-CTL-002 — G-04
        # Given
        solver = SolvePartialMagicSquare()
        grid = g1_grid

        # When
        data = solver.resolve(grid)

        # Then
        assert data == G1_EXPECTED


class TestSCCTL003G2Resolve:
    """SC-CTL-003 — G2 reverse Step B via Control.resolve()."""

    def test_sc_ctl_003_g2_resolve_returns_int_six(self, g2_grid: list[list[int]]) -> None:
        """Given G2 — When resolve — Then [3,3,6,4,4,1]."""
        # SC-CTL-003 — G-04
        # Given
        solver = SolvePartialMagicSquare()
        grid = g2_grid

        # When
        data = solver.resolve(grid)

        # Then
        assert data == G2_EXPECTED


class TestSCCTL004G3Unsolvable:
    """SC-CTL-004 — G3 both steps fail → UnsolvableDomainError."""

    def test_sc_ctl_004_g3_resolve_raises_unsolvable(self, g3_grid: list[list[int]]) -> None:
        """Given G3 — When resolve — Then UnsolvableDomainError."""
        # SC-CTL-004 — G-04
        # Given
        solver = SolvePartialMagicSquare()
        grid = g3_grid

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solver.resolve(grid)
