# Adversarial panel — pulse CI pack-blind results (2026-10-02)

Independent gap list vs [`plans/ADVERSARIAL.md`](../../../plans/ADVERSARIAL.md). Not implementer recap.

## Gaps (ranked)

**G1 — Archived stub is not auto-regenerated (severity: medium)**  
CI compares live stub grades to a hand-pinned JSON file. If the harness adds a third case but nobody updates the stub, the gate fails — good — but success does not prove the stub was refreshed after intentional harness changes.  
*Cheap check:* brief must say when to bump `stub.report.v0.json`.

**G2 — Schema allows null accuracy but not wrong types (severity: low)**  
`accuracy_stub` is nullable; no pulse-eval probe injects a string into that field on the archived file.  
*Cheap check:* optional future negative test on schema-only validate path.

**G3 — LLM lane still off CI (severity: low for this pulse)**  
Live compare runs with default env; `llm_invoked` stays false. External model scores remain unclaimed.  
*Cheap check:* executive report “Next” mentions live baselines.

**G4 — Meaty duration is honor-system (severity: low)**  
Five-minute meaty rule lives in docs; no Makefile timer enforces it.  
*Cheap check:* report metadata must show plausible UTC span and double `pulse-loop`.

**G5 — E5-depth not in default verify (severity: low)**  
Optional spot check script exists; not wired into `make verify`. Comprehension depth claims still frozen elsewhere.  
*Cheap check:* report “Tested” notes one-off e5 grade run if executed.

## MUST-PROVE hooks

- MP-ci-results-1: `make pack-blind-results-check` in pulse-eval with deliberate drift failure case.
- MP-ci-results-2: CONTEXT-COMPACT “next scale jumps” advances past archived-results CI item.

## Suggested non-echo checks

| Check | Status |
|-------|--------|
| Tampered `questions_count` in archived JSON fails compare | covered in pulse-eval |
| Schema reject missing `firewall` const | not yet (schema validate only on good file) |
| Unified eval JSON still independent of archived stub | covered by existing pulse-eval |
