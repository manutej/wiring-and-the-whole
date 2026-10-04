import type { WiringMapV0 } from "./wiringmap-types";
import {
  buildWiringRows,
  shortJunctionLabel,
  shortUnitId,
  type MermaidOptions,
} from "./wiringMapViewModel";

function mermaidId(raw: string): string {
  return raw.replace(/[^a-zA-Z0-9_]/g, "_");
}

function nodeLabel(id: string): string {
  if (id.startsWith("unit:")) {
    const short = shortUnitId(id);
    return short.length > 36 ? `${short.slice(0, 33)}…` : short;
  }
  if (id.startsWith("junction:")) {
    return shortJunctionLabel(id);
  }
  return id;
}

function resolveNodeId(map: WiringMapV0, endpoint: string): string | null {
  if (endpoint.startsWith("unit:") || endpoint.startsWith("junction:")) {
    return endpoint;
  }
  if (endpoint.startsWith("port:")) {
    const unit = map.units.find((u) => u.ports.some((p) => p.id === endpoint));
    return unit?.id ?? null;
  }
  return null;
}

/** Focused neighborhood or compact bipartite-style LR diagram. */
export function wiringMapToMermaid(map: WiringMapV0, options: MermaidOptions = {}): string {
  const style = options.style ?? "compact";
  if (style === "full") {
    return wiringMapToMermaidFull(map);
  }
  if (options.focusUnitId) {
    return wiringMapFocusMermaid(map, options.focusUnitId);
  }
  return wiringMapOverviewMermaid(map, options.maxNodes ?? 24);
}

function wiringMapFocusMermaid(map: WiringMapV0, unitId: string): string {
  const lines: string[] = ["flowchart LR"];
  const unit = map.units.find((u) => u.id === unitId);
  if (!unit) {
    return "flowchart LR\n  missing[\"unit not found\"]";
  }
  const hId = mermaidId(unit.id);
  lines.push(`  ${hId}(["${nodeLabel(unit.id)}"])`);

  const junctions = new Set<string>();
  for (const e of map.edges) {
    if (resolveNodeId(map, e.from) !== unitId) continue;
    const to = resolveNodeId(map, e.to);
    if (!to || !to.startsWith("junction:")) continue;
    junctions.add(to);
  }

  for (const j of junctions) {
    const jId = mermaidId(j);
    lines.push(`  ${jId}["${nodeLabel(j)}"]`);
    lines.push(`  ${hId} --> ${jId}`);
  }
  return lines.join("\n");
}

/** Top handlers by fan-out → shared services (no edge labels). */
function wiringMapOverviewMermaid(map: WiringMapV0, maxNodes: number): string {
  const rows = buildWiringRows(map);
  const picked = rows.slice(0, Math.min(rows.length, Math.max(4, Math.floor(maxNodes / 2))));
  const services = new Set<string>();
  for (const r of picked) {
    for (const t of r.targets) services.add(t);
  }

  const lines: string[] = [
    "flowchart LR",
    '  subgraph H["Handlers (sample)"]',
    "    direction TB",
  ];
  for (const r of picked) {
    lines.push(`    ${mermaidId(r.unitId)}("${r.handlerName}")`);
  }
  lines.push("  end");
  lines.push('  subgraph S["Cal targets"]');
  lines.push("    direction TB");
  for (const s of [...services].slice(0, maxNodes - picked.length)) {
    lines.push(`    ${mermaidId("junction:" + s)}["${s}"]`);
  }
  lines.push("  end");

  for (const r of picked) {
    for (const t of r.targets) {
      if (![...services].slice(0, maxNodes - picked.length).includes(t)) continue;
      lines.push(`  ${mermaidId(r.unitId)} --> ${mermaidId("junction:" + t)}`);
    }
  }
  lines.push(
    `  %% overview: ${picked.length} of ${rows.length} handlers, ${services.size} callees`,
  );
  return lines.join("\n");
}

function wiringMapToMermaidFull(map: WiringMapV0): string {
  const unitIds = map.units.map((u) => u.id);
  const junctionIds = map.junctions.map((j) => j.id);

  const lines: string[] = ["flowchart TB"];

  lines.push('  subgraph units["units"]');
  for (const u of map.units) {
    const nid = mermaidId(u.id);
    lines.push(`    ${nid}["${nodeLabel(u.id)}"]`);
  }
  lines.push("  end");

  if (junctionIds.length > 0) {
    lines.push('  subgraph junctions["junctions (shared)"]');
    for (const j of map.junctions) {
      const nid = mermaidId(j.id);
      lines.push(`    ${nid}["${nodeLabel(j.id)}"]`);
    }
    lines.push("  end");
  }

  const seen = new Set<string>();
  for (const e of map.edges) {
    const fromNode = resolveNodeId(map, e.from);
    const toNode = resolveNodeId(map, e.to);
    if (!fromNode || !toNode) continue;
    const key = `${fromNode}|${toNode}`;
    if (seen.has(key)) continue;
    seen.add(key);
    lines.push(`  ${mermaidId(fromNode)} --> ${mermaidId(toNode)}`);
  }

  const connected = new Set<string>();
  for (const e of map.edges) {
    const fromNode = resolveNodeId(map, e.from);
    const toNode = resolveNodeId(map, e.to);
    if (fromNode) connected.add(fromNode);
    if (toNode) connected.add(toNode);
  }
  for (const u of unitIds) {
    if (!connected.has(u)) {
      lines.push(`  %% isolated unit: ${u}`);
    }
  }

  return lines.join("\n");
}

export const pipelineIoMermaid = `sequenceDiagram
  participant Repo as repo / witness
  participant Extract as extract_refs
  participant WM as WiringMap v0 JSON
  participant L2 as L2 pack
  participant Out as pipeline-io report

  Repo->>Extract: Java refs comments
  Extract->>WM: validate tokens / edges
  WM->>L2: build_l2_pack
  L2->>Out: JSON stdout (make pipeline-io)`;
