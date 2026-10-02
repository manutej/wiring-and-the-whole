---
name: systems-intake
description: Scope a slice before L1/wiringmap work — six systems-theory questions, omissions log, covariant eval reminder. Auto-apply before new witness slices, Fineract handler packs, or WiringMap v0 JSON instances.
---

# systems-intake

**Status:** v0 instrument — feeds step 1 of [`interface-first-context`](../interface-first-context/SKILL.md).

## When to use

- New witness slice or density fixture before writing `// refs:` lines.
- Before hand-authoring a WiringMap v0 JSON instance.
- When changing **harness + fixture together** (covariant eval — see below).

## When NOT to use

- Full automated extraction or doctrine proving (GA10 — witness demonstrated only).
- Replacing pulse adversarial / evaluator lanes.

## Six questions (scope questionnaire)

1. **What is a system here?** — Name compilation units / services that count as nodes (not files for their own sake).
2. **What is an interface?** — Exported ports only: signatures, topics, DTO fields visible from outside.
3. **What is an interaction?** — Typed edges between interfaces (call, ref, import, …); no bodies yet.
4. **What is a system map?** — Vertical maps (refactor, port, mock) you care about for this slice.
5. **What is an interaction map?** — Horizontal compatibility (API version, protocol) across the boundary.
6. **What is omitted and why?** — Bodies, other verticals, shared libs — each with a reason tag (`out-of-slice`, `impl-local`, …).

## Covariant evals (W&B / Paris `wb-covariant-evals`)

Benchmark, **harness**, and agent **config** move together. When intake adds a new ref edge or handler to a slice:

- Bump **wiringmap JSON** and **`// refs:`** in the **same PR** as any change to `extract_refs.py`, `fineract_slice_check.sh`, or L1 grading heuristics.
- If you change how success is measured, change the **frozen fixture or gate** that proves it — not slides alone.
- Programme gates: `make external-slice-check`, `make verify-research` (research lane), `make pulse-eval` (functional) as applicable.

## Outputs (target)

- Slice path + budget (file count / depth).
- Parallel product marks (`witness/.../savings/ ‖ accounts/`).
- Omissions log table (feeds L1 pack quality gate).

## Quality checklist

- [ ] Every wired handler has matching `// refs:` tokens reflected in wiringmap `evidence` fields.
- [ ] Junction nodes label out-of-slice platform services (not fake internal units).
- [ ] README states what is **not** included (not a full upstream checkout).

## Provenance

- Paris insight: `docs/research-insights/paris-2026.yaml` → `wb-covariant-evals` (adopted 2026-10-02).
