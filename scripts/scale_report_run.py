#!/usr/bin/env python3
"""Generate scale report JSON, markdown, and HTML dashboard."""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "fixtures/scale-report/latest.v0.json"
OUT_MD = ROOT / "docs/operations/reports/SCALE-REPORT-LATEST.md"
OUT_HTML = ROOT / "docs/operations/scale-dashboard/index.html"
PREVIEW_JSON = ROOT / "preview/graph/public/scale-report.v0.json"
CHARTER_10K = ROOT / "fixtures/external/fineract-charter-10k"


def git_sha() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (proc.stdout or "").strip() or "unknown"


def run_json(cmd: list[str], extra_env: dict[str, str] | None = None) -> dict[str, object]:
    env = {**os.environ, **(extra_env or {})}
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed:\n{proc.stderr or proc.stdout}")
    return json.loads(proc.stdout)


def charter_10k_breakdown() -> dict[str, object]:
    handler_loc = 0
    context_loc = 0
    handler_files = 0
    context_files = 0
    for p in CHARTER_10K.glob("*.java"):
        loc = len(p.read_text(encoding="utf-8").splitlines())
        if p.name.endswith("CommandHandler.java"):
            handler_loc += loc
            handler_files += 1
        else:
            context_loc += loc
            context_files += 1
    total = handler_loc + context_loc
    wm = json.loads((CHARTER_10K / "wiringmap.v0.json").read_text(encoding="utf-8"))
    return {
        "handler_java_files": handler_files,
        "context_java_files": context_files,
        "handler_loc": handler_loc,
        "context_loc": context_loc,
        "total_loc": total,
        "mapped_fraction_loc": round(handler_loc / total, 4) if total else 0,
        "wiringmap_units": len(wm.get("units") or []),
        "wiringmap_edges": len(wm.get("edges") or []),
        "wiringmap_junctions": len(wm.get("junctions") or []),
    }


def corpus_block() -> dict[str, object]:
    return {
        "kind": "experiments_path_list_not_checkout",
        "summary": (
            "Charter 10k is NOT a full Apache Fineract clone. It copies real Fineract-derived "
            "Java from in-repo experiment corpora (e3-ablation, e5-depth, e2-tokens) with "
            "parser-injected // refs: — not hand-wrapped placeholder code."
        ),
        "upstream_repo": "https://github.com/apache/fineract.git",
        "upstream_commit_pinned": False,
        "source_pools": [
            "experiments/e3-ablation/raw (*CommandHandler.java)",
            "experiments/e5-depth/raw (*.java services)",
            "experiments/e2-tokens/raw (*.java)",
        ],
        "this_repo": "https://github.com/manutej/wiring-and-the-whole",
        "charter_fixture": "fixtures/external/fineract-charter-10k",
    }


def viewing_block() -> dict[str, object]:
    base = "https://wiring-graph-preview.vercel.app"
    return {
        "comprehensive_wiring_mermaid": f"{base}/charter-10k",
        "charter_1k": f"{base}/charter",
        "scale_ladder_diagrams": f"{base}/scale",
        "html_dashboard": f"{base}/scale-dashboard",
        "static_html": "docs/operations/scale-dashboard/index.html",
        "local_makefile": "make charter-10k-check",
        "docs": "docs/operations/VIEWING-WIRING-DIAGRAMS.md",
    }


