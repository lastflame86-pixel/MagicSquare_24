"""PRD reference grids (§16.4) — demo and test SSOT (RF-07, R-L2)."""

from __future__ import annotations

from magicsquare.entity.value_objects.grid import Grid

G0_GRID: Grid = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G1_GRID: Grid = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

G2_GRID: Grid = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

G3_GRID: Grid = [
    [1, 2, 3, 0],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]
