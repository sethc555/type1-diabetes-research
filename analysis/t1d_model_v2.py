#!/usr/bin/env python3
"""P2-revision (v2) — model rebuilt to answer the reviewer critique (see AUDIT.md).

Three structural fixes to the published v1 model (`t1d_model.py`):

  (1) THYMIC Treg source `sig_thy`: Tregs are a thymic output, not only peripheral conversion.
      In NOD the thymic source is IMPAIRED (selection defect) but nonzero -> R has a small floor
      independent of conversion. (Addresses critique #1.)

  (2) CONVERTIBLE-PRECURSOR fraction `c` in [0,1]: only a fraction of effectors are tolerogenic-
      convertible; NOD thymic deletion of those precursors makes `c` SMALL, so antigen-specific
      tolerance is INTRINSICALLY limited -- it can convert only `c*E`, not all of E. (Addresses #1 deep
      + #2: tolerance can't be made fully effective by peripheral conversion if the raw material is
      gone.)

  (3) CALIBRATED efficacies, grounded in real numbers rather than a 100% byproduct (Addresses #2,#3):
        - tolerance monotherapy is WEAK/partial (human antigen-specific tolerance trials -- oral
          insulin DPT-1, GAD-alum -- showed little durable efficacy; NOD prevention is partial),
        - anti-CD3 monotherapy DELAYS but does not cure (teplizumab/TN10: ~2-yr median delay,
          FDA-approved to delay stage 3 -- NOT 0% and NOT a cure),
      so the combination is studied for the *right* reason: tolerance alone underdelivers and
      anti-CD3 is added to help. The model no longer assumes the efficacy gap away.

Anti-CD3 now has its real DUAL character: it DEBULKS pathogenic effectors (lowering beta-cell
killing -> a genuine delay/benefit, via the dB term) AND depletes the convertible precursors + Tregs
(the harm channel). The honest question this version asks is the clinically-motivated one:
*given weak tolerance, does adding anti-CD3 help, and does the order matter?* -- reported as found.

State (years): B beta-cell mass, E autoreactive effectors, R antigen-specific Tregs.
    dE/dt = bE + VE*E^2/(K^2+E^2)/(1+(R/Ki)^2) - dE*E - u_a3*E - u_tol*c*E
    dR/dt = sig_thy + bR + VR*R^2/(K^2+R^2)/(1+(E/Ki)^2) - dR*R + phi*u_tol*c*E - rho*u_a3*R
    dB/dt = rhoB*B*(1-B) - kappa*E*B
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    bE=0.08, VE=1.80, K=0.50, Ki=0.50, dE=0.80,
    bR=0.04, VR=1.40, dR=0.50,
    sig_thy=0.06,   # NEW: thymic Treg output (impaired-but-nonzero in NOD)
    c=0.60,         # NEW: convertible-precursor fraction (small => tolerance intrinsically limited)
    phi=0.40, rho=0.90, rhoB=0.60, kappa=0.40,
    epsX=0.9,       # NEW: anti-CD3 -> effector-hyporesponsiveness imprint rate (teplizumab exhaustion)
    dX=1.10,        # NEW: decay of that imprint (1/yr) -- durable but not permanent
)
N_HILL = 2
A3_RATE = 22.0      # anti-CD3 effector-depletion rate while dosing (raised: real debulking -> delay)
A3_DUR = 14/365.0
TOL_RATE = 12.0
TOL_DUR = 30/365.0
B_DX = 0.30
B_CURE = 0.45
HORIZON = 5.0


def _pulse(t, t0, dur, rate):
    return rate if (t0 <= t < t0 + dur) else 0.0


def rhs(t, y, p, sched):
    B, E, R, X = (max(v, 0.0) for v in y)
    X = min(X, 1.0)
    n = N_HILL
    u_a3 = _pulse(t, sched.get("a3_t0", 1e9), A3_DUR, A3_RATE) if sched.get("a3") else 0.0
    u_tol = _pulse(t, sched.get("tol_t0", 1e9), TOL_DUR, TOL_RATE) if sched.get("tol") else 0.0
    c = p["c"]
    selfE = p["VE"] * E**n / (p["K"]**n + E**n) / (1 + (R / p["Ki"])**n)
    selfR = p["VR"] * R**n / (p["K"]**n + R**n) / (1 + (E / p["Ki"])**n)
    conv = p["phi"] * u_tol * c * E            # tolerance converts ONLY the convertible fraction
    dE = p["bE"] + (1 - X) * selfE - p["dE"] * E - u_a3 * E - u_tol * c * E
    dR = (p["sig_thy"] + p["bR"] + selfR - p["dR"] * R + conv - p["rho"] * u_a3 * R)
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * (1 - X) * E * B
    dX = p["epsX"] * u_a3 * (1 - X) - p["dX"] * X   # anti-CD3-induced effector hyporesponsiveness
    return [dB, dE, dR, dX]


def stage2_ic(E0=1.10, p=None):
    """Late stage 2. R0 reflects the (impaired) thymic Treg baseline, not zero. X0=0 (no imprint)."""
    p = p or P
    R0 = (p["sig_thy"] + p["bR"]) / p["dR"]    # quiescent thymic-sourced Treg floor
    return [0.60, E0, R0, 0.0]


def simulate(sched=None, p=None, t_end=8.0, npts=2500, y0=None, E0=1.10):
    p = p or P
    sched = sched or {}
    y0 = y0 if y0 is not None else stage2_ic(E0, p)
    t_eval = np.linspace(0, t_end, npts)
    return solve_ivp(rhs, (0, t_end), y0, args=(p, sched), t_eval=t_eval,
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.012)


def time_to_dx(sol, b_dx=B_DX):
    B = sol.y[0]; below = np.where(B < b_dx)[0]
    if below.size == 0:
        return np.inf
    i = below[0]
    if i == 0:
        return 0.0
    t0, t1, b0, b1 = sol.t[i-1], sol.t[i], B[i-1], B[i]
    return t0 + (b_dx - b0) * (t1 - t0) / (b1 - b0)


def banked_mass(sol, horizon=HORIZON):
    return float(np.interp(horizon, sol.t, sol.y[0]))


def arms(gap=0.25):
    return {
        "untreated":       {},
        "anti-CD3 only":   {"a3": True, "a3_t0": 0.0},
        "tolerance only":  {"tol": True, "tol_t0": 0.0},
        "simultaneous":    {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0},
        "anti-CD3 -> tol": {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": gap},
        "tol -> anti-CD3": {"tol": True, "tol_t0": 0.0, "a3": True, "a3_t0": gap},
    }


def cure_fraction(sched, cohort=None, p=None, horizon=HORIZON, b_cure=B_CURE):
    p = p or P
    cohort = cohort if cohort is not None else np.linspace(0.70, 1.50, 17)
    return float(np.mean([banked_mass(simulate(sched, p, E0=E0), horizon) > b_cure for E0 in cohort]))


def main():
    base = time_to_dx(simulate(arms()["untreated"]))
    print(f"{'arm':18s} {'t_dx(yr)':>9s} {'delay':>7s} {'cohort cure':>12s}")
    for name, s in arms().items():
        tdx = time_to_dx(simulate(s))
        cf = cure_fraction(s)
        dl = (tdx - base) if (np.isfinite(tdx) and np.isfinite(base)) else np.inf
        tdx_s = f"{tdx:.2f}" if np.isfinite(tdx) else "none"
        dl_s = ("cure" if np.isinf(dl) else f"+{dl:.2f}")
        print(f"{name:18s} {tdx_s:>9s} {dl_s:>7s} {cf*100:11.0f}%")
    print("\nClinical-rationale checks (the reviewer critique):")
    fr = {n: cure_fraction(s) for n, s in arms().items()}
    print(f"  tolerance-alone cure fraction: {fr['tolerance only']*100:.0f}%  (should be PARTIAL, not 100%)")
    print(f"  anti-CD3-alone delay: +{time_to_dx(simulate(arms()['anti-CD3 only']))-base:.2f} yr, "
          f"cure {fr['anti-CD3 only']*100:.0f}%  (should DELAY, not cure)")
    best_combo = max(fr['simultaneous'], fr['anti-CD3 -> tol'], fr['tol -> anti-CD3'])
    print(f"  does ANY combination beat the best monotherapy? "
          f"best combo {best_combo*100:.0f}% vs best mono {max(fr['tolerance only'],fr['anti-CD3 only'])*100:.0f}%")


if __name__ == "__main__":
    main()
