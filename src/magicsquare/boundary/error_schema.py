"""Failure response models for Boundary OUT contract."""

from __future__ import annotations

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error payload for FailureResponse."""

    code: str
    message: str


class FailureResponse(BaseModel):
    """Boundary failure envelope (AC-FR-01-01)."""

    type: str = "ERROR"
    error: ErrorDetail


class ValidationSuccess(BaseModel):
    """FR-01 validation pass; allows Domain resolve (no error field)."""

    type: str = "OK"


class SuccessResponse(BaseModel):
    """Boundary success envelope (AC-FR05-04, AC-FR05-07, BR-20)."""

    type: str = "OK"
    data: list[int]
