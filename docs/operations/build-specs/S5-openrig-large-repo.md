# Build spec S5 — large repo leap (OpenRig)

**Target upstream:** [mvschwarz/openrig](https://github.com/mvschwarz/openrig) — YAML RigSpec topologies, daemon domain services, CLI/MCP/UI (TypeScript).

**Goal:** Measure and **partially wire** a large external repo without reading every line in the idle case; batch workers append structured facts to memory.

## Principles

1. **Inventory before content** — `scripts/repo_inventory_v0.py` uses `stat()` only (file counts, bytes by extension). Optional shallow `max-depth` for triage.
2. **Slice before whole** — define PATH LIST / package roots (e.g. `packages/daemon/src/domain/`, `packages/cli/src/`) before extract.
3. **Incremental memory** — `fixtures/wiring-index/discoveries.jsonl` via `scripts/wiring_index_store.py` (`wiring-index-record.v0`).
4. **Schema-first** — WiringMap v0 for wired verticals; repo inventory v0 for size; index records for partial facts.
5. **Workers** — future: N shard walkers (paths only) → M deep parsers (handler patterns, RigSpec `edges`) → reducer merges JSONL.

## Phases

| ID | Deliverable | Gate |
|----|-------------|------|
| S5a | Pin OpenRig ref + `repo_inventory_v0` report artifact | JSON schema validate |
| S5b | RigSpec / YAML edge extractor stub → index store | `wiring_index_store stats` |
| S5c | TS import graph sample (one package) without full-repo AST | bounded file list |
| S5d | Preview diagram route for OpenRig **slice** map (not full monorepo) | manual + eval |
| S5× | Independent SHIP | eval doc |

## Wiring hypothesis (OpenRig)

- **Nodes:** pods, seats, harness runtimes (from RigSpec).
- **Edges:** `delegates_to`, queue handoffs, MCP tool calls (to be validated against specs in repo).
- **Not in scope v0:** live tmux/session state — static spec + code cross-ref only.

## Commands (today)

```bash
# Inventory this repo (baseline)
python3 scripts/repo_inventory_v0.py --out fixtures/repo-inventory/wiring-and-the-whole.v0.json

# When OPENRIG_ROOT is cloned locally:
python3 scripts/repo_inventory_v0.py "$OPENRIG_ROOT" --out fixtures/repo-inventory/openrig.v0.json
```

## Open items

- Clone/pin OpenRig commit in fetch script (like Fineract charter fetch).
- Line-count estimation without full read: `wc -l` on PATH LIST batches only.
- Deduplicate index records by `(repo_root, path, kind, payload hash)`.
