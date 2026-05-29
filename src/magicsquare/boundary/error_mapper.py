"""Map Domain exceptions to Boundary FailureResponse (PRD §13.2)."""

from __future__ import annotations

from magicsquare.boundary.error_schema import ErrorDetail, FailureResponse
from magicsquare.entity.exceptions import (
    InvalidGridStateError,
    InvalidNumberSetError,
    UnsolvableDomainError,
)

E006_CODE = "E006"
E006_MESSAGE = "UNSOLVABLE: no valid magic square completion"
E007_CODE = "E007"
E007_MESSAGE = "INTERNAL_ERROR: unexpected domain failure"


def map_domain_exception(exc: Exception) -> FailureResponse:
    """Convert a Domain exception into a PRD FailureResponse envelope."""
    if isinstance(exc, UnsolvableDomainError):
        return FailureResponse(
            type="ERROR",
            error=ErrorDetail(code=E006_CODE, message=E006_MESSAGE),
        )
    if isinstance(exc, (InvalidGridStateError, InvalidNumberSetError)):
        return FailureResponse(
            type="ERROR",
            error=ErrorDetail(code=E007_CODE, message=E007_MESSAGE),
        )
    raise exc
