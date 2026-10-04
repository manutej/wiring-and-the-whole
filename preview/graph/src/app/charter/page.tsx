import { WiringMapBrowser } from "@/components/WiringMapBrowser";
import charter from "@/lib/data/charter-1k.v0.json";
import type { WiringMapV0 } from "@/lib/wiringmap-types";

const map = charter as WiringMapV0;

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
      <WiringMapBrowser map={map} />
    </article>
  );
}
