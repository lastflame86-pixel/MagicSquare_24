"""D-SOL-01~04 (AC-FR05-01~03, AC-FR05-06, FR-05, I8~I10).

Domain Mock forbidden. FR-05 resolve via Control SolvePartialMagicSquare (RF-04).
"""

from __future__ import annotations

import pytest

from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import UnsolvableDomainError

G1_EXPECTED = [2, 2, 10, 3, 3, 7]
G2_EXPECTED = [3, 3, 6, 4, 4, 1]


class TestDSOL01G1StepAB:
    """D-SOL-01 — G1 Step A fails, Step B succeeds (oracle TD-04)."""

    def test_d_sol_01_g1_solution_step_b_int_six(self, g1_grid: list[list[int]]) -> None:
        """Given G1 — When resolve — Then [2,2,10,3,3,7] 1-index coords."""
        # D-SOL-01 — FR-05 tries Step A then Step B
        # Given
        grid = g1_grid
        solver = SolvePartialMagicSquare()

        # When
        data = solver.resolve(grid)

        # Then
        assert data == G1_EXPECTED


class TestDSOL02G2StepB:
    """D-SOL-02 — G2 Step B success."""

    def test_d_sol_02_g2_solution_step_b_reverse(self, g2_grid: list[list[int]]) -> None:
        """Given G2 — When resolve — Then [3,3,6,4,4,1]."""
        # D-SOL-02
        # Given
        grid = g2_grid
        solver = SolvePartialMagicSquare()

        # When
        data = solver.resolve(grid)

        # Then
        assert data == G2_EXPECTED


class TestDSOL03G3Unsolvable:
    """D-SOL-03 — G3 both steps fail → UnsolvableDomainError."""

    def test_d_sol_03_g3_solution_raises_unsolvable(self, g3_grid: list[list[int]]) -> None:
        """Given G3 — When resolve — Then UnsolvableDomainError."""
        # D-SOL-03
        # Given
        grid = g3_grid
        solver = SolvePartialMagicSquare()

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solver.resolve(grid)


class TestDSOL04NumberSetContract:
    """D-SOL-04 — solution n1,n2 match {smaller,larger} from FR-03 (AC-FR05-06)."""

    def test_d_sol_04_g1_solution_numbers_match_missing_pair(
        self, g1_grid: list[list[int]]
    ) -> None:
        """Given G1 — When resolve — Then {n1,n2} == {smaller,larger}."""
        # D-SOL-04
        # Given
        grid = g1_grid
        solver = SolvePartialMagicSquare()

        # When
        data = solver.resolve(grid)

        # Then
        assert {data[2], data[5]} == {7, 10}
