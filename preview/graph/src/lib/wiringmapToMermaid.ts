import type { WiringMapV0 } from "./wiringmap-types";

function mermaidId(raw: string): string {
  return raw.replace(/[^a-zA-Z0-9_]/g, "_");
}

function nodeLabel(id: string): string {
  if (id.startsWith("unit:")) {
    return id.slice("unit:".length);
  }
  if (id.startsWith("junction:")) {
    return id.slice("junction:".length);
  }
  return id;
}

/** Resolve edge endpoint to a graph node (unit or junction). */
function resolveNodeId(map: WiringMapV0, endpoint: string): string | null {
  if (endpoint.startsWith("unit:") || endpoint.startsWith("junction:")) {
    return endpoint;
  }
  if (endpoint.startsWith("port:")) {
    const unit = map.units.find((u) =>
      u.ports.some((p) => p.id === endpoint),
    );
    return unit?.id ?? null;
  }
  return null;
}

export function wiringMapToMermaid(map: WiringMapV0): string {
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
    const key = `${fromNode}|${toNode}|${e.id}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const label = `${e.edge_kind} ${e.id}`;
    lines.push(
      `  ${mermaidId(fromNode)} -->|"${label}"| ${mermaidId(toNode)}`,
    );
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
