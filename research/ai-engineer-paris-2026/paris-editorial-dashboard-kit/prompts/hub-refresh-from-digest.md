# Prompt: refresh hub editorial layer from digest

---

Refresh the Paris explorer **hub** (`explorer/src/pages/HubPage.tsx`) using latest `data/digest.json` and `data/catalog.json`.

1. Update headline/subcopy to reflect `dominant_narratives` (max 2 sentences each in UI).
2. Sort featured talks by `views` from catalog; annotate `transcript` when id is in `transcripts_ingested`.
3. Add a compact “ingest status” line: `last_ingest_at`, count ingested, count catalog sample.
4. Do **not** change talk concept pages unless facts are wrong.
5. `npm run build` must pass.

Keep Station F dark editorial styling; no new decorative animations on the hub.
