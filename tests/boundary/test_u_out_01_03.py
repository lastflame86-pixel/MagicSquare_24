"""RED skeleton — U-OUT-01~03 (AC-FR05-04~07, AC-FR05-03/08, PRD Success/E006/E007).

Control execute Mock allowed (PRD §15.1). Domain Entity Mock forbidden.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.ui_boundary import UIBoundary


@pytest.fixture
def ui_boundary_with_mock_execute() -> tuple[UIBoundary, Mock]:
    """UIBoundary with mock solver.execute — spy call_count in GREEN phase."""
    mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
    mock_solver = Mock(execute=mock_execute)
    boundary = UIBoundary(solver=mock_solver)
    return boundary, mock_execute


class TestUOUT01SuccessDataLength:
    """U-OUT-01 — valid G1 solve → OK, len(data)==6."""

    def test_u_out_01_valid_g1_solve_data_length_six(
        self, ui_boundary_with_mock_execute: tuple[UIBoundary, Mock]
    ) -> None:
        """Given G1 + mock execute — When solve — Then type OK, len(data)==6."""
        # Given
        # boundary, mock_execute = ui_boundary_with_mock_execute
        # matrix = G1_GRID
        # mock_execute.return_value = [2, 2, 7, 3, 3, 10]
        # When
        # result = boundary.solve(matrix)
        # Then — (Full RED in GREEN phase)
        pytest.fail(
            "RED: U-OUT-01 — G1 solve → type OK, len(data)==6, no error field"
        )


class TestUOUT02OneIndexedCoords:
    """U-OUT-02 — G1 solve coordinates 1-indexed in [1,4]."""

    def test_u_out_02_valid_g1_solve_coords_one_indexed(
        self, ui_boundary_with_mock_execute: tuple[UIBoundary, Mock]
    ) -> None:
        """Given G1 + mock — When solve — Then data[0,1,3,4] in [1,4]."""
        # Given
        # boundary, mock_execute = ui_boundary_with_mock_execute
        # matrix = G1_GRID
        # When
        # result = boundary.solve(matrix)
        pytest.fail(
            "RED: U-OUT-02 — G1 solve coords r1,c1,r2,c2 are 1-indexed in [1,4]"
        )


class TestUOUT03DomainErrorMapping:
    """U-OUT-03 — ErrorMapper: Domain failure → Boundary E006/E007."""

    def test_u_out_03_g3_unsolvable_maps_to_e006(
        self, ui_boundary_with_mock_execute: tuple[UIBoundary, Mock]
    ) -> None:
        """Given G3 + mock raising UnsolvableDomainError — When solve — Then E006."""
        # Given
        # boundary, mock_execute = ui_boundary_with_mock_execute
        # matrix = G3_GRID
        # mock_execute.side_effect = UnsolvableDomainError(...)
        # When
        # result = boundary.solve(matrix)  # via ErrorMapper
        pytest.fail(
            "RED: U-OUT-03 — G3 unsolvable → E006 UNSOLVABLE (ErrorMapper)"
        )
