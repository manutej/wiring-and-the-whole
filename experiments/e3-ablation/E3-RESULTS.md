# E3-RESULTS

## Question

Do models read the factored form, or do you pay a comprehension tax?

## Authoritative recovered results

- Wiring pool: **16** questions.
- Arms: **A = explicit**, **B = factored**, **C = degraded control**.
- Accuracy: **A 93.8% / B 95.3% / C 0%**.
- Prompt cost: **A = 2089 tokens / B = 1316 tokens / B = 63% of A**.
- Recovery note from issue #1: hashes were frozen pre-call and the gate was byte-identical.

## What this MAY mean

- On one convention-heavy `@CommandType` family, the factored representation did **not** show a
  ≥5-point comprehension tax at pilot scale.
- A useful control floor existed: the degraded control arm scored 0%.

## What this MAY NOT mean

- The result generalizes across repos or corpora.
- Full-protocol E3 has been done.
- CR@F95 or any larger benchmark claim has been established.
