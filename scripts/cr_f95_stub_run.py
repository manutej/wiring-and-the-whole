#!/usr/bin/env python3
"""CR@F95 harness stub: validate run config, grade frozen questions, emit token column — no LLM."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "experiments/cr-f95-stub/run_config.handler-wedge.v0.json"
SCHEMA = ROOT / "experiments/cr-f95-stub/schema.run_config.v0.json"
ACCURACY_SCHEMA = ROOT / "experiments/cr-f95-stub/schema.accuracy_column.v0.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_config(config: dict) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "jsonschema",
        ],
        check=True,
        capture_output=True,
    )
    import jsonschema

    schema = load_json(SCHEMA)
    jsonschema.validate(config, schema)


def run_cr_f95_stub(config_path: Path) -> dict:
    """Run CR@F95 stub harness; return report dict (raises on failure)."""
    config = load_json(config_path)
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    validate_config(config)

    questions = ROOT / config["questions_path"]
    if not questions.is_file():
        raise FileNotFoundError(f"missing questions file: {questions}")

    grade_cmd = [
        sys.executable,
        str(ROOT / "scripts/grade_l1_questions.py"),
        "--questions",
        str(questions),
    ]
    if config["expected_grade_mode"] == "io":
        grade_cmd.append("--answer-mode")
        grade_cmd.append("io")

    proc = subprocess.run(grade_cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"grade failed: {proc.stdout}\n{proc.stderr}")

    tokens_factored: int | None = None
    token_pack = config.get("token_pack_dir")
    if token_pack:
        tok_proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/handler_family_token_report.py")],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        if tok_proc.returncode != 0:
            raise RuntimeError(tok_proc.stderr)
        tok_report = json.loads(tok_proc.stdout)
        tokens_factored = tok_report["tokens"]["factored_full"]

    question_doc = load_json(questions)
    n_q = len(question_doc.get("questions") or [])

    accuracy_column = config.get("accuracy_column", None)
    if accuracy_column is not None:
        import jsonschema

        jsonschema.validate(accuracy_column, load_json(ACCURACY_SCHEMA))

    return {
        "status": "ok",
        "harness": "cr-f95-stub-v0",
        "llm_invoked": False,
        "pack_id": config["pack_id"],
        "questions_path": config["questions_path"],
        "questions_count": n_q,
        "grade_mode": config["expected_grade_mode"],
        "tokens_factored_full": tokens_factored,
        "token_budget_column": config.get("token_budget"),
        "accuracy_column": accuracy_column,
        "accuracy_column_schema": "experiments/cr-f95-stub/schema.accuracy_column.v0.json",
        "note": "Stub only — not CR@F95 accuracy; firewall + token + accuracy column plumbing.",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--write-report", type=Path, default=None)
    args = p.parse_args(argv)

    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    try:
        report = run_cr_f95_stub(config_path)
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
