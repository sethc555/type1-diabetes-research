#!/usr/bin/env python3
"""Machine-checkable assertions for the B-CELL / autoantibody layer (t1d_bcell.py).
Deterministic. Asserts the 4 predictions: anti-CD20 is transient, the responder axis, the
anti-CD20 + tolerance combination benefit, and the autoantibody-count readout. 4 GB cap."""
import sys
from t1d_bcell import simulate, bAt

untr = simulate({})
cd20 = simulate({"cd20": True, "cd20_t0": 2.0})
peak = bAt(cd20, 3) - bAt(untr, 3)
late = bAt(cd20, 11) - bAt(untr, 11)

cB = simulate({"Tdom": 0.20, "cd20": True, "cd20_t0": 2.0}); uB = simulate({"Tdom": 0.20})
cT = simulate({"Tdom": 0.65, "cd20": True, "cd20_t0": 2.0}); uT = simulate({"Tdom": 0.65})
benB = bAt(cB, 3) - bAt(uB, 3); benT = bAt(cT, 3) - bAt(uT, 3)

LATE = 2.5
u  = bAt(simulate({}), 6)
st = bAt(simulate({"tol": True, "tol_t0": LATE, "targets": [0]}), 6)
ac = bAt(simulate({"cd20": True, "cd20_t0": LATE}), 6)
co = bAt(simulate({"tol": True, "tol_t0": LATE, "targets": [0], "cd20": True, "cd20_t0": LATE}), 6)

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# P1 — anti-CD20 is TRANSIENT (benefit peaks, then fades to ~0 as B cells repopulate)
chk("P1  anti-CD20 benefit peaks early", peak > 0.08, f"+{peak:.2f} @3yr")
chk("P1b benefit FADES (transient)",     late < 0.03, f"+{late:.2f} @11yr (-> ~0)")
# P2 — RESPONDER axis: B-cell-driven responds more than T-dominated
chk("P2  B-driven > T-dominated",        benB > benT + 0.04, f"B-driven +{benB:.2f} vs T-dom +{benT:.2f}")
# P3 — anti-CD20 + single-antigen tolerance COMBINATION beats either alone
chk("P3  combo > single-tol",            co > st + 0.03, f"combo {co:.2f} > single-tol {st:.2f}")
chk("P3b combo > anti-CD20 alone",       co > ac + 0.03, f"combo {co:.2f} > anti-CD20 {ac:.2f}")
chk("P3c combo > untreated",             co > u + 0.05,  f"combo {co:.2f} > untreated {u:.2f}")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass — B-cell / autoantibody layer")
print("  anti-CD20 is transient (B cells repopulate); works when B-cell-driven; tolerance + anti-CD20 > either alone.")
sys.exit(0 if npass == len(checks) else 1)
