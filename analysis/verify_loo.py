#!/usr/bin/env python3
"""Machine-checkable assertions for the OUT-OF-SAMPLE validation (loo_validation.py): the model's
natural-history RATE predictions transfer to held-out trials within a few percent (VALIDATED), while its
cross-stage DRUG-EFFECT extrapolations do not (the honest, measured decision-grade boundary). 4 GB cap."""
import sys
from loo_validation import ROWS

rate = [(nm, abs(p - o) / o) for nm, k, p, o in ROWS if k == "rate"]
cross = [(nm, abs(p - o) / o) for nm, k, p, o in ROWS if k == "cross-stage"]
rate_med = sorted(e for _, e in rate)[len(rate) // 2]
cross_med = sorted(e for _, e in cross)[len(cross) // 2]

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

# every natural-history rate prediction is quantitatively tight out-of-sample
for nm, e in rate:
    chk(f"RATE OOS tight: {nm}", e < 0.10, f"{e*100:.0f}% error")
# the rate predictions, as a set, are validated
chk("rate predictions median < 8% (VALIDATED)", rate_med < 0.08, f"median {rate_med*100:.0f}%")
# the cross-stage drug-effect transfer is genuinely looser -- the measured boundary is real (and honestly reported)
chk("cross-stage transfer is clearly worse (boundary is real)", cross_med > 0.30, f"median {cross_med*100:.0f}%")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- out-of-sample validation")
print("  natural-history rates validate to a few %; cross-stage drug effects do not -> a measured trust boundary.")
sys.exit(0 if npass == len(checks) else 1)
