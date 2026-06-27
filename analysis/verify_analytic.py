#!/usr/bin/env python3
"""Machine-checkable assertions for the DERIVED ANALYTIC results (analytic.py): each closed form, derived
from the model equations, reproduces the real/calibrated value -- the 'derived formulas for review' a
reviewer can check by hand. Deterministic. 4 GB cap."""
import sys
from analytic import h2, spread, k_cpep, KAPPA_TN10, Delta, D_S2, D_S1

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

# 1. multi-Ab natural history -- exact closed forms reproduce Ziegler
chk("h2 = -ln(1-F)/t -> Ziegler 70% @10yr", abs(D_S2(h2, 10) - 0.70) < 0.03, f"{D_S2(h2,10)*100:.0f}%")
chk("                 -> Ziegler 84% @15yr", abs(D_S2(h2, 15) - 0.84) < 0.03, f"{D_S2(h2,15)*100:.0f}%")
chk("single-Ab two-step closed form -> 14.5% @10yr", abs(D_S1(spread, h2, 10) - 0.145) < 0.02, f"{D_S1(spread,h2,10)*100:.0f}%")
chk("spreading rate plausible (~0.04/yr)", 0.02 < spread < 0.08, f"{spread:.3f}/yr")
# 2. C-peptide half-life closed form + the cross-validation
chk("k = ln2/t_half = 0.63/yr (Shields)", abs(k_cpep - 0.63) < 0.02, f"{k_cpep:.3f}/yr")
chk("cross-validation: k_cpep ~ kappa(TN10) within 10%", abs(k_cpep - KAPPA_TN10) / KAPPA_TN10 < 0.10, f"{k_cpep:.2f} vs {KAPPA_TN10:.2f}")
# 3. anti-CD20 shift closed form
chk("Delta=(1-Tdom)(1/r_bc)ln(1/Bc0) = 8.2mo (Pescovitz)", abs(Delta * 12 - 8.2) < 0.6, f"{Delta*12:.1f} mo")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- derived analytic formulas reproduce the real values")
sys.exit(0 if npass == len(checks) else 1)
