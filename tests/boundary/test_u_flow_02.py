"""U-FLOW-02 extended (AC-FR01-01, AC-FR01-08, BR-05).

Invalid Boundary input → Control resolve **0** calls. Mock/spy on resolve only.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from magicsquare.boundary.error_schema import FailureResponse
from magicsquare.boundary.input_validator import E002_CODE, INVALID_SIZE_CODE
from magicsquare.boundary.ui_boundary import UIBoundary
from tests.entity.conftest import G0_GRID


@pytest.fixture
def ui_boundary_with_mock_resolve() -> tuple[UIBoundary, Mock]:
    """UIBoundary with mock solver.resolve for call_count isolation."""
    mock_resolve = Mock()
    mock_solver = Mock(resolve=mock_resolve)
    boundary = UIBoundary(solver=mock_solver)
    return boundary, mock_resolve


class TestUFLOW02ResolveNeverCalled:
    """U-FLOW-02 — invalid input variants; resolve must not run."""

    def test_u_flow_02_null_matrix_resolve_never_called(
        self, ui_boundary_with_mock_resolve: tuple[UIBoundary, Mock]
    ) -> None:
        """Given matrix=None — When solve — Then INVALID_SIZE and resolve call_count==0."""
        # U-FLOW-02
        # Given
        boundary, mock_resolve = ui_boundary_with_mock_resolve

        # When
        result = boundary.solve(None)

        # Then
        mock_resolve.assert_not_called()
        assert isinstance(result, FailureResponse)
        assert result.error.code == INVALID_SIZE_CODE

    def test_u_flow_02_invalid_size_resolve_never_called(
        self, ui_boundary_with_mock_resolve: tuple[UIBoundary, Mock]
    ) -> None:
        """Given 3x4 matrix — When solve — Then INVALID_SIZE and resolve call_count==0."""
        # U-FLOW-02 (ext)
        # Given
        boundary, mock_resolve = ui_boundary_with_mock_resolve
        matrix = [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12]]

        # When
        result = boundary.solve(matrix)

        # Then
        mock_resolve.assert_not_called()
        assert isinstance(result, FailureResponse)
        assert result.error.code == INVALID_SIZE_CODE

    def test_u_flow_02_invalid_empty_count_resolve_never_called(
        self, ui_boundary_with_mock_resolve: tuple[UIBoundary, Mock]
    ) -> None:
        """Given G0 (0 empties) — When solve — Then E002 and resolve call_count==0."""
        # U-FLOW-02 (ext)
        # Given
        boundary, mock_resolve = ui_boundary_with_mock_resolve
        matrix = [row[:] for row in G0_GRID]

        # When
        result = boundary.solve(matrix)

        # Then
        mock_resolve.assert_not_called()
        assert isinstance(result, FailureResponse)
        assert result.error.code == E002_CODE
