#!/usr/bin/env python3
"""E3 grading — deterministic, against frozen gold. Strict = exact normalized match.
Lenient (labeled sensitivity only) = for single-target questions, gold ∈ comma-set answer.
Arm-C audit: any question arm C answers correctly (majority over its 4 runs) is flagged
'answerable-without-wiring' and EXCLUDED from the wiring-comprehension pool."""
import json, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from wiring import norm, eq, parse_answers
qs = json.load(open(os.path.join(HERE, "questions.json")))
GOLD, QTYPE = qs["gold"], qs["qtype"]
N = len(GOLD)

runs = {}
for f in sorted(os.listdir(os.path.join(HERE, "responses"))):
    arm, pos, model = f[:-4].split("_")
    runs[(arm, pos, model)] = parse_answers(os.path.join(HERE, "responses", f))[0]

def grade(ans, i, lenient=False):
    g, a = GOLD[i], ans.get(i + 1, "")
    if eq(a, g): return True
    if lenient and "," in a and "," not in g:
        return norm(g) in [norm(x) for x in a.split(",")]
    return False

# arm-C audit: majority-correct over C runs => answerable without wiring
c_correct = defaultdict(int); c_total = defaultdict(int)
for (arm, pos, model), ans in runs.items():
    if arm != "C": continue
    for i in range(N):
        c_total[i] += 1
        if grade(ans, i): c_correct[i] += 1
flagged = sorted(i for i in range(N) if c_correct[i] * 2 > c_total[i])
wiring_pool = [i for i in range(N) if i not in flagged]

def score(ans, pool, lenient=False):
    return sum(grade(ans, i, lenient) for i in pool)

results = {"n_questions": N, "flagged_answerable_without_wiring_q": [i + 1 for i in flagged],
           "flagged_qtypes": sorted({QTYPE[i] for i in flagged}),
           "wiring_pool_size": len(wiring_pool), "runs": {}}
pooled = defaultdict(list)
for key, ans in sorted(runs.items()):
    arm, pos, model = key
    s_all = score(ans, range(N)); s_w = score(ans, wiring_pool); s_wl = score(ans, wiring_pool, True)
    results["runs"]["_".join(key)] = {
        "acc_all_25": round(s_all / N, 3),
        "acc_wiring_pool_strict": round(s_w / len(wiring_pool), 3),
        "acc_wiring_pool_lenient": round(s_wl / len(wiring_pool), 3)}
    pooled[arm].append(s_w / len(wiring_pool))
    pooled[arm + "_lenient"].append(s_wl / len(wiring_pool))
for arm in ["A", "B", "C"]:
    results[f"pooled_{arm}_wiring_strict"] = round(sum(pooled[arm]) / len(pooled[arm]), 3)
    results[f"pooled_{arm}_wiring_lenient"] = round(sum(pooled[arm + "_lenient"]) / len(pooled[arm + "_lenient"]), 3)
dAB = results["pooled_A_wiring_strict"] - results["pooled_B_wiring_strict"]
results["A_minus_B_pts_strict"] = round(dAB * 100, 1)
results["decision_rule"] = "L2 FAILS as serialized iff B <= A - 5pts pooled on wiring pool"
results["verdict"] = ("B-PASSES (parity or better)" if dAB * 100 <= 5 else "B-FAILS (comprehension tax > 5pts)")
# per-question breakdown for the report
perq = []
for i in range(N):
    row = {"q": i + 1, "type": QTYPE[i], "gold": GOLD[i], "flagged": i in flagged}
    for arm in ["A", "B", "C"]:
        arm_runs = [ans for (a, p, m), ans in runs.items() if a == arm]
        row[arm] = sum(grade(ans, i) for ans in arm_runs)
    perq.append(row)
results["per_question_correct_of_4runs"] = perq
json.dump(results, open(os.path.join(HERE, "E3-GRADES.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in results.items() if k != "per_question_correct_of_4runs"}, indent=1))
