#!/usr/bin/env bash
# Run validate + extract over density ladder (D0–D3). Subcommand non-zero exits are
# expected for adversarial fixtures; this script exits 0 when all expectations match.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="${ROOT}/fixtures/density/stress_manifest.json"
SCHEMA="${ROOT}/wiringmap/schema.v0.json"

if [[ ! -f "${MANIFEST}" ]]; then
  echo "ERROR: missing stress manifest: ${MANIFEST}" >&2
  exit 1
fi

python3 -m pip install -q jsonschema

python3 - "${ROOT}" "${SCHEMA}" "${MANIFEST}" <<'PY'
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
schema = Path(sys.argv[2])
manifest_path = Path(sys.argv[3])
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

failures: list[str] = []


def run(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


for case in manifest["cases"]:
    cid = case["id"]
    label = case.get("label", cid)
    expect = case["expect"]
    refs_dir = root / case["refs_dir"]

    print(f"=== {cid}: {label} ===")

    if "validate_instance" in case:
        instance = root / case["validate_instance"]
        code = run(
            [
                "python3",
                "scripts/validate_wiringmap.py",
                str(schema),
                str(instance),
            ]
        )
        want = expect.get("validate_exit")
        if want is not None and code != want:
            failures.append(
                f"{cid} validate: expected exit {want}, got {code} ({instance})"
            )
        else:
            print(f"{cid} validate: exit {code} (expected {want})", file=sys.stderr)

    if "extract_example" in case:
        example = root / case["extract_example"]
        code = run(
            [
                "python3",
                "scripts/extract_refs.py",
                str(refs_dir),
                "--example",
                str(example),
            ]
        )
        want = expect.get("extract_exit")
        if want is not None and code != want:
            failures.append(
                f"{cid} extract: expected exit {want}, got {code} ({refs_dir})"
            )
        else:
            print(f"{cid} extract: exit {code} (expected {want})", file=sys.stderr)

    print()

if failures:
    for line in failures:
        print(line, file=sys.stderr)
    sys.exit(1)

print(
    f"OK: {len(manifest['cases'])} density cases matched expectations "
    f"({manifest_path.relative_to(root)})",
    file=sys.stderr,
)
PY
