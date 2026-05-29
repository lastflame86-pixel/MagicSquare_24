"""Blank cell discovery — FR-02, I6."""

from __future__ import annotations

from magicsquare.entity.constants import GRID_SIZE
from magicsquare.entity.value_objects.cell_coordinate import CellCoordinate

Grid = list[list[int]]


def find_blank_coords(grid: Grid) -> tuple[CellCoordinate, CellCoordinate]:
    """Return the two blank cells in row-major order (1-index)."""
    blanks: list[CellCoordinate] = []
    for row_index in range(GRID_SIZE):
        for col_index in range(GRID_SIZE):
            if grid[row_index][col_index] == 0:
                blanks.append(CellCoordinate(row_index + 1, col_index + 1))
    first, second = blanks[0], blanks[1]
    return first, second
