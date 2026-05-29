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


def _failure(code: str, message: str) -> FailureResponse:
    """Build a PRD FailureResponse envelope for the given error code and message."""
    return FailureResponse(
        type="ERROR",
        error=ErrorDetail(code=code, message=message),
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
                return _failure(E004_CODE, E004_MESSAGE)
            non_zero_values.append(value)
    if empty_count != EXPECTED_EMPTY_CELLS:
        return _failure(E002_CODE, E002_MESSAGE)
    if len(non_zero_values) != len(set(non_zero_values)):
        return _failure(E005_CODE, E005_MESSAGE)
    return None


class InputValidator:
    """Validates caller matrix; failures return FailureResponse."""

    def validate(self, matrix: list[list[int]] | None) -> ValidationOutcome:
        """Validate grid; return FailureResponse or ValidationSuccess."""
        if matrix is None:
            return _failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        if not _is_4x4(matrix):
            return _failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        rule_failure = _fr01_rule_failure(matrix)
        if rule_failure is not None:
            return rule_failure
        return ValidationSuccess()
