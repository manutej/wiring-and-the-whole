import { WiringMapBrowser } from "@/components/WiringMapBrowser";
import toybank from "@/lib/data/toybank-accounts.v0.json";
import type { WiringMapV0 } from "@/lib/wiringmap-types";

const map = toybank as WiringMapV0;

export default function WiringMapPage() {
  return (
    <article className="space-y-4">
      <div>
        <h2 className="text-xl font-normal mb-2">Toybank accounts slice</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          {map.meta.slice} · {map.units.length} units · {map.junctions.length}{" "}
          junctions · {map.edges.length} edges · schema{" "}
          <code className="font-mono text-xs">{map.schema_version}</code>
        </p>
      </div>
      <div className="diagram-panel">
        <MermaidChart chart={chart} className="mermaid-output" />
      </div>
      <details className="text-sm font-sans">
        <summary className="cursor-pointer text-[var(--vermillion)]">
          Mermaid source (generated)
        </summary>
        <pre className="mt-2 p-3 bg-[var(--paper)] border border-[var(--line)] overflow-x-auto text-xs font-mono">
          {chart}
        </pre>
      </details>
    </article>
  );
}
