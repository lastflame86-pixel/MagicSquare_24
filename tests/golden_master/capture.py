"""Serialize UIBoundary.solve results for Golden Master baselines."""

from __future__ import annotations

from magicsquare.boundary.error_mapper import E006_CODE
from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.boundary.input_validator import E002_CODE, E005_CODE
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare

from tests.golden_master.scenarios import (
    DUPLICATE_NUMBER,
    GOLDEN_SCENARIOS,
    INVALID_BLANK_COUNT,
    NO_VALID_MAGIC_SQUARE,
    GoldenScenario,
)

# Stable semantic Error labels in golden_master_expected.txt (approve contract).
ERROR_SEMANTIC_BY_CODE: dict[str, str] = {
    E002_CODE: INVALID_BLANK_COUNT,
    E005_CODE: DUPLICATE_NUMBER,
    E006_CODE: NO_VALID_MAGIC_SQUARE,
}

Grid = list[list[int]]


def format_grid_input(grid: Grid) -> str:
    """Format 4x4 grid as four space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def capture_section(boundary: UIBoundary, scenario: GoldenScenario) -> str:
    """Capture one [section_id] block from UIBoundary.solve."""
    result = boundary.solve(scenario.grid)
    lines = [
        f"[{scenario.section_id}]",
        "Input:",
        format_grid_input(scenario.grid),
    ]
    if isinstance(result, SuccessResponse):
        lines.extend(["Output:", str(result.data)])
    elif isinstance(result, FailureResponse):
        code = result.error.code
        semantic = ERROR_SEMANTIC_BY_CODE.get(code, code)
        lines.extend(["Error:", semantic])
    else:
        lines.extend(["Error:", "UNEXPECTED_RESPONSE"])
    return "\n".join(lines)


def capture_all_sections() -> str:
    """Capture all scenarios; sections separated by a blank line."""
    boundary = UIBoundary(solver=SolvePartialMagicSquare())
    blocks = [capture_section(boundary, scenario) for scenario in GOLDEN_SCENARIOS]
    return "\n\n".join(blocks) + "\n"
