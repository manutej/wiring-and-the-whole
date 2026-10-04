import type { WiringMapV0 } from "./wiringmap-types";

export type WiringRow = {
  unitId: string;
  handlerName: string;
  path: string;
  targets: string[];
};

function shortUnitId(unitId: string): string {
  return unitId.startsWith("unit:") ? unitId.slice("unit:".length) : unitId;
}

function shortJunctionLabel(junctionId: string): string {
  const raw = junctionId.startsWith("junction:") ? junctionId.slice("junction:".length) : junctionId;
  const parts = raw.split(".");
  return parts[parts.length - 1] ?? raw;
}

function resolveTargetLabel(map: WiringMapV0, endpoint: string): string | null {
  if (endpoint.startsWith("junction:")) {
    return shortJunctionLabel(endpoint);
  }
  if (endpoint.startsWith("unit:")) {
    return shortUnitId(endpoint);
  }
  if (endpoint.startsWith("port:")) {
    const unit = map.units.find((u) => u.ports.some((p) => p.id === endpoint));
    return unit ? shortUnitId(unit.id) : null;
  }
  return null;
}

export function buildWiringRows(map: WiringMapV0): WiringRow[] {
  const byUnit = new Map<string, Set<string>>();

  for (const edge of map.edges) {
    const fromUnit = edge.from.startsWith("unit:")
      ? edge.from
      : map.units.find((u) => u.ports.some((p) => p.id === edge.from))?.id;
    if (!fromUnit) continue;
    const label = resolveTargetLabel(map, edge.to);
    if (!label) continue;
    if (!byUnit.has(fromUnit)) byUnit.set(fromUnit, new Set());
    byUnit.get(fromUnit)!.add(label);
  }

  return map.units
    .map((u) => {
      const targets = [...(byUnit.get(u.id) ?? [])].sort();
      const handlerName = shortUnitId(u.id);
      const base = u.path.split("/").pop() ?? handlerName;
      return {
        unitId: u.id,
        handlerName: base.replace(/\.java$/, ""),
        path: u.path,
        targets,
      };
    })
    .filter((r) => r.targets.length > 0)
    .sort((a, b) => a.handlerName.localeCompare(b.handlerName));
}

export function uniqueTargetServices(rows: WiringRow[]): string[] {
  const s = new Set<string>();
  for (const r of rows) {
    for (const t of r.targets) s.add(t);
  }
  return [...s].sort();
}

export type MermaidOptions = {
  style?: "compact" | "full";
  focusUnitId?: string;
  maxNodes?: number;
};

export { shortUnitId, shortJunctionLabel, resolveTargetLabel };
