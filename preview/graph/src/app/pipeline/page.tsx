import { MermaidChart } from "@/components/MermaidChart";
import { pipelineIoMermaid } from "@/lib/wiringmapToMermaid";

export default function PipelinePage() {
  return (
    <article className="space-y-4">
      <div>
        <h2 className="text-xl font-normal mb-2">Pipeline I/O (programme flow)</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          High-level sequence aligned with{" "}
          <code className="font-mono text-xs">make pipeline-io</code> and{" "}
          <code className="font-mono text-xs">docs/GRAPH-SHOWCASE.md</code>.
          Validates extract ↔ WiringMap ↔ L2 pack ↔ re-expand; emits JSON to
          stdout.
        </p>
      </div>
      <div className="diagram-panel">
        <MermaidChart chart={pipelineIoMermaid} />
      </div>
    </article>
  );
}
