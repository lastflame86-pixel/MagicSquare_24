"""FR-05 partial magic square resolve — Control orchestration (RF-03, RF-04)."""

from __future__ import annotations

from magicsquare.control.solution_result import SolutionResult
from magicsquare.entity.exceptions import UnsolvableDomainError
from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums
from magicsquare.entity.services.two_cell_solver import (
    build_solution_tuple,
    is_valid_two_cell_placement,
)
from magicsquare.entity.value_objects.grid import Grid


class SolvePartialMagicSquare:
    """Orchestrates locate → find missing → Step A/B for validated partial grids."""

    def resolve(self, grid: Grid) -> list[int]:
        """Return int[6] solution tuple [r1,c1,n1,r2,c2,n2] (1-index)."""
        return self._resolve_to_result(grid).values

    def _resolve_to_result(self, grid: Grid) -> SolutionResult:
        """Run FR-05 orchestration and return SolutionResult SSOT."""
        first, second = find_blank_coords(grid)
        smaller, larger = find_not_exist_nums(grid)

        step_a = build_solution_tuple(
            first.row,
            first.col,
            smaller,
            second.row,
            second.col,
            larger,
        )
        if is_valid_two_cell_placement(
            grid, first.row, first.col, smaller, second.row, second.col, larger
        ):
            return SolutionResult(values=step_a)

        step_b = build_solution_tuple(
            first.row,
            first.col,
            larger,
            second.row,
            second.col,
            smaller,
        )
        if is_valid_two_cell_placement(
            grid, first.row, first.col, larger, second.row, second.col, smaller
        ):
            return SolutionResult(values=step_b)

        raise UnsolvableDomainError("no valid magic square completion")
