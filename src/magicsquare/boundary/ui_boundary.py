"""UIBoundary orchestrates validation before Domain resolve (AC-FR-01-01)."""

from __future__ import annotations

from typing import Protocol

from magicsquare.boundary.error_mapper import map_domain_exception
from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.boundary.input_validator import InputValidator, ValidationOutcome
from magicsquare.entity.exceptions import (
    InvalidGridStateError,
    InvalidNumberSetError,
    UnsolvableDomainError,
)


class SolverProtocol(Protocol):
    """Solver contract exposed to UIBoundary."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Return int[6] solution tuple after validation passes."""


class UIBoundary:
    """Boundary entry point; blocks Domain resolve on validation failure."""

    def __init__(self, solver: SolverProtocol) -> None:
        """Initialize with a solver exposing resolve()."""
        self._solver = solver
        self._validator = InputValidator()

    def solve(self, grid: list[list[int]] | None) -> FailureResponse | SuccessResponse:
        """Validate grid; return Success or Failure envelope."""
        outcome: ValidationOutcome = self._validator.validate(grid)
        if isinstance(outcome, FailureResponse):
            return outcome
        try:
            data = self._solver.resolve(grid)
        except (
            UnsolvableDomainError,
            InvalidGridStateError,
            InvalidNumberSetError,
        ) as exc:
            return map_domain_exception(exc)
        return SuccessResponse(data=data)
