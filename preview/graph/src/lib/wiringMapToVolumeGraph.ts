import type { WiringMapV0 } from "./wiringmap-types";
import {
  inferOntologyFromText,
  layerToLevel,
  type OntologyGroupId,
  WIRING_LEVELS,
  WIRING_ONTOLOGY_GROUPS,
} from "./wiringOntology";
import { layoutVolumeForce, type Vec3 } from "./wiringSheafLayout";
import {
  wiringMapToLatticeGraph,
  type GlueStatus,
  type LatticeLink,
  type LatticeNode,
} from "./wiringMapToLatticeGraph";

export type VolumeNode = LatticeNode & {
  ontology: OntologyGroupId;
  level: number;
  dim: number;
  known: boolean;
  position: Vec3;
  pillarHeight: number;
};

export type VolumeGraph = {
  nodes: VolumeNode[];
  links: LatticeLink[];
  presentOntologies: OntologyGroupId[];
  levels: typeof WIRING_LEVELS;
};

function stalkDim(node: LatticeNode): number {
  const base = node.role === "unit" ? 3 : 2;
  return Math.min(16, Math.max(2, base + Math.min(node.fanIn, 8)));
}

function assignJunctionOntology(
  junctionId: string,
  links: LatticeLink[],
  nodeById: Map<string, LatticeNode>,
): OntologyGroupId {
  const counts = new Map<OntologyGroupId, number>();
  for (const l of links) {
    if (l.target !== junctionId) continue;
    const src = nodeById.get(l.source);
    if (!src || src.role !== "unit") continue;
    const g = inferOntologyFromText(src.label);
    counts.set(g, (counts.get(g) ?? 0) + 1);
  }
  let best: OntologyGroupId = inferOntologyFromText(junctionId.replace(/^glue:/, ""));
  let max = 0;
  for (const [g, c] of counts) {
    if (c > max) {
      max = c;
      best = g;
    }
  }
  return best;
}

export function wiringMapToVolumeGraph(map: WiringMapV0): VolumeGraph {
  const lattice = wiringMapToLatticeGraph(map);
  const nodeById = new Map(lattice.nodes.map((n) => [n.id, n]));

  const enriched: Omit<VolumeNode, "position">[] = lattice.nodes.map((n) => {
    const level = layerToLevel(n.layer);
    const ontology =
      n.role === "unit"
        ? inferOntologyFromText(n.label)
        : assignJunctionOntology(n.id, lattice.links, nodeById);
    const dim = stalkDim(n);
    return {
      ...n,
      ontology,
      level,
      dim,
      known: n.glueStatus === "ok",
      pillarHeight: 10 + dim * 2.2,
    };
  });

  const presentOntologies = WIRING_ONTOLOGY_GROUPS.map((g) => g.id).filter((id) =>
    enriched.some((n) => n.ontology === id),
  );

  const positions = layoutVolumeForce(
    enriched.map((n) => ({ id: n.id, level: n.level, ontology: n.ontology })),
    lattice.links.map((l) => ({ source: l.source, target: l.target })),
    presentOntologies,
  );

  const nodes: VolumeNode[] = enriched.map((n) => ({
    ...n,
    position: positions[n.id] ?? { x: 0, y: n.level * 4.2, z: 0 },
  }));

  return {
    nodes,
    links: lattice.links,
    presentOntologies,
    levels: WIRING_LEVELS,
  };
}

/** Export for [stalks-and-sections](https://github.com/manutej/stalks-and-sections) explorer. */
export function wiringMapToStalksSectionsJson(map: WiringMapV0) {
  const vol = wiringMapToVolumeGraph(map);
  const residualFor = (s: GlueStatus) => (s === "ok" ? 0.06 : s === "strange" ? 0.22 : 0.48);

  return {
    id: map.meta?.slice?.replace(/\W+/g, "-").toLowerCase() ?? "wiring-map",
    title: map.meta?.slice ?? "Wiring map",
    kicker: "wiring",
    residualMeaning:
      "Terracotta restriction = non-example wiring or ambiguous glue; teal = example edge with consistent junction.",
    levels: WIRING_LEVELS.map((l) => ({
      id: l.id,
      code: l.code,
      label: l.label,
      kicker: l.kicker,
      blurb: l.blurb,
    })),
    nodes: vol.nodes.map((n) => ({
      id: n.id,
      title: n.label,
      kind: n.role === "unit" ? "handler" : "platform",
      level: n.level,
      dim: n.dim,
      known: n.known,
      section: n.known ? Array.from({ length: n.dim }, (_, i) => (i === 0 ? 1 : 0)) : [],
      summary: `${n.ontology} · ${n.layer}`,
      sources: [],
    })),
    edges: vol.links.map((l) => ({
      id: l.id,
      source: l.source,
      target: l.target,
      relation: l.edgeKind,
      restrictKind: "embed",
      residual: residualFor(l.glueStatus),
      note: l.glueStatus,
    })),
  };
}
