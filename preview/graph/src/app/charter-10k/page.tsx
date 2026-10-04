import { MermaidChart } from "@/components/MermaidChart";
import charter from "@/lib/data/charter-10k.v0.json";
import type { WiringMapV0 } from "@/lib/wiringmap-types";
import { wiringMapToMermaid } from "@/lib/wiringmapToMermaid";

const map = charter as WiringMapV0;
const chart = wiringMapToMermaid(map);

export default function Charter10kWiringMapPage() {
  return (
    <article className="space-y-4">
      <div>
        <h2 className="text-xl font-normal mb-2">Fineract charter (~10k LOC)</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          {map.meta.slice} · {map.meta.notes} · {map.units.length} units ·{" "}
          {(map.junctions ?? []).length} junctions · {map.edges.length} edges ·{" "}
          <code className="font-mono text-xs">make charter-10k-check</code>
        </p>
        <p className="text-sm font-sans mt-2">
          Metrics & timing:{" "}
          <a href="/scale-dashboard" className="text-[var(--vermillion)]">
            scale dashboard
          </a>
          . Corpus honesty:{" "}
          <code className="font-mono text-xs">docs/operations/CORPUS-PROVENANCE.md</code>
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
