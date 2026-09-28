#!/usr/bin/env python3
"""E5 grading — per-depth accuracy per arm/model; OC consistency (composed sub-answer vs
direct answer) and OC↔correctness relation; duplicate-question dedup; ambiguity accounting."""
import json, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from wiring import eq, parse_answers
qs = json.load(open(os.path.join(HERE, "questions.json")))
GOLD, DEPTH, OC = qs["gold"], qs["depth"], qs["oc"]
N = len(GOLD)

# dedupe: identical question text keeps first occurrence
seen, keep = {}, []
for i, q in enumerate(qs["questions"]):
    if q not in seen: seen[q] = i; keep.append(i)
DUPS = N - len(keep)

# sub-question numbering: sequential over trees
subidx = []  # (parent_i, sub_j) for each S number
for i, subs in enumerate(OC):
    for j, s in enumerate(subs): subidx.append((i, j))

runs = {}
for f in sorted(os.listdir(os.path.join(HERE, "responses"))):
    runs[f[:-4]] = parse_answers(os.path.join(HERE, "responses", f))

out = {"n_questions": N, "n_unique": len(keep), "duplicates_removed": DUPS, "runs": {}, "oc": {}}
depth_acc = defaultdict(lambda: defaultdict(list))
for name, (Qa, Sa) in runs.items():
    arm = name.split("_")[0]
    per_depth = defaultdict(lambda: [0, 0])
    for i in keep:
        d = DEPTH[i]; per_depth[d][1] += 1
        if eq(Qa.get(i + 1, ""), GOLD[i]): per_depth[d][0] += 1
    accs = {f"D{d}": round(c / t, 3) for d, (c, t) in sorted(per_depth.items())}
    overall = sum(c for c, t in per_depth.values()) / sum(t for c, t in per_depth.values())
    out["runs"][name] = {"overall": round(overall, 3), "per_depth": accs}
    for d, (c, t) in per_depth.items(): depth_acc[d][arm].append(c / t)
    # OC analysis: last sub answer vs direct answer (consistency), + correctness
    ocs = []
    for i, subs in enumerate(OC):
        if not subs: continue
        snums = [k + 1 for k, (pi, sj) in enumerate(subidx) if pi == i]
        last = Sa.get(snums[-1], "")
        direct = Qa.get(i + 1, "")
        consistent = eq(last, direct) if (last and direct) else False
        correct = eq(direct, GOLD[i])
        subs_correct = all(eq(Sa.get(sn, ""), OC[i][k]["gold"]) for k, sn in enumerate(snums))
        ocs.append({"q": i + 1, "depth": DEPTH[i], "oc_consistent": consistent,
                    "direct_correct": correct, "all_subs_correct": subs_correct})
    cc = [o for o in ocs if o["oc_consistent"]]
    ic = [o for o in ocs if not o["oc_consistent"]]
    out["oc"][name] = {
        "trees": len(ocs),
        "consistent": len(cc),
        "P(correct|consistent)": round(sum(o["direct_correct"] for o in cc) / len(cc), 3) if cc else None,
        "P(correct|inconsistent)": round(sum(o["direct_correct"] for o in ic) / len(ic), 3) if ic else None,
        "inconsistent_qs": [o["q"] for o in ic]}
# pooled A vs B per depth
pool = {}
for d in sorted(depth_acc):
    row = {}
    for arm in ("A", "B"):
        v = depth_acc[d][arm]
        row[arm] = round(sum(v) / len(v), 3) if v else None
    row["B_minus_A_pts"] = round((row["B"] - row["A"]) * 100, 1) if row["A"] is not None else None
    pool[f"D{d}"] = row
out["pooled_per_depth"] = pool
oa = [v["overall"] for k, v in out["runs"].items() if k.startswith("A")]
ob = [v["overall"] for k, v in out["runs"].items() if k.startswith("B")]
out["pooled_overall"] = {"A": round(sum(oa) / len(oa), 3), "B": round(sum(ob) / len(ob), 3),
                         "B_minus_A_pts": round((sum(ob) / len(ob) - sum(oa) / len(oa)) * 100, 1)}
json.dump(out, open(os.path.join(HERE, "E5-GRADES.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
