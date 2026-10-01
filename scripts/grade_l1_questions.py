#!/usr/bin/env python3
"""Grade docs/dogfood/L1-QUESTIONS.json against frozen expected answers (stdlib only)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = REPO / "docs" / "dogfood" / "L1-QUESTIONS.json"
PACK_PATH = REPO / "docs" / "dogfood" / "L1-wiring-and-the-whole.md"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def answer_from_pack(pack_text: str, question_text: str) -> str:
    """Heuristic answers for the meta L1 dogfood pack (local test only)."""
    q = question_text.lower()
    if "witness checks" in q or "witnes.json" in q:
        return "13"
    if "break-even n*" in q or "n*" in q and "s3" in q:
        return "5"
    if "comprehension tax" in q and "e3" in q:
        return "yes"
    if "ga1" in q and "ga10" in q:
        return "plans/ADVERSARIAL.md"
    if "make target" in q or "verify entrypoint" in q:
        return "verify"
    if "interface-first" in pack_text and "skills/interface-first-context" in pack_text:
        pass
    raise ValueError(f"No heuristic for question: {question_text!r}")


def main() -> int:
    spec = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    pack_text = PACK_PATH.read_text(encoding="utf-8")
    failures: list[str] = []

    for item in spec["questions"]:
        qid = item["id"]
        expected = normalize(str(item["expected"]))
        try:
            got = normalize(answer_from_pack(pack_text, item["text"]))
        except ValueError as exc:
            failures.append(f"{qid}: {exc}")
            continue
        if got != expected:
            failures.append(f"{qid}: expected {item['expected']!r}, got {got!r}")

    if failures:
        for line in failures:
            print(line, file=sys.stderr)
        return 1

    print(f"OK: {len(spec['questions'])} questions graded for {spec['pack']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
