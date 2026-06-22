#!/usr/bin/env python3
"""P1 — core within-host T1D model: a bistable effector<->Treg immune "toggle switch"
driving beta-cell mass, with two interventions (anti-CD3 and antigen-specific tolerance)
whose ORDER of administration changes the outcome.

The open lane (see analysis/MEMO.md): Foster et al. 2025 (NOD) reported that anti-CD3 mAb
*reduces* the efficacy of antigen-specific (mRNA/peptide) tolerance therapy -- an
unexplained, unmodeled drug-drug antagonism. This module encodes one mechanistic
hypothesis and shows it reproduces the antagonism and predicts a SEQUENCING rule.

Mechanistic hypothesis
----------------------
The autoreactive-effector (E) and antigen-specific regulatory (R) T-cell pools form a
mutual-repression bistable switch (each self-promotes, each represses the other -- the
standard motif for immune cell-fate decisions). Two stable states exist: an AUTOIMMUNE
basin (E high, R low -> beta-cells killed -> progression to stage 3) and a TOLERANT basin
(E low, R high -> beta-cells recover). Late stage 2 sits in the autoimmune basin.

- Antigen-specific tolerance *converts* circulating effectors into antigen-specific Tregs
  ("infectious tolerance"): it moves flux phi*u_tol*E from E into R. It NEEDS effectors
  present to convert, and the converted R must self-stabilize to flip the switch.
- anti-CD3 (teplizumab-class) is *lymphodepleting*: it removes activated effectors (u_a3*E)
  but ALSO depletes Tregs (rho*u_a3*R) and its lymphopenic/cytokine aftermath opposes Treg
  consolidation. By itself it debulks effectors transiently -> the switch reverts to the
  autoimmune basin -> it only DELAYS progression.

=> Giving anti-CD3 FIRST or SIMULTANEOUSLY removes the effector substrate tolerance needs to
   convert AND depletes the nascent Tregs, so the switch fails to flip (the Foster
   antagonism). Giving tolerance FIRST builds and self-stabilizes the Treg pool, flipping the
   switch; a later anti-CD3 course then merely debulks residual effectors -> durable control.

State (units): B beta-cell mass (fraction of healthy, ~ proportional to C-peptide; 0..1),
E autoreactive effector burden (a.u.), R antigen-specific Treg burden (a.u.). Time in YEARS.

Equations  (n=2 Hill; g not needed -- bistability is in the E<->R switch)
    dE/dt = bE + VE * E^n/(K^n+E^n) / (1+(R/Ki)^n)  - dE*E - u_a3(t)*E - u_tol(t)*E
    dR/dt = bR + VR * R^n/(K^n+R^n) / (1+(E/Ki)^n)  - dR*R + phi*u_tol(t)*E - rho*u_a3(t)*R
    dB/dt = rhoB * B*(1-B) - kappa * E * B
"""
import numpy as np
from scipy.integrate import solve_ivp

# ---- operating parameters (illustrative; the antagonism is robust over a region, see P-sweeps) ----
P = dict(
    bE=0.08,    # baseline effector influx
    VE=1.80,    # effector self-activation max rate
    K=0.50,     # half-saturation of self-activation
    Ki=0.50,    # cross-repression half-saturation
    dE=0.80,    # effector loss (1/yr)
    bR=0.04,    # baseline Treg influx
    VR=1.40,    # Treg self-activation max rate (< VE: switch is biased toward autoimmunity)
    dR=0.50,    # Treg loss (1/yr)
    phi=0.40,   # tolerance conversion efficiency (fraction of removed E that becomes R)
    rho=0.90,   # anti-CD3 Treg-depletion factor (relative to its effector-depletion rate)
    rhoB=0.60,  # beta-cell logistic regeneration rate (1/yr)
    kappa=0.40, # per-effector beta-cell kill rate
)
N_HILL = 2

# intervention strengths (effective per-year rates during a short clinical course) / durations
A3_RATE = 18.0      # anti-CD3 effector-depletion rate while dosing (1/yr)
A3_DUR = 14/365.0   # anti-CD3 course length ~14 days (TN10 single course)
TOL_RATE = 12.0     # antigen-specific tolerance conversion rate while dosing (1/yr)
TOL_DUR = 30/365.0  # tolerance course length ~30 days

B_DX = 0.30         # stage-3 diagnosis threshold (fraction of healthy beta-cell mass)
B_CURE = 0.45       # "durable control" threshold at the evaluation horizon
HORIZON = 5.0       # years


def _pulse(t, t0, dur, rate):
    return rate if (t0 <= t < t0 + dur) else 0.0


