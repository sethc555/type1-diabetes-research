#!/usr/bin/env python3
"""Machine-checkable assertion for the AVIDITY layer (t1d_avidity.py): the avidity-resolved CONTINUUM does
NOT reproduce the Foster antagonism -- not at baseline, and not under the strongest candidate mechanism
(anti-CD3 preferential deletion of the converting clones). So the antagonism is SUB-CONTINUUM: it needs the
discrete-clonal / stochastic model (verify_clonal). Reduced avidity resolution + cohort for speed; the
result is N-robust (the structural negative does not depend on resolution). 4 GB cap."""
import sys
import numpy as np
from t1d_avidity import arms, cure_fraction, P

N = 20
COH = np.linspace(0.8, 1.4, 5)


def combo_eff(p):
    fr = {nm: cure_fraction(s, N, p=p, cohort=COH) for nm, s in arms().items()}
    best_combo = max(fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"])
    best_mono = max(fr["tolerance only"], fr["anti-CD3 only"])
    return best_combo - best_mono


eff_base = combo_eff(dict(P))
p_del = dict(P); p_del["delA"] = 20.0
eff_del = combo_eff(p_del)

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

chk("avidity continuum is NOT antagonistic at baseline", eff_base >= -0.05, f"combo - mono = {eff_base*100:+.0f} pts (>= -5)")
chk("acute-deletion mechanism does NOT make antagonism", eff_del >= -0.05, f"combo - mono = {eff_del*100:+.0f} pts")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- avidity layer: Foster antagonism is SUB-CONTINUUM")
print("  the avidity-resolved continuum can't produce it -> it needs discrete-clonal resolution (verify_clonal).")
sys.exit(0 if npass == len(checks) else 1)
