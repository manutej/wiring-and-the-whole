#!/usr/bin/env python3
"""Normalize TubeAlfred transcript JSON into research/every-to/transcripts/raw/."""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "transcripts" / "raw"


def save_payload(vid: str, payload: dict) -> None:
    data = payload.get("data", payload)
    tr = data.get("transcript") or []
    meta = {
        "video_id": data.get("video_id", vid),
        "url": data.get("url") or f"https://www.youtube.com/watch?v={vid}",
        "language": data.get("language"),
        "language_code": data.get("language_code"),
        "is_auto_generated": data.get("is_auto_generated"),
        "availability": data.get("availability"),
        "fetched_via": "TubeAlfred youtube_video_transcript",
    }
    out_json = RAW / f"{vid}.json"
    out_txt = RAW / f"{vid}.txt"
    out_json.write_text(
        json.dumps({"meta": meta, "transcript": tr, "transcript_only_text": data.get("transcript_only_text", "")}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    lines = []
    for seg in tr:
        ts = seg.get("start_time_text", "")
        text = (seg.get("text") or "").strip()
        if text:
            lines.append(f"[{ts}] {text}")
    out_txt.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print("saved", vid, len(tr), "segments")


def main() -> None:
    for path in sys.argv[1:]:
        p = pathlib.Path(path)
        payload = json.loads(p.read_text())
        vid = payload.get("data", {}).get("video_id") or payload.get("video_id")
        if not vid:
            print("skip", path, "no video_id")
            continue
        save_payload(vid, payload)


if __name__ == "__main__":
    main()
