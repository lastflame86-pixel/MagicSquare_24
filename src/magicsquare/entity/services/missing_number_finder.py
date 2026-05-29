"""Missing number discovery — FR-03, I7."""

from __future__ import annotations

from magicsquare.entity.constants import CELL_MAX, CELL_MIN, EXPECTED_EMPTY_CELLS
from magicsquare.entity.exceptions import InvalidNumberSetError

Grid = list[list[int]]


def find_not_exist_nums(grid: Grid) -> tuple[int, int]:
    """Return missing values from {CELL_MIN..CELL_MAX} as (smaller, larger)."""
    present = {value for row in grid for value in row if value != 0}
    missing = sorted(
        value for value in range(CELL_MIN, CELL_MAX + 1) if value not in present
    )
    if len(missing) != EXPECTED_EMPTY_CELLS:
        raise InvalidNumberSetError(
            f"expected exactly {EXPECTED_EMPTY_CELLS} missing values, found {len(missing)}"
        )
    return missing[0], missing[1]
