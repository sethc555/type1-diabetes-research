#!/usr/bin/env python3
"""CALIBRATION #2 -- the SPREADING rate fit to the TEDDY/Ziegler natural history.

REAL targets:
  * Ziegler 2013 (JAMA, 1092 cites): MULTIPLE islet autoantibodies -> T1D = 44% @5yr, 70% @10yr, 84% @15yr;
    SINGLE autoantibody -> T1D = 14.5% @10yr (~5x lower).
  * Vehik 2020 (TEDDY, Diabetes Care): the second-appearing autoantibody is the inflection (HR 6-16 for
    progression); spreading 1 -> multiple is what converts the slow single-Ab course into the fast one.

This pins the EMPIRICAL spreading timescale behind AE1 (t1d_spreading.py). Compartmental natural-history:
  S1 (single-Ab) --spread--> S2 (multiple-Ab) --h2--> D (clinical)
with h1=0 (clinical progression REQUIRES spreading -- the hypothesis the data strongly supports: single-Ab
risk is only 14.5%). Fit (spread, h2) to the four real points. Reports the fit + identifiability.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

# real targets (start-state, years, cumulative T1D fraction)
TARGETS = [("multiple", 5, 0.44), ("multiple", 10, 0.70), ("multiple", 15, 0.84), ("single", 10, 0.145)]


def progressed(spread, h2, start, t, h1=0.0):
    def rhs(tt, y):
        S1, S2, D = y
        return [-(spread + h1) * S1, spread * S1 - h2 * S2, h1 * S1 + h2 * S2]
    y0 = [1.0, 0.0, 0.0] if start == "single" else [0.0, 1.0, 0.0]
    sol = solve_ivp(rhs, (0, t), y0, t_eval=[t], rtol=1e-10, atol=1e-12, max_step=0.1)
    return float(sol.y[2, -1])


def resid(p):
    spread, h2 = p
    return [progressed(spread, h2, s, t) - f for (s, t, f) in TARGETS]


def main():
    print("CALIBRATION #2 -- spreading rate <- TEDDY/Ziegler natural history\n")
    fit = least_squares(resid, [0.04, 0.12], bounds=([1e-3, 1e-3], [1.0, 1.0]))
    spread, h2 = fit.x
    print(f"  FIT  spreading rate (single->multiple) : {spread:.3f} /yr  (median time to 2nd Ab ~{np.log(2)/spread:.1f} yr)")
    print(f"  FIT  multiple-Ab -> clinical hazard h2  : {h2:.3f} /yr  (median ~{np.log(2)/h2:.1f} yr)")
    print(f"  (h1 = 0 fixed: clinical progression REQUIRES spreading -- the data-supported hypothesis)\n")
    print(f"  {'cohort':10s} {'yr':>3}  {'TEDDY/Ziegler':>13}  {'model':>7}")
    for s, t, f in TARGETS:
        print(f"  {s:10s} {t:>3}  {f*100:>12.0f}%  {progressed(spread,h2,s,t)*100:>6.0f}%")
    print(f"\n  worst residual: {max(abs(r) for r in resid(fit.x))*100:.1f} percentage points")

    print("\n  IDENTIFIABILITY -- what the data pins (honest):")
    print("   * h2 is pinned by the MULTIPLE-Ab curve (44/70/84% @ 5/10/15 yr -- ~exponential).")
    print("   * spread is pinned by the SINGLE-Ab endpoint (14.5% @10yr) GIVEN h1=0; relaxing h1>0")
    print("     would trade off against spread (single-Ab data alone can't separate them).")
    print("   * This anchors AE1's spreading TIMESCALE (~0.04/yr, multi-year) -- complementary to the")
    print("     fast stage-2->3 timescale kappa (TN10, ~2 yr). Pre-clinical clock vs final-approach clock.")


if __name__ == "__main__":
    main()
