import { MermaidChart } from "@/components/MermaidChart";
import {
  compoundProgrammeDag,
  rustPipelineSeq,
  scaleLadderDag,
  sliceMatrixDag,
  wiringMathDag,
} from "@/lib/scaleDiagrams";

const sections = [
  {
    title: "Scale ladder (programme)",
    body: "M0 demo through M3 — current tip: S2 slice matrix + S3 metrics on branch scale-build-2.",
    chart: scaleLadderDag,
  },
  {
    title: "Compound build loop",
    body: "Segregated builder / eval / adversarial — one PR when checklist + SHIP.",
    chart: compoundProgrammeDag,
  },
  {
    title: "Slice matrix (6 shards)",
    body: "make slice-matrix-check — same hot path as pipeline-io per shard; reducer JSON on stdout.",
    chart: sliceMatrixDag,
  },
  {
    title: "Wiring + math gates",
    body: "Wiring: extract ↔ map ↔ pack ↔ reexpand. Math: charter LOC, recall pairs, handler token WIN.",
    chart: wiringMathDag,
  },
  {
    title: "Rust engine sequence",
    body: "Default WIRING_ENGINE=rust; Python fallback for debug only.",
    chart: rustPipelineSeq,
  },
];

export default function ScaleDiagramsPage() {
  return (
    <article className="space-y-8">
      <div>
        <h2 className="text-xl font-normal mb-2">Scale & compound diagrams</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          Live Mermaid from{" "}
          <code className="font-mono text-xs">preview/graph/src/lib/scaleDiagrams.ts</code>
          . Markdown mirror:{" "}
          <code className="font-mono text-xs">docs/SCALE-DIAGRAMS.md</code>.
        </p>
      </div>
      {sections.map((s) => (
        <section key={s.title} className="space-y-3">
          <h3 className="text-lg font-normal">{s.title}</h3>
          <p className="text-sm text-[var(--mute)] font-sans m-0">{s.body}</p>
          <div className="diagram-panel">
            <MermaidChart chart={s.chart} className="mermaid-output" />
          </div>
        </section>
      ))}
    </article>
  );
}
