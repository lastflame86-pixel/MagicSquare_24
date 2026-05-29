"""Golden Master input scenarios (PRD G1/G2/G3 + boundary failures)."""

from __future__ import annotations

from dataclasses import dataclass

from tests.entity.conftest import G0_GRID, G1_GRID, G2_GRID, G3_GRID

DUPLICATE_NUMBER_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 10, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

INVALID_BLANK_COUNT = "INVALID_BLANK_COUNT"
DUPLICATE_NUMBER = "DUPLICATE_NUMBER"
NO_VALID_MAGIC_SQUARE = "NO_VALID_MAGIC_SQUARE"


@dataclass(frozen=True)
class GoldenScenario:
    """One GM section: test case id, section id, grid, expected error semantic."""

    test_case_id: str
    section_id: str
    grid: list[list[int]]
    expected_error: str | None = None


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario("GM-TC-01", "normal_success", [row[:] for row in G2_GRID]),
    GoldenScenario("GM-TC-02", "reverse_success", [row[:] for row in G1_GRID]),
    GoldenScenario(
        "GM-TC-03",
        "invalid_blank_count",
        [row[:] for row in G0_GRID],
        expected_error=INVALID_BLANK_COUNT,
    ),
    GoldenScenario(
        "GM-TC-04",
        "duplicate_number",
        [row[:] for row in DUPLICATE_NUMBER_GRID],
        expected_error=DUPLICATE_NUMBER,
    ),
    GoldenScenario(
        "GM-TC-05",
        "no_valid_magic_square",
        [row[:] for row in G3_GRID],
        expected_error=NO_VALID_MAGIC_SQUARE,
    ),
)

SCENARIO_BY_TEST_CASE: dict[str, GoldenScenario] = {
    scenario.test_case_id: scenario for scenario in GOLDEN_SCENARIOS
}
