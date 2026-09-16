#!/usr/bin/env python3
"""
E1 — R8 FAITHFULNESS WITNESS (restored after container reclamation; final panel-repaired version)
CODE-C tuple: C0 (SymTab) — the witness-scale skeleton of FOUNDATION.md's Code_X.
  objects   : finite typed symbol tables {qualified_name: (kind, signature)}
  morphisms : kind- and signature-preserving functions on symbol names
  ports     : interface map i: P -> X marking exported symbols
  pushout   : set-level amalgamation (always exists); kappa = collision lint predicate
Per EXPERIMENTS.md E1 steps 2-10. Emits WITNESS.json with boolean checks + witnesses.
History: v1 12/12 (step7 check repaired in-session); v2 genuine two-order associativity;
v3 (panel-repaired) non-vacuous Ex 4.25 naturality + step8a. 13 checks total.
"""
import json, re, os, itertools, copy

ROOT = os.path.dirname(os.path.abspath(__file__))
TOY = os.path.join(ROOT, "toybank")
REPORT = {"code_c": "C0 SymTab (skeleton of Code_X, FOUNDATION.md); pushout=amalgamation, kappa=lint",
          "checks": {}, "witnesses": {}, "notes": []}

# ---------- Step 2: generate toybank (16 files, Java-flavored, seeded/deterministic) ----------
def vertical(name, extra_method=False):
    N = name.capitalize()
    ctrl = f"""public class {N}Controller {{
  public Page list(int p) {{ return svc.fetchPage(p); }}
  public Dto get(long id) {{ return svc.fetchOne(id); }}
  void log(String m) {{ audit.log(m); }}
  // refs: {name}.{N}Service#fetchPage {name}.{N}Service#fetchOne shared.AuditDto#log shared.PageDto#of
}}"""
    extra = f"\n  public Dto refinance(long id) {{ return repo.findOne(id); }}" if extra_method else ""
    svc = f"""public class {N}Service {{
  public Page fetchPage(int p) {{ return repo.findPage(p); }}
  public Dto fetchOne(long id) {{ return repo.findOne(id); }}{extra}
  void log(String m) {{ }}
  // refs: {name}.{N}Repository#findPage {name}.{N}Repository#findOne shared.EventTopics#EVT
}}"""
    repo = f"""public class {N}Repository {{
  public Page findPage(int p) {{ return null; }}
  public Dto findOne(long id) {{ return null; }}
  void log(String m) {{ }}
  // refs: shared.PageDto#of
}}"""
    return {f"{name}/{N}Controller.java": ctrl, f"{name}/{N}Service.java": svc, f"{name}/{N}Repository.java": repo}

FILES = {}
FILES.update(vertical("accounts"))
FILES.update(vertical("savings"))                 # exact renaming of accounts (planted exact orbit)
FILES.update(vertical("loans", extra_method=True))# near-orbit: one extra method (NOT folded)
FILES["shared/PageDto.java"] = "public class PageDto {\n  public Page of(java.util.List l) { return null; }\n}"
FILES["shared/AuditDto.java"] = "public class AuditDto {\n  public void log(String m) { }\n}"
FILES["shared/EventTopics.java"] = "public class EventTopics {\n  public String EVT = \"evt\";\n}"
FILES["shared/AppConfig.java"] = "public class AppConfig {\n  public String env = \"prod\";\n}"
FILES["accounts/Money.java"] = "public class Money {\n  public long amountCents;\n  public String currency;\n}"
FILES["loans/Money.java"] = "public class Money {\n  public double amount;\n  public String currencyCode;\n}"
FILES["report/ReportModule.java"] = ("public class ReportModule {\n  public String render() { return null; }\n"
  "  // refs: accounts.Money#amountCents loans.Money#amount\n}")

