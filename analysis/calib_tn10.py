#!/usr/bin/env python3
"""CALIBRATION #1 -- disease TIMESCALE (kappa) fit to the TN10 placebo progression curve.

REAL target (Herold 2019, NEJM NEJMoa1902226; TrialNet TN10): stage-2 relatives (>=2 islet autoantibodies +
dysglycemia), n=32 placebo / 44 teplizumab. Median time to clinical T1D: PLACEBO 24.4 mo, TEPLIZUMAB 48.4 mo
(~2-yr delay); annualized placebo progression ~36%/yr.

This pins the SHARED disease-timescale knob (AK2's kappa) that the body's models use, in a MINIMAL,
identifiable model: dB = rhoB*B*(1-B) - kappa*B (the established stage-2 attack folded into kappa with the
effector burden E normalized to 1); clinical onset when functional beta-mass B crosses B_clin. Cohort =
lognormal spread of kappa (patient heterogeneity). Fit kappa to the placebo MEDIAN, then fit the anti-CD3
effect to the teplizumab median. Reports the fit AND its identifiability (what the median actually constrains).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import norm
from scipy.optimize import brentq

MED_PLACEBO = 24.4 / 12.0      # yr (Herold 2019)
MED_TEPLI = 48.4 / 12.0        # yr

# structural assumptions (STATED, not fit) -- the onset depends on these, so they bound what kappa means
RHOB = 0.5
B0 = 0.55                      # stage-2 enrollment functional beta-mass (dysglycemic, pre-clinical)
B_CLIN = 0.30                  # clinical-diagnosis threshold (functional mass at hyperglycemia)
GSD = 1.6                      # cohort geometric SD of kappa (patient heterogeneity) -- sets KM width
NQ = 151


def onset_time(kappa, b0=B0, bclin=B_CLIN, rhob=RHOB):
    ev = lambda t, y: y[0] - bclin
    ev.terminal = True; ev.direction = -1
    sol = solve_ivp(lambda t, y: [rhob * y[0] * (1 - y[0]) - kappa * y[0]], (0, 80), [b0],
                    events=ev, rtol=1e-9, atol=1e-11, max_step=0.1)
    return float(sol.t_events[0][0]) if len(sol.t_events[0]) else np.inf


def fit_kappa(target_median, b0=B0, bclin=B_CLIN):
    return brentq(lambda k: onset_time(k, b0, bclin) - target_median, 0.05, 8.0, xtol=1e-5)


def cohort_onsets(kappa_med, gsd=GSD):
    z = norm.ppf(np.linspace(0.005, 0.995, NQ))
    return np.array([onset_time(kappa_med * np.exp(np.log(gsd) * zi)) for zi in z])


def main():
    print("CALIBRATION #1 -- disease timescale (kappa) <- TN10 placebo (Herold 2019, NEJM)\n")

    kappa = fit_kappa(MED_PLACEBO)
    print(f"  TARGET  placebo median onset : {MED_PLACEBO*12:.1f} mo")
    print(f"  FIT     kappa (E=1 normalized): {kappa:.3f} /yr   ->  model median {onset_time(kappa)*12:.1f} mo")

    on = cohort_onsets(kappa)
    haz = np.log(2) / MED_PLACEBO
    print(f"  cohort KM (gsd={GSD}):  progressed @12mo {np.mean(on<=1)*100:.0f}%  @24mo {np.mean(on<=2)*100:.0f}%  @36mo {np.mean(on<=3)*100:.0f}%")
    print(f"    cross-check vs exponential at hazard ln2/median={haz:.2f}/yr (~TN10 ~36%/yr): "
          f"{(1-np.exp(-haz*1))*100:.0f}% / 50% / {(1-np.exp(-haz*3))*100:.0f}%\n")

    eff = brentq(lambda e: onset_time(kappa * (1 - e)) - MED_TEPLI, 0.01, 0.95, xtol=1e-5)
    print(f"  TARGET  teplizumab median onset: {MED_TEPLI*12:.1f} mo (~2-yr delay)")
    print(f"  FIT     anti-CD3 effective attack reduction: {eff*100:.0f}%  ->  model median {onset_time(kappa*(1-eff))*12:.1f} mo\n")

    print("  IDENTIFIABILITY -- what the median actually pins (honest):")
    print("   * The median constrains the PRODUCT kappa x E (E set =1 here) and the RATIO B0/B_clin -- not")
    print("     kappa alone. The TIMESCALE is pinned; the kappa-vs-effector-burden split is NOT.")
    print("   * kappa shifts with the (unmeasured) enrollment/threshold assumptions B0, B_clin:")
    for b0 in (0.50, 0.55, 0.60):
        print(f"       B0={b0:.2f}: kappa={fit_kappa(MED_PLACEBO, b0=b0):.3f}/yr", end="")
    print()
    for bc in (0.25, 0.30, 0.35):
        print(f"       B_clin={bc:.2f}: kappa={fit_kappa(MED_PLACEBO, bclin=bc):.3f}/yr", end="")
    print("\n   -> the disease TIMESCALE (median 24.4 mo) is the calibrated, identifiable quantity;")
    print("      report kappa as 'the rate that yields it under B0=0.55, B_clin=0.30, E=1'.")


if __name__ == "__main__":
    main()
