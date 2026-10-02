import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { SiteNav } from "@/components/SiteNav";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Wiring & the Whole — graph preview",
  description:
    "Live preview of WiringMap v0, E1 witness, and pipeline I/O graphs for wiring-and-the-whole.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen`}
      >
        <header className="max-w-4xl mx-auto px-5 pt-8 pb-4 border-b border-[var(--line)]">
          <p className="text-xs uppercase tracking-widest text-[var(--mute)] font-sans">
            wiring-and-the-whole · graph preview
          </p>
          <h1 className="text-2xl font-normal mt-1 mb-3">
            Graph-level views
          </h1>
          <SiteNav />
        </header>
        <main className="max-w-4xl mx-auto px-5 py-8">{children}</main>
        <footer className="max-w-4xl mx-auto px-5 pb-10 text-sm text-[var(--mute)]">
          Source:{" "}
          <a
            className="text-[var(--vermillion)]"
            href="https://github.com/manutej/wiring-and-the-whole"
          >
            manutej/wiring-and-the-whole
          </a>
          {" · "}
          <a
            className="text-[var(--vermillion)]"
            href="https://github.com/manutej/wiring-and-the-whole/blob/main/docs/GRAPH-SHOWCASE.md"
          >
            GRAPH-SHOWCASE.md
          </a>
        </footer>
      </body>
    </html>
  );
}
