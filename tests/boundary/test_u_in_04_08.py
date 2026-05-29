"""RED skeleton — U-IN-04~08 (AC-FR01-04~06, PRD E002/E004/E005).

Report/05 §Track A. U-IN-01~03 covered by test_RED_AC_FR01_01_null_and_size.py (Report/04).
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.error_schema import FailureResponse, ValidationSuccess
from magicsquare.boundary.input_validator import (
    E002_CODE,
    E002_MESSAGE,
    E004_CODE,
    E004_MESSAGE,
    E005_CODE,
    E005_MESSAGE,
    InputValidator,
)
from tests.entity.conftest import G0_GRID, G1_GRID


@pytest.fixture
def input_validator() -> InputValidator:
    """Provide InputValidator for Arrange sections."""
    return InputValidator()


class TestG1GivenPassesValidation:
    """G1 Given — canonical grid passes FR-01 (AC-FR01-07 prep)."""

    def test_g1_given_validate_returns_ok_not_failure(
        self, input_validator: InputValidator
    ) -> None:
        """Given G1 — When validate — Then ValidationSuccess (not FailureResponse)."""
        # AC-FR-01-07 prep — G1 Given
        # Given
        grid = [row[:] for row in G1_GRID]

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, ValidationSuccess)
        assert result.type == "OK"
        assert not isinstance(result, FailureResponse)


class TestUIN04EmptyCellCount:
    """U-IN-04 — G0 complete grid (zero empty cells) → E002."""

    def test_u_in_04_zero_empty_cells_returns_e002(
        self, input_validator: InputValidator
    ) -> None:
        """Given G0 (no zeros) — When validate — Then E002 empty count."""
        # U-IN-04
        # Given
        grid = [row[:] for row in G0_GRID]

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.error.code == E002_CODE
        assert result.error.message == E002_MESSAGE


class TestUIN05EmptyCellCount:
    """U-IN-05 — three empty cells → E002."""

    def test_u_in_05_three_empty_cells_returns_e002(
        self, input_validator: InputValidator
    ) -> None:
        """Given 4x4 with three zeros — When validate — Then E002."""
        # U-IN-05
        # Given
        grid = [row[:] for row in G1_GRID]
        grid[0][1] = 0

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.error.code == E002_CODE
        assert result.error.message == E002_MESSAGE


class TestUIN06CellValueRange:
    """U-IN-06 — cell value -1 → E004."""

    def test_u_in_06_cell_minus_one_returns_e004(
        self, input_validator: InputValidator
    ) -> None:
        """Given G1 with (1,0)=-1 — When validate — Then E004."""
        # U-IN-06
        # Given
        grid = [row[:] for row in G1_GRID]
        grid[1][0] = -1

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.error.code == E004_CODE
        assert result.error.message == E004_MESSAGE


class TestUIN07CellValueRange:
    """U-IN-07 — cell value 17 → E004."""

    def test_u_in_07_cell_seventeen_returns_e004(
        self, input_validator: InputValidator
    ) -> None:
        """Given G1 with (0,0)=17 — When validate — Then E004."""
        # U-IN-07
        # Given
        grid = [row[:] for row in G1_GRID]
        grid[0][0] = 17

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.error.code == E004_CODE
        assert result.error.message == E004_MESSAGE


class TestUIN08DuplicateNonZero:
    """U-IN-08 — duplicate non-zero with two empties → E005."""

    def test_u_in_08_duplicate_nonzero_returns_e005(
        self, input_validator: InputValidator
    ) -> None:
        """Given 4x4 with duplicate non-zero — When validate — Then E005."""
        # U-IN-08
        # Given
        grid = [row[:] for row in G1_GRID]
        grid[2][1] = 5

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.error.code == E005_CODE
        assert result.error.message == E005_MESSAGE
