# Blind pack-only eval (v0)

Bundles **L1 markdown + question text** for external or stub grading. Frozen `expected` values stay in repo question JSON only — not in prompt bundles under [`fixtures/pack-blind-eval/bundles/`](../../fixtures/pack-blind-eval/bundles/).

## Stub mode (default)

```bash
make pack-blind-eval-check
```

Runs pack I/O grader (`grade_l1_questions.py --answer-mode io`) per case and writes prompt-only JSON bundles.

## Optional LLM lane

Set `PACK_EVAL_LLM=1` and `OPENAI_API_KEY` (or `PACK_EVAL_OPENAI_API_KEY`). Without a key, the harness reports `skipped_no_api_key` and still passes stub checks.

```bash
PACK_EVAL_LLM=1 OPENAI_API_KEY=... python3 scripts/pack_blind_eval_run.py
```

## Cases (v0)

| pack_id | Questions |
|---------|-----------|
| `meta-l1-wiring-and-the-whole` | `docs/dogfood/L1-QUESTIONS.json` |
| `handler-wedge-l1` | `docs/dogfood/L1-E3-COMMANDHANDLER-WEDGE-QUESTIONS.json` |
