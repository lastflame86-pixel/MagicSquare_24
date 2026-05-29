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
