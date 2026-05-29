"""G-05 — Screen headless tests (MagicSquareMainWindow, run_verify_diagnostic, main).

AC: Screen composition root wired to UIBoundary; result label reflects Success/Failure.
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from unittest.mock import Mock, patch

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication

from magicsquare.boundary.error_schema import ErrorDetail, FailureResponse, SuccessResponse
from magicsquare.boundary.screen.app import (
    G1_GRID,
    MagicSquareMainWindow,
    main,
    run_verify_diagnostic,
)
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare

G1_EXPECTED_TEXT = "2, 2, 10, 3, 3, 7"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."


@pytest.fixture(scope="module")
def qapp() -> QApplication:
    """Provide a single QApplication for headless Screen tests."""
    instance = QApplication.instance()
    if instance is None:
        instance = QApplication([])
    return instance


class TestRunVerifyDiagnostic:
    """G-05 — run_verify_diagnostic grid=None diagnostic path."""

    def test_g05_verify_diagnostic_none_grid_shows_invalid_size(self) -> None:
        """Given default boundary — When run_verify_diagnostic — Then INVALID_SIZE message."""
        # G-05
        # Given / When
        result = run_verify_diagnostic()

        # Then
        assert result.startswith("오류:")
        assert INVALID_SIZE_MESSAGE in result

    def test_g05_verify_diagnostic_mock_boundary_success(self) -> None:
        """Given mock boundary Success — When run_verify_diagnostic — Then formatted success."""
        # G-05
        # Given
        mock_boundary = Mock(spec=UIBoundary)
        mock_boundary.solve.return_value = SuccessResponse(data=[1, 1, 1, 2, 2, 2])

        # When
        result = run_verify_diagnostic(boundary=mock_boundary)

        # Then
        assert "1, 1, 1, 2, 2, 2" in result


class TestMagicSquareMainWindow:
    """G-05 — MagicSquareMainWindow headless solve and result label."""

    def test_g05_g1_default_solve_shows_success(self, qapp: QApplication) -> None:
        """Given G1 preloaded grid — When solve clicked — Then success label with int[6]."""
        # G-05
        # Given
        window = MagicSquareMainWindow()

        # When
        window._on_solve_clicked()

        # Then
        assert G1_EXPECTED_TEXT in window.result_text

    def test_g05_mock_boundary_failure_shows_error(self, qapp: QApplication) -> None:
        """Given mock FailureResponse — When solve clicked — Then error label."""
        # G-05
        # Given
        mock_boundary = Mock(spec=UIBoundary)
        mock_boundary.solve.return_value = FailureResponse(
            type="ERROR",
            error=ErrorDetail(code="E006", message="UNSOLVABLE: no valid magic square completion"),
        )
        window = MagicSquareMainWindow(boundary=mock_boundary)

        # When
        window._on_solve_clicked()

        # Then
        assert window.result_text.startswith("오류:")
        assert "UNSOLVABLE" in window.result_text

    def test_g05_unexpected_response_type_shows_fallback_error(
        self, qapp: QApplication
    ) -> None:
        """Given unexpected solve return — When solve clicked — Then fallback error label."""
        # G-05
        # Given
        mock_boundary = Mock(spec=UIBoundary)
        mock_boundary.solve.return_value = "unexpected"
        window = MagicSquareMainWindow(boundary=mock_boundary)

        # When
        window._on_solve_clicked()

        # Then
        assert window.result_text == "오류: Unexpected response type"

    def test_g05_read_grid_returns_current_spinbox_values(self, qapp: QApplication) -> None:
        """Given window with G1 defaults — When _read_grid — Then matches G1_GRID."""
        # G-05
        # Given
        window = MagicSquareMainWindow()

        # When
        grid = window._read_grid()

        # Then
        assert grid == G1_GRID

    def test_g05_show_does_not_raise(self, qapp: QApplication) -> None:
        """Given window — When show — Then no exception (headless smoke)."""
        # G-05
        # Given
        window = MagicSquareMainWindow(boundary=UIBoundary(solver=SolvePartialMagicSquare()))

        # When / Then
        window.show()


class TestMainEntryPoint:
    """G-05 — main() --verify and normal launch paths."""

    def test_g05_main_verify_mode_prints_diagnostic(
        self, qapp: QApplication, capsys
    ) -> None:
        """Given --verify — When main — Then diagnostic printed and exit 0."""
        # G-05
        # Given
        with patch("PyQt6.QtWidgets.QApplication", return_value=qapp):
            # When
            exit_code = main(["--verify"])

        # Then
        captured = capsys.readouterr()
        assert exit_code == 0
        assert INVALID_SIZE_MESSAGE in captured.out

    def test_g05_main_ui_mode_exits_when_app_exec_returns(self) -> None:
        """Given no --verify — When main — Then window shown and app.exec result returned."""
        # G-05
        # Given
        mock_app = Mock()
        mock_app.exec.return_value = 0
        with (
            patch("PyQt6.QtWidgets.QApplication", return_value=mock_app),
            patch("magicsquare.boundary.screen.app.MagicSquareMainWindow") as mock_window_cls,
        ):
            # When
            exit_code = main([])

        # Then
        assert exit_code == 0
        mock_app.exec.assert_called_once()
        mock_window_cls.return_value.show.assert_called_once()
