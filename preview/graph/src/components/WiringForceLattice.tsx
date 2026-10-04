"use client";

import {
  forceCenter,
  forceCollide,
  forceLink,
  forceManyBody,
  forceSimulation,
  forceX,
  forceY,
  type SimulationLinkDatum,
  type SimulationNodeDatum,
} from "d3-force";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import type { WiringMapV0 } from "@/lib/wiringmap-types";
import {
  wiringMapToLatticeGraph,
  type GlueStatus,
  type LatticeLink,
  type LatticeNode,
} from "@/lib/wiringMapToLatticeGraph";

type SimNode = LatticeNode &
  SimulationNodeDatum & {
    x: number;
    y: number;
  };

type SimLink = Omit<LatticeLink, "source" | "target"> &
  SimulationLinkDatum<SimNode> & {
    source: SimNode;
    target: SimNode;
  };

const GLUE_COLOR: Record<GlueStatus, string> = {
  ok: "#437742",
  strange: "#c47b2b",
  missing: "#6d6a55",
};

const LAYER_Y = [0.78, 0.48, 0.18];

type Props = {
  map: WiringMapV0;
  height?: number;
  /** Handler unit id from table selection (`unit:…`). */
  focusId?: string | null;
  onFocusChange?: (id: string | null) => void;
};

