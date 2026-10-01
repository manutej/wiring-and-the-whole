# Context compact — cold-start snapshot (2026-10-01)

Single page for agents resuming on **`main`**. Detail lives in linked files; do not duplicate long inventories here.

## Mission

Map production codebases as a **module of systems** (T1), find symmetries/invariants (T2), beat naive token dumps at matched fidelity (T3). Paper: Libkind & Myers arXiv:2505.18329v2. Claims ladder in `plans/ADVERSARIAL.md` — **demonstrated ≠ proved**.

## On main today

| Area | Status |
|------|--------|
| E1 witness | **13/13** — `witness/` + `make witness` |
| E2 / E3 | WIN + B-PASSES — frozen under **`make verify`** |
| E5 depth | B-PASSES AT DEPTH — scripts in `experiments/e5-depth/` (not in verify yet) |
| Repro | **`make verify`** = witness + E2 JSON + E3 grades (needs python3 + node) |
| SKILL mint | **1/3:** `skills/interface-first-context/` — `systems-intake`, `symmetry-lens` **stub only** (outline below) |
| WiringMap | **This PR line:** `wiringmap/schema.v0.json` + toybank example — **no extractor** |

## Verify

```bash
make verify    # from repo root; see experiments/README.md
```

## Open work (PRs may land out of order)

Check GitHub for live state; merge-conflict pass (2026-10-01) resolved memo-only overlaps:

- interface-first-context skill, repro runner, dogfood L1 meta pack, ASCII HANDOFF note — see `docs/MERGE-CONFLICT-REPORT.md` for history, not live queue.

**Engineering queue (artifacts-first):**

1. WiringMap v0 schema + one populated example (toybank) — **in flight**
2. Mint `systems-intake`, `symmetry-lens` SKILL.md (zero-code; one dogfood each)
3. Pack builder v0 (one Fineract family; E2 re-expansion gate)
4. Witness C₀ → Code_X split; MUST-PROVE 1–2 hook
5. Full E3 + Fineract wedge + E4 migration (after map + pack)

## Next 3 jumps (small, stable)

```
  [A] wiringmap schema + toybank instance  ──►  [B] L1 dogfood accounts slice
           │                                              │
           └──────────────────┬───────────────────────────┘
                              v
                    [C] static extractor stub (imports/refs only)
```

1. **A** — `wiringmap/schema.v0.json`, README, example JSON from `witness/toybank/accounts/` (3–4 units, typed edges).
2. **B** — `docs/dogfood/L1-toybank-accounts.md` companion to meta L1 pack.
3. **C** — read-only extractor CLI that emits v0 JSON from toybank (no Fineract yet).

## systems-intake / symmetry-lens (mint debt — not shipped)

- **systems-intake:** scope questionnaire → slice boundary + parallel product marks (`‖`) + omissions reasons; feeds L1 skill step 1.
- **symmetry-lens:** orbit table on exact-iso cells only (GA2); toybank planted orbit as demo; no L3 packer.

## Pointers

- Resume narrative: `HANDOFF.md` (trimmed; defers here for queue)
- Build order: `docs/roadmap/BUILD-OUT-RESEARCH.md`
- L1 instrument: `skills/interface-first-context/SKILL.md`
