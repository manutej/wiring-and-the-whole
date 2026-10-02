# Adversarial panel — meta-evaluator hook pulse (2026-10-02)

Independent gap list vs [`plans/ADVERSARIAL.md`](../../../plans/ADVERSARIAL.md). Not implementer recap.

## Gaps (ranked)

**G1 — Craft checkout is optional (severity: medium)**  
The post-loop bundle lists craft skills only when a sibling `craft/` tree or `CRAFT_SKILLS_ROOT` is present. Operators without that checkout get programme pointers only — not a failure, but easy to misread as “craft integrated” when the index is empty.  
*Cheap check:* pulse gate requires ≥9 skills only when craft root resolves; missing root must stay a hard fail in CI only if we pin craft as submodule later.

**G2 — Meta bundle is not the firewalled evaluator (severity: high if confused)**  
Hook output names forbidden paths but does not score the pulse. Treating JSON stdout as SHIP would skip rubric lane.  
*Cheap check:* META-EVALUATOR.md “When to run” table says post-SHIP only.

**G3 — GA7 / live accuracy unchanged (severity: low)**  
Unified eval and blind-pack stubs still run with no model call; accuracy column stays empty.  
*Cheap check:* bundle must not mention CR@F95 as measured.

**G4 — Paris research still off main (severity: low)**  
Craft index points at external repo; Paris ingest branches unchanged.  
*Cheap check:* LOOP-ENGINEERING lane table unchanged.

**G5 — Rubric text leakage regression (severity: medium)**  
New JSON generator could accidentally embed evaluator dimensions in future edits.  
*Cheap check:* meta-evaluator-check asserts no `D1`–`D7` substrings and no RUBRIC-EVALUATOR path contents in bundle.

## MUST-PROVE hooks

- MP-meta-1: Any future craft submodule must not bypass implementer firewall (craft is guardrails, not programme scorer).
- MP-meta-2: Executive reports stay jargon-free per PULSE-REPORT-SPEC; meta JSON stays operator-facing.

## Suggested non-echo checks

| Check | Status |
|-------|--------|
| Invalid `CRAFT_SKILLS_ROOT` fails meta-evaluator-check | covered (manual probe) |
| meta-evaluator-check inside pulse-eval battery | covered (34/34) |
| Bundle omits rubric file bodies | covered in hook asserts |
