#!/usr/bin/env python3
"""
Re-expansion gate v0: expand pack_factored.txt inst rows and byte-compare to pack_explicit.txt.
LEGEND.txt must match canonical E2 pack legend before re-expansion byte check.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_LEGEND = ROOT / "experiments/e2-tokens/pack_LEGEND.txt"


def normalize_text(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def validate_legend(pack_dir: Path) -> None:
    legend_path = pack_dir / "LEGEND.txt"
    if not legend_path.is_file():
        print(f"FAIL: missing {legend_path}", file=sys.stderr)
        sys.exit(1)
    legend = normalize_text(legend_path.read_text(encoding="utf-8"))
    canonical = normalize_text(CANONICAL_LEGEND.read_text(encoding="utf-8"))
    if legend != canonical:
        print(
            "FAIL reexpand gate: LEGEND.txt must match canonical E2 pack legend "
            f"({CANONICAL_LEGEND})",
            file=sys.stderr,
        )
        sys.exit(1)


def expand_slice_unit_row(row: str) -> list[str]:
    m = re.match(r"inst SliceUnit\((\w+), edges=\[(.*)\]\)\s*$", row.strip(), re.S)
    if not m:
        raise ValueError(f"bad SliceUnit inst row: {row!r}")
    unit, edges_s = m.groups()
    lines = [f"unit {unit}"]
    edges = [e.strip() for e in edges_s.split(",") if e.strip()]
    for target in sorted(edges):
        lines.append(f"edge {unit} -> {target}")
    return lines


def expand_command_handler_row(row: str) -> list[str]:
    stripped = row.strip()
    m6 = re.match(
        r"inst CommandHandler\((\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\s*$",
        stripped,
    )
    if m6:
        handler, dep_field, service, method, entity, action = m6.groups()
        return [
            f"unit {handler}",
            f"anno {handler} @CommandType entity={entity} action={action}",
            f"dep {handler}.{dep_field}: {service}",
            f"edge {handler} -> {service}#{method}",
        ]
    m5 = re.match(
        r"inst CommandHandler\((\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\s*$",
        stripped,
    )
    if not m5:
        raise ValueError(f"bad CommandHandler inst row: {row!r}")
    handler, service, method, entity, action = m5.groups()
    return [
        f"unit {handler}",
        f"anno {handler} @CommandType entity={entity} action={action}",
        f"dep {handler}.writePlatformService: {service}",
        f"edge {handler} -> {service}#{method}",
    ]


def expand_inst_row(row: str) -> list[str]:
    stripped = row.strip()
    if stripped.startswith("inst CommandHandler("):
        return expand_command_handler_row(row)
    if stripped.startswith("inst SliceUnit("):
        return expand_slice_unit_row(row)
    raise ValueError(f"unknown inst row: {row!r}")


def expand_factored(factored_text: str) -> str:
    lines: list[str] = []
    for raw in factored_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("motif ") or line.startswith("foreach "):
            continue
        if line.startswith("inst "):
            lines.extend(expand_inst_row(line))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Byte gate: factored pack re-expansion")
    parser.add_argument(
        "pack_dir",
        type=Path,
        help="directory containing pack_explicit.txt and pack_factored.txt",
    )
    args = parser.parse_args()
    pack_dir = args.pack_dir.resolve()
    explicit_path = pack_dir / "pack_explicit.txt"
    factored_path = pack_dir / "pack_factored.txt"

    for p in (explicit_path, factored_path):
        if not p.is_file():
            print(f"FAIL: missing {p}", file=sys.stderr)
            sys.exit(1)

    explicit = explicit_path.read_text(encoding="utf-8")
    factored = factored_path.read_text(encoding="utf-8")
    validate_legend(pack_dir)
    reexpanded = expand_factored(factored)

    if reexpanded == explicit:
        print(f"PASS reexpand gate ({pack_dir})")
        sys.exit(0)

    print(f"FAIL reexpand gate ({pack_dir}): factored expansion != pack_explicit.txt", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
