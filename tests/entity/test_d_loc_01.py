"""RED skeleton — D-LOC-01 (AC-FR02-01, FR-02, I6).

Domain Mock forbidden. find_blank_coords on G1 → first=(2,2), second=(3,3) 1-index.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.services.empty_cell_locator import find_blank_coords


class TestDLOC01BlankCoords:
    """D-LOC-01 — row-major blank coordinate pair on G1."""

    def test_d_loc_01_g1_find_blank_coords_row_major_pair(self) -> None:
        """Given G1 — When find_blank_coords — Then (2,2) and (3,3) 1-index."""
        # Given
        # grid = G1_GRID
        # When
        # first, second = find_blank_coords(grid)
        # Then — first==(2,2), second==(3,3)
        pytest.fail(
            "RED: D-LOC-01 — G1 row-major blanks at (2,2) and (3,3) 1-index"
        )