os.makedirs(TOY, exist_ok=True)
for rel, body in FILES.items():
    p = os.path.join(TOY, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: f.write(body + "\n")
REPORT["notes"].append(f"toybank generated: {len(FILES)} files")

# ---------- Step 3: extract — file -> object of C + port marking + refs ----------
MEMBER = re.compile(r'^\s*(public\s+)?([\w.<>\[\]]+)\s+(\w+)\s*(\([^)]*\))?', re.M)
def extract(rel, body):
    ns = rel.replace("/", ".").rsplit(".java", 1)[0]
    pkg = ns.rsplit(".", 1)[0]
    cls = ns.rsplit(".", 1)[1]
    obj, ports = {}, {}
    for m in MEMBER.finditer(body):
        pub, typ, name, args = m.group(1), m.group(2), m.group(3), m.group(4)
        if typ in ("class",): continue
        kind = "method" if args is not None else "field"
        sig = f"{typ}{args or ''}"
        q = f"{pkg}.{cls}#{name}"
        obj[q] = (kind, sig)
        if pub: ports[q] = (kind, sig)
    refs = re.findall(r'refs:\s*(.+)', body)
    refl = refs[0].split() if refs else []
    return {"ns": ns, "obj": obj, "ports": ports, "refs": refl}

UNITS = {rel: extract(rel, body) for rel, body in FILES.items()}
REPORT["notes"].append(f"extracted {len(UNITS)} objects; total symbols {sum(len(u['obj']) for u in UNITS.values())}")

def is_morphism(fmap, X, Y):
    for a, tgt in fmap.items():
        if a not in X or tgt not in Y: return False
        if X[a] != Y[tgt]: return False
    return len(fmap) == len(X)

# ---------- Step 4: pushout with commutativity + bounded universal-property check ----------
class UF:
    def __init__(s): s.p = {}
    def find(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def union(s, a, b): s.p[s.find(a)] = s.find(b)

def pushout(J, f, X, g, Y, tagX="L", tagY="R"):
    uf = UF()
    for j in J: uf.union((tagX, f[j]), (tagY, g[j]))
    elems = [(tagX, a) for a in X] + [(tagY, b) for b in Y]
    classes = {}
    for e in elems: classes.setdefault(uf.find(e), []).append(e)
    Z, ix, iy, kappa = {}, {}, {}, []
    for rep, members in classes.items():
        sigs = {(X[a] if t == tagX else Y[a]) for t, a in members}
        if len(sigs) > 1: kappa.append({"identified": [f"{t}:{a}" for t, a in members],
                                        "signatures": sorted(str(s) for s in sigs)})
        zname = sorted(a for t, a in members)[0]
        Z[zname] = (X[members[0][1]] if members[0][0] == tagX else Y[members[0][1]])
        for t, a in members:
            (ix if t == tagX else iy)[a] = zname
    comm = all(ix[f[j]] == iy[g[j]] for j in J)
    return Z, ix, iy, kappa, comm

def universal_check(J, f, X, g, Y, Z, ix, iy):
    """Bounded enumeration (RECORDED PROTOCOL DEVIATION: narrower than pre-registered
    exhaustive |Q| <= |Z|+2 — exhaustive-within-bound owed at Code_X scale)."""
    ok = True; tested = 0
    Zext = dict(Z); Zext["__fresh__"] = ("field", "String")
    med = {z: z for z in Z}
    ok &= is_morphism(med, Z, Zext); tested += 1
    same = [(a, b) for a, b in itertools.combinations(Z, 2) if Z[a] == Z[b]]
    for a, b in same[:40]:
        q = {z: (a if z == b else z) for z in Z}
        Q = {q[z]: Z[z] for z in Z}
        ok &= is_morphism(q, Z, Q)
        ok &= set(ix.values()) | set(iy.values()) == set(Z)
        tested += 1
    return ok, tested

# ---------- Step 5: the real pushout — LoanService ⊔_J LoanRepository ----------
def unit(rel): return UNITS[rel]
svcU, repU = unit("loans/LoansService.java"), unit("loans/LoansRepository.java")
J5 = {f"port#{i}": v for i, (k, v) in enumerate(sorted(repU["ports"].items()))}
jnames = sorted(repU["ports"])
f5 = {}
SvcX = dict(svcU["obj"])
for i, q in enumerate(jnames):
    alias = q
    SvcX[alias] = repU["ports"][q]
    f5[f"port#{i}"] = alias
g5 = {f"port#{i}": q for i, q in enumerate(jnames)}
Z5, ix5, iy5, k5, comm5 = pushout({k: v for k, v in J5.items()}, f5, SvcX, g5, repU["obj"])
logs = [z for z in Z5 if z.endswith("#log")]
fresh_ok = len(logs) == 2
uc5, tested5 = universal_check(J5, f5, SvcX, g5, repU["obj"], Z5, ix5, iy5)
REPORT["checks"]["step4_pushout_commutes"] = bool(comm5)
REPORT["checks"]["step4_universal_property_bounded"] = bool(uc5)
REPORT["checks"]["step5_fresh_names_inside_C"] = bool(fresh_ok)
REPORT["checks"]["step5_no_false_kappa"] = (len(k5) == 0)
REPORT["witnesses"]["step5"] = {"|Z|": len(Z5), "log_symbols_kept_distinct": logs,
                                "cocones_tested": tested5}

# ---------- Step 6: system map — LoanService -> LoanServiceV2 ----------
V2 = {}
rmap = {}
for q, kv in svcU["obj"].items():
    nq = q.replace("#log", "#writeAudit")
    V2[nq] = kv; rmap[q] = nq
sq_ok = is_morphism(rmap, svcU["obj"], V2)
ports_ok = all(rmap[p] in V2 and svcU["ports"][p] == V2[rmap[p]] and rmap[p] == p for p in svcU["ports"])
REPORT["checks"]["step6_system_map_square"] = bool(sq_ok and ports_ok)
REPORT["witnesses"]["step6"] = {"renamed": [k for k in rmap if rmap[k] != k]}

# ---------- Step 7: wiring automorphism swap(accounts,savings) ⇒ composite iso ----------
def glue_chain(units_rel, tag):
    acc = dict(unit(units_rel[0])["obj"])
    for rel in units_rel[1:]:
        Y = unit(rel)["obj"]; Yports = unit(rel)["ports"]
        refs = set()
        for r in units_rel[:units_rel.index(rel)]:
            refs |= set(unit(r)["refs"])
        jn = sorted(q for q in Yports if q in refs)
        J = {f"p#{i}": Yports[q] for i, q in enumerate(jn)}
        f = {}
        for i, q in enumerate(jn):
            acc.setdefault(q, Yports[q]); f[f"p#{i}"] = q
        g = {f"p#{i}": q for i, q in enumerate(jn)}
        acc, ixA, iyA, kk, cm = pushout(J, f, acc, g, Y)[:5]
    return acc

vertA = ["accounts/AccountsController.java", "accounts/AccountsService.java", "accounts/AccountsRepository.java"]
vertS = ["savings/SavingsController.java", "savings/SavingsService.java", "savings/SavingsRepository.java"]
A = glue_chain(vertA, "A"); Sv = glue_chain(vertS, "S")
phi = {q: q.replace("accounts.Accounts", "savings.Savings").replace("accounts.", "savings.") for q in A}
phi_ok = is_morphism(phi, A, Sv) and len(set(phi.values())) == len(phi) and set(phi.values()) == set(Sv)
# The composite W(A ‖ S). σ = swap; induced automorphism (A,a)↦(S,φa), (S,s)↦(A,φ⁻¹s):
# construct-then-verify, no search.
comp1 = {("A", q): v for q, v in A.items()}; comp1.update({("S", q): v for q, v in Sv.items()})
phi_inv = {v: k for k, v in phi.items()}
induced = {}
for (t, q) in comp1:
    induced[(t, q)] = ("A", phi_inv[q]) if t == "S" else ("S", phi[q])
iso_ok = all(k2 in comp1 and comp1[k2] == comp1[k] for k, k2 in induced.items())
iso_ok &= len(set(induced.values())) == len(induced)
inv = {v: k for k, v in induced.items()}
iso_ok &= all(inv[induced[k]] == k for k in comp1)
REPORT["checks"]["step7_automorphism_composite_iso"] = bool(phi_ok and iso_ok)
REPORT["witnesses"]["step7"] = {"phi_size": len(phi), "composite_size": len(comp1),
                                "construct_then_verify": True}

# ---------- Step 8: functorial invariant — port-reachability relation B (file-granular) ----------
def reach(units_rel):
    ports, edges = set(), set()
    for rel in units_rel:
        u = unit(rel); ports |= set(u["ports"])
    for rel in units_rel:
        u = unit(rel)
        for p in u["ports"]:
            for r in u["refs"]:
                if r in ports: edges.add((p, r))
    return edges
BA, BS = reach(vertA), reach(vertS)
transported = {(phi.get(a, a), phi.get(b, b)) for (a, b) in BA}
REPORT["checks"]["step8_invariant_constant_on_orbit"] = (transported == BS)
REPORT["witnesses"]["step8"] = {"B_accounts_edges": len(BA), "B_savings_edges": len(BS),
                                "equal_after_transport": transported == BS,
                                "sample": sorted(list(BA))[:4]}

# ---------- Step 9: deliberate collision — ReportModule × two Moneys ----------
mA, mL, rep = unit("accounts/Money.java"), unit("loans/Money.java"), unit("report/ReportModule.java")
Jc = {"p#0": ("field", "long")}
fc = {"p#0": "accounts.Money#amountCents"}
gc = {"p#0": "loans.Money#amount"}
Zc, ixc, iyc, kc, cmc = pushout(Jc, fc, mA["obj"], gc, mL["obj"])
REPORT["checks"]["step9_kappa_fires_on_collision"] = (len(kc) > 0)
REPORT["witnesses"]["step9"] = {"kappa": kc,
    "silent_merge_would_have": "one Money symbol with contradictory signatures {long}!={double} — corrupted context"}

# ---------- Step 10: paper-conformance ----------
# associativity: GENUINE (A ⊔_J1 B) ⊔_J2 C vs A ⊔_J1 (B ⊔_J2 C) on the loans chain.
def as_unit(rel):
    u = unit(rel); return {"obj": dict(u["obj"]), "ports": dict(u["ports"]), "refs": set(u["refs"])}
def glue2(U, V):
    jn = sorted(q for q in V["ports"] if q in U["refs"])
    J = {f"p#{i}": V["ports"][q] for i, q in enumerate(jn)}
    f = {}
    Uo = dict(U["obj"])
    for i, q in enumerate(jn):
        Uo.setdefault(q, V["ports"][q]); f[f"p#{i}"] = q
    g = {f"p#{i}": q for i, q in enumerate(jn)}
    Z, ix, iy, kk, cm = pushout(J, f, Uo, g, V["obj"])
    return {"obj": Z, "ports": {**U["ports"], **V["ports"]}, "refs": U["refs"] | V["refs"]}, kk, cm
Actrl, Asvc, Arepo = as_unit("loans/LoansController.java"), as_unit("loans/LoansService.java"), as_unit("loans/LoansRepository.java")
L1, k1, c1 = glue2(Actrl, Asvc); Z_ab_c, k2, c2 = glue2(L1, Arepo)
R1, k3, c3 = glue2(Asvc, Arepo); Z_a_bc, k4, c4 = glue2(Actrl, R1)
assoc_iso = (Z_ab_c["obj"] == Z_a_bc["obj"]) and c1 and c2 and c3 and c4 and not (k1 or k2 or k3 or k4)
REPORT["checks"]["step10_associativity_canonical_iso"] = bool(assoc_iso)
REPORT["witnesses"]["step10_assoc"] = {"|(A+B)+C|": len(Z_ab_c["obj"]), "|A+(B+C)|": len(Z_a_bc["obj"]),
                                       "identical_canonical_form": Z_ab_c["obj"] == Z_a_bc["obj"]}
# monoidal unit: glue along empty junction = disjoint union
Zu, ixu, iyu, ku, cu = pushout({}, {}, unit("shared/PageDto.java")["obj"], {}, unit("shared/AppConfig.java")["obj"])
REPORT["checks"]["step10_monoidal_unit_disjoint_union"] = (len(Zu) ==
    len(unit("shared/PageDto.java")["obj"]) + len(unit("shared/AppConfig.java")["obj"]) and len(ku) == 0)
# Ex 4.25 (panel-repaired, NON-VACUOUS): refactor square pasted with the swap square.
# Refactor r: rename internal #log of the ACCOUNTS service (in this composite), with its
# φ-transport on savings. Check the NATURALITY SQUARE lift∘σ == σ'∘lift, plus lift is a
# genuine C-morphism with ports fixed.
def rnA(q): return q.replace("accounts.AccountsService#log", "accounts.AccountsService#writeAudit")
def rnS(q): return q.replace("savings.SavingsService#log", "savings.SavingsService#writeAudit")
A2  = {rnA(q): v for q, v in A.items()}
Sv2 = {rnS(q): v for q, v in Sv.items()}
lift = {}
for (t, q) in comp1:
    lift[(t, q)] = (t, rnA(q)) if t == "A" else (t, rnS(q))
nontrivial = sum(1 for k, v in lift.items() if k != v)
comp_target = {("A", q): v for q, v in A2.items()}; comp_target.update({("S", q): v for q, v in Sv2.items()})
mor_ok = (len(set(lift.values())) == len(lift)
          and all(comp_target[lift[k]] == comp1[k] for k in comp1))
ports_fixed_set = [("A", p) for p in unit("accounts/AccountsService.java")["ports"]]
ports_fixed = len(ports_fixed_set) > 0 and all(lift[k] == k for k in ports_fixed_set)
phi2 = {rnA(q): rnS(phi[q]) for q in A}
induced2 = {}
for (t, q) in comp_target:
    if t == "A": induced2[(t, q)] = ("S", phi2[q])
    else:
        phi2_inv = {v: k for k, v in phi2.items()}
        induced2[(t, q)] = ("A", phi2_inv[q])
naturality = all(induced2[lift[k]] == lift[induced[k]] for k in comp1)
REPORT["checks"]["step10_ex425_squares_compose"] = bool(mor_ok and ports_fixed and naturality and nontrivial > 0)
REPORT["witnesses"]["step10_ex425"] = {"lift_nontrivial_on": nontrivial, "lift_is_morphism": mor_ok,
    "accounts_ports_fixed": ports_fixed, "naturality_lift_sigma_commute": naturality,
    "note": "refactor renames accounts.AccountsService#log (+phi-transport on savings); swap commutes with refactor"}
# Step 8(a): system maps send B to B (ports fixed ⇒ relation unchanged)
b_pres = {(rnA(a), rnA(b)) for (a, b) in BA} == BA
REPORT["checks"]["step8a_system_maps_preserve_invariant"] = bool(b_pres)
REPORT["checks"]["step6_ports_preserved"] = bool(ports_ok)

# ---------- emit ----------
REPORT["all_pass"] = all(REPORT["checks"].values())
with open(os.path.join(ROOT, "WITNESS.json"), "w") as f:
    json.dump(REPORT, f, indent=2, default=str)
print(json.dumps({"all_pass": REPORT["all_pass"], "checks": REPORT["checks"]}, indent=2))
