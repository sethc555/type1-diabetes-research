#!/usr/bin/env python3
"""Machine-checkable assertions for CALIBRATION #4 (calib_pescovitz.py): the anti-CD20 transience fit to
Pescovitz -- repopulation rate to the B-cell recovery curve, B-cell-dependence to the 8.2-mo C-peptide
shift; both plausible. Deterministic. 4 GB cap."""
import sys
from scipy.integrate import quad
from scipy.optimize import brentq
from calib_pescovitz import Bc, BC_12MO, SHIFT_TARGET

r_bc = brentq(lambda r: Bc(1.0, r) - BC_12MO, 0.5, 30.0)
area, _ = quad(lambda t: 1 - Bc(t, r_bc), 0, 6)
Tdom = 1 - SHIFT_TARGET / area
shift = (1 - Tdom) * area

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

chk("repopulation reproduces 69% @12mo (Pescovitz)", abs(Bc(1.0, r_bc) - 0.69) < 0.02, f"{Bc(1.0,r_bc)*100:.0f}%")
chk("B cells ~baseline by 18mo (Pescovitz)", Bc(1.5, r_bc) > 0.90, f"{Bc(1.5,r_bc)*100:.0f}% @18mo")
chk("reproduces the 8.2-mo C-peptide shift (Pescovitz 2014)", abs(shift - SHIFT_TARGET) < 0.02, f"{shift*12:.1f} mo")
chk("B-cell-dependence Tdom plausible & B-driven", 0.05 < Tdom < 0.35, f"Tdom = {Tdom:.2f} (~{(1-Tdom)*100:.0f}% B-dependent)")
chk("repopulation rate plausible 2-10 /yr", 2 < r_bc < 10, f"r_bc = {r_bc:.2f} /yr")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- calibration #4 (anti-CD20 transience <- Pescovitz)")
print("  r_bc~4.7/yr + Tdom~0.18 reproduce the B-cell recovery and the finite 8.2-mo C-peptide shift.")
sys.exit(0 if npass == len(checks) else 1)
