# WiringMap v0 (schema only)

Machine-readable **L1 feedstock**: compilation units, exported ports, typed wiring edges, optional junction nodes. Feeds [`skills/interface-first-context/`](../skills/interface-first-context/SKILL.md) and future pack builder v0. **No extractor in this folder yet** — examples are hand-curated.

## Files

| File | Purpose |
|------|---------|
| [`schema.v0.json`](schema.v0.json) | JSON Schema (draft 2020-12) for instances |
| [`examples/toybank-accounts.v0.json`](examples/toybank-accounts.v0.json) | 4 units, 8 edges from `witness/toybank/accounts/` |

## Instance shape (ASCII)

```
  meta { repo, ref, slice }
        │
        ├── junctions[]  (DTO / topic / table glue)
        │
        ├── units[] ── ports[]  (exported flags)
        │
        └── edges[]   from ──edge_kind──► to
                      (port:id | unit:id)     (port:id | junction:id)
```

## ID conventions

- `unit:{qualified.name}` — one compilation unit / system card
- `port:{qualified.name}#{symbol}` — exported or internal port
- `junction:{label}` — shared node not owned by one unit
- `edge:{slug}` — stable edge name for diffs

## Edge kinds

| `edge_kind` | Meaning |
|-------------|---------|
| `call` | Control/data flow to another unit's port |
| `ref` | Static reference (comment-mined or import) |
| `import` | Module/import edge (extractor future) |
| `di` | Injection/wiring config (Fineract future) |
| `link` | Non-call association (doc, config) |

`doctrine_tag` is a **v0 naming convention only** — optional prose alignment (`interface`, `system_map`, `junction`, `unknown`); **not proven doctrine** and not a formal guarantee until MUST-PROVE 1 (see `plans/ADVERSARIAL.md` GA1 / GA10).

## Validate locally

From repo root (installs `jsonschema` if needed):

```bash
make wiringmap-check
```

Or run scripts directly:

```bash
python3 -m pip install jsonschema
python3 scripts/validate_wiringmap.py
python3 scripts/extract_toybank_refs.py
python3 scripts/extract_refs.py witness/toybank/accounts
make wiringmap-stress   # density ladder D0–D3 (see fixtures/density/README.md)
```

## Dogfood grading

```bash
make dogfood-grade          # meta L1 pack
make dogfood-grade-toybank  # toybank accounts L1 pack
```

## Meta-structure (Data / Backend / …) — not a v0 primitive yet

**WiringMap v0 is an evidence graph only:** `units`, `junctions`, `edges`. It does **not** declare:

- architectural meta-layers (`Data`, `Backend`, `API`, …),
- parent/child **cluster** trees,
- or domain ontologies (`loan`, `savings`, …).

What exists today that *resembles* layering (all optional / weak):

| Field | Scope | Limit |
|-------|--------|--------|
| `junction` + `junction_kind` | Shared **hub** nodes (`dto`, `table`, `topic`, …) | Fineract charter maps mostly use `other`; not “Backend vs Data”. |
| `unit.role` | Free string on each unit | No enum, no hierarchy. |
| `edge.doctrine_tag` | Hint on an edge | Not structure; not proven doctrine (GA10). |

**Hub-and-spoke** (handler units → platform junctions) is implicit in edges, not a declared tree.

Preview UI (`stalk volume`, ontology chips) **derives** stack strata (handler / platform / infra), domain sectors, and layout from heuristics — that logic must **not** become the long-term source of truth at 10k+ LOC / multi-repo scale.

### Scalable direction: facts + frame overlay

Keep **`wiringmap.v0.json`** as immutable-ish **facts** (extractor output + human evidence).

Add a separate artifact (proposed name **`wiring-frame.v0`**) for **views**:

- **`frames[]`** — nodes in a meta-taxonomy (`frame_kind`: `meta_layer` | `domain` | `package` | `hub_cluster`), optional **`parent_id`** for hierarchy.
- **`memberships[]`** — `{ entity_id, frame_id, role?: hub | leaf | member }` linking `unit:` / `junction:` / `port:` ids into frames.
- **`levels[]`** (optional) — ordered planes for viz (substrate → platform → surface), aligned with [stalks-and-sections](https://github.com/manutej/stalks-and-sections) / [cell-sheaf](https://github.com/manutej/cell-sheaf) without overloading WiringMap.

Extractors may **suggest** memberships (package path → `package` frame; `*WritePlatformService` → `Backend` + `Data` edges); humans or pulse eval **pin** frames for charter slices. One **`wiring_core` graph IR** should load map + frame and feed preview, pack, and sheaf export — see [`docs/architecture/2026-10-02-rust-core-multireader.md`](../docs/architecture/2026-10-02-rust-core-multireader.md) (D1 paydown).

**Trimming rule:** delete or demote preview-only classifiers once the same classification is stored in `wiring-frame.v0` or emitted from Rust IR.

## Next engineering jumps

1. Read-only extractor: parse `// refs:` lines in toybank → emit v0 JSON.
2. Fineract vertical slice (30–50 files) with same schema.
3. L1 markdown emitter from v0 JSON (interface-first-context output template).
4. **`wiring-frame.v0` schema + charter overlay** (meta-layers + domain groups + hub clusters) before more viz features.
