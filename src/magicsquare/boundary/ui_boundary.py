"""UIBoundary orchestrates validation before Control resolve (AC-FR-01-01)."""

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
from magicsquare.entity.value_objects.grid import Grid


class SolverProtocol(Protocol):
    """Solver contract exposed to UIBoundary."""

    def resolve(self, grid: Grid) -> list[int]:
        """Return int[6] solution tuple after validation passes."""


class UIBoundary:
    """Boundary entry point; blocks Control resolve on validation failure."""

    def __init__(self, solver: SolverProtocol) -> None:
        """Initialize with a solver exposing resolve()."""
        self._solver = solver
        self._validator = InputValidator()

    def solve(self, grid: Grid | None) -> FailureResponse | SuccessResponse:
        """Validate grid; return Success or Failure envelope."""
        validation_outcome = self._validate(grid)
        if isinstance(validation_outcome, FailureResponse):
            return validation_outcome
        return self._resolve_validated(self._require_validated_grid(grid))

    def _validate(self, grid: Grid | None) -> ValidationOutcome:
        """Run FR-01 input validation."""
        return self._validator.validate(grid)

    def _require_validated_grid(self, grid: Grid | None) -> Grid:
        """Return grid after validation pass; grid is non-None 4x4 (R-U3)."""
        if grid is None:
            msg = "validated grid must not be None"
            raise ValueError(msg)
        return grid

    def _resolve_validated(self, grid: Grid) -> SuccessResponse | FailureResponse:
        """Call Control resolve and map domain exceptions (R-U2)."""
        try:
            data = self._solver.resolve(grid)
        except (
            UnsolvableDomainError,
            InvalidGridStateError,
            InvalidNumberSetError,
        ) as exc:
            return map_domain_exception(exc)
        return SuccessResponse(data=data)
