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
      <WiringMapBrowser map={map} />
    </article>
  );
}
