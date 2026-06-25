#!/usr/bin/env python3
"""P4 (v4) — the reconciling model: adds the ACUTE-DELETION channel so the same model reproduces
BOTH the antagonism (Foster 2025 mRNA; Stewart 2020 microparticle) AND the synergy (Salmonella:
Mbongue 2019/Cobb 2021-24; L. lactis: Sassi 2023) of anti-CD3 + antigen-specific tolerance.

Verified-biology basis (deep-research + Semantic Scholar retrieval):
  - Tolerance bottleneck is PERIPHERAL (Feuerer 2007/09; Mhanna/Tang 2021), effectors RESIST
    suppression (D'Alise 2008) -> `res`.
  - anti-CD3 = durable-but-waning, beneficial effector hyporesponsiveness (Long 2016; Lledo-Delgado
    2024) -> state X.
  - NEW mechanism reconciling the heterogeneous combination data: antigen-specific tolerance first
    ACTIVATES the target autoreactive effectors (engages them, antigen presentation) into a converting
    pool A en route to becoming Tregs; anti-CD3 PREFERENTIALLY deletes activated/cycling cells, so if
    it hits A before conversion completes, it ABORTS the conversion -> ANTAGONISM. Treg-EXPANSION
    platforms (TGF-b/IL-10/IL-2-like, `psi`) raise Tregs INDEPENDENTLY of A, so they are NOT undercut
    by anti-CD3 and instead COMBINE with the X window -> SYNERGY.

=> a single regime map over (platform independence psi, anti-CD3 timing) reproduces antagonism for
   conversion-dependent platforms (low psi) and synergy for expansion platforms (high psi), and makes
   the acute-vs-durable timescale falsifiable: does anti-CD3 delete antigen-activated autoreactive
   clones before they convert?

State (years): B beta-cell, E effectors, A antigen-activated converting cells, R Tregs,
               X anti-CD3 hyporesponsiveness.
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    bE=0.08, VE=1.80, K=0.50, Ki=0.50, dE=0.80,
    bR=0.05, VR=1.40, dR=0.50,
    res=1.30,         # effector resistance to suppression (NOD Tconv)
    c=0.95,           # rate tolerance ACTIVATES convertible effectors into A (per dose-unit)
    conv=3.0,         # A -> Treg conversion rate (1/yr)
    dA=1.2,           # decay/reversion of un-converted activated cells (1/yr)
    delA=2.2,         # anti-CD3 PREFERENTIAL deletion of activated A (>> its effect on resting E)
    psi=0.0,          # substrate-INDEPENDENT Treg expansion (PLATFORM axis): 0=pure antigen, high=Treg-boost
    Rmax=2.2,
    phi=0.80, rho=0.90, rhoB=0.60, kappa=0.40,
    epsX=0.9, dX=1.10,
)
N_HILL = 2
A3_RATE = 22.0
A3_DUR = 14/365.0
TOL_RATE = 12.0
TOL_DUR = 30/365.0
B_DX = 0.30
B_CURE = 0.45
HORIZON = 5.0


def _pulse(t, t0, dur, rate):
    return rate if (t0 <= t < t0 + dur) else 0.0


def rhs(t, y, p, sched):
    B, E, A, R, X = (max(v, 0.0) for v in y)
    X = min(X, 1.0)
    n = N_HILL
    u_a3 = _pulse(t, sched.get("a3_t0", 1e9), A3_DUR, A3_RATE) if sched.get("a3") else 0.0
    u_tol = _pulse(t, sched.get("tol_t0", 1e9), TOL_DUR, TOL_RATE) if sched.get("tol") else 0.0
    psi = sched.get("psi", p["psi"])
    selfE = p["VE"] * E**n / (p["K"]**n + E**n) / (1 + (R / (p["Ki"] * p["res"]))**n)
    selfR = p["VR"] * R**n / (p["K"]**n + R**n) / (1 + (E / p["Ki"])**n)
    activate = u_tol * p["c"] * E                       # tolerance activates effectors into A
    convert = p["conv"] * A                             # A -> Treg
    expand = psi * u_tol * R * (1 - R / p["Rmax"])      # substrate-INDEPENDENT Treg expansion (platform)
    dE = p["bE"] + (1 - X) * selfE - p["dE"] * E - u_a3 * E - activate
    dA = activate - convert - p["delA"] * u_a3 * A - p["dA"] * A   # anti-CD3 PREFERENTIALLY deletes A
    dR = p["bR"] + selfR - p["dR"] * R + p["phi"] * convert + expand - p["rho"] * u_a3 * R
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * (1 - X) * E * B
    dX = p["epsX"] * u_a3 * (1 - X) - p["dX"] * X
    return [dB, dE, dA, dR, dX]


def stage2_ic(E0=1.10, p=None):
    p = p or P
    return [0.60, E0, 0.0, p["bR"] / p["dR"], 0.0]


def simulate(sched=None, p=None, t_end=8.0, npts=2500, y0=None, E0=1.10):
    p = p or P
    sched = dict(sched or {})
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


def arms(psi, gap=0.25):
    return {
        "untreated":       {},
        "anti-CD3 only":   {"a3": True, "a3_t0": 0.0},
        "tolerance only":  {"tol": True, "tol_t0": 0.0, "psi": psi},
        "simultaneous":    {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0, "psi": psi},
        "anti-CD3 -> tol": {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": gap, "psi": psi},
        "tol -> anti-CD3": {"tol": True, "tol_t0": 0.0, "psi": psi, "a3": True, "a3_t0": gap},
    }


def cure_fraction(sched, cohort=None, p=None, horizon=HORIZON, b_cure=B_CURE):
    p = p or P
    cohort = cohort if cohort is not None else np.linspace(0.70, 1.50, 17)
    return float(np.mean([banked_mass(simulate(sched, p, E0=E0), horizon) > b_cure for E0 in cohort]))


def main():
    base = time_to_dx(simulate(arms(0.0)["untreated"]))
    print(f"untreated median t_dx = {base:.2f} yr\n")
    print(f"{'platform psi':>12} {'tol':>5} {'a3':>5} {'sim':>5} {'a3>t':>6} {'t>a3':>6}"
          f" {'bestcombo-bestmono':>19} {'regime':>11}")
    for psi in [0.0, 0.4, 0.8, 1.2, 1.8, 2.6]:
        A = arms(psi)
        fr = {n: cure_fraction(s) for n, s in A.items()}
        bc = max(fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"])
        bm = max(fr["tolerance only"], fr["anti-CD3 only"])
        eff = bc - bm
        reg = "SYNERGY" if eff > 0.05 else ("ANTAGONISM" if eff < -0.05 else "neutral")
        print(f"{psi:>12.1f} {fr['tolerance only']*100:>4.0f}% {fr['anti-CD3 only']*100:>4.0f}%"
              f" {fr['simultaneous']*100:>4.0f}% {fr['anti-CD3 -> tol']*100:>5.0f}% {fr['tol -> anti-CD3']*100:>5.0f}%"
              f" {eff*100:>+14.0f} pts {reg:>11}")
    print("\nFoster 2025 (mRNA) / Stewart 2020 (microparticle) ~ low psi (ANTAGONISM);")
    print("Salmonella (Cobb/Mbongue) / L. lactis (Sassi 2023) ~ high psi (SYNERGY).")


if __name__ == "__main__":
    main()
