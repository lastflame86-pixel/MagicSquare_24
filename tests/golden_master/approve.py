"""Approve pattern: auto-baseline or compare with unified diff on mismatch."""

from __future__ import annotations

import difflib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPECTED_PATH = PROJECT_ROOT / "tests" / "golden_master_expected.txt"


def approve_golden_master(
    actual: str,
    expected_path: Path = DEFAULT_EXPECTED_PATH,
    *,
    update: bool = False,
) -> str:
    """Apply approve pattern.

    When expected file is missing or ``update`` is True, write ``actual`` to
    ``expected_path`` and return ``"created"`` or ``"updated"``.

    When expected exists and ``update`` is False, compare line-by-line; on
    mismatch raise ``AssertionError`` with a unified diff.
    """
    expected_path = expected_path.resolve()
    expected_path.parent.mkdir(parents=True, exist_ok=True)

    if update or not expected_path.is_file():
        action = "updated" if expected_path.is_file() else "created"
        expected_path.write_text(actual, encoding="utf-8", newline="\n")
        return action

    expected = expected_path.read_text(encoding="utf-8")
    if actual == expected:
        return "matched"

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    diff_text = "".join(diff)
    raise AssertionError(
        "Golden Master mismatch (actual vs expected):\n" + diff_text
    )


def approve_section(
    actual: str,
    expected: str,
    *,
    context: str,
) -> None:
    """Compare one section block; on mismatch raise with unified diff."""
    if actual == expected:
        return
    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    diff_text = "".join(diff)
    raise AssertionError(f"{context} Golden Master mismatch:\n{diff_text}")


def read_expected_file(expected_path: Path) -> str:
    """Read baseline file (``open(expected).read()`` contract)."""
    return expected_path.read_text(encoding="utf-8")
