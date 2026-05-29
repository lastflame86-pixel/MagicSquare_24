"""U-OUT-01~03 (AC-FR05-04~07, AC-FR05-03/08, PRD Success/E006/E007).

Control resolve Mock allowed (PRD §15.1). Domain Entity Mock forbidden.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.error_mapper import E006_CODE, E006_MESSAGE
from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import UnsolvableDomainError
from tests.entity.conftest import G1_GRID, G3_GRID

G1_EXPECTED = [2, 2, 10, 3, 3, 7]


@pytest.fixture
def ui_boundary_with_mock_resolve() -> tuple[UIBoundary, Mock]:
    """UIBoundary with mock solver.resolve — spy call_count in isolation tests."""
    mock_resolve = Mock(return_value=G1_EXPECTED)
    mock_solver = Mock(resolve=mock_resolve)
    boundary = UIBoundary(solver=mock_solver)
    return boundary, mock_resolve


class TestSuccessOutputContract:
    """U-OUT-01 — Success envelope (AC-FR05-04, AC-FR05-07, BR-20)."""

    def test_u_out_01_success_returns_int_six_tuple(self) -> None:
        """Given G1 — When solve — Then type OK, data int[6], no error field."""
        # U-OUT-01
        # Given
        boundary = UIBoundary(solver=SolvePartialMagicSquare())
        grid = [row[:] for row in G1_GRID]

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, SuccessResponse)
        assert result.type == "OK"
        assert result.data == G1_EXPECTED
        assert len(result.data) == 6
        assert "error" not in SuccessResponse.model_fields


class TestUOUT01SuccessDataLength:
    """U-OUT-01 — valid G1 solve → OK, len(data)==6."""

    def test_u_out_01_valid_g1_solve_data_length_six(
        self, ui_boundary_with_mock_resolve: tuple[UIBoundary, Mock]
    ) -> None:
        """Given G1 + mock resolve — When solve — Then type OK, len(data)==6."""
        # U-OUT-01
        # Given
        boundary, _mock_resolve = ui_boundary_with_mock_resolve
        grid = [row[:] for row in G1_GRID]

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, SuccessResponse)
        assert result.type == "OK"
        assert len(result.data) == 6
        assert "error" not in SuccessResponse.model_fields


class TestUOUT02OneIndexedCoords:
    """U-OUT-02 — G1 solve coordinates 1-indexed in [1,4]."""

    def test_u_out_02_valid_g1_solve_coords_one_indexed(self) -> None:
        """Given G1 — When solve — Then data[0,1,3,4] in [1,4]."""
        # U-OUT-02
        # Given
        boundary = UIBoundary(solver=SolvePartialMagicSquare())
        grid = [row[:] for row in G1_GRID]

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, SuccessResponse)
        for index in (0, 1, 3, 4):
            assert 1 <= result.data[index] <= 4


class TestUOUT03DomainErrorMapping:
    """U-OUT-03 — ErrorMapper: Domain failure → Boundary E006/E007."""

    def test_u_out_03_g3_unsolvable_maps_to_e006(self) -> None:
        """Given G3 — When solve — Then E006."""
        # U-OUT-03
        # Given
        boundary = UIBoundary(solver=SolvePartialMagicSquare())
        grid = [row[:] for row in G3_GRID]

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.error.code == E006_CODE
        assert result.error.message == E006_MESSAGE

    def test_u_out_03_mock_unsolvable_maps_to_e006(
        self, ui_boundary_with_mock_resolve: tuple[UIBoundary, Mock]
    ) -> None:
        """Given mock resolve raising UnsolvableDomainError — When solve — Then E006."""
        # U-OUT-03 — ErrorMapper isolation
        # Given
        boundary, mock_resolve = ui_boundary_with_mock_resolve
        mock_resolve.side_effect = UnsolvableDomainError("no valid magic square completion")
        grid = [row[:] for row in G1_GRID]

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, FailureResponse)
        assert result.error.code == E006_CODE
