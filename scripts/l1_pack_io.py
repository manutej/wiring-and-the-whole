#!/usr/bin/env python3
"""Derive L1 dogfood answers by parsing pack markdown (I/O contract — no question-key heuristics)."""

from __future__ import annotations

import re
from pathlib import Path


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_h = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + next_h.start() if next_h else len(text)
    return text[start:end]


def catalog_unit_count(pack_text: str) -> str:
    body = section(pack_text, "Interface catalog")
    count = 0
    for line in body.splitlines():
        if re.match(r"^\|\s*`[^`]+`\s*\|", line):
            count += 1
    return str(count)


def flat_wiring_edge_count(pack_text: str) -> str:
    body = section(pack_text, "Wiring edges (flat)")
    count = sum(1 for line in body.splitlines() if line.strip().startswith("- ") and "→" in line)
    return str(count)


def skill_directory_from_pack(pack_text: str) -> str:
    match = re.search(r"\*\*Skill under test:\*\*\s*\[`([^`]+)`\]", pack_text)
    if not match:
        match = re.search(r"skills/([a-z0-9-]+)/", pack_text)
    if not match:
        raise ValueError("no skill under test in pack")
    return match.group(1)


def parallel_witness_path(pack_text: str) -> str:
    body = section(pack_text, "Parallel product boundary")
    match = re.search(r"`(witness/toybank/[^`]+/)`", body)
    if not match:
        raise ValueError("no parallel witness path in pack")
    return match.group(1)


def answer_from_pack_io(pack_path: Path, pack_text: str, question_text: str) -> str:
    q = question_text.lower()
    if "interface catalog" in q and "unit_id" in q:
        return catalog_unit_count(pack_text)
    if "wiring edges" in q and "flat" in q:
        return flat_wiring_edge_count(pack_text)
    if "skill" in q and "under test" in q:
        return skill_directory_from_pack(pack_text)
    if "parallel" in q and ("accounts" in q or "‖" in question_text):
        return parallel_witness_path(pack_text)
    raise ValueError(f"no I/O parser for question: {question_text!r}")
