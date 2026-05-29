"""Magic Square 4x4 PyQt screen — wired to UIBoundary (manual verification)."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.boundary.screen.composition import create_default_boundary
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.entity.constants import CELL_MAX, GRID_SIZE
from magicsquare.entity.demo_grids import G1_GRID

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QGridLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QWidget

WINDOW_TITLE = "Magic Square 4x4"
SCREEN_CELL_MIN = 0


def _format_success(data: list[int]) -> str:
    """Format SuccessResponse data for the result label."""
    values = ", ".join(str(value) for value in data)
    return f"결과 (r1, c1, n1, r2, c2, n2): {values}"


def _format_failure(message: str) -> str:
    """Format FailureResponse message for the result label."""
    return f"오류: {message}"


class MagicSquareMainWindow:
    """Main window: 4x4 grid, solve button, result label."""

    def __init__(self, boundary: UIBoundary | None = None) -> None:
        """Build UI; inject UIBoundary at composition root."""
        from PyQt6.QtWidgets import QGridLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget

        self._boundary = boundary or create_default_boundary()
        self._spinboxes: list[list[QSpinBox]] = []

        self._window = QMainWindow()
        self._window.setWindowTitle(WINDOW_TITLE)

        central = QWidget()
        self._window.setCentralWidget(central)
        layout = QVBoxLayout(central)

        grid_layout = QGridLayout()
        for row_index in range(GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col_index in range(GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(SCREEN_CELL_MIN, CELL_MAX)
                spin.setValue(G1_GRID[row_index][col_index])
                grid_layout.addWidget(spin, row_index, col_index)
                row_boxes.append(spin)
            self._spinboxes.append(row_boxes)
        layout.addLayout(grid_layout)

        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        layout.addWidget(solve_button)

        self._result_label = QLabel("")
        layout.addWidget(self._result_label)

    def show(self) -> None:
        """Show the main window."""
        self._window.show()

    def _read_grid(self) -> list[list[int]]:
        """Read current 4x4 values from spin boxes."""
        return [[spin.value() for spin in row] for row in self._spinboxes]

    def _on_solve_clicked(self) -> None:
        """Call UIBoundary.solve and display Success or Failure on the label."""
        grid = self._read_grid()
        result = self._boundary.solve(grid)

        if isinstance(result, SuccessResponse):
            self._result_label.setText(_format_success(result.data))
        elif isinstance(result, FailureResponse):
            self._result_label.setText(_format_failure(result.error.message))
        else:
            self._result_label.setText(_format_failure("Unexpected response type"))

    @property
    def result_text(self) -> str:
        """Expose result label text for headless verification."""
        return self._result_label.text()


def run_verify_diagnostic(boundary: UIBoundary | None = None) -> str:
    """Diagnostic: UIBoundary.solve(None) — not the main UI."""
    ui = boundary or create_default_boundary()
    result = ui.solve(None)
    if isinstance(result, FailureResponse):
        return _format_failure(result.error.message)
    return _format_success(result.data)


def main(argv: list[str] | None = None) -> int:
    """Delegate to screen CLI module (RF-08)."""
    from magicsquare.boundary.screen.cli import main as cli_main

    return cli_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
