#!/usr/bin/env python3
"""E5.1 grading — panel-corrected: dual-key D9, item-recall alongside strict, OC restricted
to the COMPOSE-valid trees (from the build-time witness in manifest.json) with
all_subs_correct reported, D6 flagged non-discriminating. Grades v1 A-runs (unchanged arm)
+ v2 B-runs (fixed legend/gloss)."""
import json, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from wiring import norm, eq, parse_answers
qs = json.load(open(os.path.join(HERE, "questions.json")))
manifest = json.load(open(os.path.join(HERE, "manifest.json")))
G = json.load(open(os.path.join(HERE, "graph.json")))
GOLD, DEPTH, OC = qs["gold"], qs["depth"], qs["oc"]
N = len(GOLD)
handlers = [x for x in G if x["kind"] == "handler"]

def as_set(a): return set(filter(None, (norm(x) for x in a.split(","))))
def recall(a, g):
    gs = as_set(g)
    if not gs or g == "none": return 1.0 if eq(a, g) else 0.0
    return len(as_set(a) & gs) / len(gs)

# dual-key D9: also accept the any-invoker reading
def d9_alt_gold(qtext):
    m = re.search(r'type (\w+) is removed', qtext)
    if not m: return None
    s = m.group(1)
    return ",".join(sorted(x["cls"] for x in handlers if any(t == s for t, m2 in x["edges"])))

seen, keep = {}, []
for i, q in enumerate(qs["questions"]):
    if q not in seen: seen[q] = i; keep.append(i)

runs = {}
for f in sorted(os.listdir(os.path.join(HERE, "responses"))):
    if f.startswith("A"): runs[f[:-4] + "_v1"] = parse_answers(os.path.join(HERE, "responses", f))
for f in sorted(os.listdir(os.path.join(HERE, "responses_v2"))):
    runs[f[:-4] + "_v2"] = parse_answers(os.path.join(HERE, "responses_v2", f))

subidx = []
for i, subs in enumerate(OC):
    for j, s in enumerate(subs): subidx.append((i, j))
VALID_TREES = [q - 1 for q in manifest["oc_compose_valid_q"]]  # build-time COMPOSE witness (was hard-coded D5/D6 per QA-3)

def correct(i, ans):
    if eq(ans, GOLD[i]): return True
    if DEPTH[i] == 9:
        alt = d9_alt_gold(qs["questions"][i])
        if alt is not None and eq(ans, alt): return True
    return False

out = {"grading": "panel-corrected (dual-key D9, OC valid-trees only, item-recall reported)",
       "runs": {}, "pooled_per_depth": {}, "oc": {}}
depth_acc = defaultdict(lambda: defaultdict(list))
for name, (Qa, Sa) in sorted(runs.items()):
    arm = name.split("_")[0]
    per, rec = defaultdict(lambda: [0, 0]), defaultdict(list)
    for i in keep:
        d = DEPTH[i]; per[d][1] += 1
        a = Qa.get(i + 1, "")
        if correct(i, a): per[d][0] += 1
        rec[d].append(max(recall(a, GOLD[i]),
                          recall(a, d9_alt_gold(qs["questions"][i]) or GOLD[i]) if d == 9 else 0))
    accs = {f"D{d}": round(c / t, 3) for d, (c, t) in sorted(per.items())}
    recs = {f"D{d}": round(sum(v) / len(v), 3) for d, v in sorted(rec.items())}
    overall = sum(c for c, t in per.values()) / sum(t for c, t in per.values())
    out["runs"][name] = {"overall_strict": round(overall, 3), "per_depth_strict": accs,
                         "per_depth_item_recall": recs}
    for d, (c, t) in per.items(): depth_acc[d][arm].append(c / t)
    ocs = []
    for i in VALID_TREES:
        snums = [k + 1 for k, (pi, sj) in enumerate(subidx) if pi == i]
        last, direct = Sa.get(snums[-1], ""), Qa.get(i + 1, "")
        ocs.append({"q": i + 1, "consistent": eq(last, direct) if last and direct else False,
                    "direct_correct": correct(i, direct),
                    "all_subs_correct": all(eq(Sa.get(sn, ""), OC[i][k]["gold"]) for k, sn in enumerate(snums))})
    out["oc"][name] = {"valid_trees": len(ocs),
                       "consistent": sum(o["consistent"] for o in ocs),
                       "consistent_and_correct": sum(o["consistent"] and o["direct_correct"] for o in ocs),
                       "all_subs_correct": sum(o["all_subs_correct"] for o in ocs),
                       "raw": ocs}
for d in sorted(depth_acc):
    row = {}
    for arm in ("A", "B"):
        v = depth_acc[d][arm]
        row[arm] = round(sum(v) / len(v), 3) if v else None
    row["B_minus_A_pts"] = round((row["B"] - row["A"]) * 100, 1)
    if d == 6: row["flag"] = "NON-DISCRIMINATING (uniform gold, name-derivable) per QA-2"
    out["pooled_per_depth"][f"D{d}"] = row
oa = [v["overall_strict"] for k, v in out["runs"].items() if k.startswith("A")]
ob = [v["overall_strict"] for k, v in out["runs"].items() if k.startswith("B")]
out["pooled_overall"] = {"A_v1": round(sum(oa) / len(oa), 3), "B_v2": round(sum(ob) / len(ob), 3),
                         "B_minus_A_pts": round((sum(ob) / len(ob) - sum(oa) / len(oa)) * 100, 1)}
out["panel_predictions"] = {
  "QA2#1 sentinel fix -> B D7 >= 0.75": out["pooled_per_depth"]["D7"]["B"],
  "QA2#2 glob gloss -> B_haiku D5 >= 0.83": out["runs"].get("B_haiku_v2", {}).get("per_depth_strict", {}).get("D5"),
  "QA1 corrected pooled ~ -2pts": out["pooled_overall"]["B_minus_A_pts"]}
json.dump(out, open(os.path.join(HERE, "E5.1-GRADES.json"), "w"), indent=1)
compact = {k: v for k, v in out.items() if k != "oc"}
compact["oc_summary"] = {k: {kk: vv for kk, vv in v.items() if kk != "raw"} for k, v in out["oc"].items()}
print(json.dumps(compact, indent=1))
