import Link from "next/link";

const cards = [
  {
    href: "/wiringmap",
    title: "WiringMap v0 — toybank accounts",
    body: "Mermaid flowchart from toybank-accounts.v0.json (4 units, 3 junctions, 8 edges).",
  },
  {
    href: "/fineract",
    title: "Fineract thin slice (7 handlers)",
    body: "Real vendored @CommandType handlers — map matches make pipeline-io on main.",
  },
  {
    href: "/charter",
    title: "Fineract charter (~1k LOC)",
    body: "29-handler pinned vertical — manifest drift + 90 ref tokens (M2 scale-honest slice).",
  },
  {
    href: "/scale",
    title: "Scale & compound diagrams",
    body: "Mermaid: programme ladder, slice matrix shards, wiring+math gates, Rust pipeline.",
  },
  {
    href: "/spine",
    title: "Rust migration spine",
    body: "This repo’s own harness wiring: Python tools → wiring-core Phase 1 targets.",
  },
  {
    href: "/witness",
    title: "E1 witness narrative",
    body: "Embedded docs/witness/index.html — pipeline ASCII, toybank module graph, pushout diagram, 13-check table.",
  },
  {
    href: "/pipeline",
    title: "make pipeline-io flow",
    body: "Sequence diagram for extract → WiringMap → L2 pack → JSON report (from programme docs).",
  },
];

export default function Home() {
  return (
    <div className="space-y-6">
      <p className="max-w-2xl leading-relaxed">
        Stakeholder preview for graph-shaped artefacts in the repo — not raw JSON.
        Data is loaded from checked-in WiringMap JSON (toybank, Fineract thin, repo spine) and static witness HTML.
      </p>
      <ul className="grid gap-4 sm:grid-cols-1">
        {cards.map((c) => (
          <li key={c.href}>
            <Link
              href={c.href}
              className="block diagram-panel hover:border-[var(--vermillion)] transition-colors"
            >
              <h2 className="text-lg font-normal mb-1">{c.title}</h2>
              <p className="text-sm text-[var(--mute)] font-sans m-0">
                {c.body}
              </p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
