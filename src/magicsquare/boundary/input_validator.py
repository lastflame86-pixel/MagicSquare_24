"""Boundary input validation for 4x4 grid (FR-01, AC-FR-01-01)."""

from __future__ import annotations

from magicsquare.boundary.error_schema import (
    ErrorDetail,
    FailureResponse,
    ValidationSuccess,
)
from magicsquare.entity.constants import (
    CELL_MAX,
    CELL_MIN,
    EXPECTED_EMPTY_CELLS,
    GRID_SIZE,
)

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."
E002_CODE = "E002"
E002_MESSAGE = "INVALID_EMPTY_COUNT: expected exactly 2 empty cells (0)"
E004_CODE = "E004"
E004_MESSAGE = "INVALID_CELL_VALUE: each cell must be 0 or 1..16"
E005_CODE = "E005"
E005_MESSAGE = "DUPLICATE_VALUE: non-zero values must be unique"

ValidationOutcome = FailureResponse | ValidationSuccess


def _invalid_size_failure() -> FailureResponse:
    """Build PRD §8.1 INVALID_SIZE failure response."""
    return FailureResponse(
        type="ERROR",
        error=ErrorDetail(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE),
    )


def _e002_failure() -> FailureResponse:
    """Build E002 empty-cell count failure response."""
    return FailureResponse(
        type="ERROR",
        error=ErrorDetail(code=E002_CODE, message=E002_MESSAGE),
    )


def _e004_failure() -> FailureResponse:
    """Build E004 cell value range failure response."""
    return FailureResponse(
        type="ERROR",
        error=ErrorDetail(code=E004_CODE, message=E004_MESSAGE),
    )


def _e005_failure() -> FailureResponse:
    """Build E005 duplicate non-zero failure response."""
    return FailureResponse(
        type="ERROR",
        error=ErrorDetail(code=E005_CODE, message=E005_MESSAGE),
    )


def _is_4x4(matrix: list[list[int]]) -> bool:
    """Return True when matrix has exactly four rows of four columns."""
    if len(matrix) != GRID_SIZE:
        return False
    return all(len(row) == GRID_SIZE for row in matrix)


def _fr01_rule_failure(matrix: list[list[int]]) -> FailureResponse | None:
    """Return FailureResponse when FR-01 rules 3~5 fail; None when all pass."""
    empty_count = 0
    non_zero_values: list[int] = []
    for row in matrix:
        for value in row:
            if value == 0:
                empty_count += 1
                continue
            if value < CELL_MIN or value > CELL_MAX:
                return _e004_failure()
            non_zero_values.append(value)
    if empty_count != EXPECTED_EMPTY_CELLS:
        return _e002_failure()
    if len(non_zero_values) != len(set(non_zero_values)):
        return _e005_failure()
    return None


class InputValidator:
    """Validates caller matrix; failures return FailureResponse."""

    def validate(self, matrix: list[list[int]] | None) -> ValidationOutcome:
        """Validate grid; return FailureResponse or ValidationSuccess."""
        if matrix is None:
            return _invalid_size_failure()
        if not _is_4x4(matrix):
            return _invalid_size_failure()
        rule_failure = _fr01_rule_failure(matrix)
        if rule_failure is not None:
            return rule_failure
        return ValidationSuccess()
