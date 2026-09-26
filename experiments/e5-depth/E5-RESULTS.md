# E5-RESULTS

## Question

Does E3-style parity survive multi-hop / depth?

## Authoritative recovered results

- Evaluation size: **112 questions × 10 depth levels**.
- Corpus slice: **40 real Fineract units**.
- Audit: **veteran-QA evaluators** plus a **3-fable QA panel** review of the raw run.
- Raw run: pooled **B−A = −10.2 pts**, later attributed mostly to harness/spec defects.
- Audit finding: roughly **80%** of the apparent collapse was harness artifact.
- Spec defects called out in `HANDOFF.md`: undocumented `-` sentinel, ambiguous `*Repository*`
  glob, self-contradictory D9 key, and 4/10 decomposition-theater interview trees.
- Rerun / E5.1: **Sonnet 100% at every depth in both arms**; pooled **B−A = −3.7 pts**, inside
  the 5-point rule.
- Residual: haiku-only weakness on large-list enumeration, affecting both arms.
- Extra finding from issue #1: at this mixed 40-unit scale, **B = 11787** tokens vs
  **A = 12493** tokens, only **5.7% cheaper**.

## What this MAY mean

- Information-equivalence has to be **reader spec-equivalence**, not just builder re-expandability.
- After the legend/spec fixes, a strong model can read both forms at parity through depth 10.
- L2 savings appear sensitive to family homogeneity.

## What this MAY NOT mean

- The raw v1 collapse was evidence of model failure.
- Cross-corpus generality, CR@F95, or repo-scale savings have been shown.
- The operadic-interview v1 harness validated model reasoning.
