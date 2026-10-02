# External research corpus charter

YouTube / conference ingest (`research/ai-engineer-paris-2026/`, `research/every-to/`, future corpora) is **hypothesis inventory and cited evidence**. It is **not** the double operadic programme (HANDOFF T1–T3).

## Allowed effects

- Add or update **catalog**, **digest**, **transcript** files with provenance and timestamps.
- Propose **registry rows** in `docs/research-insights/*.yaml` for adoption into SKILL / L1 / pulse.
- Optional **editorial UI** on dedicated branches; teaching pages must separate fact vs inference.

## Forbidden without programme pulse

- Changing **claims** in HANDOFF, OPTIONS, ADVERSARIAL, or MUST-PROVE status based on talk themes alone.
- Reordering **BUILD-OUT-RESEARCH** priority using `dominant_narratives` without adversarial note.
- Editing **`witness/WITNESS.json`**, **`experiments/e2-tokens/E2-RESULTS.json`**, **`experiments/e3-ablation/E3-GRADES.json`** from research lanes without protocol + verify intent.
- **Generative hub/explorer** copy merged to `main` without `make verify-research` (when implemented) and pulse docs lane.

## Ingest loop rules

- **TubeAlfred / API failures** must set explicit status in `digest.json` or `ingest.json` (e.g. skipped credits)—never silent no-op.
- **CI must not** depend on live transcript fetch; committed JSON is truth.
- Batch transcripts when credits allow; prioritize `next_ingest_priority` / views.

## Generative work

Follow **`docs/PULSE.md`**: implementer brief, separate adversarial panel, `make verify`, `make pulse-eval`, firewalled evaluator. Implementer **must not** read `docs/pulse/RUBRIC-EVALUATOR.md` during the same pulse.

## Merge to `main`

Research merges should prefer **corpus allowlist**: JSON, schemas, scripts, LOOP logs, README, registry YAML—not frontend vendor trees unless verify includes reproducible build.
