"""Domain exceptions for magic-square solver (PRD §13.2)."""

from __future__ import annotations


class UnsolvableDomainError(Exception):
    """Raised when Step A and Step B both fail is_valid_complete."""


class InvalidGridStateError(Exception):
    """Raised when blank-cell count is not exactly two."""


class InvalidNumberSetError(Exception):
    """Raised when present values cannot yield exactly two missing numbers."""
