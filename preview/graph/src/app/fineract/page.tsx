import { WiringMapBrowser } from "@/components/WiringMapBrowser";
import fineract from "@/lib/data/fineract-thin.v0.json";
import type { WiringMapV0 } from "@/lib/wiringmap-types";

const map = fineract as WiringMapV0;

export default function FineractWiringMapPage() {
  return (
    <article className="space-y-4">
      <div>
        <h2 className="text-xl font-normal mb-2">Fineract handlers (thin slice)</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          {map.meta.slice} · {map.units.length} units ·{" "}
          {(map.junctions ?? []).length} junctions · {map.edges.length} edges ·
          full <code className="font-mono text-xs">pipeline-io</code> round-trip
          on main
        </p>
      </div>
      <WiringMapBrowser map={map} />
    </article>
  );
}
