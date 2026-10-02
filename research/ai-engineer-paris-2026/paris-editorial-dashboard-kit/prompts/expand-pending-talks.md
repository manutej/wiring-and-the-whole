# Prompt: expand pending Paris talk pages

Use with a high-quality coding agent after extracting the editorial kit.

---

Expand every entry in `stubs/talks-pending.json` into a full `Talk` in `explorer/src/data/talks.ts`.

**Inputs:** `data/digest.json`, `data/transcript-summaries.json`, `data/catalog.json`, existing `talks.ts` for tone.

**Rules:**

1. Assign a unique `slug` per talk; wire hash route if needed.
2. `thesis` = one argumentative paragraph; `hook` = scene-setting (can use digest hook, trimmed).
3. Pull **at least two** digest `bullets` into `stats` or symbol meanings with timestamps preserved in `cite` or label footnotes.
4. Choose `diagram` + `vocab[].viz` from existing unions when possible; only extend `MiniViz` / `SymbolDiagram` if the talk needs a new teaching visual (e.g. covariant eval flywheel for W&B).
5. Update `HubPage.tsx` so new talks appear in the grid with transcript badge and theme.
6. Run `npm run build` in `explorer/` and fix errors.

**Pending IDs (snapshot):** see `stubs/talks-pending.json` — typically W&B self-improving agent, Warp harness, WorkOS factory skeptic.

Deliver: diff summary listing new slugs, new viz/diagram types (if any), and hub changes.
