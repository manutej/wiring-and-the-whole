import type { OntologyGroupId } from "./wiringOntology";

export type Vec3 = { x: number; y: number; z: number };

export const LAYER_Z = 4.2;

type LayoutNode = {
  id: string;
  level: number;
  ontology: OntologyGroupId;
};

type LayoutEdge = { source: string; target: string };

function hash(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

function clusterAngle(ontology: OntologyGroupId, present: OntologyGroupId[]): number {
  const idx = present.indexOf(ontology);
  const n = present.length || 1;
  const slot = idx >= 0 ? idx : present.length;
  return (slot / n) * Math.PI * 2 - Math.PI / 2;
}

/** Seed positions: level → Y, ontology → angular sector on XZ (stalks-and-sections ring idiom). */
export function seedOntologyPositions(
  nodes: LayoutNode[],
  presentGroups: OntologyGroupId[],
): Record<string, Vec3> {
  const byLevelOnt = new Map<string, LayoutNode[]>();
  for (const n of nodes) {
    const key = `${n.level}|${n.ontology}`;
    const g = byLevelOnt.get(key) ?? [];
    g.push(n);
    byLevelOnt.set(key, g);
  }

  const pos: Record<string, Vec3> = {};
  for (const [key, group] of byLevelOnt) {
    const [levelStr, ont] = key.split("|") as [string, OntologyGroupId];
    const level = Number(levelStr);
    const ang0 = clusterAngle(ont, presentGroups);
    const span = (Math.PI * 2) / Math.max(presentGroups.length, 1);
    group.forEach((node, i) => {
      const n = group.length;
      const ang = ang0 + ((i - (n - 1) / 2) / Math.max(n, 1)) * span * 0.35;
      const ring = 2.4 + (2 - level) * 1.35 + Math.min(2.8, n * 0.18);
      const jitter = ((hash(node.id) % 1000) / 1000 - 0.5) * 0.45;
      pos[node.id] = {
        x: Math.cos(ang) * ring + jitter,
        y: level * LAYER_Z,
        z: Math.sin(ang) * (ring * 0.82) + jitter * 0.5,
      };
    });
  }
  return pos;
}

/** Lightweight 3D force relax (ported from stalks-and-sections layoutForce). */
export function layoutVolumeForce(
  nodes: LayoutNode[],
  edges: LayoutEdge[],
  presentGroups: OntologyGroupId[],
  steps = 200,
): Record<string, Vec3> {
  const pos = seedOntologyPositions(nodes, presentGroups);
  const vel: Record<string, Vec3> = {};
  for (const n of nodes) vel[n.id] = { x: 0, y: 0, z: 0 };

  const ids = nodes.map((n) => n.id);
  const rest = 2.15;

  for (let s = 0; s < steps; s++) {
    const alpha = 1 - s / steps;
    for (let i = 0; i < ids.length; i++) {
      const a = ids[i]!;
      const pa = pos[a]!;
      for (let j = i + 1; j < ids.length; j++) {
        const b = ids[j]!;
        const pb = pos[b]!;
        let dx = pa.x - pb.x;
        let dy = (pa.y - pb.y) * 0.28;
        let dz = pa.z - pb.z;
        const d2 = dx * dx + dy * dy + dz * dz + 0.1;
        const f = (16 * alpha) / d2;
        dx *= f;
        dy *= f;
        dz *= f;
        vel[a]!.x += dx;
        vel[a]!.y += dy;
        vel[a]!.z += dz;
        vel[b]!.x -= dx;
        vel[b]!.y -= dy;
        vel[b]!.z -= dz;
      }
    }
    for (const e of edges) {
      const pa = pos[e.source];
      const pb = pos[e.target];
      if (!pa || !pb) continue;
      const dx = pb.x - pa.x;
      const dy = pb.y - pa.y;
      const dz = pb.z - pa.z;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
      const mag = 0.11 * (dist - rest) / dist;
      vel[e.source]!.x += dx * mag;
      vel[e.source]!.y += dy * mag * 0.22;
      vel[e.source]!.z += dz * mag;
      vel[e.target]!.x -= dx * mag;
      vel[e.target]!.y -= dy * mag * 0.22;
      vel[e.target]!.z -= dz * mag;
    }
    for (const n of nodes) {
      const p = pos[n.id]!;
      const v = vel[n.id]!;
      const targetY = n.level * LAYER_Z;
      v.y += (targetY - p.y) * 0.24;
      const ang = clusterAngle(n.ontology, presentGroups);
      const ring = 2.4 + (2 - n.level) * 1.35;
      const tx = Math.cos(ang) * ring;
      const tz = Math.sin(ang) * ring * 0.82;
      v.x += (tx - p.x) * 0.018;
      v.z += (tz - p.z) * 0.018;
      v.x += -p.x * 0.01;
      v.z += -p.z * 0.01;
      v.x *= 0.62;
      v.y *= 0.52;
      v.z *= 0.62;
      p.x += v.x;
      p.y += v.y;
      p.z += v.z;
    }
  }

  for (const n of nodes) {
    const p = pos[n.id]!;
    p.y = n.level * LAYER_Z;
  }
  return pos;
}

export function projectOblique(
  p: Vec3,
  yaw: number,
  pitch: number,
  width: number,
  height: number,
): { x: number; y: number; f: number; z: number } {
  const cy = Math.cos(yaw);
  const sy = Math.sin(yaw);
  const cp = Math.cos(pitch);
  const sp = Math.sin(pitch);
  const x1 = p.x * cy - p.z * sy;
  const z1 = p.x * sy + p.z * cy;
  const y1 = p.y * cp - z1 * sp;
  const z2 = p.y * sp + z1 * cp;
  const f = 480 / (480 + z2 + 90);
  return {
    x: width * 0.46 + x1 * f * 2.55,
    y: height * 0.52 + y1 * f * 2.55,
    f,
    z: z2,
  };
}
