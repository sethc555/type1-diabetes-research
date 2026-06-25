#!/usr/bin/env python3
"""Machine-checkable assertions for the BETA-CELL layer (t1d_betacell.py): the beta-cell STRESS feedback
is self-amplifying (P1); beta-PROTECTION works orthogonally and the combination is SAFE / non-antagonistic
(P2-P3). P4 (a fragility lever-FLIP) is an honest NON-result and is deliberately NOT asserted. 4 GB cap."""
import sys
from t1d_betacell import bf, simulate, arms, P, BF_OK

no_fb = bf(simulate({"amp": 0.0}))
fb = bf(simulate({"amp": P["amp"]}))
a = arms()
best_mono = max(a["immune only (tep)"], a["beta-protect only"])
combo_gain = a["combination"] - best_mono

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

chk("P1 stress feedback is self-amplifying (worse WITH feedback)", fb < no_fb - 0.02, f"feedback {fb:.2f} < no-feedback {no_fb:.2f}")
chk("P2 beta-protection ALONE has an orthogonal benefit (> untreated)", a["beta-protect only"] > a["untreated"] + 0.05, f"protect {a['beta-protect only']:.2f} vs untreated {a['untreated']:.2f}")
chk("P3 combination is SAFE -- no antagonism", combo_gain >= -0.02, f"combo - best monotherapy = {combo_gain:+.2f}")
chk("P3 combination preserves beta", a["combination"] > BF_OK, f"{a['combination']:.2f}")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- beta-cell layer (self-amplifying loop + safe orthogonal combination)")
sys.exit(0 if npass == len(checks) else 1)
