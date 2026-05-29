"""Two-cell placement helpers — domain primitives for FR-05 Step A/B (RF-04)."""

from __future__ import annotations

from magicsquare.entity.services.magic_square_validator import is_valid_complete
from magicsquare.entity.value_objects.grid import Grid


def copy_grid(grid: Grid) -> Grid:
    """Return a deep copy of grid without mutating the caller input."""
    return [row[:] for row in grid]


def apply_fill(grid: Grid, row: int, col: int, value: int) -> Grid:
    """Return grid copy with one cell filled (0-index row/col)."""
    filled = copy_grid(grid)
    filled[row][col] = value
    return filled


def build_solution_tuple(
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


def is_valid_two_cell_placement(
    grid: Grid,
    row_one_index: int,
    col_one_index: int,
    first_value: int,
    row_two_index: int,
    col_two_index: int,
    second_value: int,
) -> bool:
    """Return True when filling grid produces a complete magic square."""
    candidate = apply_fill(grid, row_one_index - 1, col_one_index - 1, first_value)
    candidate = apply_fill(
        candidate, row_two_index - 1, col_two_index - 1, second_value
    )
    return is_valid_complete(candidate)
