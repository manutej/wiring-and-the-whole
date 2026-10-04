"use client";

import { useMemo, useState } from "react";

import { MermaidChart } from "@/components/MermaidChart";
import { WiringForceLattice } from "@/components/WiringForceLattice";
import type { WiringMapV0 } from "@/lib/wiringmap-types";
import { buildWiringRows, uniqueTargetServices } from "@/lib/wiringMapViewModel";
import { wiringMapToMermaid } from "@/lib/wiringmapToMermaid";

type Props = {
  map: WiringMapV0;
  title?: string;
};

export function WiringMapBrowser({ map, title }: Props) {
  const rows = useMemo(() => buildWiringRows(map), [map]);
  const services = useMemo(() => uniqueTargetServices(rows), [rows]);
  const [query, setQuery] = useState("");
  const [focusId, setFocusId] = useState<string | null>(rows[0]?.unitId ?? null);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return rows;
    return rows.filter(
      (r) =>
        r.handlerName.toLowerCase().includes(q) ||
        r.targets.some((t) => t.toLowerCase().includes(q)),
    );
  }, [rows, query]);

  const focusChart = focusId
    ? wiringMapToMermaid(map, { style: "compact", focusUnitId: focusId })
    : null;
  const overviewChart = wiringMapToMermaid(map, { style: "compact", maxNodes: 22 });

  return (
    <div className="space-y-6 font-sans text-sm">
      {title && <h3 className="text-base font-medium">{title}</h3>}

      <p className="text-[var(--mute)] max-w-2xl">
        Primary view: layered force lattice (handlers → glued services → infra), aligned with{" "}
        <a
          className="text-[var(--vermillion)]"
          href="https://github.com/manutej/cell-sheaf"
          target="_blank"
          rel="noreferrer"
        >
          cell-sheaf
        </a>{" "}
        restriction / glue colors. Use the table and per-handler Mermaid for detail; avoid the
        legacy full-graph Mermaid unless you need a raw dump.
      </p>

      <section>
        <h4 className="font-medium mb-2">Force lattice (multi-layer)</h4>
        <WiringForceLattice
          map={map}
          height={520}
          focusId={focusId}
          onFocusChange={(id) => {
            if (!id) {
              setFocusId(null);
              return;
            }
            if (id.startsWith("unit:")) setFocusId(id);
          }}
        />
      </section>

      <label className="block max-w-md">
        <span className="text-[var(--mute)]">Filter handlers or services</span>
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. DisburseLoan, LoanWrite"
          className="mt-1 w-full border border-[var(--line)] bg-[var(--paper)] px-3 py-2 font-mono text-xs"
        />
      </label>

      <div className="grid gap-6 lg:grid-cols-2">
        <section>
          <h4 className="font-medium mb-2">Handler → callees ({filtered.length})</h4>
          <div className="max-h-[420px] overflow-auto border border-[var(--line)] bg-[var(--paper)]">
            <table className="w-full text-xs">
              <thead className="sticky top-0 bg-[var(--paper)] border-b border-[var(--line)]">
                <tr>
                  <th className="text-left p-2 font-medium">Handler</th>
                  <th className="text-left p-2 font-medium">Wiring targets</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r) => (
                  <tr
                    key={r.unitId}
                    className={`border-b border-[var(--line)] cursor-pointer hover:bg-[var(--cream)] ${
                      focusId === r.unitId ? "bg-[var(--cream)]" : ""
                    }`}
                    onClick={() => setFocusId(r.unitId)}
                  >
                    <td className="p-2 font-mono align-top whitespace-nowrap">{r.handlerName}</td>
                    <td className="p-2 font-mono text-[var(--mute)]">{r.targets.join(" · ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h4 className="font-medium mb-2">Focus (selected handler)</h4>
          {focusId && focusChart ? (
            <div className="diagram-panel min-h-[200px]">
              <MermaidChart chart={focusChart} className="mermaid-output mermaid-compact" />
            </div>
          ) : (
            <p className="text-[var(--mute)]">Select a row in the table.</p>
          )}
        </section>
      </div>

      <section>
        <h4 className="font-medium mb-2">Overview (sample bipartite)</h4>
        <div className="diagram-panel">
          <MermaidChart chart={overviewChart} className="mermaid-output mermaid-compact" />
        </div>
        <p className="text-xs text-[var(--mute)] mt-2">
          {services.length} distinct callees across {rows.length} wired handlers.
        </p>
      </section>

      <details className="text-sm">
        <summary className="cursor-pointer text-[var(--vermillion)]">
          Legacy full Mermaid graph (dense — not recommended)
        </summary>
        <div className="diagram-panel mt-2">
          <MermaidChart
            chart={wiringMapToMermaid(map, { style: "full" })}
            className="mermaid-output"
          />
        </div>
      </details>
    </div>
  );
}
