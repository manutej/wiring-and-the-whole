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


def parallel_experiments_path(pack_text: str) -> str:
    body = section(pack_text, "Parallel / upstream boundary")
    if not body:
        body = section(pack_text, "Parallel product boundary")
    match = re.search(r"`(experiments/[^`]+/)`", body)
    if not match:
        raise ValueError("no parallel experiments path in pack")
    return match.group(1)


def disburse_action_from_pack(pack_text: str) -> str:
    block = section(pack_text, "Per-unit cards")
    match = re.search(
        r"DisburseLoanCommandHandler[\s\S]*?@CommandType\([^)]*action\s*=\s*\"([^\"]+)\"",
        block,
    )
    if not match:
        raise ValueError("DisburseLoan @CommandType action not found in pack")
    return match.group(1)


def scale_metric_value(pack_text: str, row_prefix: str) -> str:
    body = section(pack_text, "Scale metrics")
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = cells[0].lower()
        if label.startswith(row_prefix.lower()) or row_prefix.lower() in label:
            return cells[1]
    raise ValueError(f"scale metric row not found: {row_prefix!r}")


def e2_reference_n_star(pack_text: str) -> str:
    body = section(pack_text, "E2 reference (CommandHandler family)")
    for line in body.splitlines():
        if line.strip().startswith("| S3"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 5:
                return cells[4]
    raise ValueError("E2 S3 n_star row not found in pack")


def context_only_handler_count(pack_text: str) -> str:
    catalog = section(pack_text, "Interface catalog")
    match = re.search(r"\*\*Context-only[^:]*:\*\*\s*(.+)$", catalog, re.MULTILINE)
    if not match:
        raise ValueError("context-only handler list not found")
    tail = match.group(1)
    count = len(re.findall(r"\b\w+CommandHandler\b", tail))
    if count == 0:
        raise ValueError("no CommandHandler names in context-only line")
    return str(count)


def answer_from_pack_io(pack_path: Path, pack_text: str, question_text: str) -> str:
    q = question_text.lower()
    name = pack_path.name.lower()

    if "interface catalog" in q and "unit_id" in q:
        return catalog_unit_count(pack_text)
    if "wiring edges" in q and "flat" in q:
        return flat_wiring_edge_count(pack_text)
    if "skill" in q and "under test" in q:
        return skill_directory_from_pack(pack_text)

    if "commandhandler-wedge" in name or "e3-commandhandler" in name:
        if "parsed into pack" in q:
            return scale_metric_value(pack_text, "Parsed into pack")
        if "skipped" in q and ("orthogonal" in q or "out of family" in q):
            return scale_metric_value(pack_text, "Skipped")
        if "inst commandhandler" in q:
            return scale_metric_value(pack_text, "inst CommandHandler")
        if "e2 s3" in q and "n*" in q:
            return e2_reference_n_star(pack_text)
        if "parallel" in q and "experiments" in q:
            return parallel_experiments_path(pack_text)
        if "disburseloan" in q and "action" in q:
            return disburse_action_from_pack(pack_text)

    if "fineract" in name or "handlers-thin" in name:
        if "parallel" in q and "experiments" in q:
            return parallel_experiments_path(pack_text)
        if "disburseloan" in q and "action" in q:
            return disburse_action_from_pack(pack_text)
        if "context-only" in q:
            return context_only_handler_count(pack_text)

    if "parallel" in q and ("accounts" in q or "‖" in question_text):
        return parallel_witness_path(pack_text)

    raise ValueError(f"no I/O parser for question: {question_text!r}")
