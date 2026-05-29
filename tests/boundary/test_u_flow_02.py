"""RED skeleton — U-FLOW-02 extended (AC-FR01-01, AC-FR01-08, BR-05).

Invalid Boundary input → Control execute **0** calls. Mock/spy on execute only.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.ui_boundary import UIBoundary


@pytest.fixture
def ui_boundary_with_mock_execute() -> tuple[UIBoundary, Mock]:
    """UIBoundary with mock solver.execute for call_count isolation."""
    mock_execute = Mock()
    mock_solver = Mock(execute=mock_execute)
    boundary = UIBoundary(solver=mock_solver)
    return boundary, mock_execute


class TestUFLOW02ExecuteNeverCalled:
    """U-FLOW-02 — invalid input variants; execute must not run."""

    def test_u_flow_02_null_matrix_execute_never_called(
        self, ui_boundary_with_mock_execute: tuple[UIBoundary, Mock]
    ) -> None:
        """Given matrix=None — When solve — Then E003 and execute call_count==0."""
        # Given
        # boundary, mock_execute = ui_boundary_with_mock_execute
        # matrix = None
        # When
        # result = boundary.solve(matrix)
        # Then — mock_execute.assert_not_called(); result.error.code == E003
        pytest.fail(
            "RED: U-FLOW-02 — null matrix → E003, execute never called"
        )

    def test_u_flow_02_invalid_size_execute_never_called(
        self, ui_boundary_with_mock_execute: tuple[UIBoundary, Mock]
    ) -> None:
        """Given 3x4 matrix — When solve — Then E001 and execute call_count==0."""
        # Given
        # boundary, mock_execute = ui_boundary_with_mock_execute
        # matrix = [[16,3,2,13],[5,10,11,8],[9,6,7,12]]
        # When
        # result = boundary.solve(matrix)
        pytest.fail(
            "RED: U-FLOW-02 (ext) — invalid size → E001, execute never called"
        )

    def test_u_flow_02_invalid_empty_count_execute_never_called(
        self, ui_boundary_with_mock_execute: tuple[UIBoundary, Mock]
    ) -> None:
        """Given G0 (0 empties) — When solve — Then E002 and execute call_count==0."""
        # Given
        # boundary, mock_execute = ui_boundary_with_mock_execute
        # matrix = G0_GRID
        # When
        # result = boundary.solve(matrix)
        pytest.fail(
            "RED: U-FLOW-02 (ext) — wrong empty count → E002, execute never called"
        )
