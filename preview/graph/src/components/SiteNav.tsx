import Link from "next/link";

const links = [
  { href: "/", label: "Overview" },
  { href: "/wiringmap", label: "Toybank" },
  { href: "/fineract", label: "Fineract thin" },
  { href: "/charter", label: "Charter 1k" },
  { href: "/charter-10k", label: "Charter 10k" },
  { href: "/scale", label: "Scale diagrams" },
  { href: "/spine", label: "Rust spine" },
  { href: "/witness", label: "E1 witness" },
  { href: "/pipeline", label: "Pipeline I/O" },
];

export function SiteNav() {
  return (
    <nav className="flex flex-wrap gap-3 text-sm font-sans">
      {links.map((l) => (
        <Link
          key={l.href}
          href={l.href}
          className="border-b border-[var(--line)] pb-0.5 text-[var(--vermillion)] hover:opacity-80"
        >
          {l.label}
        </Link>
      ))}
    </nav>
  );
}
