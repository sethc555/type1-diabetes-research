#!/usr/bin/env python3
"""Machine-checkable assertions for the INNATE-immunity layer (t1d_innate.py).
Deterministic. Asserts: the EARLY WINDOW (innate-targeting prevents early, fails late), the
self-sustaining transition, innate upstream of the stress hub, and innate-precedes-adaptive timing. 4 GB cap."""
import sys
import numpy as np
from t1d_innate import simulate, bend, first_t, HOR

untr = simulate({})
early = simulate({"u_innate": 8.0, "innate_t0": 0.0})
late = simulate({"u_innate": 8.0, "innate_t0": 2.5})

E_early = float(np.interp(HOR, early.t, early.y[1]))
E_late = float(np.interp(HOR, late.t, late.y[1]))
peakS_u, peakS_e = float(untr.y[3].max()), float(early.y[3].max())
tN = float(untr.t[np.argmax(untr.y[0])]); tE = first_t(untr, 1, 0.5); tB = first_t(untr, 2, 0.5, rising=False)

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# P1 — the EARLY WINDOW: innate-targeting prevents early but fails late
chk("P1  anti-innate EARLY prevents",  bend(early) > 0.30, f"early beta@6yr {bend(early):.2f} preserved")
chk("P1b anti-innate LATE fails",      bend(late) < 0.30,  f"late beta@6yr {bend(late):.2f} lost (Moran 2013)")
chk("P1c early >> late (the window)",  bend(early) > bend(late) + 0.3, f"early {bend(early):.2f} >> late {bend(late):.2f}")
# P2 — the adaptive attack is self-sustaining once established
chk("P2  EARLY: E never ignites",      E_early < 0.10, f"E@6yr {E_early:.2f}")
chk("P2b LATE: E self-sustains",       E_late > 0.50,  f"E@6yr {E_late:.2f} (innate-independent)")
# P3 — innate is upstream of the stress hub
chk("P3  early innate control cuts stress", peakS_e < peakS_u - 0.15, f"peak S {peakS_u:.2f} -> {peakS_e:.2f}")
# P4 — innate precedes adaptive precedes beta-loss
chk("P4  innate precedes adaptive precedes beta-loss", tN < tE < tB, f"N {tN:.2f} < E {tE:.2f} < beta<50% {tB:.2f}")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass — innate-immunity layer")
print("  innate is the upstream trigger; anti-innate prevents EARLY, fails at onset (Moran 2013); a narrow window.")
sys.exit(0 if npass == len(checks) else 1)
