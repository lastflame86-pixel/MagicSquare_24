"""RED/GREEN — D-MIS-01 (AC-FR03-01, FR-03, I7, I11).

Domain Mock forbidden. find_not_exist_nums on G1 → (7, 10) ascending.
"""

from __future__ import annotations

from magicsquare.entity.services.missing_number_finder import find_not_exist_nums


class TestDMIS01MissingNumbers:
    """D-MIS-01 — missing number pair on G1."""

    def test_d_mis_01_g1_find_not_exist_nums_sorted_pair(
        self, g1_grid: list[list[int]]
    ) -> None:
        """Given G1 — When find_not_exist_nums — Then (7, 10) ascending."""
        # D-MIS-01
        # Given
        grid = g1_grid

        # When
        smaller, larger = find_not_exist_nums(grid)

        # Then
        assert (smaller, larger) == (7, 10)
