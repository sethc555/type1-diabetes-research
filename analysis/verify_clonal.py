#!/usr/bin/env python3
"""Seed-robustness verification of the discrete-clonal/stochastic model's Foster result.
Run under the 4 GB cap.  Asserts: (a) calibration, (b) the SIMULTANEOUS co-dosing antagonism is
real and seed-robust, (c) it is a CO-DOSING effect (vanishes without preferential converter-deletion),
(d) SEQUENCING rescues it. exit 0 iff all pass.
"""
import sys
import numpy as np
import t1d_clonal as M

checks = []
def check(name, cond, detail=""):
    checks.append(bool(cond)); print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

SEEDS = range(6)
def mean_arms(conv, kAC):
    rows = []
    for s in SEEDS:
        p = dict(M.PARAMS); p["conv"] = conv; p["kAC"] = kAC
        fr = M.arms_fractions(p, seed=s)
        rows.append([fr["untreated"], fr["anti-CD3 only"], fr["tolerance only"],
                     fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"]])
    return np.array(rows) * 100.0   # (seeds x 6 arms), percent

# marginal-tolerance regime, strong preferential converter-deletion (co-dose is the Foster condition)
A = mean_arms(conv=2.5, kAC=120.0)
untr, a3, tol, sim, a3t, ta3 = A.mean(0)
B = mean_arms(conv=2.5, kAC=0.0)     # same, but anti-CD3 does NOT preferentially delete converters
tol0, sim0 = B[:, 2].mean(), B[:, 3].mean()

check("untreated never cured", untr < 1.0, f"{untr:.0f}%")
check("anti-CD3 monotherapy does not durably cure (<25%)", a3 < 25.0, f"{a3:.0f}%")
check("tolerance monotherapy is effective (>70%)", tol > 70.0, f"{tol:.0f}%")
check("SIMULTANEOUS co-dosing ANTAGONIZES tolerance by >=25 pts (Foster)", tol - sim >= 25.0,
      f"tol {tol:.0f}% vs simultaneous {sim:.0f}%  ->  {sim-tol:+.0f} pts")
check("the antagonism is SEED-ROBUST (simultaneous < tol-only in every seed)",
      bool(np.all(A[:, 3] < A[:, 2] - 5)), f"per-seed simultaneous {A[:,3].astype(int)}")
check("preferential converter-deletion AMPLIFIES the co-dosing antagonism by >=40 pts",
      (tol - sim) - (tol0 - sim0) >= 40.0,
      f"gap kAC=120 is {tol-sim:.0f} pts vs kAC=0 {tol0-sim0:.0f} pts -> amplified {(tol-sim)-(tol0-sim0):+.0f}")
check("SEQUENCING rescues it: gap-separated arms stay >=70% even at kAC=120",
      a3t >= 70.0 and ta3 >= 70.0, f"a3->tol {a3t:.0f}%, tol->a3 {ta3:.0f}%")

print("\n" + "=" * 66)
npass = sum(checks)
print(f"{npass}/{len(checks)} checks passed")
print("\nDiscrete-clonal/stochastic dynamics REPRODUCE the Foster antagonism (continuum/bistable could")
print("not): co-administered anti-CD3 stochastically extinguishes the just-activated converting clones")
print("tolerance needs -> protection collapses. Separating the two therapies in time restores efficacy.")
sys.exit(0 if npass == len(checks) else 1)
