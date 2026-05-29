"""Control stub for partial magic square resolve (AC-FR-01-01 isolation only)."""

from __future__ import annotations

from magicsquare.control.two_cell_solver import solution

Grid = list[list[int]]


class SolvePartialMagicSquare:
    """Resolves validated partial grids via two-cell solver (FR-05)."""

    def resolve(self, grid: Grid) -> list[int]:
        """Return int[6] solution tuple [r1,c1,n1,r2,c2,n2] (1-index)."""
        return solution(grid)
