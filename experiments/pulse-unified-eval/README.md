# Pulse unified eval (v0)

Single JSON report combining:

- [`pack-blind-eval`](../pack-blind-eval/) — prompt bundle firewall + stub I/O grade (meta + handler-wedge)
- [`cr-f95-stub`](../cr-f95-stub/) — question firewall + token column + reserved accuracy column

```bash
make pulse-unified-eval-check
```

Optional LLM lane: `PACK_EVAL_LLM=1` plus `OPENAI_API_KEY` (or `PACK_EVAL_OPENAI_API_KEY`). Top-level `llm_invoked` stays `false` unless the LLM lane actually runs.

Individual gates remain for covariant debugging:

```bash
make pack-blind-eval-check
make cr-f95-stub-check
```
