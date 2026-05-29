"""Boundary input validation for 4x4 grid (FR-01, AC-FR-01-01)."""

from __future__ import annotations

from magicsquare.boundary.error_schema import (
    ErrorDetail,
    FailureResponse,
    ValidationSuccess,
)

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

ValidationOutcome = FailureResponse | ValidationSuccess


def _invalid_size_failure() -> FailureResponse:
    """Build PRD §8.1 INVALID_SIZE failure response."""
    return FailureResponse(
        type="ERROR",
        error=ErrorDetail(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE),
    )


def _is_4x4(matrix: list[list[int]]) -> bool:
    """Return True when matrix has exactly four rows of four columns."""
    if len(matrix) != 4:
        return False
    return all(len(row) == 4 for row in matrix)


def _passes_fr01_rules(matrix: list[list[int]]) -> bool:
    """Return True when matrix satisfies FR-01 rules 3~5 (size already checked)."""
    empty_count = 0
    non_zero_values: list[int] = []
    for row in matrix:
        for value in row:
            if value == 0:
                empty_count += 1
                continue
            if value < 1 or value > 16:
                return False
            non_zero_values.append(value)
    if empty_count != 2:
        return False
    return len(non_zero_values) == len(set(non_zero_values))


class InputValidator:
    """Validates caller matrix; failures return FailureResponse."""

    def validate(self, matrix: list[list[int]] | None) -> ValidationOutcome:
        """Validate grid; return FailureResponse or ValidationSuccess."""
        if matrix is None:
            return _invalid_size_failure()
        if not _is_4x4(matrix):
            return _invalid_size_failure()
        if _passes_fr01_rules(matrix):
            return ValidationSuccess()
        raise NotImplementedError(
            "AC-FR-01-04~06 scope: rule failure responses not implemented"
        )
