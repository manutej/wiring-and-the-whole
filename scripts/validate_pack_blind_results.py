#!/usr/bin/env python3
"""Validate archived pack-blind eval results JSON and optional live-run alignment."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "experiments/pack-blind-eval/results/stub.report.v0.json"
DEFAULT_SCHEMA = ROOT / "experiments/pack-blind-eval/results/schema.results.v0.json"
DEFAULT_CONFIG = ROOT / "experiments/pack-blind-eval/run_config.v0.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(doc: dict, schema_path: Path) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "jsonschema"],
        check=True,
        capture_output=True,
    )
    import jsonschema

    schema = load_json(schema_path)
    jsonschema.validate(doc, schema)


def case_fingerprint(case: dict) -> tuple:
    return (
        case["pack_id"],
        case["questions_path"],
        case["grade_mode"],
        case["stub_io_grade"],
        case["questions_count"],
        case["firewall"],
    )


def live_summary(config_path: Path) -> dict:
    sys.path.insert(0, str(ROOT / "scripts"))
    from pack_blind_eval_run import run_pack_blind_eval

    summary = run_pack_blind_eval(
        config_path,
        skip_bundle_write=True,
    )
    return summary


def align_live_to_artifact(live: dict, artifact: dict) -> list[str]:
    errors: list[str] = []
    if live.get("status") != artifact.get("status"):
        errors.append(f"status live={live.get('status')!r} artifact={artifact.get('status')!r}")
    if live.get("harness") != artifact.get("harness"):
        errors.append(f"harness live={live.get('harness')!r} artifact={artifact.get('harness')!r}")
    live_fps = sorted(case_fingerprint(c) for c in live.get("cases") or [])
    art_fps = sorted(case_fingerprint(c) for c in artifact.get("cases") or [])
    if live_fps != art_fps:
        errors.append("case fingerprints differ between live run and archived artifact")
    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    p.add_argument(
        "--compare-live",
        action="store_true",
        help="Run pack-blind harness (no bundle write) and match case rows to artifact",
    )
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = p.parse_args(argv)

    artifact_path = args.artifact if args.artifact.is_absolute() else ROOT / args.artifact
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema
    config_path = args.config if args.config.is_absolute() else ROOT / args.config

    doc = load_json(artifact_path)
    if not isinstance(doc, dict):
        print("ERROR: artifact must be a JSON object", file=sys.stderr)
        return 1

    try:
        validate_schema(doc, schema_path)
    except Exception as exc:
        print(f"ERROR: schema validation failed: {exc}", file=sys.stderr)
        return 1

    if args.compare_live:
        try:
            live = live_summary(config_path)
        except Exception as exc:
            print(f"ERROR: live pack-blind run failed: {exc}", file=sys.stderr)
            return 1
        mismatches = align_live_to_artifact(live, doc)
        if mismatches:
            for msg in mismatches:
                print(f"ERROR: {msg}", file=sys.stderr)
            return 1

    print(
        json.dumps(
            {
                "check": "pack-blind-results",
                "artifact": str(artifact_path.relative_to(ROOT)),
                "schema_ok": True,
                "live_aligned": bool(args.compare_live),
                "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
