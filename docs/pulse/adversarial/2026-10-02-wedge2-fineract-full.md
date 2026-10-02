# Adversarial panel — Wedge 2 fineract-thin full wiring (2026-10-02)

Independent gap list vs [`plans/ADVERSARIAL.md`](../../../plans/ADVERSARIAL.md). Not implementer recap.

## Gaps (ranked)

**G1 — Still seven handlers, not a family (severity: medium)**  
Full wiringmap on `fineract-handlers-thin` proves extract ↔ map ↔ L2 pack on a **chartered PATH LIST**, not the 514-handler `@CommandType` family (Wedge 1 covers 29/30 in a separate pool).  
*Cheap check:* SCALE-PATH Wedge 1 vs Wedge 2 tables stay distinct.

**G2 — `// refs:` hand authorship (severity: medium)**  
All nine edges are comment-maintained; no auto-sync from Java bodies or Spring DI. Parser v1 in `command_handler_parse.py` is not wired into external-slice-check.  
*Cheap check:* edge-recall + pipeline-io ref count parity; no claim of reflection wiring.

**G3 — Junction stubs only (severity: low)**  
Six platform services are labels, not vendored implementations — comprehension of real Fineract behavior still out of slice.  
*Cheap check:* L1 omissions log + README “not full Fineract.”

**G4 — Graph preview stale (severity: low)**  
Vercel graph preview on `main` still toybank-only; fineract map not visualized until preview source is restored in-repo.  
*Cheap check:* GRAPH-SHOWCASE / preview rebuild when `preview/graph/src` returns.

**G5 — Live sparse-checkout pin (severity: medium, deferred)**  
`MANIFEST.txt` remains `manual pin`; `fetch_fineract_slice.sh --apply` not exercised against live apache/fineract in CI.  
*Cheap check:* fetch-slice dry-run + manifest drift gate only.

## MUST-PROVE hooks

- MP-wedge2-1: `make pipeline-io` fineract branch must keep ref_token_count == pack explicit edges when map grows.
- MP-wedge2-2: Edge-recall sample count tracks thin-slice ref pairs without implying staff-scale recall.
