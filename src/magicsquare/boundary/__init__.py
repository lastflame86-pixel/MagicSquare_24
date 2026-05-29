"""Boundary layer — input validation and response schema."""

from magicsquare.boundary.error_schema import ErrorDetail, FailureResponse
from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.ui_boundary import UIBoundary

__all__ = ["ErrorDetail", "FailureResponse", "InputValidator", "UIBoundary"]
