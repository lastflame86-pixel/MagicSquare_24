#!/usr/bin/env python3
"""Generate tests/golden_master_expected.txt from current Solver output.

Usage (from project root):

    python scripts/generate_golden_master_expected.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.golden_master.approve import DEFAULT_EXPECTED_PATH, approve_golden_master
from tests.golden_master.capture import capture_all_sections


def main() -> int:
    """Write golden master baseline from UIBoundary.solve captures."""
    actual = capture_all_sections()
    action = approve_golden_master(actual, update=True)
    print(f"Golden Master {action}: {DEFAULT_EXPECTED_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