def rhs(t, y, p, sched):
    B, E, R = (max(v, 0.0) for v in y)
    n = N_HILL
    u_a3 = _pulse(t, sched.get("a3_t0", 1e9), A3_DUR, A3_RATE) if sched.get("a3") else 0.0
    u_tol = _pulse(t, sched.get("tol_t0", 1e9), TOL_DUR, TOL_RATE) if sched.get("tol") else 0.0
    selfE = p["VE"] * E**n / (p["K"]**n + E**n) / (1 + (R / p["Ki"])**n)
    selfR = p["VR"] * R**n / (p["K"]**n + R**n) / (1 + (E / p["Ki"])**n)
    dE = p["bE"] + selfE - p["dE"] * E - u_a3 * E - u_tol * E
    dR = p["bR"] + selfR - p["dR"] * R + p["phi"] * u_tol * E - p["rho"] * u_a3 * R
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * E * B
    return [dB, dE, dR]


def stage2_ic(E0=1.10):
    """Late stage 2: beta-cell mass partly reduced, autoreactive effectors winning, Tregs low.
    E0 is the per-patient severity knob (higher = sicker). Untreated -> diagnosis."""
    return [0.60, E0, 0.12]


def simulate(sched=None, p=None, t_end=8.0, npts=2500, y0=None, E0=1.10):
    p = p or P
    sched = sched or {}
    y0 = y0 if y0 is not None else stage2_ic(E0)
    t_eval = np.linspace(0, t_end, npts)
    return solve_ivp(rhs, (0, t_end), y0, args=(p, sched), t_eval=t_eval,
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.012)


def time_to_dx(sol, b_dx=B_DX):
    B = sol.y[0]
    below = np.where(B < b_dx)[0]
    if below.size == 0:
        return np.inf
    i = below[0]
    if i == 0:
        return 0.0
    t0, t1, b0, b1 = sol.t[i - 1], sol.t[i], B[i - 1], B[i]
    return t0 + (b_dx - b0) * (t1 - t0) / (b1 - b0)


def banked_mass(sol, horizon=HORIZON):
    return float(np.interp(horizon, sol.t, sol.y[0]))


def arms(gap=0.25):
    """Named schedules. All deliver the SAME total drug; only the order/overlap differs.
    gap = inter-drug interval (years) for the two sequential arms."""
    return {
        "untreated":         {},
        "anti-CD3 only":     {"a3": True, "a3_t0": 0.0},
        "tolerance only":    {"tol": True, "tol_t0": 0.0},
        "simultaneous":      {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0},
        "anti-CD3 -> tol":   {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": gap},
        "tol -> anti-CD3":   {"tol": True, "tol_t0": 0.0, "a3": True, "a3_t0": gap},
    }


def cure_fraction(sched, cohort=None, p=None, horizon=HORIZON, b_cure=B_CURE):
    """Fraction of a severity cohort (range of E0) in durable control at the horizon."""
    p = p or P
    cohort = cohort if cohort is not None else np.linspace(0.70, 1.50, 17)
    return float(np.mean([banked_mass(simulate(sched, p, E0=E0), horizon) > b_cure
                          for E0 in cohort]))


def main():
    print("=== single representative patient (E0=1.10): time to stage-3 dx ===")
    print(f"{'arm':18s} {'t_dx(yr)':>9s} {'delay':>7s} {'B@5yr':>7s}")
    base = time_to_dx(simulate(arms()["untreated"]))
    for name, s in arms().items():
        sol = simulate(s)
        tdx = time_to_dx(sol)
        delay = (tdx - base) if (np.isfinite(tdx) and np.isfinite(base)) else np.inf
        tdx_s = f"{tdx:.2f}" if np.isfinite(tdx) else "none"
        dl_s = ("cure" if np.isinf(delay) else f"+{delay:.2f}")
        print(f"{name:18s} {tdx_s:>9s} {dl_s:>7s} {banked_mass(sol):>7.3f}")

    print("\n=== cohort durable-control fraction (Foster antagonism + sequencing rule) ===")
    fr = {name: cure_fraction(s) for name, s in arms().items()}
    for name in arms():
        print(f"  {name:18s} {fr[name]*100:5.1f}%")
    print(f"\n  anti-CD3 antagonizes tolerance (simultaneous - tol-only): "
          f"{(fr['simultaneous']-fr['tolerance only'])*100:+.1f} pts")
    print(f"  worst order (anti-CD3->tol) - tol-only:                    "
          f"{(fr['anti-CD3 -> tol']-fr['tolerance only'])*100:+.1f} pts")
    print(f"  tolerance-first rescue (tol->anti-CD3) - simultaneous:     "
          f"{(fr['tol -> anti-CD3']-fr['simultaneous'])*100:+.1f} pts")


if __name__ == "__main__":
    main()
