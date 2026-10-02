"use client";

import { useEffect, useId, useState } from "react";

type Props = {
  chart: string;
  className?: string;
};

export function MermaidChart({ chart, className }: Props) {
  const reactId = useId().replace(/:/g, "");
  const [svg, setSvg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setSvg(null);
    setError(null);

    (async () => {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({
          startOnLoad: false,
          theme: "neutral",
          securityLevel: "strict",
          flowchart: { htmlLabels: true, curve: "basis" },
        });
        const { svg: rendered } = await mermaid.render(
          `mmd-${reactId}`,
          chart,
        );
        if (!cancelled) setSvg(rendered);
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Mermaid render failed");
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [chart, reactId]);

  if (error) {
    return (
      <pre className="text-sm text-red-800 whitespace-pre-wrap">{error}</pre>
    );
  }

  if (!svg) {
    return <p className="text-sm text-[var(--mute)]">Rendering diagram…</p>;
  }

  return (
    <div
      className={className}
      dangerouslySetInnerHTML={{ __html: svg }}
      aria-label="Mermaid diagram"
    />
  );
}
