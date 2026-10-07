#!/usr/bin/env python3
"""Emit jev-tape-shaped NDJSON rows for wiring pulse eval + frozen GRADES files."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EVAL_RE = re.compile(r"^EVAL (PASS|FAIL): (.+)$")


def slug(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unnamed"


def unique_slug_key(base: str, counts: dict[str, int]) -> str:
    counts[base] = counts.get(base, 0) + 1
    n = counts[base]
    if n == 1:
        return base
    return f"{base}-{n}"


def git_head(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def env_payload() -> dict:
    u = os.uname()
    uname = f"{u.sysname} {u.release} {u.machine}"
    cargo = subprocess.run(["which", "cargo"], capture_output=True).returncode == 0
    bash_line = subprocess.check_output(["bash", "--version"], text=True).splitlines()[0]
    return {"uname": uname, "cargo": cargo, "bash": bash_line}


def iter_grades(repo: Path) -> list[Path]:
    exp = repo / "experiments"
    if not exp.is_dir():
        return []
    paths = sorted(exp.rglob("*-GRADES.json"))
    return paths


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rows_from_log(text: str, repo: Path, sha: str) -> list[dict]:
    slug_counts: dict[str, int] = {}
    env = env_payload()
    now = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    eval_count = 0

    for line in text.splitlines():
        m = EVAL_RE.match(line.strip())
        if not m:
            continue
        eval_count += 1
        outcome, name = m.group(1), m.group(2)
        base = slug(name)
        slug_key = unique_slug_key(base, slug_counts)
        rows.append(
            {
                "key": f"pulse-eval:{sha[:12]}:{slug_key}",
                "command": "pulse-eval",
                "event": "pass" if outcome == "PASS" else "fail",
                "payload": {"name": name, "sha": sha, "env": env},
                "at": now,
            }
        )

    if eval_count == 0:
        return []

    for path in iter_grades(repo):
        rel = path.relative_to(repo).as_posix()
        rows.append(
            {
                "key": f"grades:{sha[:12]}:{rel}",
                "command": "grades",
                "event": "frozen",
                "payload": {"file": rel, "sha256": sha256_file(path), "sha": sha},
                "at": now,
            }
        )

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Pulse eval → tape rows (NDJSON on stdout)")
    parser.add_argument("--repo", type=Path, default=None, help="wiring-and-the-whole repo root")
    parser.add_argument("--log", type=Path, default=None, help="capture log instead of running eval")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo = (args.repo or script_dir.parent).resolve()
    sha = git_head(repo)

    if args.log:
        text = args.log.read_text(encoding="utf-8", errors="replace")
    else:
        r = subprocess.run(
            ["bash", "scripts/pulse_eval_functional.sh"],
            cwd=repo,
            capture_output=True,
            text=True,
        )
        text = r.stdout + r.stderr

    rows = rows_from_log(text, repo, sha)
    if not rows:
        return 2

    for row in rows:
        print(json.dumps(row, separators=(",", ":")))

    return 0


if __name__ == "__main__":
    sys.exit(main())
