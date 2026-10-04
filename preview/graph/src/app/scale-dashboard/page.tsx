import { readFile } from "fs/promises";
import path from "path";

import type { ScaleReportV0 } from "@/lib/scale-report-types";

async function loadReport(): Promise<ScaleReportV0 | null> {
  try {
    const p = path.join(process.cwd(), "public", "scale-report.v0.json");
    const raw = await readFile(p, "utf-8");
    return JSON.parse(raw) as ScaleReportV0;
  } catch {
    return null;
  }
}

export default async function ScaleDashboardPage() {
  const report = await loadReport();
  if (!report) {
    return (
      <article>
        <h2 className="text-xl font-normal mb-2">Scale dashboard</h2>
        <p className="text-sm text-[var(--mute)]">
          Missing <code className="font-mono text-xs">public/scale-report.v0.json</code>. Run{" "}
          <code className="font-mono text-xs">make scale-report</code> at repo root.
        </p>
      </article>
    );
  }

  const metrics = report.metrics;
  const breakdown = report.charter_10k_breakdown;
  const rust = report.slice_matrix_timing.rust;
  const py = report.slice_matrix_timing.python;
  const perf = report.performance;
  const rep = report.representation_compare;
  const viewing = report.viewing;

  return (
    <article className="space-y-8 font-sans text-sm">
      <div>
        <h2 className="text-xl font-normal mb-2">Scale dashboard</h2>
        <p className="text-[var(--mute)] max-w-2xl">
          Generated {report.generated_at_utc} · git <code className="font-mono text-xs">{report.git_sha}</code>
        </p>
      </div>

      <section className="border-2 border-[var(--vermillion)] p-4 bg-[var(--paper)]">
        <h3 className="font-medium mb-2 text-[var(--vermillion)]">Pipeline performance (measured)</h3>
        <ul className="list-disc pl-5 space-y-1">
          <li>
            7-shard matrix: <strong>{perf?.matrix_total_ms_rust ?? rust.total_ms} ms</strong> Rust ·{" "}
            {perf?.matrix_total_ms_python ?? py.total_ms} ms Python
          </li>
          <li>
            Charter 10k shard (Rust): total <strong>{perf?.charter_10k_total_ms ?? "—"} ms</strong>
            {perf?.charter_10k_extract_ms != null ? ` (extract ${perf.charter_10k_extract_ms} ms)` : ""}
          </li>
        </ul>
      </section>

      {rep && (
        <section className="border border-[var(--line)] p-4">
          <h3 className="font-medium mb-2">L2 vs AST (29-handler test agent)</h3>
          <p>
            Tokens: factored {rep.tokens_factored} · AST {rep.tokens_ast} · raw {rep.tokens_raw} ·
            pass scores: L2 factored {rep.pass_l2_factored}/7 · L2 md {rep.pass_l2_md}/7 · AST{" "}
            {rep.pass_ast}/7
          </p>
        </section>
      )}

      <section className="border border-[var(--line)] bg-[#fff3e0] p-4">
        <h3 className="font-medium mb-2">Corpus honesty</h3>
        <p>{report.corpus.summary}</p>
        <p className="mt-2 text-[var(--mute)]">
          Upstream: {report.corpus.upstream_repo} · pinned:{" "}
          {String(report.corpus.upstream_commit_pinned)}
        </p>
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        <div>
          <h3 className="font-medium mb-2">Metrics</h3>
          <ul className="list-disc pl-5 space-y-1">
            <li>Matrix slices: {metrics.slice_matrix_slices}</li>
            <li>Unique Java LOC: {metrics.matrix_unique_java_loc}</li>
            <li>
              Recall: {metrics.edge_recall_frozen_pairs} frozen / {metrics.edge_recall_distinct_pairs}{" "}
              distinct
            </li>
            <li>Charter 10k LOC: {metrics.charter_10k?.loc ?? "—"}</li>
          </ul>
        </div>
        <div>
          <h3 className="font-medium mb-2">Charter 10k map vs context</h3>
          <ul className="list-disc pl-5 space-y-1">
            <li>
              Handler LOC: {breakdown.handler_loc} ({breakdown.handler_java_files} files)
            </li>
            <li>
              Context LOC: {breakdown.context_loc} ({breakdown.context_java_files} files)
            </li>
            <li>Mapped fraction: {(breakdown.mapped_fraction_loc * 100).toFixed(1)}%</li>
            <li>
              WiringMap: {breakdown.wiringmap_units} units · {breakdown.wiringmap_edges} edges
            </li>
          </ul>
        </div>
      </section>

      <section>
        <h3 className="font-medium mb-2">Comprehensive wiring diagram</h3>
        <p>
          Full Mermaid for all wired units:{" "}
          <a className="text-[var(--vermillion)]" href="/charter-10k">
            /charter-10k
          </a>{" "}
          (same data as{" "}
          <a className="text-[var(--vermillion)]" href={viewing.comprehensive_wiring_mermaid}>
            production preview
          </a>
          ).
        </p>
      </section>

      <section>
        <h3 className="font-medium mb-2">Slice matrix timing (Rust, ms)</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs border-collapse border border-[var(--line)]">
            <thead>
              <tr className="bg-[var(--paper)]">
                <th className="border border-[var(--line)] p-2 text-left">Shard</th>
                <th className="border border-[var(--line)] p-2">Java files</th>
                <th className="border border-[var(--line)] p-2">validate</th>
                <th className="border border-[var(--line)] p-2">extract</th>
                <th className="border border-[var(--line)] p-2">pack</th>
                <th className="border border-[var(--line)] p-2">reexpand</th>
                <th className="border border-[var(--line)] p-2">total</th>
              </tr>
            </thead>
            <tbody>
              {rust.slices.map((sl) => (
                <tr key={sl.id}>
                  <td className="border border-[var(--line)] p-2 font-mono">{sl.id}</td>
                  <td className="border border-[var(--line)] p-2 text-center">{sl.java_files}</td>
                  <td className="border border-[var(--line)] p-2 text-right">{sl.steps_ms.validate_ms}</td>
                  <td className="border border-[var(--line)] p-2 text-right">{sl.steps_ms.extract_ms}</td>
                  <td className="border border-[var(--line)] p-2 text-right">{sl.steps_ms.pack_ms}</td>
                  <td className="border border-[var(--line)] p-2 text-right">{sl.steps_ms.reexpand_ms}</td>
                  <td className="border border-[var(--line)] p-2 text-right font-medium">
                    {sl.steps_ms.total_ms}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-2 text-[var(--mute)]">
          Matrix total: {rust.total_ms} ms (Rust) · {report.slice_matrix_timing.python.total_ms} ms
          (Python)
        </p>
      </section>
    </article>
  );
}