def render_html(report: dict[str, object]) -> str:
    payload = html.escape(json.dumps(report, indent=2))
    metrics = report.get("metrics") or {}
    timing = report.get("slice_matrix_timing") or {}
    rust_timing = timing.get("rust") or {}
    py_timing = timing.get("python") or {}
    rust_slices = rust_timing.get("slices") or []
    corpus = report.get("corpus") or {}
    breakdown = report.get("charter_10k_breakdown") or {}
    viewing = report.get("viewing") or {}
    charter_10k_metrics = metrics.get("charter_10k") or {}

    rows = ""
    for sl in rust_slices:
        steps = sl.get("steps_ms") or {}
        rows += f"""<tr>
          <td>{html.escape(str(sl.get("id")))}</td>
          <td>{sl.get("java_files")}</td>
          <td>{steps.get("validate_ms")}</td>
          <td>{steps.get("extract_ms")}</td>
          <td>{steps.get("pack_ms")}</td>
          <td>{steps.get("reexpand_ms")}</td>
          <td><strong>{steps.get("total_ms")}</strong></td>
        </tr>"""

    mapped_pct = float(breakdown.get("mapped_fraction_loc") or 0) * 100

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Wiring scale dashboard</title>
  <style>
    :root {{ font-family: ui-sans-serif, system-ui, sans-serif; background: #faf9f7; color: #1a1a1a; }}
    body {{ max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
    h1 {{ font-weight: 500; font-size: 1.5rem; }}
    .banner {{ background: #fff3e0; border: 1px solid #e65100; padding: 1rem; margin: 1rem 0; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 0.875rem; }}
    th, td {{ border: 1px solid #ddd; padding: 0.4rem 0.6rem; text-align: left; }}
    th {{ background: #eee; }}
    a {{ color: #c0392b; }}
    pre {{ background: #fff; border: 1px solid #ddd; padding: 1rem; overflow: auto; font-size: 0.75rem; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    @media (max-width: 700px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <h1>Wiring scale dashboard (S4 charter 10k)</h1>
  <p>Generated <code>{html.escape(str(report.get("generated_at_utc")))}</code> · git <code>{html.escape(str(report.get("git_sha")))}</code></p>

  <div class="banner">
    <strong>What repo is this?</strong> {html.escape(str(corpus.get("summary")))}
    <br />Upstream reference: {html.escape(str(corpus.get("upstream_repo")))} · commit pinned: {corpus.get("upstream_commit_pinned")}.
  </div>

  <div class="grid">
    <section>
      <h2>Scale metrics</h2>
      <ul>
        <li>Matrix slices: {metrics.get("slice_matrix_slices")}</li>
        <li>Unique Java LOC (content hash): {metrics.get("matrix_unique_java_loc")}</li>
        <li>Edge recall: {metrics.get("edge_recall_frozen_pairs")} frozen / {metrics.get("edge_recall_distinct_pairs")} distinct</li>
        <li>Charter 10k LOC: {charter_10k_metrics.get("loc")}</li>
      </ul>
    </section>
    <section>
      <h2>Charter 10k wiring vs context</h2>
      <ul>
        <li>Handler LOC: {breakdown.get("handler_loc")} ({breakdown.get("handler_java_files")} files)</li>
        <li>Context LOC: {breakdown.get("context_loc")} ({breakdown.get("context_java_files")} files)</li>
        <li>Mapped fraction (by LOC): {mapped_pct:.1f}%</li>
        <li>WiringMap: {breakdown.get("wiringmap_units")} units · {breakdown.get("wiringmap_edges")} edges</li>
      </ul>
    </section>
  </div>

  <section>
    <h2>View comprehensive wiring diagram</h2>
    <p>Live Mermaid (all wired units + edges): <a href="{html.escape(str(viewing.get("comprehensive_wiring_mermaid")))}">charter-10k preview</a>.
    Interactive dashboard: <a href="{html.escape(str(viewing.get("html_dashboard")))}">/scale-dashboard</a>.
    Programme diagrams: <a href="{html.escape(str(viewing.get("scale_ladder_diagrams")))}">/scale</a>.</p>
  </section>

  <section>
    <h2>Slice matrix timing (Rust, ms)</h2>
    <table>
      <thead><tr><th>Shard</th><th>Java files</th><th>validate</th><th>extract</th><th>pack</th><th>reexpand</th><th>total</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p>Matrix total: {rust_timing.get("total_ms")} ms (Rust) · {py_timing.get("total_ms")} ms (Python)</p>
  </section>

  <section>
    <h2>Raw report JSON</h2>
    <pre id="json">{payload}</pre>
  </section>
</body>
</html>"""


def render_md(report: dict[str, object]) -> str:
    corpus = report.get("corpus") or {}
    viewing = report.get("viewing") or {}
    pools = corpus.get("source_pools") or []
    pool_lines = "\n".join(f"- `{p}`" for p in pools)
    return "\n".join(
        [
            "# Scale report (latest)",
            "",
            f"- **Generated:** {report.get('generated_at_utc')}",
            f"- **Git:** `{report.get('git_sha')}`",
            "",
            "## Corpus honesty",
            "",
            str(corpus.get("summary")),
            "",
            f"- Upstream: {corpus.get('upstream_repo')} (pinned: {corpus.get('upstream_commit_pinned')})",
            pool_lines,
            "",
            "## View wiring",
            "",
            f"- Comprehensive Mermaid: {viewing.get('comprehensive_wiring_mermaid')}",
            f"- HTML dashboard (preview): {viewing.get('html_dashboard')}",
            f"- Static HTML (repo): `{viewing.get('static_html')}`",
            f"- Docs: `{viewing.get('docs')}`",
            "",
            "## Metrics JSON",
            "",
            "```json",
            json.dumps(report.get("metrics"), indent=2),
            "```",
            "",
            "## Timing JSON",
            "",
            "```json",
            json.dumps(report.get("slice_matrix_timing"), indent=2),
            "```",
            "",
        ]
    )


def main() -> int:
    metrics_proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/scale_metrics_check.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if metrics_proc.returncode != 0:
        print(metrics_proc.stderr or metrics_proc.stdout, file=sys.stderr)
        return 1
    metrics = json.loads(metrics_proc.stdout)

    timing_script = str(ROOT / "scripts/slice_matrix_timing.py")
    rust_timing = run_json([sys.executable, timing_script])
    py_timing = run_json([sys.executable, timing_script], {"WIRING_ENGINE": "python"})

    report: dict[str, object] = {
        "schema_version": "scale-report.v0",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_sha": git_sha(),
        "corpus": corpus_block(),
        "metrics": metrics,
        "charter_10k_breakdown": charter_10k_breakdown(),
        "slice_matrix_timing": {"rust": rust_timing, "python": py_timing},
        "viewing": viewing_block(),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_md(report), encoding="utf-8")
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(render_html(report), encoding="utf-8")
    PREVIEW_JSON.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"OK: scale report → {OUT_JSON.relative_to(ROOT)}")
    print(f"OK: markdown → {OUT_MD.relative_to(ROOT)}")
    print(f"OK: HTML dashboard → {OUT_HTML.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
