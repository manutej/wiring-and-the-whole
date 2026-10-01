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

`doctrine_tag` is optional prose alignment (`interface`, `system_map`, `junction`, `unknown`) — **not** a formal guarantee until MUST-PROVE 1 (see `plans/ADVERSARIAL.md` GA1).

## Validate locally (optional)

Python 3.10+ with `jsonschema` (not required for `make verify`):

```bash
python3 -c "
import json
from pathlib import Path
try:
    import jsonschema
except ImportError:
    raise SystemExit('pip install jsonschema for optional validation')
inst = json.loads(Path('wiringmap/examples/toybank-accounts.v0.json').read_text())
schema = json.loads(Path('wiringmap/schema.v0.json').read_text())
jsonschema.validate(inst, schema)
print('OK: toybank-accounts.v0.json')
"
```

## Next engineering jumps

1. Read-only extractor: parse `// refs:` lines in toybank → emit v0 JSON.
2. Fineract vertical slice (30–50 files) with same schema.
3. L1 markdown emitter from v0 JSON (interface-first-context output template).
