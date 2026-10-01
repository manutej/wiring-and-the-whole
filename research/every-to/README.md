# Every (@EveryInc) — transcript corpus

Raw ingest of [Every](https://www.youtube.com/@EveryInc) YouTube uploads (Dan Shipper, CEO of [every.to](https://every.to)). **No dashboard in this branch** — only catalog + raw transcripts for downstream editorial agents.

## Layout

| Path | Purpose |
|------|---------|
| `catalog.json` | Latest page of channel uploads (TubeAlfred snapshot) |
| `ingest.json` | Which IDs have raw transcripts, pending, unavailable |
| `transcripts/raw/{videoId}.json` | Full segment list + metadata from TubeAlfred |
| `transcripts/raw/{videoId}.txt` | Same content, `[MM:SS] line` format |
| `transcripts/unavailable/` | Videos checked but no captions yet |
| `scripts/save-transcripts.py` | Normalize TubeAlfred JSON dumps into `raw/` |

## Re-ingest

```bash
# After TubeAlfred youtube_video_transcript (save API JSON to /tmp/vid.json):
python3 scripts/save-transcripts.py /tmp/vid.json
```

Update `ingest.json` manually or re-run the catalog script in commit history.

## Credits / gaps (2026-10-01)

- **5** talks saved with full segment JSON (`WW_0xPcFbzw`, `vey_dBnDTAU`, `yZddAiz4HP8`, `tqF8Ffv7tDs`, `x9BNBcP_C7Q`).
- **`1EEw36H2zLo`** (Astra vibe check): fetched successfully via TubeAlfred but not persisted before credits hit zero — **re-fetch** and run `save-transcripts.py`.
- **`jZh55CQwSh8`** (Sam Altman / Dots): **no captions** in YouTube metadata at check time.
