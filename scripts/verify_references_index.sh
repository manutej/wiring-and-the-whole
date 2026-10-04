#!/usr/bin/env bash
# Validate Paris references index vs digest ingested IDs and plugin skill mapping.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$ROOT/research/ai-engineer-paris-2026/references/index.yaml"
MANIFEST="$ROOT/skills/paris-level-up/plugin-manifest.json"
DIGEST="$ROOT/research/ai-engineer-paris-2026/digest.json"

fail() { echo "verify-references-index: $*" >&2; exit 1; }

[[ -f "$INDEX" ]] || fail "missing $INDEX"
[[ -f "$MANIFEST" ]] || fail "missing $MANIFEST"
[[ -f "$DIGEST" ]] || fail "missing $DIGEST"

export INDEX MANIFEST DIGEST ROOT
python3 << 'PY'
import json, pathlib, sys

root = pathlib.Path(__import__("os").environ["ROOT"])
index_path = pathlib.Path(__import__("os").environ["INDEX"])
manifest_path = pathlib.Path(__import__("os").environ["MANIFEST"])
digest_path = pathlib.Path(__import__("os").environ["DIGEST"])

try:
    import yaml
except ImportError:
    sys.exit("verify-references-index: FAIL PyYAML required (pip install pyyaml)")

index = yaml.safe_load(index_path.read_text())
digest = json.loads(digest_path.read_text())
manifest = json.loads(manifest_path.read_text())

ingested = set(digest.get("transcripts_ingested") or [])
talks = index.get("talks") or {}

segment_ids: set[str] = set()
segment_video: dict[str, str | None] = {}

for vid, body in talks.items():
    if vid not in ingested:
        sys.exit(f"verify-references-index: FAIL talks key {vid} not in transcripts_ingested")
    for seg in (body or {}).get("segments") or []:
        sid = seg.get("id")
        if not sid:
            sys.exit(f"verify-references-index: FAIL segment missing id under {vid}")
        segment_ids.add(sid)
        segment_video[sid] = vid

for seg in index.get("programme_segments") or []:
    sid = seg.get("id")
    if sid:
        segment_ids.add(sid)
        segment_video[sid] = None

skills_map = index.get("skills") or {}
manifest_ids = {s["id"] for s in manifest.get("skills", []) if isinstance(s, dict)}
index_skill_ids = set(skills_map.keys())
if manifest_ids != index_skill_ids:
    missing = manifest_ids - index_skill_ids
    extra = index_skill_ids - manifest_ids
    sys.exit(
        f"verify-references-index: FAIL manifest skills != index skills "
        f"missing_in_index={sorted(missing)} extra_in_index={sorted(extra)}"
    )

def skill_segment_list(cfg):
    if isinstance(cfg, list):
        return cfg
    if isinstance(cfg, dict):
        return cfg.get("segments") or []
    return []

for skill_id, cfg in skills_map.items():
    segs = skill_segment_list(cfg)
    if not segs:
        sys.exit(f"verify-references-index: FAIL skill {skill_id} has no segments")
    for sid in segs:
        if sid not in segment_ids:
            sys.exit(f"verify-references-index: FAIL skill {skill_id} unknown segment {sid}")

covered_vids = {v for v in segment_video.values() if v is not None}
if set(talks.keys()) != ingested:
    sys.exit(
        "verify-references-index: FAIL index talks keys != transcripts_ingested: "
        f"missing={sorted(ingested - set(talks.keys()))} extra={sorted(set(talks.keys()) - ingested)}"
    )
if not ingested <= covered_vids:
    sys.exit(
        "verify-references-index: FAIL ingested video not in talks index: "
        + ", ".join(sorted(ingested - covered_vids))
    )

for vid, body in talks.items():
    if len((body or {}).get("segments") or []) < 3:
        sys.exit(f"verify-references-index: FAIL {vid} has fewer than 3 L4 segments")

skills_dir = root / "skills"
for skill_id in manifest_ids:
    skill_md = skills_dir / skill_id / "SKILL.md"
    if not skill_md.is_file():
        sys.exit(f"verify-references-index: FAIL missing {skill_md}")
    text = skill_md.read_text()
    for sid in skill_segment_list(skills_map[skill_id]):
        if sid not in text:
            sys.exit(
                f"verify-references-index: FAIL {skill_id}/SKILL.md missing segment id {sid}"
            )

print("verify-references-index: OK")
PY
