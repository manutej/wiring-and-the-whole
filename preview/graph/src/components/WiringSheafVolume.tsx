"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import type { WiringMapV0 } from "@/lib/wiringmap-types";
import {
  ontologyAccent,
  ontologyGroupMeta,
  type OntologyGroupId,
} from "@/lib/wiringOntology";
import {
  LAYER_Z,
  projectOblique,
  type Vec3,
} from "@/lib/wiringSheafLayout";
import {
  wiringMapToStalksSectionsJson,
  wiringMapToVolumeGraph,
  type VolumeNode,
} from "@/lib/wiringMapToVolumeGraph";
import type { GlueStatus } from "@/lib/wiringMapToLatticeGraph";

const GLUE_COLOR: Record<GlueStatus, string> = {
  ok: "#437742",
  strange: "#c47b2b",
  missing: "#6d6a55",
};

const PAPER = "#c1c494";
const INK = "#253122";
const GOLD = "#fdc57e";
const UBE = "#501345";

function hex(h: string, a: number): string {
  const n = parseInt(h.slice(1), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
}

type Props = {
  map: WiringMapV0;
  height?: number;
  focusId?: string | null;
  onFocusChange?: (id: string | null) => void;
};

export function WiringSheafVolume({
  map,
  height = 560,
  focusId = null,
  onFocusChange,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const vol = useMemo(() => wiringMapToVolumeGraph(map), [map]);
  const [pinId, setPinId] = useState<string | null>(null);
  const selected = pinId ?? focusId;
  const [yaw, setYaw] = useState(0.55);
  const [pitch, setPitch] = useState(0.46);
  const dragRef = useRef({
    active: false,
    lx: 0,
    ly: 0,
    sx: 0,
    sy: 0,
    moved: false,
  });
  const [highlightOntology, setHighlightOntology] = useState<OntologyGroupId | "all">("all");

  useEffect(() => {
    setPinId(null);
  }, [focusId]);

  const nodeById = useMemo(() => new Map(vol.nodes.map((n) => [n.id, n])), [vol.nodes]);

  const linkGeom = useMemo(() => {
    return vol.links
      .map((l) => {
        const a = nodeById.get(l.source);
        const b = nodeById.get(l.target);
        if (!a || !b) return null;
        return { ...l, a, b };
      })
      .filter(Boolean) as Array<
      (typeof vol.links)[0] & { a: VolumeNode; b: VolumeNode }
    >;
  }, [vol, nodeById]);

  const focusSet = useMemo(() => {
    if (!selected) return null;
    const set = new Set<string>([selected]);
    for (const l of linkGeom) {
      if (l.source === selected || l.target === selected) {
        set.add(l.source);
        set.add(l.target);
      }
    }
    return set;
  }, [selected, linkGeom]);

  const paint = useCallback(
    (ctx: CanvasRenderingContext2D, w: number, h: number) => {
      ctx.clearRect(0, 0, w, h);
      const grad = ctx.createRadialGradient(w * 0.3, h * 0.1, 8, w * 0.5, h * 0.55, Math.max(w, h) * 0.75);
      grad.addColorStop(0, hex(UBE, 0.09));
      grad.addColorStop(0.55, hex(PAPER, 0));
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      for (const level of vol.levels) {
        const y = level.id * LAYER_Z;
        const corners: Vec3[] = [
          { x: -14, y, z: -12 },
          { x: 14, y, z: -12 },
          { x: 14, y, z: 12 },
          { x: -14, y, z: 12 },
        ];
        const proj = corners.map((c) => projectOblique(c, yaw, pitch, w, h));
        ctx.beginPath();
        ctx.moveTo(proj[0]!.x, proj[0]!.y);
        for (let i = 1; i < proj.length; i++) ctx.lineTo(proj[i]!.x, proj[i]!.y);
        ctx.closePath();
        ctx.fillStyle = hex(PAPER, 0.12 + level.id * 0.04);
        ctx.fill();
        ctx.strokeStyle = hex(INK, 0.12);
        ctx.setLineDash([4, 8]);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.font = "600 10px ui-sans-serif, system-ui";
        ctx.fillStyle = hex(INK, 0.55);
        ctx.fillText(`${level.code} · ${level.label}`, proj[0]!.x + 8, proj[0]!.y - 4);
      }

      const sortedLinks = [...linkGeom].sort(
        (a, b) =>
          projectOblique(mid(a.a, a.b), yaw, pitch, w, h).z -
          projectOblique(mid(b.a, b.b), yaw, pitch, w, h).z,
      );

      for (const l of sortedLinks) {
        const onFocus = !focusSet || focusSet.has(l.source) || focusSet.has(l.target);
        const onOnt =
          highlightOntology === "all" ||
          l.a.ontology === highlightOntology ||
          l.b.ontology === highlightOntology;
        if (!onFocus || !onOnt) continue;
        drawRestriction(ctx, l.a, l.b, l.glueStatus, yaw, pitch, w, h, onFocus ? 0.7 : 0.15);
      }

      const sortedNodes = [...vol.nodes].sort(
        (a, b) =>
          projectOblique(base(a), yaw, pitch, w, h).z -
          projectOblique(base(b), yaw, pitch, w, h).z,
      );

      for (const n of sortedNodes) {
        const onFocus = !focusSet || focusSet.has(n.id);
        const onOnt = highlightOntology === "all" || n.ontology === highlightOntology;
        drawStalk(ctx, n, yaw, pitch, w, h, onFocus && onOnt, selected === n.id);
      }
    },
    [vol, yaw, pitch, focusSet, highlightOntology, selected, linkGeom],
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      paint(ctx, rect.width, height);
    };

    resize();
    window.addEventListener("resize", resize);
    let raf = 0;
    const loop = () => {
      paint(ctx, canvas.clientWidth, height);
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [paint, height]);

  const pickNode = (x: number, y: number): string | null => {
    const canvas = canvasRef.current;
    if (!canvas) return null;
    const w = canvas.clientWidth;
    const h = height;
    let best: { id: string; d: number } | null = null;
    for (const n of vol.nodes) {
      const p = projectOblique(base(n), yaw, pitch, w, h);
      const r = (0.18 + n.dim * 0.042) * p.f * 28;
      const d = (p.x - x) ** 2 + (p.y - y) ** 2;
      if (d <= r * r && (!best || d < best.d)) best = { id: n.id, d };
    }
    return best?.id ?? null;
  };

  const onPointerDown = (ev: React.PointerEvent<HTMLCanvasElement>) => {
    dragRef.current = {
      active: true,
      lx: ev.clientX,
      ly: ev.clientY,
      sx: ev.clientX,
      sy: ev.clientY,
      moved: false,
    };
    (ev.target as HTMLCanvasElement).setPointerCapture(ev.pointerId);
  };

  const onPointerMove = (ev: React.PointerEvent<HTMLCanvasElement>) => {
    if (!dragRef.current.active) return;
    const dx = ev.clientX - dragRef.current.lx;
    const dy = ev.clientY - dragRef.current.ly;
    dragRef.current.lx = ev.clientX;
    dragRef.current.ly = ev.clientY;
    if (Math.abs(ev.clientX - dragRef.current.sx) + Math.abs(ev.clientY - dragRef.current.sy) > 5) {
      dragRef.current.moved = true;
    }
    if (dragRef.current.moved) {
      setYaw((y) => y + dx * 0.004);
      setPitch((p) => Math.max(0.25, Math.min(0.85, p + dy * 0.003)));
    }
  };

  const onPointerUp = (ev: React.PointerEvent<HTMLCanvasElement>) => {
    const wasDrag = dragRef.current.moved;
    dragRef.current.active = false;
    if (!wasDrag) {
      const rect = canvasRef.current!.getBoundingClientRect();
      const hit = pickNode(ev.clientX - rect.left, ev.clientY - rect.top);
      const next = hit === selected ? null : hit;
      setPinId(next);
      if (next?.startsWith("unit:")) onFocusChange?.(next);
      if (next === null) onFocusChange?.(null);
    }
  };

  const downloadStalks = () => {
    const json = wiringMapToStalksSectionsJson(map);
    const blob = new Blob([JSON.stringify(json, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${json.id}.sheaf.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-3">
      <p className="text-xs text-[var(--mute)] max-w-2xl">
        Oblique stalk volume (orbit drag) — hierarchy planes + ontological sectors, inspired by{" "}
        <a
          className="text-[var(--vermillion)]"
          href="https://github.com/manutej/stalks-and-sections"
          target="_blank"
          rel="noreferrer"
        >
          stalks-and-sections
        </a>{" "}
        and{" "}
        <a
          className="text-[var(--vermillion)]"
          href="https://github.com/manutej/cell-sheaf"
          target="_blank"
          rel="noreferrer"
        >
          cell-sheaf
        </a>
        . Node height ≈ stalk dim; edge colour = glue/residual.
      </p>
      <div className="flex flex-wrap gap-2 text-xs font-sans items-center">
        <span className="text-[var(--mute)]">Ontology:</span>
        <button
          type="button"
          className={`border px-2 py-1 ${highlightOntology === "all" ? "border-[var(--vermillion)] bg-[var(--cream)]" : "border-[var(--line)] bg-[var(--paper)]"}`}
          onClick={() => setHighlightOntology("all")}
        >
          All
        </button>
        {vol.presentOntologies.map((id) => (
          <button
            key={id}
            type="button"
            title={ontologyGroupMeta(id).kicker}
            className={`border px-2 py-1 ${highlightOntology === id ? "border-[var(--vermillion)] bg-[var(--cream)]" : "border-[var(--line)] bg-[var(--paper)]"}`}
            style={{ borderLeftColor: ontologyAccent(id), borderLeftWidth: 3 }}
            onClick={() => setHighlightOntology(id)}
          >
            {ontologyGroupMeta(id).label}
          </button>
        ))}
        <button
          type="button"
          className="border border-[var(--line)] px-2 py-1 bg-[var(--paper)] ml-auto"
          onClick={() => {
            setPinId(null);
            onFocusChange?.(null);
          }}
        >
          Clear focus
        </button>
        <button
          type="button"
          className="border border-[var(--line)] px-2 py-1 bg-[var(--paper)]"
          onClick={downloadStalks}
        >
          Export stalks JSON
        </button>
      </div>
      <div className="diagram-panel p-0 overflow-hidden">
        <canvas
          ref={canvasRef}
          className="w-full cursor-grab active:cursor-grabbing touch-none"
          style={{ height }}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          aria-label="Oblique sheaf volume of wiring map"
        />
      </div>
    </div>
  );
}

function base(n: VolumeNode): Vec3 {
  return n.position;
}

function mid(a: VolumeNode, b: VolumeNode): Vec3 {
  return {
    x: (a.position.x + b.position.x) / 2,
    y: (a.position.y + b.position.y) / 2,
    z: (a.position.z + b.position.z) / 2,
  };
}

function drawStalk(
  ctx: CanvasRenderingContext2D,
  n: VolumeNode,
  yaw: number,
  pitch: number,
  w: number,
  h: number,
  on: boolean,
  pinned: boolean,
) {
  const bot = projectOblique(n.position, yaw, pitch, w, h);
  const topP = projectOblique(
    { x: n.position.x, y: n.position.y + n.pillarHeight * 0.08, z: n.position.z },
    yaw,
    pitch,
    w,
    h,
  );
  const color = n.role === "unit" ? ontologyAccent(n.ontology) : GLUE_COLOR[n.glueStatus];
  const rx = (0.14 + n.dim * 0.035) * bot.f * 26;
  const rxt = rx * 0.92;

  ctx.beginPath();
  ctx.moveTo(bot.x - rx, bot.y);
  ctx.lineTo(topP.x - rxt, topP.y);
  ctx.lineTo(topP.x + rxt, topP.y);
  ctx.lineTo(bot.x + rx, bot.y);
  ctx.closePath();
  ctx.fillStyle = hex(color, on ? 0.5 : 0.1);
  ctx.fill();

  ctx.beginPath();
  ctx.ellipse(topP.x, topP.y, rxt, rxt * 0.42, 0, 0, Math.PI * 2);
  ctx.fillStyle = hex(color, on ? 0.88 : 0.18);
  ctx.fill();
  ctx.strokeStyle = pinned ? GOLD : hex(INK, on ? 0.35 : 0.08);
  ctx.lineWidth = pinned ? 2 : 0.8;
  ctx.stroke();

  if (n.known && on) {
    ctx.beginPath();
    ctx.arc(topP.x + rxt * 0.6, topP.y - rxt * 0.3, 2.5 * bot.f, 0, Math.PI * 2);
    ctx.fillStyle = GOLD;
    ctx.fill();
  }

  if (on && (n.role === "unit" || n.fanIn >= 4)) {
    ctx.fillStyle = hex(INK, 0.82);
    ctx.font = `600 ${Math.max(9, 10 * bot.f)}px ui-monospace, monospace`;
    ctx.textAlign = "center";
    const short = n.label.length > 20 ? `${n.label.slice(0, 17)}…` : n.label;
    ctx.fillText(short, bot.x, bot.y + 14 * bot.f);
  }
}

function drawRestriction(
  ctx: CanvasRenderingContext2D,
  a: VolumeNode,
  b: VolumeNode,
  glue: GlueStatus,
  yaw: number,
  pitch: number,
  w: number,
  h: number,
  alpha: number,
) {
  const pa = projectOblique(
    { x: a.position.x, y: a.position.y + a.pillarHeight * 0.05, z: a.position.z },
    yaw,
    pitch,
    w,
    h,
  );
  const pb = projectOblique(
    { x: b.position.x, y: b.position.y + b.pillarHeight * 0.05, z: b.position.z },
    yaw,
    pitch,
    w,
    h,
  );
  const midX = (pa.x + pb.x) / 2;
  const midY = (pa.y + pb.y) / 2 - 18;
  const dx = pb.x - pa.x;
  const dz = (b.position.z - a.position.z) || 1;
  const len = Math.hypot(dx, dz) || 1;
  const ctrlX = midX - (dz / len) * 16;
  const ctrlY = midY + 12;

  ctx.beginPath();
  ctx.moveTo(pa.x, pa.y);
  ctx.quadraticCurveTo(ctrlX, ctrlY, pb.x, pb.y);
  ctx.strokeStyle = GLUE_COLOR[glue];
  ctx.globalAlpha = alpha;
  ctx.lineWidth = glue === "ok" ? 1.5 : 1;
  if (glue === "missing") ctx.setLineDash([4, 4]);
  else ctx.setLineDash([]);
  ctx.stroke();
  ctx.globalAlpha = 1;
  ctx.setLineDash([]);
}
