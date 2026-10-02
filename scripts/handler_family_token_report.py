#!/usr/bin/env python3
"""Token report for E3 CommandHandler family wedge (same tokcount.js as E2)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E2_DIR = ROOT / "experiments/e2-tokens"
DEFAULT_PACK = ROOT / "fixtures/e3-commandhandler-wedge/pack"
DEFAULT_OUT = ROOT / "fixtures/e3-commandhandler-wedge/token_report.json"
E2_S3 = ROOT / "experiments/e2-tokens/E2-RESULTS.json"
FAMILY_N = 514


def tokcount(texts: dict[str, str]) -> dict[str, int]:
    proc = subprocess.run(
        ["node", str(E2_DIR / "tokcount.js")],
        input=json.dumps(texts),
        capture_output=True,
        text=True,
        check=True,
        cwd=str(E2_DIR),
    )
    return json.loads(proc.stdout)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pack-dir", type=Path, default=DEFAULT_PACK)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--write", action="store_true", help="Write JSON report to --out")
    args = p.parse_args(argv)

    pack_dir = args.pack_dir if args.pack_dir.is_absolute() else ROOT / args.pack_dir
    explicit = (pack_dir / "pack_explicit.txt").read_text(encoding="utf-8")
    factored = (pack_dir / "pack_factored.txt").read_text(encoding="utf-8")
    legend = (pack_dir / "LEGEND.txt").read_text(encoding="utf-8")
    motif_path = E2_DIR / "pack_S3_motif.txt"
    motif = motif_path.read_text(encoding="utf-8")

    inst_lines = [
        line.strip()
        for line in factored.splitlines()
        if line.strip().startswith("inst CommandHandler(")
    ]
    n = len(inst_lines)
    if n == 0:
        print("ERROR: no inst CommandHandler rows", file=sys.stderr)
        return 1

    per_row = inst_lines[0] + "\n"
    per_explicit = "\n".join(explicit.splitlines()[:4]) + "\n"

    tok = tokcount(
        {
            "legend": legend,
            "motif": motif,
            "explicit_full": explicit,
            "factored_full": factored,
            "per_explicit": per_explicit,
            "per_row": per_row,
        }
    )

    e_one = tok["per_explicit"]
    m_one = tok["per_row"]
    f_fixed = tok["legend"] + tok["motif"]
    n_star = float("inf") if e_one <= m_one else -(-f_fixed // (e_one - m_one))

    e2_s3 = json.loads(E2_S3.read_text(encoding="utf-8"))["sites"]["S3"]
    report = {
        "pack_dir": str(pack_dir.relative_to(ROOT)),
        "handlers_inst_rows": n,
        "tokenizer": "cl100k_base (tiktoken npm, vendored encoder)",
        "tokens": {
            "legend": tok["legend"],
            "motif": tok["motif"],
            "explicit_full": tok["explicit_full"],
            "factored_full": tok["factored_full"],
            "per_handler_explicit": e_one,
            "per_handler_inst_row": m_one,
            "fixed_overhead_legend_plus_motif": f_fixed,
        },
        "breakeven": {
            "n_star_from_per_handler_rates": n_star,
            "n_actual_repo_wide_CommandHandler": FAMILY_N,
            "verdict_at_n": (
                "WIN"
                if e_one > m_one and n_star < FAMILY_N
                else ("KILL" if e_one <= m_one else "AMBIGUOUS")
            ),
        },
        "e2_S3_frozen_reference": {
            "e_explicit_tokens": e2_s3["e_explicit_tokens"],
            "m_factored_row_tokens": e2_s3["m_factored_row_tokens"],
            "F_fixed_overhead_tokens": e2_s3["F_fixed_overhead_tokens"],
            "n_star_breakeven": e2_s3["n_star_breakeven"],
        },
        "consistency_checks": {
            "per_handler_explicit_matches_e2_S3": e_one == e2_s3["e_explicit_tokens"],
            "per_handler_row_matches_e2_S3": m_one == e2_s3["m_factored_row_tokens"],
        },
    }

    if args.write:
        out = args.out if args.out.is_absolute() else ROOT / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    if f_fixed != e2_s3["F_fixed_overhead_tokens"]:
        print("FAIL: legend+motif token overhead != E2 S3 F_fixed", file=sys.stderr)
        return 1
    if e_one <= m_one:
        print("FAIL: factored row not cheaper than explicit per handler", file=sys.stderr)
        return 1
    if n_star >= FAMILY_N:
        print("FAIL: breakeven n* not below repo-wide CommandHandler count", file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
