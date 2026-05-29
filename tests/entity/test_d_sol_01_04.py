"""RED skeleton — D-SOL-01~04 (AC-FR05-01~03, AC-FR05-06, FR-05, I8~I10).

Domain Mock forbidden. solution() via Control layer.
"""

from __future__ import annotations

import pytest

from magicsquare.control.two_cell_solver import solution


class TestDSOL01G1StepA:
    """D-SOL-01 — G1 Step A success → int[6]."""

    def test_d_sol_01_g1_solution_step_a_int_six(self, g1_grid: list[list[int]]) -> None:
        """Given G1 — When solution — Then [2,2,7,3,3,10] 1-index coords."""
        # D-SOL-01
        # Given
        grid = g1_grid

        # When
        data = solution(grid)

        # Then
        assert data == [2, 2, 7, 3, 3, 10]


class TestDSOL02G2StepB:
    """D-SOL-02 — G2 Step B success (G2 fixture TBD in design)."""

    def test_d_sol_02_g2_solution_step_b_reverse(self) -> None:
        """Given G2 — When solution — Then [3,3,6,4,4,1]."""
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSOL03G3Unsolvable:
    """D-SOL-03 — G3 both steps fail → UnsolvableDomainError."""

    def test_d_sol_03_g3_solution_raises_unsolvable(self) -> None:
        """Given G3 — When solution — Then UnsolvableDomainError."""
        pytest.fail(
            "RED: D-SOL-03 — G3 → UnsolvableDomainError (I10, AC-FR05-03)"
        )


class TestDSOL04NumberSetContract:
    """D-SOL-04 — solution n1,n2 match {smaller,larger} from FR-03 (AC-FR05-06)."""

    def test_d_sol_04_g1_solution_numbers_match_missing_pair(self) -> None:
        """Given G1 — When solution — Then {n1,n2} == {smaller,larger}."""
        pytest.fail(
            "RED: D-SOL-04 — G1 solution n1,n2 equal missing pair {7,10} (AC-FR05-06)"
        )
