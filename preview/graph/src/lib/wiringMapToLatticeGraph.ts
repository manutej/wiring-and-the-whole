import type { WiringMapV0 } from "./wiringmap-types";
import { shortJunctionLabel, shortUnitId } from "./wiringMapViewModel";

/** Glue status — aligned with cell-sheaf restriction semantics (see manutej/cell-sheaf). */
export type GlueStatus = "ok" | "strange" | "missing";

export type LatticeNode = {
  id: string;
  label: string;
  layer: "handler" | "service" | "infra";
  role: "unit" | "junction";
  glueStatus: GlueStatus;
  unitId?: string;
  fanIn: number;
};

export type LatticeLink = {
  id: string;
  source: string;
  target: string;
  edgeKind: string;
  glueStatus: GlueStatus;
};

export type WiringLatticeGraph = {
  nodes: LatticeNode[];
  links: LatticeLink[];
  layers: Array<{ id: LatticeNode["layer"]; label: string; y: number }>;
};

const INFRA_HINTS = ["JsonCommand", "DataIntegrityErrorHandler"];

function infraJunction(label: string): boolean {
  return INFRA_HINTS.some((h) => label.includes(h));
}

/** Merge FQCN + short junction labels into one glued node (sheaf-style restriction target). */
function glueKey(junctionId: string): string {
  const short = shortJunctionLabel(junctionId);
  return `glue:${short}`;
}

function resolveEndpoint(map: WiringMapV0, endpoint: string): string | null {
  if (endpoint.startsWith("unit:")) return endpoint;
  if (endpoint.startsWith("junction:")) return glueKey(endpoint);
  if (endpoint.startsWith("port:")) {
    const unit = map.units.find((u) => u.ports.some((p) => p.id === endpoint));
    return unit?.id ?? null;
  }
  return null;
}

export function wiringMapToLatticeGraph(map: WiringMapV0): WiringLatticeGraph {
  const nodeMap = new Map<string, LatticeNode>();
  const links: LatticeLink[] = [];
  const seenLinks = new Set<string>();

  for (const u of map.units) {
    nodeMap.set(u.id, {
      id: u.id,
      label: shortUnitId(u.id).replace(/\.java$/, ""),
      layer: "handler",
      role: "unit",
      glueStatus: "ok",
      unitId: u.id,
      fanIn: 0,
    });
  }

  const glueSources = new Map<string, Set<string>>();

  for (const j of map.junctions ?? []) {
    const gk = glueKey(j.id);
    const sources = glueSources.get(gk) ?? new Set<string>();
    sources.add(j.id);
    glueSources.set(gk, sources);
    if (nodeMap.has(gk)) continue;
    const label = shortJunctionLabel(j.id);
    nodeMap.set(gk, {
      id: gk,
      label,
      layer: infraJunction(label) ? "infra" : "service",
      role: "junction",
      glueStatus: "ok",
      fanIn: 0,
    });
  }

  for (const [gk, sources] of glueSources) {
    if (sources.size <= 1) continue;
    const node = nodeMap.get(gk);
    if (node) node.glueStatus = "strange";
  }

  for (const e of map.edges) {
    const from = resolveEndpoint(map, e.from);
    const to = resolveEndpoint(map, e.to);
    if (!from || !to) continue;
    const key = `${from}|${to}`;
    if (seenLinks.has(key)) continue;
    seenLinks.add(key);
    const tgtNode = nodeMap.get(to);
    let glueStatus: GlueStatus = e.edge_kind === "example" ? "ok" : "strange";
    if (!tgtNode) glueStatus = "missing";
    else if (tgtNode.glueStatus === "strange") glueStatus = "strange";
    links.push({
      id: e.id,
      source: from,
      target: to,
      edgeKind: e.edge_kind,
      glueStatus,
    });
    if (tgtNode) tgtNode.fanIn += 1;
  }

  const layers: WiringLatticeGraph["layers"] = [
    { id: "handler", label: "Handlers (@CommandType units)", y: 0 },
    { id: "service", label: "Platform services (glued junctions)", y: 1 },
    { id: "infra", label: "Shared infra (JsonCommand, DI handler)", y: 2 },
  ];

  return { nodes: [...nodeMap.values()], links, layers };
}

/** Minimal sheaf-graph/2020-12 stub for future cell-sheaf roll (pillars + restrictions only). */
export function wiringMapToSheafGraphStub(map: WiringMapV0, id = "wiring.trunk") {
  const lattice = wiringMapToLatticeGraph(map);
  const kindForLayer = (layer: LatticeNode["layer"]) =>
    layer === "handler" ? "core" : layer === "service" ? "lib" : "app";

  return {
    schema: "sheaf-graph/2020-12",
    id,
    title: map.meta?.slice ?? id,
    pillars: lattice.nodes.map((n, i) => ({
      id: n.id,
      folder: n.label,
      kind: kindForLayer(n.layer),
      known: n.glueStatus === "ok",
      dim: Math.max(1, Math.min(8, n.fanIn + (n.role === "unit" ? 2 : 1))),
      x: -120 + (240 * (i % 12)) / 11,
      z: n.layer === "handler" ? -40 : n.layer === "service" ? 0 : 40,
    })),
    restrictions: lattice.links.map((l) => ({
      id: l.id,
      source: l.source,
      target: l.target,
      relation: l.edgeKind,
      kind: "embed",
      status: l.glueStatus === "strange" ? "strange" : l.glueStatus === "missing" ? "missing" : "ok",
      residual: l.glueStatus === "ok" ? 0.05 : l.glueStatus === "strange" ? 0.18 : 0.5,
      residualMeaning: `WiringMap edge ${l.edgeKind} → glued junction`,
    })),
  };
}
