"""RED skeleton — U-IN-04~08 (AC-FR01-04~06, PRD E002/E004/E005).

Report/05 §Track A. U-IN-01~03 covered by test_RED_AC_FR01_01_null_and_size.py (Report/04).
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.error_schema import FailureResponse, ValidationSuccess
from magicsquare.boundary.input_validator import InputValidator

# Report/02 · PRD §16.4 — G1 Given (Step A, exactly two zeros)
G1_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


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
        # Given
        # matrix = g0_grid  # fixture: tests/entity/conftest.py G0_GRID
        # validator = input_validator
        # When
        # result = validator.validate(matrix)
        # Then — (Full RED in GREEN phase)
        pytest.fail(
            "RED: U-IN-04 — G0 with 0 empty cells → E002 INVALID_EMPTY_COUNT"
        )


class TestUIN05EmptyCellCount:
    """U-IN-05 — three empty cells → E002."""

    def test_u_in_05_three_empty_cells_returns_e002(
        self, input_validator: InputValidator
    ) -> None:
        """Given 4x4 with three zeros — When validate — Then E002."""
        # Given
        # matrix = G1 variant with count(0)==3
        # When
        # result = input_validator.validate(matrix)
        pytest.fail(
            "RED: U-IN-05 — three empty cells → E002 INVALID_EMPTY_COUNT"
        )


class TestUIN06CellValueRange:
    """U-IN-06 — cell value -1 → E004."""

    def test_u_in_06_cell_minus_one_returns_e004(
        self, input_validator: InputValidator
    ) -> None:
        """Given G1 with (1,0)=-1 — When validate — Then E004."""
        # Given
        # matrix = copy(G1_GRID); matrix[1][0] = -1
        # When
        # result = input_validator.validate(matrix)
        pytest.fail(
            "RED: U-IN-06 — cell -1 → E004 INVALID_CELL_VALUE"
        )


class TestUIN07CellValueRange:
    """U-IN-07 — cell value 17 → E004."""

    def test_u_in_07_cell_seventeen_returns_e004(
        self, input_validator: InputValidator
    ) -> None:
        """Given G1 with (0,0)=17 — When validate — Then E004."""
        # Given
        # matrix = copy(G1_GRID); matrix[0][0] = 17
        # When
        # result = input_validator.validate(matrix)
        pytest.fail(
            "RED: U-IN-07 — cell 17 → E004 INVALID_CELL_VALUE"
        )


class TestUIN08DuplicateNonZero:
    """U-IN-08 — duplicate non-zero with two empties → E005."""

    def test_u_in_08_duplicate_nonzero_returns_e005(
        self, input_validator: InputValidator
    ) -> None:
        """Given 4x4 with duplicate non-zero — When validate — Then E005."""
        # Given
        # matrix = partial grid: two zeros, duplicate non-zero value 5
        # When
        # result = input_validator.validate(matrix)
        pytest.fail(
            "RED: U-IN-08 — duplicate non-zero → E005 DUPLICATE_VALUE"
        )
