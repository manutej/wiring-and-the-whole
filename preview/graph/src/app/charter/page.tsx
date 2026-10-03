import { MermaidChart } from "@/components/MermaidChart";
import charter from "@/lib/data/charter-1k.v0.json";
import type { WiringMapV0 } from "@/lib/wiringmap-types";
import { wiringMapToMermaid } from "@/lib/wiringmapToMermaid";

const map = charter as WiringMapV0;
const chart = wiringMapToMermaid(map);

export default function CharterWiringMapPage() {
  return (
    <article className="space-y-4">
      <div>
        <h2 className="text-xl font-normal mb-2">Fineract charter (~1k LOC)</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          {map.meta.slice} · {map.units.length} units ·{" "}
          {(map.junctions ?? []).length} junctions · {map.edges.length} edges ·{" "}
          <code className="font-mono text-xs">make charter-1k-check</code>
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
