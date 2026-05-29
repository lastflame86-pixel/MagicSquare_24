"""Parse golden_master_expected.txt into per-section blocks."""

from __future__ import annotations

import re

_SECTION_HEADER = re.compile(r"^\[([a-z_]+)\]\s*$", re.MULTILINE)


def parse_sections(document: str) -> dict[str, str]:
    """Split a golden master file into ``section_id -> block`` (no trailing file newline)."""
    matches = list(_SECTION_HEADER.finditer(document))
    if not matches:
        return {}
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        section_id = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document)
        block = document[start:end].rstrip("\n")
        sections[section_id] = block
    return sections
