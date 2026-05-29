"""RED tests for AC-FR-01-01 null and invalid-size grid boundary validation.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid=None and size violations return
code=\"INVALID_SIZE\" and message=\"Grid must be 4x4.\"
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.error_schema import FailureResponse
from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.ui_boundary import UIBoundary

# PRD §8.1 / README RED checklist — exact message contract
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

# AC-FR-01-02~05 / FR-02~05 — explicitly out of scope for this RED commit
OUT_OF_SCOPE_ERROR_CODES = frozenset(
    {
        "INVALID_EMPTY_COUNT",
        "INVALID_CELL_VALUE",
        "DUPLICATE_VALUE",
        "UNSOLVABLE",
        "INTERNAL_ERROR",
    }
)


@pytest.fixture
def input_validator() -> InputValidator:
    """Provide InputValidator for Arrange sections."""
    return InputValidator()


@pytest.fixture
def ui_boundary_with_mock_solver() -> tuple[UIBoundary, Mock]:
    """Provide UIBoundary with a mock solver exposing resolve()."""
    mock_resolve = Mock()
    mock_solver = Mock(resolve=mock_resolve)
    boundary = UIBoundary(solver=mock_solver)
    return boundary, mock_resolve


class TestACFR0101NullGridFailure:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — null grid failure contract."""

    def test_none_grid_returns_failure_invalid_size_code(
        self, input_validator: InputValidator
    ) -> None:
        """Given grid=None — When validate — Then failure code is INVALID_SIZE."""
        # AC-FR-01-01
        # Given
        grid = None

        # When
        result = input_validator.validate(grid)

        # Then
        assert result.error.code == INVALID_SIZE_CODE

    def test_none_grid_message_exact_match_prd_section_8_1(
        self, input_validator: InputValidator
    ) -> None:
        """Given grid=None — When validate — Then message matches PRD §8.1 exactly."""
        # AC-FR-01-01
        # Given
        grid = None

        # When
        result = input_validator.validate(grid)

        # Then
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_none_grid_resolve_called_zero_times(
        self, ui_boundary_with_mock_solver: tuple[UIBoundary, Mock]
    ) -> None:
        """Given grid=None — When solve — Then resolve() is never called."""
        # AC-FR-01-01
        # Given
        boundary, mock_resolve = ui_boundary_with_mock_solver
        grid = None

        # When
        boundary.solve(grid)

        # Then
        mock_resolve.assert_not_called()

    def test_none_grid_returns_failure_response_type(
        self, input_validator: InputValidator
    ) -> None:
        """Given grid=None — When validate — Then result is FailureResponse."""
        # AC-FR-01-01
        # Given
        grid = None

        # When
        result = input_validator.validate(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"

    def test_none_grid_code_not_out_of_scope_error_codes(
        self, input_validator: InputValidator
    ) -> None:
        """Given grid=None — When validate — Then code stays within AC-FR-01-01 scope."""
        # AC-FR-01-01 — AC-FR-01-02~05 / FR-02~05 cases excluded
        # Given
        grid = None

        # When
        result = input_validator.validate(grid)

        # Then
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.code not in OUT_OF_SCOPE_ERROR_CODES


class TestACFR0101SizeBoundaryFailures:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — size boundary failure contract."""

    def test_empty_list_grid_returns_failure_invalid_size(
        self, input_validator: InputValidator
    ) -> None:
        """Given grid=[] — When validate — Then failure with INVALID_SIZE."""
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []

        # When
        result = input_validator.validate(grid)

        # Then
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_empty_rows_grid_returns_failure_invalid_size(
        self, input_validator: InputValidator
    ) -> None:
        """Given grid=[[]]*4 — When validate — Then failure with INVALID_SIZE."""
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = [[]] * 4

        # When
        result = input_validator.validate(grid)

        # Then
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_3x4_grid_returns_failure_invalid_size(
        self, input_validator: InputValidator
    ) -> None:
        """Given 3×4 grid — When validate — Then failure with INVALID_SIZE."""
        # AC-FR-01-01
        # Given
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        # When
        result = input_validator.validate(grid)

        # Then
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.message == INVALID_SIZE_MESSAGE
