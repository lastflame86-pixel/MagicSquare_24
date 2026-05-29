"""1-index cell coordinate (FR-02, BR-12)."""

from __future__ import annotations

from typing import NamedTuple


class CellCoordinate(NamedTuple):
    """Row and column on a 1-indexed 4x4 grid."""

    row: int
    col: int
