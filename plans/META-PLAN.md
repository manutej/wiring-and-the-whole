# META-PLAN (L2) — "Wiring-Mapper from Double Operadic Systems Theory"
[restored verbatim 2026-09-16; kaizen edit #1 from CONSENSUS.md applies]

Generated per /meta-planning consuming /meta-prompting output; operadically typed per
/meta-operad (edges are colored; every phase gate is an OC check: composed parts must agree
with the collapsed whole). Assumptions stated inline; no clarifying questions.

## Level check
Input TASK is itself meta-shaped: "do to this paper what meta-suite did to On Meta-Prompting."
Category = *paper → instrument-suite transformation*. Free variables: source paper, target
capability set, deliverable media. Invariants: tunnel-vision sourcing; think-before-code;
consensus gate before digestion; rich indexed knowledge base; options split code/mental-model.

## Typed work-unit graph

Colors (edge types): `:ideation`, `:consensus`, `:wiki_page`, `:index`, `:synthesis`,
`:dashboard_html`, `:options`, `:verdict`. [+`:skill` per kaizen edit #1]

- **WU0 Frame** (done): brief → IDEATION.md + this plan. out: `:ideation`
- **WU1 Consensus** — 4 fable agents, ONE parallel batch, headless. in: `:ideation` out: 4×`:verdict`
  Gate G1 (OC): agents receive the *collapsed* brief (one paragraph) AND the *decomposed*
  ideation; if their reconstruction of "what should be built" diverges from IDEATION.md's T1–T3,
  the framing is inconsistent → repair before digestion. Consensus rule: majority keep/kill per
  hypothesis; all P0 objections must be integrated or explicitly rebutted in CONSENSUS.md.
- **WU2 Digest ×7** — parallel subagents, page-ranged (§1:1–8, §2:9–18, §3:19–31, §4:32–48,
  §5–6:49–54, §7:55–67, §8:68–80). Each writes `wiki/NN-*.md`: plain summary, key definitions
  (real math), theorems/constructions, and JUICE HOOKS (mappings to T1/T2/T3) [+INSTRUMENT
  HOOKS per kaizen edit #1]. in: paper pages out: `:wiki_page`. Lane law: disjoint page ranges
  ⇒ parallel is algebraically licensed.
- **WU3 Index** — INDEX.md + glossary + concept→page→use-case crosswalk. in: 7×`:wiki_page`
  out: `:index`. Gate G2 (OC): index claims vs. per-page summaries must agree; spot-check 3
  concepts by re-reading source pages.
- **WU4 Synthesis** — SYNTHESIS.md: paper concept → codebase construct crosswalk; NOETHER.md:
  the symmetry⇒invariant program made precise; COMPRESSION.md: the token-accounting argument
  vs AST-aware/Headroom. in: `:index`,`:ideation`,4×`:verdict` out: `:synthesis`
- **WU5 Dashboard** — single-file HTML dashboard of the knowledge base + program [redefined as
  suite/knowledge INDEX per kaizen edit #1]. in: `:synthesis`,`:index` out: `:dashboard_html`
- **WU6 Options** — 3–5 practical high-ROI implementations; each: what it is, why direct ROI,
  code-required vs mental-model split, first falsifiable milestone, cost sketch. in:
  `:synthesis` out: `:options`. Gate G3 (OC): each option must re-compose to the brief's three
  targets; any option not traceable to a wiki page + ideation hypothesis is decomposition
  theater → cut. [+G3 amendment: every option mints an instrument or states why it can't.]
- **WU7 Mint** [added by kaizen edit #1] — each chosen instrument ships as a full SKILL.md.
  in: `:synthesis` out: N×`:skill`.

Critical path: WU0→WU1→WU2→WU3→WU4→(WU5∥WU6∥WU7).

## Verification & anti-slop
- No code written in this phase (constitution rule); "code" appearing in options is *description*.
- Every synthesis claim carries a provenance tag (wiki file / page number).
- OC discipline: consistency ≠ correctness — consensus and gates calibrate, they do not prove.
- Budget honesty: fable is expensive → exactly one consensus batch; digestion agents are
  page-scoped so no agent reads all 80 pages; index built from returns, not re-reads.

## Escalation
Blocked unknowns (U1–U5 in IDEATION.md) are spiked in later sessions, not now. Human-of-record:
CETI. Stop-the-line: any consensus agent flags the core compression claim as unfalsifiable.
