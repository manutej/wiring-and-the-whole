#!/usr/bin/env python3
"""
Wedge: build L2 CommandHandler family pack from experiments/e3-ablation/raw (PATH LIST scale).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from command_handler_parse import HandlerSpec, explicit_block, inst_row, parse_handler_java

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = ROOT / "experiments/e3-ablation/raw"
DEFAULT_OUT = ROOT / "fixtures/e3-commandhandler-wedge/pack"
MOTIF_PATH = ROOT / "experiments/e2-tokens/pack_S3_motif.txt"
LEGEND_PATH = ROOT / "experiments/e2-tokens/pack_LEGEND.txt"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--limit", type=int, default=0, help="0 = all CommandHandler.java files")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw_dir = args.raw_dir if args.raw_dir.is_absolute() else ROOT / args.raw_dir
    out_dir = args.out if args.out.is_absolute() else ROOT / args.out

    paths = sorted(raw_dir.glob("*CommandHandler.java"))
    if args.limit > 0:
        paths = paths[: args.limit]

    specs: list[HandlerSpec] = []
    skipped: list[dict[str, str]] = []
    for path in paths:
        spec = parse_handler_java(path)
        if spec is None:
            skipped.append({"file": path.name, "reason": "no @CommandType or writePlatformService call"})
            continue
        specs.append(spec)

    if not specs:
        print("ERROR: no handlers parsed", file=sys.stderr)
        return 1

    specs.sort(key=lambda s: s.handler)
    motif = MOTIF_PATH.read_text(encoding="utf-8").rstrip() + "\n"
    legend = LEGEND_PATH.read_text(encoding="utf-8")
    if not legend.endswith("\n"):
        legend += "\n"

    explicit_lines: list[str] = []
    inst_lines: list[str] = []
    for spec in specs:
        explicit_lines.extend(explicit_block(spec))
        inst_lines.append(inst_row(spec))

    explicit = "\n".join(explicit_lines) + "\n"
    factored = motif + "\n" + "\n".join(inst_lines) + "\n"

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "LEGEND.txt").write_text(legend, encoding="utf-8")
    (out_dir / "pack_explicit.txt").write_text(explicit, encoding="utf-8")
    (out_dir / "pack_factored.txt").write_text(factored, encoding="utf-8")

    manifest = {
        "raw_dir": str(raw_dir.relative_to(ROOT) if raw_dir.is_relative_to(ROOT) else raw_dir),
        "parsed": len(specs),
        "skipped": skipped,
        "handlers": [s.handler for s in specs],
    }
    (out_dir.parent / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {out_dir} ({len(specs)} handlers, {len(skipped)} skipped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
