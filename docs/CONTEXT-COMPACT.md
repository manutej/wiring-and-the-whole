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
| Pulse | **`docs/PULSE.md`** — trigger word `pulse`; **`make pulse-gate`** |
| WiringMap v0 | `wiringmap/schema.v0.json` + toybank example; **`make wiringmap-check`** |
| Density ladder | D0–D3 `fixtures/density/` + **D4** external slice — **`make wiringmap-stress`** |
| External thin slice | `fixtures/external/fineract-handlers-thin/` (7 handlers, vendored) — **`make external-slice-check`** |
| L1 dogfood | meta / toybank / fineract-thin packs + **`make dogfood-grade*`** |
| SKILL mint | **2/3 stub:** `interface-first-context`, `systems-intake` — **`symmetry-lens`** not minted |

## Verify & interface checks

```bash
make verify                      # witness + E2 + E3 frozen
make wiringmap-check             # toybank accounts
make wiringmap-stress            # D0–D4 expectations
make external-slice-check        # fineract-handlers-thin
make dogfood-grade               # meta L1 questions
make dogfood-grade-toybank
make dogfood-grade-fineract-thin
make pulse-gate
```

## Honest limits (external slice)

- Extractors read **`// refs:`** only — not full Spring DI graphs.
- Fineract slice is **vendored subset**, not live `apache/fineract` checkout.
- `doctrine_tag` on edges is **v0 convention**, not proven doctrine (GA10).

## Next 3 jumps (small, stable)

```
  [A] fetch/pin slice script     [B] symmetry-lens SKILL
         │                              │
         └──────────┬───────────────────┘
                    v
           [C] pack builder v0 (one handler family, E2 gate)
```

1. **A** — `scripts/fetch_fineract_slice.sh` or submodule pin; refresh thin slice without whole-tree reads.
2. **B** — mint `symmetry-lens`; dogfood on D3 orbit or toybank savings boundary.
3. **C** — L2 factored pack from one family; byte-identical re-expansion (E2 pattern).

## Pointers

- Resume: `HANDOFF.md` · Build order: `docs/roadmap/BUILD-OUT-RESEARCH.md`
- Witness: `docs/witness/index.html` · L1 skill: `skills/interface-first-context/SKILL.md`
- Fixtures: `fixtures/density/README.md`, `fixtures/external/README.md`
