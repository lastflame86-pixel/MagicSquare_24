"""Boundary input validation for 4x4 grid (FR-01, AC-FR-01-01)."""

from __future__ import annotations

from magicsquare.boundary.error_schema import ErrorDetail, FailureResponse

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."


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


class InputValidator:
    """Validates caller matrix; null and size failures return FailureResponse."""

    def validate(self, matrix: list[list[int]] | None) -> FailureResponse:
        """Validate grid; return FailureResponse on null or size violation."""
        if matrix is None:
            return _invalid_size_failure()
        if not _is_4x4(matrix):
            return _invalid_size_failure()
        raise NotImplementedError(
            "AC-FR-01-01 scope: valid grid validation not implemented"
        )
