"""Complete-grid magic square validation — FR-04, I1~I5."""

from __future__ import annotations

from magicsquare.entity.constants import (
    CELL_MAX,
    CELL_MIN,
    GRID_SIZE,
    MAGIC_CONSTANT,
)

from magicsquare.entity.value_objects.grid import Grid


def is_magic_square(grid: Grid) -> bool:
    """Return True when grid is a complete magic square (no zeros, I1~I5)."""
    return is_valid_complete(grid)


def is_valid_complete(grid: Grid) -> bool:
    """Alias for PRD FR-05 Step A/B complete-grid check."""
    values: list[int] = []
    for row in grid:
        for value in row:
            if value == 0:
                return False
            values.append(value)
    if len(values) != GRID_SIZE * GRID_SIZE:
        return False
    if set(values) != set(range(CELL_MIN, CELL_MAX + 1)):
        return False
    for row in grid:
        if sum(row) != MAGIC_CONSTANT:
            return False
    for col_index in range(GRID_SIZE):
        if sum(grid[row_index][col_index] for row_index in range(GRID_SIZE)) != (
            MAGIC_CONSTANT
        ):
            return False
    main_diagonal = sum(grid[index][index] for index in range(GRID_SIZE))
    anti_diagonal = sum(
        grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)
    )
    return main_diagonal == anti_diagonal == MAGIC_CONSTANT
