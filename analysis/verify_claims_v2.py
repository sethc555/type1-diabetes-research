#!/usr/bin/env python3
"""Machine-checkable verification of the v2 (post-critique) headline claims.
Run:  python3 verify_claims_v2.py   (-> exit 0 if all pass). Under the 4 GB cap per project policy.
"""
import sys
import numpy as np
import t1d_model_v2 as M

checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

base = M.time_to_dx(M.simulate(M.arms()["untreated"]))
fr = {n: M.cure_fraction(s) for n, s in M.arms().items()}

# (1) critique point #2 fixed: tolerance monotherapy is PARTIAL, not 100% (and not 0%)
check("tolerance monotherapy is partial (20-80%), not 100%", 0.20 <= fr["tolerance only"] <= 0.80,
      f"{fr['tolerance only']*100:.0f}%")

# (2) critique point #3 fixed: anti-CD3 monotherapy DELAYS (>~1 yr) but does NOT cure
a3_delay = M.time_to_dx(M.simulate(M.arms()["anti-CD3 only"])) - base
check("anti-CD3 monotherapy delays >=1 yr (matches TN10)", a3_delay >= 1.0, f"+{a3_delay:.2f} yr")
check("anti-CD3 monotherapy does NOT cure (low cohort cure)", fr["anti-CD3 only"] <= 0.15,
      f"{fr['anti-CD3 only']*100:.0f}%")

# (3) critique point #1 fixed: thymic Treg source gives R a nonzero floor at baseline
R0 = M.stage2_ic()[2]
check("thymic Treg source -> nonzero baseline Treg floor", R0 > 0.05, f"R0={R0:.3f}")

# (4) THE robust v2 result: combination beats the best monotherapy
best_combo = max(fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"])
best_mono = max(fr["tolerance only"], fr["anti-CD3 only"])
check("combination beats best monotherapy by >=20 pts (the clinical rationale)",
      best_combo - best_mono >= 0.20, f"combo {best_combo*100:.0f}% vs mono {best_mono*100:.0f}%")

# (5) synergy is ROBUST across anti-CD3 imprint strength
robust = True
for epsX in [0.3, 0.6, 0.9, 1.2]:
    p = dict(M.P); p["epsX"] = epsX
    f2 = {n: M.cure_fraction(s, p=p) for n in ["tolerance only", "anti-CD3 only", "simultaneous",
                                               "anti-CD3 -> tol", "tol -> anti-CD3"]
          for s in [M.arms()[n]]}
    bc = max(f2["simultaneous"], f2["anti-CD3 -> tol"], f2["tol -> anti-CD3"])
    bm = max(f2["tolerance only"], f2["anti-CD3 only"])
    robust = robust and (bc - bm >= 0.20)
check("combination>monotherapy holds across imprint strength (epsX 0.3-1.2)", robust)

# (6) the v1 sequencing claim is DOWNGRADED: tol-first ~ a3-first at the operating point
seq_gap = fr["tol -> anti-CD3"] - fr["anti-CD3 -> tol"]
check("sequencing is second-order at the operating point (|tol-first - a3-first| <= 10 pts)",
      abs(seq_gap) <= 0.10, f"{seq_gap*100:+.0f} pts")

# (7) ...but re-appears when anti-CD3's durable benefit is weak (epsX low) -- the honest hedge
p_weak = dict(M.P); p_weak["epsX"] = 0.3
fw = {n: M.cure_fraction(M.arms()[n], p=p_weak) for n in ["anti-CD3 -> tol", "tol -> anti-CD3"]}
check("sequencing re-appears (tol-first > a3-first) only when imprint is weak (epsX=0.3)",
      fw["tol -> anti-CD3"] - fw["anti-CD3 -> tol"] >= 0.10,
      f"{(fw['tol -> anti-CD3']-fw['anti-CD3 -> tol'])*100:+.0f} pts at epsX=0.3")

print("\n" + "=" * 60)
npass = sum(c for _, c, _ in checks)
print(f"{npass}/{len(checks)} checks passed")
sys.exit(0 if npass == len(checks) else 1)
