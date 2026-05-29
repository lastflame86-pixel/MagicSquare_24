"""Screen composition root — UIBoundary wiring (RF-06)."""

from __future__ import annotations

from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare


def create_default_boundary() -> UIBoundary:
    """Build UIBoundary with default SolvePartialMagicSquare solver."""
    return UIBoundary(solver=SolvePartialMagicSquare())
