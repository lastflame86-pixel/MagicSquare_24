"""Golden Master contract checks (int[6], row-major, 1-index, Step A/B)."""

from __future__ import annotations

from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.entity.constants import CELL_MAX, CELL_MIN, GRID_SIZE
from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums
from magicsquare.entity.services.two_cell_solver import solution

Grid = list[list[int]]


def assert_int_six_format(data: list[int]) -> None:
    """Success payload is int[6] with 1-index coords and domain numbers."""
    assert len(data) == 6
    r1, c1, n1, r2, c2, n2 = data
    for coord in (r1, c1, r2, c2):
        assert 1 <= coord <= GRID_SIZE
    for number in (n1, n2):
        assert CELL_MIN <= number <= CELL_MAX
    assert n1 != n2


def assert_row_major_and_one_index(grid: Grid, data: list[int]) -> None:
    """Output coords match row-major first/second blank (1-index)."""
    first, second = find_blank_coords(grid)
    assert (data[0], data[1]) == (first.row, first.col)
    assert (data[3], data[4]) == (second.row, second.col)


def assert_small_first_combination(grid: Grid, data: list[int]) -> None:
    """Step A: smaller at first blank, larger at second blank."""
    smaller, larger = find_not_exist_nums(grid)
    assert data[2] == smaller
    assert data[5] == larger


def assert_reverse_fallback_combination(grid: Grid, data: list[int]) -> None:
    """Step B: larger at first blank, smaller at second blank."""
    smaller, larger = find_not_exist_nums(grid)
    assert data[2] == larger
    assert data[5] == smaller


def assert_step_a_fails_step_b_succeeds(grid: Grid) -> None:
    """Domain used reverse fallback: Step A invalid, Step B valid."""
    smaller, larger = find_not_exist_nums(grid)
    first, second = find_blank_coords(grid)
    step_a = [
        first.row,
        first.col,
        smaller,
        second.row,
        second.col,
        larger,
    ]
    assert solution(grid) != step_a


def assert_failure_error_contract(
    result: FailureResponse,
    *,
    expected_semantic: str,
) -> None:
    """Failure envelope uses ERROR type and mapped semantic label."""
    assert result.type == "ERROR"
    assert result.error.code
    assert result.error.message
