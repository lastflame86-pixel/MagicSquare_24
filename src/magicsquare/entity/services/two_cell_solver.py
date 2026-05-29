"""Two-cell solver — FR-05 Step A/B with is_valid_complete (D-SOL-01~03)."""

from __future__ import annotations

from magicsquare.entity.exceptions import UnsolvableDomainError
from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.magic_square_validator import is_valid_complete
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums

Grid = list[list[int]]


def _copy_grid(grid: Grid) -> Grid:
    """Return a deep copy of grid without mutating the caller input."""
    return [row[:] for row in grid]


def _apply_fill(grid: Grid, row: int, col: int, value: int) -> Grid:
    """Return grid copy with one cell filled (0-index row/col)."""
    filled = _copy_grid(grid)
    filled[row][col] = value
    return filled


def _build_tuple(
    first_row: int,
    first_col: int,
    first_value: int,
    second_row: int,
    second_col: int,
    second_value: int,
) -> list[int]:
    """Build int[6] solution tuple with 1-index coordinates."""
    return [
        first_row,
        first_col,
        first_value,
        second_row,
        second_col,
        second_value,
    ]


def _is_valid_placement(
    grid: Grid,
    row_one_index: int,
    col_one_index: int,
    first_value: int,
    row_two_index: int,
    col_two_index: int,
    second_value: int,
) -> bool:
    """Return True when filling grid produces a complete magic square."""
    candidate = _apply_fill(grid, row_one_index - 1, col_one_index - 1, first_value)
    candidate = _apply_fill(
        candidate, row_two_index - 1, col_two_index - 1, second_value
    )
    return is_valid_complete(candidate)


def solution(grid: Grid) -> list[int]:
    """Try Step A then Step B; raise UnsolvableDomainError when both fail."""
    first, second = find_blank_coords(grid)
    smaller, larger = find_not_exist_nums(grid)

    step_a = _build_tuple(
        first.row,
        first.col,
        smaller,
        second.row,
        second.col,
        larger,
    )
    if _is_valid_placement(
        grid, first.row, first.col, smaller, second.row, second.col, larger
    ):
        return step_a

    step_b = _build_tuple(
        first.row,
        first.col,
        larger,
        second.row,
        second.col,
        smaller,
    )
    if _is_valid_placement(
        grid, first.row, first.col, larger, second.row, second.col, smaller
    ):
        return step_b

    raise UnsolvableDomainError("no valid magic square completion")
