"""Blank cell discovery — FR-02, I6."""

from __future__ import annotations

from magicsquare.entity.constants import EXPECTED_EMPTY_CELLS, GRID_SIZE
from magicsquare.entity.exceptions import InvalidGridStateError
from magicsquare.entity.value_objects.cell_coordinate import CellCoordinate

Grid = list[list[int]]


def find_blank_coords(grid: Grid) -> tuple[CellCoordinate, CellCoordinate]:
    """Return the two blank cells in row-major order (1-index)."""
    blanks: list[CellCoordinate] = []
    for row_index in range(GRID_SIZE):
        for col_index in range(GRID_SIZE):
            if grid[row_index][col_index] == 0:
                blanks.append(CellCoordinate(row_index + 1, col_index + 1))
    if len(blanks) != EXPECTED_EMPTY_CELLS:
        raise InvalidGridStateError(
            f"expected exactly {EXPECTED_EMPTY_CELLS} empty cells, found {len(blanks)}"
        )
    return blanks[0], blanks[1]
