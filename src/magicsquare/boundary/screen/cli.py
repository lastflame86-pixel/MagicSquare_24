"""Screen CLI entry point (RF-08)."""

from __future__ import annotations

import argparse
import sys

from magicsquare.boundary.screen.app import MagicSquareMainWindow, run_verify_diagnostic


def main(argv: list[str] | None = None) -> int:
    """Application entry point; use --verify for grid=None diagnostic only."""
    from PyQt6.QtWidgets import QApplication

    parser = argparse.ArgumentParser(description="Magic Square 4x4 screen")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run grid=None diagnostic (not the main UI)",
    )
    args = parser.parse_args(argv)

    app = QApplication(sys.argv if argv is None else argv)

    if args.verify:
        sys.stdout.write(f"{run_verify_diagnostic()}\n")
        return 0

    window = MagicSquareMainWindow()
    window.show()
    return app.exec()
