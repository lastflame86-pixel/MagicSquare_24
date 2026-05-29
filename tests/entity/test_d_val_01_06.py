"""D-VAL-01~06 (AC-FR04-01~06, FR-04, I1~I5).

Domain Mock forbidden. is_magic_square on G0 and rule-breaking variants.
"""

from __future__ import annotations

from magicsquare.entity.services.magic_square_validator import is_magic_square
from tests.entity.conftest import G0_GRID


class TestDVAL01G0Baseline:
    """D-VAL-01 — complete G0 is a magic square."""

    def test_d_val_01_g0_is_magic_square_true(self, g0_grid: list[list[int]]) -> None:
        """Given G0 — When is_magic_square — Then True."""
        # D-VAL-01
        # Given
        grid = g0_grid

        # When
        result = is_magic_square(grid)

        # Then
        assert result is True


class TestDVAL02RowSumBreak:
    """D-VAL-02 — broken row sum → False."""

    def test_d_val_02_row_sum_break_is_magic_square_false(self) -> None:
        """Given G0 with row-1 sum broken — When is_magic_square — Then False."""
        # D-VAL-02
        # Given
        grid = [row[:] for row in G0_GRID]
        grid[0][0] = 15

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False


class TestDVAL03ColSumBreak:
    """D-VAL-03 — broken column sum → False."""

    def test_d_val_03_col_sum_break_is_magic_square_false(self) -> None:
        """Given G0 with column sum broken — When is_magic_square — Then False."""
        # D-VAL-03
        # Given
        grid = [row[:] for row in G0_GRID]
        grid[1][0] = 6

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False


class TestDVAL04DiagonalSumBreak:
    """D-VAL-04 — broken diagonal sum → False."""

    def test_d_val_04_diagonal_sum_break_is_magic_square_false(self) -> None:
        """Given G0 with diagonal sum broken — When is_magic_square — Then False."""
        # D-VAL-04
        # Given
        grid = [row[:] for row in G0_GRID]
        grid[0][0] = 15

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False


class TestDVAL05Duplicate:
    """D-VAL-05 — duplicate values in complete grid → False."""

    def test_d_val_05_duplicate_is_magic_square_false(self) -> None:
        """Given G0 with duplicate — When is_magic_square — Then False."""
        # D-VAL-05
        # Given
        grid = [row[:] for row in G0_GRID]
        grid[0][1] = grid[0][0]

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False


class TestDVAL06ZeroInComplete:
    """D-VAL-06 — zero in complete grid → False."""

    def test_d_val_06_zero_in_complete_is_magic_square_false(self) -> None:
        """Given G0 with a zero cell — When is_magic_square — Then False."""
        # D-VAL-06
        # Given
        grid = [row[:] for row in G0_GRID]
        grid[1][1] = 0

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False