export function WiringForceLattice({
  map,
  height = 480,
  focusId = null,
  onFocusChange,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const graph = useMemo(() => wiringMapToLatticeGraph(map), [map]);
  /** Glue / infra pin independent of table focus. */
  const [pinId, setPinId] = useState<string | null>(null);
  const selected = pinId ?? focusId;

  useEffect(() => {
    setPinId(null);
  }, [focusId]);
  const [paused, setPaused] = useState(false);
  const simRef = useRef<ReturnType<typeof forceSimulation<SimNode>> | null>(null);
  const nodesRef = useRef<SimNode[]>([]);

  const layerIndex = (layer: LatticeNode["layer"]) =>
    layer === "handler" ? 0 : layer === "service" ? 1 : 2;

  const initSimulation = useCallback(
    (width: number, h: number) => {
      simRef.current?.stop();
      const nodes: SimNode[] = graph.nodes.map((n, i) => ({
        ...n,
        x: width * (0.15 + (0.7 * (i % 10)) / 10),
        y: h * LAYER_Y[layerIndex(n.layer)],
      }));
      const nodeById = new Map(nodes.map((n) => [n.id, n]));
      const links: SimLink[] = graph.links
        .map((l) => ({
          ...l,
          source: nodeById.get(l.source)!,
          target: nodeById.get(l.target)!,
        }))
        .filter((l) => l.source && l.target);

      const layerY = (d: SimNode) => h * LAYER_Y[layerIndex(d.layer)];

      const sim = forceSimulation(nodes)
        .force(
          "link",
          forceLink<SimNode, SimLink>(links)
            .id((d) => d.id)
            .distance(70)
            .strength(0.85),
        )
        .force("charge", forceManyBody().strength(-140))
        .force("collide", forceCollide<SimNode>(22))
        .force("y", forceY<SimNode>(layerY).strength(1))
        .force("x", forceX<SimNode>(width / 2).strength(0.06))
        .force("center", forceCenter(width / 2, h / 2).strength(0.02));

      simRef.current = sim;
      nodesRef.current = nodes;
      return { sim, nodes, links };
    },
    [graph.nodes, graph.links],
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf = 0;
    let links: SimLink[] = [];

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const bundle = initSimulation(rect.width, height);
      links = bundle.links;
    };

    const drawEdge = (l: SimLink, alpha: number) => {
      const s = l.source as SimNode;
      const t = l.target as SimNode;
      const midX = (s.x + t.x) / 2;
      const midY = (s.y + t.y) / 2 - 28;
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.quadraticCurveTo(midX, midY, t.x, t.y);
      ctx.strokeStyle = GLUE_COLOR[l.glueStatus];
      ctx.globalAlpha = alpha;
      ctx.lineWidth = l.glueStatus === "ok" ? 1.4 : 1;
      if (l.glueStatus === "missing") ctx.setLineDash([4, 4]);
      else ctx.setLineDash([]);
      ctx.stroke();
      ctx.globalAlpha = 1;
    };

    const draw = () => {
      const w = canvas.clientWidth;
      const h = height;
      ctx.clearRect(0, 0, w, h);

      ctx.strokeStyle = "rgba(109, 106, 85, 0.25)";
      ctx.setLineDash([2, 6]);
      for (let i = 0; i < 3; i++) {
        const y = h * LAYER_Y[i];
        ctx.beginPath();
        ctx.moveTo(12, y);
        ctx.lineTo(w - 12, y);
        ctx.stroke();
      }
      ctx.setLineDash([]);

      ctx.font = "600 10px ui-sans-serif, system-ui";
      ctx.fillStyle = "#6a6258";
      ctx.fillText("Handlers", 14, h * LAYER_Y[0] + 14);
      ctx.fillText("Services (glued)", 14, h * LAYER_Y[1] + 14);
      ctx.fillText("Infra", 14, h * LAYER_Y[2] + 14);

      const focus = selected
        ? new Set(
            links.flatMap((l) => {
              const s = (l.source as SimNode).id;
              const t = (l.target as SimNode).id;
              if (s === selected || t === selected) return [s, t];
              return [];
            }).concat(selected),
          )
        : null;

      for (const l of links) {
        const s = (l.source as SimNode).id;
        const t = (l.target as SimNode).id;
        const on = !focus || focus.has(s) || focus.has(t);
        drawEdge(l, on ? 0.55 : 0.08);
      }

      for (const n of nodesRef.current) {
        const on = !focus || focus.has(n.id);
        const r = n.role === "unit" ? 10 : 8 + Math.min(n.fanIn, 6);
        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        ctx.fillStyle = on
          ? n.role === "unit"
            ? "#c23b22"
            : GLUE_COLOR[n.glueStatus]
          : "rgba(28, 25, 22, 0.12)";
        ctx.fill();
        ctx.strokeStyle = selected === n.id ? "#fdc57e" : "rgba(28, 25, 22, 0.35)";
        ctx.lineWidth = selected === n.id ? 2 : 0.8;
        ctx.stroke();
        if (on && (n.role === "unit" || n.fanIn >= 3)) {
          ctx.fillStyle = "#1c1916";
          ctx.font = "10px ui-monospace, monospace";
          ctx.textAlign = "center";
          const short =
            n.label.length > 22 ? `${n.label.slice(0, 19)}…` : n.label;
          ctx.fillText(short, n.x, n.y + r + 12);
        }
      }
    };

    const loop = () => {
      if (!paused) simRef.current?.tick();
      draw();
      raf = requestAnimationFrame(loop);
    };

    resize();
    window.addEventListener("resize", resize);
    raf = requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      simRef.current?.stop();
    };
  }, [graph, height, initSimulation, paused, selected, focusId]);

  const onClick = (ev: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = ev.clientX - rect.left;
    const y = ev.clientY - rect.top;
    let hit: string | null = null;
    for (const n of nodesRef.current) {
      const r = n.role === "unit" ? 12 : 14;
      if ((n.x - x) ** 2 + (n.y - y) ** 2 <= r * r) hit = n.id;
    }
    const next = hit === selected ? null : hit;
    setPinId(next);
    if (next?.startsWith("unit:")) onFocusChange?.(next);
    if (next === null) onFocusChange?.(null);
  };

  return (
    <div className="space-y-2">
      <p className="text-xs text-[var(--mute)] max-w-2xl">
        Layered force layout (handlers → glued services → infra). Curved edges follow{" "}
        <a
          className="text-[var(--vermillion)]"
          href="https://github.com/manutej/cell-sheaf"
          target="_blank"
          rel="noreferrer"
        >
          cell-sheaf
        </a>{" "}
        restriction / strata idiom — junctions with the same short name are glued. Tap a node to
        focus; gold ring = selection.
      </p>
      <div className="flex gap-2 text-xs font-sans">
        <button
          type="button"
          className="border border-[var(--line)] px-2 py-1 bg-[var(--paper)]"
          onClick={() => setPaused((p) => !p)}
        >
          {paused ? "Resume motion" : "Pause"}
        </button>
        <button
          type="button"
          className="border border-[var(--line)] px-2 py-1 bg-[var(--paper)]"
          onClick={() => {
            setPinId(null);
            onFocusChange?.(null);
          }}
        >
          Clear focus
        </button>
      </div>
      <div className="diagram-panel p-0 overflow-hidden">
        <canvas
          ref={canvasRef}
          className="w-full cursor-pointer"
          style={{ height }}
          onClick={onClick}
          aria-label="Force-directed wiring lattice"
        />
      </div>
    </div>
  );
}
