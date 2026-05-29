"""SolutionResult SSOT — FR-05 int[6] payload (RF-03)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionResult:
    """Control-layer FR-05 result; values are [r1,c1,n1,r2,c2,n2] (1-index)."""

    values: list[int]

    def __post_init__(self) -> None:
        """Validate int[6] contract at construction."""
        if len(self.values) != 6:
            msg = f"SolutionResult requires int[6], got length {len(self.values)}"
            raise ValueError(msg)
