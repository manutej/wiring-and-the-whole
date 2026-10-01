# Context compact — cold-start snapshot (2026-10-01)

Single page for agents resuming on **`main`**. Detail lives in linked files; do not duplicate long inventories here.

## Mission

Map production codebases as a **module of systems** (T1), find symmetries/invariants (T2), beat naive token dumps at matched fidelity (T3). Paper: Libkind & Myers arXiv:2505.18329v2. Claims ladder in `plans/ADVERSARIAL.md` — **demonstrated ≠ proved**.

## On main today

| Area | Status |
|------|--------|
| E1 witness | **13/13** — `witness/` |
| E2 / E3 | WIN + B-PASSES — frozen under **`make verify`** |
| E5 depth | B-PASSES AT DEPTH — `experiments/e5-depth/` (not in verify yet) |
| Pulse | **`docs/PULSE.md`** — trigger `pulse`; **`make pulse-eval`** (functional) + **`make pulse-gate`** |
| WiringMap v0 | `wiringmap/schema.v0.json` + toybank example; **`make wiringmap-check`** |
| Density ladder | D0–D3 `fixtures/density/` + **D4** external slice — **`make wiringmap-stress`** |
| External thin slice | `fixtures/external/fineract-handlers-thin/` (7 handlers, vendored) — **`make external-slice-check`** |
| L1 dogfood | meta / toybank / fineract-thin packs + **`make dogfood-grade*`** |
| SKILL mint | **3/3:** `interface-first-context`, `systems-intake`, **`symmetry-lens`** — [`skills/symmetry-lens/SKILL.md`](../skills/symmetry-lens/SKILL.md) |

## Verify & interface checks

```bash
make verify                      # witness + E2 + E3 frozen
make wiringmap-check             # toybank accounts
make wiringmap-stress            # D0–D4 expectations
make external-slice-check        # fineract-handlers-thin
make dogfood-grade               # meta L1 questions
make dogfood-grade-toybank
make dogfood-grade-fineract-thin
make fetch-slice-dry-run        # fineract thin slice stub; temp staging only
make pack-v0-check              # L2 pack + reexpand + canonical LEGEND gate
make pulse-eval                 # functional negative/positive interface eval
make pipeline-io                # E2E: files → subprocess tools → JSON report
make pulse-gate
```

## Honest limits (external slice)

- Extractors read **`// refs:`** only — not full Spring DI graphs.
- Fineract slice is **vendored subset**, not live `apache/fineract` checkout.
- `doctrine_tag` on edges is **v0 convention**, not proven doctrine (GA10).

## Pulse R4 on main (2026-10-01)

- **A** — `scripts/fetch_fineract_slice.sh` + **`make fetch-slice-dry-run`** (PATH LIST stub; `--apply` updates slice + MANIFEST).
- **B** — **`symmetry-lens`** minted; dogfood D3 orbit / toybank boundary next.
- **C** — `scripts/build_l2_pack.py` + **`make pack-v0-check`** (reexpand + canonical LEGEND).

## Next jumps

1. Real upstream sparse-checkout / archive in fetch script (replace local corpus stub).
2. symmetry-lens dogfood report on D3 + fineract thin wiringmap.
3. Pack v0 on fineract handler family; keep LEGEND parity with E5 rules.

## Pointers

- Resume: `HANDOFF.md` · Build order: `docs/roadmap/BUILD-OUT-RESEARCH.md`
- Witness: `docs/witness/index.html` · L1 skill: `skills/interface-first-context/SKILL.md`
- Fixtures: `fixtures/density/README.md`, `fixtures/external/README.md`
