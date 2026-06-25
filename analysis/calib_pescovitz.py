#!/usr/bin/env python3
"""CALIBRATION #4 -- anti-CD20 TRANSIENCE fit to Pescovitz (rituximab in new-onset T1D).

REAL targets:
  * Pescovitz 2009/2014 (NEJM / Diabetes Care): peripheral B cells depleted by the 4-dose course, recover to
    69% of baseline by 12 mo and ~baseline by 18 mo.
  * Pescovitz 2014 (2-yr results): the C-peptide decline rate was PARALLEL between groups but SHIFTED by
    8.2 months in rituximab subjects -- i.e. a finite one-time delay, NOT a sustained slowing; benefit gone by 30 mo.

This pins BC1's transience knobs (t1d_bcell.py): the B-cell repopulation rate r_bc, and -- via the observed
shift -- the B-cell-dependence of the attack (Tdom). Mechanism: while B cells are depleted the attack is
paused (kill scaled by helpf = Tdom + (1-Tdom)*Bc); for exponential decline the net curve SHIFT equals the
integrated pause INT (1-helpf) dt. Fit r_bc to the repopulation curve, then Tdom to the 8.2-mo shift.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

BC_12MO = 0.69                 # B cells = 69% of baseline at 12 mo (Pescovitz)
SHIFT_TARGET = 8.2 / 12.0      # yr  -- C-peptide decline shifted by 8.2 mo (Pescovitz 2014)
BC0 = 0.02                     # depleted at t=0 (4-dose rituximab course)


def Bc(t, r):
    return 1.0 / (1.0 + ((1 - BC0) / BC0) * np.exp(-r * t))   # logistic repopulation from depletion


def main():
    print("CALIBRATION #4 -- anti-CD20 transience <- Pescovitz 2009/2014\n")

    r_bc = brentq(lambda r: Bc(1.0, r) - BC_12MO, 0.5, 30.0)
    print(f"  FIT  repopulation rate r_bc = {r_bc:.2f}/yr")
    print(f"       -> Bc(12mo) = {Bc(1.0,r_bc)*100:.0f}% (target 69%),  Bc(18mo) = {Bc(1.5,r_bc)*100:.0f}% (~baseline)\n")

    area, _ = quad(lambda t: 1 - Bc(t, r_bc), 0, 6)            # integrated depletion = the curve shift at full B-dependence
    Tdom = 1 - SHIFT_TARGET / area
    shift = (1 - Tdom) * area
    print(f"  integral (1-Bc) dt = {area:.2f} yr  (the max possible shift, at full B-dependence)")
    print(f"  FIT  attack B-cell-dependence: Tdom = {Tdom:.2f}  -> C-peptide shift {shift*12:.1f} mo (target 8.2)")
    print(f"       (Tdom={Tdom:.2f} ~ the t1d_bcell layer's illustrative 0.20 -- consistent; ~{(1-Tdom)*100:.0f}% B-cell-dependent,")
    print(f"        matching 'rituximab responders are B-cell-driven', Linsley 2018 / Herold 2011)\n")

    print("  RESULT -- the transience is anchored, and it is genuinely TRANSIENT:")
    print(f"   * anti-CD20 buys a finite ~{shift*12:.0f}-month shift in the C-peptide curve, then the decline resumes")
    print(f"     at the placebo rate (curves PARALLEL) -- exactly Pescovitz 2014, benefit gone by 30 mo.")
    print(f"   * This is why BC1 says anti-CD20 needs a durable partner: alone it only shifts, never bends, the curve.")


if __name__ == "__main__":
    main()
