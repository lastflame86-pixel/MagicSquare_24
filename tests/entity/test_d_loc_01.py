"""RED/GREEN — D-LOC-01 (AC-FR02-01, FR-02, I6).

Domain Mock forbidden. find_blank_coords on G1 → first=(2,2), second=(3,3) 1-index.
"""

from __future__ import annotations

from magicsquare.entity.services.empty_cell_locator import find_blank_coords


class TestDLOC01BlankCoords:
    """D-LOC-01 — row-major blank coordinate pair on G1."""

    def test_d_loc_01_g1_find_blank_coords_row_major_pair(
        self, g1_grid: list[list[int]]
    ) -> None:
        """Given G1 — When find_blank_coords — Then (2,2) and (3,3) 1-index."""
        # D-LOC-01
        # Given
        grid = g1_grid

        # When
        first, second = find_blank_coords(grid)

        # Then
        assert first == (2, 2)
        assert second == (3, 3)
