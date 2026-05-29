"""Two-cell solver orchestration — FR-05 Step A/B (D-SOL-01)."""

from __future__ import annotations

from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums

Grid = list[list[int]]


def solution(grid: Grid) -> list[int]:
    """Return Step A tuple [r1,c1,n1,r2,c2,n2] (1-index); Step B in D-SOL-02."""
    first, second = find_blank_coords(grid)
    smaller, larger = find_not_exist_nums(grid)
    return [
        first.row,
        first.col,
        smaller,
        second.row,
        second.col,
        larger,
    ]
