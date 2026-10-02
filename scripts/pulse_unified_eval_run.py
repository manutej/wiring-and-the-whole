#!/usr/bin/env python3
"""Pulse unified eval: one JSON report for pack-blind-eval + cr-f95-stub (covariant harness)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from cr_f95_stub_run import run_cr_f95_stub
from pack_blind_eval_run import run_pack_blind_eval

DEFAULT_CONFIG = ROOT / "experiments/pulse-unified-eval/run_config.v0.json"
SCHEMA = ROOT / "experiments/pulse-unified-eval/schema.run_config.v0.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_unified_config(config: dict) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "jsonschema"],
        check=True,
        capture_output=True,
    )
    import jsonschema

    schema = load_json(SCHEMA)
    jsonschema.validate(config, schema)


def resolve_config_path(raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else ROOT / path


def run_pulse_unified_eval(config_path: Path) -> dict:
    config = load_json(config_path)
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    validate_unified_config(config)

    pack_cfg = resolve_config_path(config["pack_blind_eval_config"])
    cr_cfg = resolve_config_path(config["cr_f95_stub_config"])

    pack_report = run_pack_blind_eval(pack_cfg)
    cr_report = run_cr_f95_stub(cr_cfg)

    llm_invoked = bool(pack_report.get("llm_invoked")) or bool(cr_report.get("llm_invoked"))

    return {
        "status": "ok",
        "harness": config["harness_version"],
        "llm_requested": pack_report.get("llm_requested", False),
        "llm_invoked": llm_invoked,
        "pack_blind_eval": pack_report,
        "cr_f95_stub": cr_report,
        "note": (
            "Unified pulse eval — pack I/O firewall + CR@F95 stub columns in one report; "
            "LLM only when PACK_EVAL_LLM=1 and API key present."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--write-report", type=Path, default=None)
    args = p.parse_args(argv)

    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    try:
        report = run_pulse_unified_eval(config_path)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    out = json.dumps(report, indent=2) + "\n"
    if args.write_report:
        out_path = args.write_report if args.write_report.is_absolute() else ROOT / args.write_report
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
    print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
