#!/usr/bin/env python3
"""Time validate → extract → pack → reexpand per slice-matrix shard (JSON to stdout)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fixtures/slice-matrix/manifest.v0.json"
SCHEMA = ROOT / "wiringmap/schema.v0.json"
CRATE = ROOT / "crates/wiring-core"
CANONICAL_LEGEND = ROOT / "experiments/e2-tokens/pack_LEGEND.txt"


def run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def ensure_rust() -> None:
    if not shutil_which("cargo"):
        raise RuntimeError("cargo not installed")
    proc = run(
        ["cargo", "build", "--quiet", "--manifest-path", f"{CRATE}/Cargo.toml", "--release", "--bins"]
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)


def shutil_which(name: str) -> str | None:
    from shutil import which

    return which(name)


def validate_wm(engine: str, inst: Path) -> None:
    if engine == "rust":
        bin_path = CRATE / "target/release/wiring-validate"
        proc = run([str(bin_path), "--schema", str(SCHEMA), "--instance", str(inst)])
    else:
        proc = run([sys.executable, str(ROOT / "scripts/validate_wiringmap.py"), str(SCHEMA), str(inst)])
    if proc.returncode != 0:
        raise RuntimeError(f"validate: {proc.stderr or proc.stdout}")


def extract_refs(engine: str, refs_dir: Path, wm: Path) -> None:
    if engine == "rust":
        bin_path = CRATE / "target/release/wiring-extract-java-refs"
        proc = run([str(bin_path), str(refs_dir), "--example", str(wm)])
    else:
        proc = run(
            [sys.executable, str(ROOT / "scripts/extract_refs.py"), str(refs_dir), "--example", str(wm)]
        )
    if proc.returncode != 0:
        raise RuntimeError(f"extract: {proc.stderr or proc.stdout}")


def build_pack(engine: str, wm: Path) -> Path:
    if engine == "rust":
        bin_path = CRATE / "target/release/wiring-build-l2-pack"
        proc = run([str(bin_path), str(wm), "--canonical-legend", str(CANONICAL_LEGEND)])
    else:
        proc = run([sys.executable, str(ROOT / "scripts/build_l2_pack.py"), str(wm)])
    if proc.returncode != 0:
        raise RuntimeError(f"pack: {proc.stderr or proc.stdout}")
    return Path(str(wm).replace(".json", ".pack"))


def reexpand_pack(engine: str, pack_dir: Path) -> None:
    if engine == "rust":
        bin_path = CRATE / "target/release/wiring-reexpand"
        proc = run([str(bin_path), str(pack_dir), "--canonical-legend", str(CANONICAL_LEGEND)])
    else:
        proc = run([sys.executable, str(ROOT / "scripts/reexpand_gate.py"), str(pack_dir)])
    if proc.returncode != 0:
        raise RuntimeError(f"reexpand: {proc.stderr or proc.stdout}")


def time_slice(engine: str, sid: str, refs_rel: str, wm_rel: str) -> dict[str, object]:
    refs = ROOT / refs_rel
    wm = ROOT / wm_rel
    steps: dict[str, float] = {}
    t0 = time.perf_counter()
    t = time.perf_counter()
    validate_wm(engine, wm)
    steps["validate_ms"] = round((time.perf_counter() - t) * 1000, 2)
    t = time.perf_counter()
    extract_refs(engine, refs, wm)
    steps["extract_ms"] = round((time.perf_counter() - t) * 1000, 2)
    t = time.perf_counter()
    pack_path = build_pack(engine, wm)
    steps["pack_ms"] = round((time.perf_counter() - t) * 1000, 2)
    t = time.perf_counter()
    reexpand_pack(engine, pack_path)
    steps["reexpand_ms"] = round((time.perf_counter() - t) * 1000, 2)
    steps["total_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    java_files = len(list(refs.rglob("*.java"))) if refs.is_dir() else 0
    return {"id": sid, "refs_dir": refs_rel, "java_files": java_files, "steps_ms": steps}


def main() -> int:
    engine = os.environ.get("WIRING_ENGINE", "rust")
    if engine not in ("rust", "python"):
        print(f"ERROR: invalid WIRING_ENGINE={engine}", file=sys.stderr)
        return 1
    if engine == "rust":
        ensure_rust()

    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    slices: list[dict[str, object]] = []
    for sl in doc.get("slices") or []:
        slices.append(time_slice(engine, sl["id"], sl["refs_dir"], sl["wiringmap"]))

    out = {
        "schema_version": "slice-matrix-timing.v0",
        "wiring_engine": engine,
        "slice_count": len(slices),
        "slices": slices,
        "total_ms": round(sum(float(s["steps_ms"]["total_ms"]) for s in slices), 2),  # type: ignore[index]
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
