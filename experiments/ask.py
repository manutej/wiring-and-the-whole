#!/usr/bin/env python3
"""Pinned-model evaluator call for E3/E5-style runs.

    python3 ask.py --model claude-sonnet-5 prompts/B_v2.txt responses_v2/B_sonnet.txt

Sends one prompt file as a single user turn to exactly one model, writes the text
reply to the output path, and appends a run record (model requested, model served,
prompt sha256, response id, usage, stop reason) to runs.jsonl beside the output.
Credentials come from the environment (ANTHROPIC_API_KEY or an `ant auth login`
profile); nothing is read from the repo.

Deliberate choices, recorded so the protocol reads them:
- The model id is required and passed through unchanged. No server-side fallbacks:
  a fallback would silently answer with a different model and break the pin.
- No `thinking` parameter is sent, so each model runs its own default and the pin
  is the model id alone. Nothing about reasoning depth is being measured here.
- A reply that stops for any reason other than end_turn is an error, not data.
"""
import argparse, datetime, hashlib, json, os, sys
import anthropic

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--model", required=True, help="exact model id, e.g. claude-sonnet-5")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("prompt", help="prompt file sent as the single user message")
    ap.add_argument("out", help="where the reply text is written")
    a = ap.parse_args()

    prompt = open(a.prompt).read()
    client = anthropic.Anthropic()
    try:
        r = client.messages.create(model=a.model, max_tokens=a.max_tokens,
                                   messages=[{"role": "user", "content": prompt}])
    except anthropic.NotFoundError as e:
        sys.exit(f"model {a.model!r} not found or not available to this key: {e.message}")
    except anthropic.APIStatusError as e:
        sys.exit(f"API error {e.status_code} ({e.type}): {e.message}")
    except anthropic.APIConnectionError as e:
        sys.exit(f"connection failed: {e}")

    if r.stop_reason != "end_turn":
        sys.exit(f"reply stopped with {r.stop_reason!r}, not end_turn; nothing written")
    text = "".join(b.text for b in r.content if b.type == "text")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w").write(text)

    record = {"at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "model_requested": a.model, "model_served": r.model, "response_id": r.id,
              "prompt": os.path.relpath(a.prompt), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
              "out": os.path.relpath(a.out), "stop_reason": r.stop_reason,
              "usage": {"input": r.usage.input_tokens, "output": r.usage.output_tokens}}
    with open(os.path.join(os.path.dirname(os.path.abspath(a.out)), "runs.jsonl"), "a") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps(record, indent=1))

if __name__ == "__main__":
    main()
