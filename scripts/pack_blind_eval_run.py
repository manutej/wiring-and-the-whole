#!/usr/bin/env python3
"""Blind pack-only eval: bundle L1 markdown + question text (no answers); stub grades via I/O parser."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "experiments/pack-blind-eval/run_config.v0.json"
SCHEMA = ROOT / "experiments/pack-blind-eval/schema.run_config.v0.json"
DEFAULT_BUNDLE_DIR = ROOT / "fixtures/pack-blind-eval/bundles"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_config(config: dict) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "jsonschema"],
        check=True,
        capture_output=True,
    )
    import jsonschema

    schema = load_json(SCHEMA)
    jsonschema.validate(config, schema)


def prompt_questions(questions_doc: dict) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in questions_doc.get("questions") or []:
        out.append({"id": str(item["id"]), "text": str(item["text"])})
    return out


def build_bundle(case: dict, questions_doc: dict, pack_text: str) -> dict:
    return {
        "harness": "pack-blind-eval-v0",
        "pack_id": case["pack_id"],
        "pack_path": questions_doc["pack"],
        "pack_markdown": pack_text,
        "questions": prompt_questions(questions_doc),
    }


def assert_firewall(bundle: dict) -> None:
    """Prompt bundle must not ship grader keys (answers live in frozen questions JSON only)."""
    for item in bundle.get("questions") or []:
        if "expected" in item:
            raise ValueError(f"prompt question {item.get('id')} must not include expected")


def grade_case(questions_path: Path, grade_mode: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(ROOT / "scripts/grade_l1_questions.py"),
        "--questions",
        str(questions_path),
        "--answer-mode",
        grade_mode,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def llm_answer_one(pack_markdown: str, question_text: str) -> str | None:
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("PACK_EVAL_OPENAI_API_KEY")
    if not api_key:
        return None
    model = os.environ.get("PACK_EVAL_MODEL", "gpt-4o-mini")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    system = (
        "Answer using ONLY the provided L1 context pack. "
        "Reply with the answer string only — no explanation."
    )
    user = f"--- PACK ---\n{pack_markdown}\n--- QUESTION ---\n{question_text}"
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"WARN: LLM call failed: {exc}", file=sys.stderr)
        return None
    choices = payload.get("choices") or []
    if not choices:
        return None
    content = choices[0].get("message", {}).get("content", "")
    return content.strip()


def run_llm_lane(bundle: dict, questions_doc: dict) -> dict:
    results: list[dict[str, str | bool | None]] = []
    for pq, full in zip(bundle["questions"], questions_doc["questions"], strict=True):
        raw = llm_answer_one(bundle["pack_markdown"], pq["text"])
        expected = str(full["expected"])
        match = raw is not None and raw.strip().lower() == expected.strip().lower()
        results.append(
            {
                "id": pq["id"],
                "llm_answer": raw,
                "expected": expected,
                "match": match if raw is not None else None,
            }
        )
    return {"llm_results": results}


def run_pack_blind_eval(
    config_path: Path,
    *,
    write_bundles: Path = DEFAULT_BUNDLE_DIR,
    skip_bundle_write: bool = False,
) -> dict:
    """Run blind pack eval; return summary report dict (raises on failure)."""
    config = load_json(config_path)
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    validate_config(config)

    llm_requested = os.environ.get("PACK_EVAL_LLM", "").strip() in ("1", "true", "yes")
    llm_invoked = False
    case_reports: list[dict] = []

    bundle_dir = write_bundles if write_bundles.is_absolute() else ROOT / write_bundles
    if not skip_bundle_write:
        bundle_dir.mkdir(parents=True, exist_ok=True)

    for case in config["cases"]:
        questions_path = ROOT / case["questions_path"]
        questions_doc = load_json(questions_path)
        if not isinstance(questions_doc, dict):
            raise ValueError(f"invalid questions doc: {questions_path}")

        pack_path = ROOT / questions_doc["pack"]
        pack_text = pack_path.read_text(encoding="utf-8")
        bundle = build_bundle(case, questions_doc, pack_text)
        assert_firewall(bundle)

        if not skip_bundle_write:
            out_path = bundle_dir / f"{case['pack_id']}.prompt.json"
            out_path.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")

        proc = grade_case(questions_path, case["grade_mode"])
        if proc.returncode != 0:
            raise RuntimeError(f"grade failed: {proc.stdout}\n{proc.stderr}")

        report: dict = {
            "pack_id": case["pack_id"],
            "questions_path": case["questions_path"],
            "grade_mode": case["grade_mode"],
            "stub_io_grade": "ok",
            "questions_count": len(questions_doc.get("questions") or []),
            "firewall": "no_expected_in_prompt_bundle",
        }

        if llm_requested:
            api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("PACK_EVAL_OPENAI_API_KEY")
            if not api_key:
                report["llm_lane"] = "skipped_no_api_key"
            else:
                llm_invoked = True
                report["llm_lane"] = run_llm_lane(bundle, questions_doc)
        case_reports.append(report)

    return {
        "status": "ok",
        "harness": config["harness_version"],
        "cases": case_reports,
        "llm_requested": llm_requested,
        "llm_invoked": llm_invoked,
        "note": "Stub mode proves pack I/O grading firewall; LLM lane optional via PACK_EVAL_LLM=1.",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument(
        "--write-bundles",
        type=Path,
        default=DEFAULT_BUNDLE_DIR,
        help="Write prompt-only bundles for external grading (default: fixtures/pack-blind-eval/bundles)",
    )
    p.add_argument("--skip-bundle-write", action="store_true")
    args = p.parse_args(argv)

    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    try:
        summary = run_pack_blind_eval(
            config_path,
            write_bundles=args.write_bundles,
            skip_bundle_write=args.skip_bundle_write,
        )
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
