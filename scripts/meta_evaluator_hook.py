#!/usr/bin/env python3
"""Post-loop meta-evaluator bundle: programme pointers + external craft skill index.

Implements docs/pulse/META-EVALUATOR.md. Does not read or emit RUBRIC-EVALUATOR.md
body text — only lists forbidden paths for implementer firewall enforcement.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CRAFT_ROOT = ROOT / "craft"
CRAFT_UPSTREAM = "https://github.com/manutej/craft"
CRAFT_RAW = "https://raw.githubusercontent.com/manutej/craft/main"

FORBIDDEN_IMPLEMENTER_PATHS = [
    "docs/pulse/RUBRIC-EVALUATOR.md",
    "docs/pulse/evaluations/",
]

PROGRAMME_POINTERS = [
    {"path": "docs/CONTEXT-COMPACT.md", "role": "cold-start architecture snapshot"},
    {"path": "docs/PULSE.md", "role": "pulse operator protocol"},
    {"path": "docs/pulse/LOOP-ENGINEERING.md", "role": "implementer vs evaluator lanes"},
    {"path": "docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md", "role": "implementer scope template"},
    {"path": "HANDOFF.md", "role": "claims discipline and history"},
    {"path": "docs/SCALE-PATH.md", "role": "measurement ladder"},
]

IN_REPO_SKILLS = [
    "skills/interface-first-context/SKILL.md",
    "skills/systems-intake/SKILL.md",
    "skills/symmetry-lens/SKILL.md",
]


def _parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []
    for line in block.splitlines():
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m:
            if key is not None:
                out[key] = "\n".join(buf).strip()
            key = m.group(1)
            rest = m.group(2)
            if rest in (">", ">-", "|"):
                buf = []
            elif rest:
                buf = [rest.strip()]
            else:
                buf = []
        elif key is not None:
            buf.append(line)
    if key is not None:
        out[key] = "\n".join(buf).strip()
    return out


def _craft_skills(craft_root: Path) -> list[dict[str, str]]:
    skills_dir = craft_root / "skills"
    if not skills_dir.is_dir():
        return []
    rows: list[dict[str, str]] = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        meta = _parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = meta.get("name") or skill_md.parent.name
        rel = skill_md.relative_to(craft_root).as_posix()
        rows.append(
            {
                "name": name,
                "description": meta.get("description", "").replace("\n", " ").strip(),
                "local_path": str(craft_root / rel),
                "upstream_path": rel,
                "raw_url": f"{CRAFT_RAW}/{rel}",
            }
        )
    return rows


def build_bundle(craft_root: Path) -> dict:
    craft_skills = _craft_skills(craft_root)
    return {
        "harness": "meta-evaluator-hook-v0",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "firewall": {
            "lane": "post-loop-meta",
            "implementer_must_not_read": FORBIDDEN_IMPLEMENTER_PATHS,
            "note": (
                "This bundle is for operators and the next pulse planner after "
                "evaluator SHIP|NO-SHIP — not for implementers mid-pulse."
            ),
        },
        "programme_pointers": [
            {**p, "exists": (ROOT / p["path"]).is_file()} for p in PROGRAMME_POINTERS
        ],
        "in_repo_skills": [
            {"path": p, "exists": (ROOT / p).is_file()} for p in IN_REPO_SKILLS
        ],
        "craft": {
            "upstream": CRAFT_UPSTREAM,
            "resolved_root": str(craft_root) if craft_root.is_dir() else None,
            "router_skill": "production-grade",
            "skills": craft_skills,
            "rules_constitution": f"{CRAFT_RAW}/RULES.md",
        },
        "post_loop_guidance": [
            "Prefer programme cold-start (CONTEXT-COMPACT) before browsing the tree.",
            "Route broad code-quality asks through craft production-grade; use a single member skill when scope is narrow.",
            "Keep pulse artifacts separated: adversarial gaps, evaluator scorecard, executive report.",
            "Do not paste rubric dimension scores into implementer-facing docs or AGENTS.md.",
        ],
    }


def assert_bundle_sane(doc: dict) -> None:
    blob = json.dumps(doc)
    if "dimension scores" in blob.lower() and "do not paste" not in blob.lower():
        raise ValueError("bundle may contain rubric leakage")
    if "D1" in blob and "RUBRIC" in blob:
        raise ValueError("bundle may contain rubric dimension labels")
    forbidden = doc.get("firewall", {}).get("implementer_must_not_read", [])
    if "docs/pulse/RUBRIC-EVALUATOR.md" not in forbidden:
        raise ValueError("missing rubric path in firewall list")
    skills = doc.get("craft", {}).get("skills", [])
    if len(skills) < 9:
        raise ValueError(f"expected >=9 craft skills, got {len(skills)}")
    rubric_path = ROOT / "docs/pulse/RUBRIC-EVALUATOR.md"
    if rubric_path.is_file() and rubric_path.read_text(encoding="utf-8")[:200] in blob:
        raise ValueError("bundle must not embed RUBRIC-EVALUATOR.md content")


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit post-loop meta-evaluator JSON bundle.")
    parser.add_argument(
        "--craft-root",
        type=Path,
        default=Path(
            __import__("os").environ.get("CRAFT_SKILLS_ROOT", str(DEFAULT_CRAFT_ROOT))
        ),
        help="Path to manutej/craft checkout (default: ../craft or CRAFT_SKILLS_ROOT)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate bundle sanity (for make pulse-eval)",
    )
    args = parser.parse_args()
    doc = build_bundle(args.craft_root.expanduser().resolve())
    assert_bundle_sane(doc)
    if args.check:
        print("OK: meta-evaluator hook bundle")
        return 0
    json.dump(doc, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
