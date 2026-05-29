"""UIBoundary orchestrates validation before Domain resolve (AC-FR-01-01)."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.boundary.input_validator import InputValidator, ValidationOutcome


class UIBoundary:
    """Boundary entry point; blocks Domain resolve on validation failure."""

    def __init__(self, solver: Any) -> None:
        """Initialize with a solver exposing resolve()."""
        self._solver = solver
        self._validator = InputValidator()

    def solve(self, grid: list[list[int]] | None) -> FailureResponse | SuccessResponse:
        """Validate grid; return Success or Failure envelope."""
        outcome: ValidationOutcome = self._validator.validate(grid)
        if isinstance(outcome, FailureResponse):
            return outcome
        data = self._solver.resolve(grid)
        return SuccessResponse(data=data)
