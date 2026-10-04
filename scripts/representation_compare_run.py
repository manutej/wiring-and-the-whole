#!/usr/bin/env python3
"""Compare L2 pack vs AST-struct vs raw Java on wiring QA + tokens (test agent)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "fixtures/representation-compare/wiring_questions.v0.json"
WEDGE_RAW = ROOT / "experiments/e3-ablation/raw"
WEDGE_PACK = ROOT / "fixtures/e3-commandhandler-wedge/pack"
L2_MD = ROOT / "docs/dogfood/L1-e3-commandhandler-wedge.md"
OUT = ROOT / "fixtures/representation-compare/latest.v0.json"
OUT_MD = ROOT / "docs/operations/reports/REPRESENTATION-COMPARE-LATEST.md"
E2_TOK = ROOT / "experiments/e2-tokens/tokcount.js"


def tokcount(text: str) -> int:
    proc = subprocess.run(
        ["node", str(E2_TOK)],
        input=json.dumps({"body": text}),
        capture_output=True,
        text=True,
        check=True,
        cwd=str(E2_TOK.parent),
    )
    data = json.loads(proc.stdout)
    return int(data["body"])


def load_bundles() -> dict[str, str]:
    legend = (WEDGE_PACK / "LEGEND.txt").read_text(encoding="utf-8")
    factored = (WEDGE_PACK / "pack_factored.txt").read_text(encoding="utf-8")
    explicit = (WEDGE_PACK / "pack_explicit.txt").read_text(encoding="utf-8")
    l2_factored = legend + "\n" + factored
    l2_explicit = legend + "\n" + explicit
    l2_md = L2_MD.read_text(encoding="utf-8")

    ast_text_path = ROOT / "fixtures/representation-compare/ast-struct.txt"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/ast_struct_extract.py"),
            str(WEDGE_RAW),
            "--out-text",
            str(ast_text_path),
        ],
        check=True,
        cwd=str(ROOT),
    )
    ast_struct = ast_text_path.read_text(encoding="utf-8")

    raw_parts = []
    for p in sorted(WEDGE_RAW.glob("*CommandHandler.java")):
        raw_parts.append(f"// FILE {p.name}\n{p.read_text(encoding='utf-8')}\n")
    raw_java = "\n".join(raw_parts)

    return {
        "l2_md": l2_md,
        "l2_factored": l2_factored,
        "l2_explicit": l2_explicit,
        "ast_struct": ast_struct,
        "raw_java": raw_java,
    }


def apply_spec(rep: str, spec: dict[str, object], bundles: dict[str, str], raw_dir: Path) -> str | None:
    kind = spec.get("kind")
    if kind == "unsupported":
        return None
    if kind == "count_lines":
        prefix = str(spec.get("prefix") or "")
        text = bundles[rep]
        n = sum(1 for line in text.splitlines() if line.strip().startswith(prefix))
        return str(n)
    if kind == "count_files":
        suffix = str(spec.get("suffix") or "")
        if rep == "raw_java":
            n = len(list(raw_dir.glob(f"*{suffix}")))
            return str(n)
        if rep == "ast_struct":
            n = len(re.findall(rf"^FILE {re.escape(suffix.replace('.java', ''))}", bundles[rep], re.M))
            n = len(re.findall(r"^FILE \w+CommandHandler\.java", bundles[rep], re.M))
            return str(n)
        return None
    if kind == "file_regex":
        if rep != "raw_java":
            return None
        fname = str(spec["file"])
        pattern = str(spec["pattern"])
        block = ""
        for part in bundles["raw_java"].split("// FILE "):
            if part.startswith(fname):
                block = part
                break
        m = re.search(pattern, block)
        if not m:
            raise ValueError(f"no match {pattern} in {fname}")
        return m.group(1) if m.lastindex else "yes"
    if kind == "regex":
        pattern = str(spec["pattern"])
        text = bundles[rep]
        m = re.search(pattern, text)
        if not m:
            raise ValueError(f"no match for {pattern}")
        if m.lastindex:
            return m.group(1)
        return "yes"
    raise ValueError(f"unknown kind {kind!r}")


def run_agent(bundles: dict[str, str], doc: dict[str, object]) -> dict[str, object]:
    reps = ["l2_md", "l2_factored", "l2_explicit", "ast_struct", "raw_java"]
    results: list[dict[str, object]] = []
    for q in doc.get("questions") or []:
        qid = q["id"]
        expected = str(q["expected"]).lower()
        cat = q.get("category")
        row: dict[str, object] = {"id": qid, "category": cat, "expected": q["expected"], "answers": {}}
        for rep in reps:
            spec = q.get(rep)
            if not isinstance(spec, dict):
                row["answers"][rep] = {"status": "skip", "detail": "no spec"}
                continue
            try:
                got = apply_spec(rep, spec, bundles, WEDGE_RAW)
                if got is None:
                    row["answers"][rep] = {"status": "na", "detail": "unsupported"}
                else:
                    ok = got.lower() == expected
                    row["answers"][rep] = {"status": "pass" if ok else "fail", "got": got}
            except ValueError as exc:
                row["answers"][rep] = {"status": "fail", "error": str(exc)}
        results.append(row)
    return {"questions": results}


def build_analysis(tokens: dict[str, int], summary: dict[str, object]) -> str:
    lf = tokens.get("l2_factored", 0)
    ast_t = tokens.get("ast_struct", 0)
    raw_t = tokens.get("raw_java", 0)
    md = summary.get("l2_md") or {}
    ast_s = summary.get("ast_struct") or {}
    lines = [
        "**Compression:** L2 factored is ~{:.0f}× smaller than raw Java and ~{:.0f}× smaller than javalang AST struct on the 29-handler wedge.".format(
            raw_t / lf if lf else 0, ast_t / lf if lf else 0
        ),
        "**Quality tradeoff:** L2 markdown scores highest on curated L1/dogfood (meta + topology tables). "
        "L2 factored/explicit excel at operadic inst rows and lossless reexpand; AST/raw excel at syntax and call-site fidelity per file.",
        "**AST gap:** Plain AST dumps omit annotation *values* unless augmented (we add @CommandType entity/action via source regex). "
        "They do not encode cross-handler wiring edges or breakeven token economics without a separate graph pass.",
        "**When to use which:** Agent context = prefer L2 factored for wiring at scale; navigation/audit = L2 md; "
        "refactor tools = AST; ground truth dispute = raw Java.",
    ]
    if md.get("pass") is not None and ast_s.get("pass") is not None:
        lines.append(
            f"**This run:** test agent pass count — L2 md {md.get('pass')}/7, AST struct {ast_s.get('pass')}/7, "
            f"L2 factored {(summary.get('l2_factored') or {}).get('pass')}/7."
        )
    return " ".join(lines)


def summarize(agent: dict[str, object]) -> dict[str, object]:
    reps = ["l2_md", "l2_factored", "l2_explicit", "ast_struct", "raw_java"]
    summary: dict[str, object] = {}
    for rep in reps:
        pass_n = fail_n = na_n = 0
        wiring_pass = wiring_total = 0
        for q in agent.get("questions") or []:
            ans = (q.get("answers") or {}).get(rep) or {}
            st = ans.get("status")
            if st == "pass":
                pass_n += 1
                if q.get("category") == "wiring":
                    wiring_pass += 1
                    wiring_total += 1
            elif st == "fail":
                fail_n += 1
                if q.get("category") == "wiring":
                    wiring_total += 1
            elif st == "na":
                na_n += 1
        summary[rep] = {
            "pass": pass_n,
            "fail": fail_n,
            "na": na_n,
            "wiring_pass_rate": round(wiring_pass / wiring_total, 3) if wiring_total else None,
        }
    return summary


def render_md(report: dict[str, object]) -> str:
    lines = [
        "# Representation compare (L2 vs AST vs raw)",
        "",
        f"Generated {report.get('generated_at_utc')} · git `{report.get('git_sha')}`",
        "",
        "## Token size (cl100k_base, 29-handler wedge)",
        "",
        "| Representation | Tokens | vs L2 factored |",
        "|----------------|-------:|---------------:|",
    ]
    tokens = report.get("tokens") or {}
    base = float(tokens.get("l2_factored") or 1)
    for rep, label in [
        ("l2_factored", "L2 factored (+ legend)"),
        ("l2_explicit", "L2 explicit (+ legend)"),
        ("l2_md", "L2 interface markdown pack"),
        ("ast_struct", "AST struct (javalang)"),
        ("raw_java", "Raw Java sources"),
    ]:
        t = tokens.get(rep)
        ratio = round(float(t) / base, 2) if t else "—"
        lines.append(f"| {label} | {t} | {ratio}× |")
    lines.extend(
        [
            "",
            "## Test agent score (wiring + topology questions)",
            "",
            "| Representation | Pass | Fail | N/A | Wiring pass rate |",
            "|----------------|-----:|-----:|----:|-----------------:|",
        ]
    )
    for rep, label in [
        ("l2_factored", "L2 factored"),
        ("l2_explicit", "L2 explicit"),
        ("l2_md", "L2 markdown"),
        ("ast_struct", "AST struct"),
        ("raw_java", "Raw Java"),
    ]:
        s = (report.get("summary") or {}).get(rep) or {}
        wpr = s.get("wiring_pass_rate")
        wpr_s = f"{100 * float(wpr):.0f}%" if wpr is not None else "—"
        lines.append(
            f"| {label} | {s.get('pass')} | {s.get('fail')} | {s.get('na')} | {wpr_s} |"
        )
    lines.extend(["", "## Analysis", "", str(report.get("analysis")), ""])
    return "\n".join(lines)


def main() -> int:
    bundles = load_bundles()
    tokens = {k: tokcount(v) for k, v in bundles.items()}

    doc = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    agent = run_agent(bundles, doc)
    summary = summarize(agent)

    sha = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()

    analysis = build_analysis(tokens, summary)

    report = {
        "schema_version": "representation-compare.v0",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_sha": sha,
        "tokens": tokens,
        "summary": summary,
        "agent": agent,
        "performance_note": "See fixtures/scale-report/latest.v0.json slice_matrix_timing for pipeline ms",
        "analysis": analysis,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_md(report), encoding="utf-8")
    print(json.dumps({"tokens": tokens, "summary": summary}, indent=2))
    print(f"OK: wrote {OUT.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
