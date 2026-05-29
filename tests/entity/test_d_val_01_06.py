"""RED skeleton — D-VAL-01~06 (AC-FR04-01~06, FR-04, I1~I5).

Domain Mock forbidden. is_magic_square on G0 and rule-breaking variants.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.services.magic_square_validator import is_magic_square


class TestDVAL01G0Baseline:
    """D-VAL-01 — complete G0 is a magic square."""

    def test_d_val_01_g0_is_magic_square_true(self) -> None:
        """Given G0 — When is_magic_square — Then True."""
        # Given
        # grid = G0_GRID
        # When
        # result = is_magic_square(grid)
        pytest.fail(
            "RED: D-VAL-01 — G0 complete grid → is_magic_square True (I1~I5)"
        )


class TestDVAL02RowSumBreak:
    """D-VAL-02 — broken row sum → False."""

    def test_d_val_02_row_sum_break_is_magic_square_false(self) -> None:
        """Given G0 with row-1 sum broken — When is_magic_square — Then False."""
        # Given
        # grid = copy(G0_GRID); break row 0 sum (I1)
        # When
        # result = is_magic_square(grid)
        pytest.fail(
            "RED: D-VAL-02 — row sum violation → is_magic_square False (I1)"
        )


class TestDVAL03ColSumBreak:
    """D-VAL-03 — broken column sum → False."""

    def test_d_val_03_col_sum_break_is_magic_square_false(self) -> None:
        """Given G0 with column sum broken — When is_magic_square — Then False."""
        # Given
        # grid = copy(G0_GRID); break column sum (I2)
        pytest.fail(
            "RED: D-VAL-03 — column sum violation → is_magic_square False (I2)"
        )


class TestDVAL04DiagonalSumBreak:
    """D-VAL-04 — broken diagonal sum → False."""

    def test_d_val_04_diagonal_sum_break_is_magic_square_false(self) -> None:
        """Given G0 with diagonal sum broken — When is_magic_square — Then False."""
        # Given
        # grid = copy(G0_GRID); break diagonal (I3)
        pytest.fail(
            "RED: D-VAL-04 — diagonal sum violation → is_magic_square False (I3)"
        )


class TestDVAL05Duplicate:
    """D-VAL-05 — duplicate values in complete grid → False."""

    def test_d_val_05_duplicate_is_magic_square_false(self) -> None:
        """Given G0 with duplicate — When is_magic_square — Then False."""
        # Given
        # grid = copy(G0_GRID); introduce duplicate (I4)
        pytest.fail(
            "RED: D-VAL-05 — duplicate in complete grid → is_magic_square False (I4)"
        )


class TestDVAL06ZeroInComplete:
    """D-VAL-06 — zero in complete grid → False."""

    def test_d_val_06_zero_in_complete_is_magic_square_false(self) -> None:
        """Given G0 with a zero cell — When is_magic_square — Then False."""
        # Given
        # grid = copy(G0_GRID); set one cell to 0
        pytest.fail(
            "RED: D-VAL-06 — zero in complete grid → is_magic_square False (I4)"
        )
