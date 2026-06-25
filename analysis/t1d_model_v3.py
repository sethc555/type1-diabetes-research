#!/usr/bin/env python3
"""P3-revision (v3) — model rebuilt on the VERIFIED biology (deep-research + Semantic Scholar).

Corrections over v2, each grounded in retrieved primary literature:

  (A) PERIPHERAL, not thymic, tolerance bottleneck. NOD thymic Treg generation is normal-to-enhanced
      with intact suppression (Feuerer 2007/2009 PNAS; D'Alise 2008); the corrigible deficit is
      peripheral activated/memory-Treg CLONAL EXPANSION, restored by IL-2 (Mhanna/Tang 2021 Diabetes).
      So the cap on tolerance is PERIPHERAL conversion/expansion efficiency, not a thymic precursor pool.
      (v2's `sig_thy`/thymic-precursor framing is dropped; the reviewer's thymic mechanism is NOD-contradicted,
      though his clinical points -- tolerance impaired, monotherapy weak -- stand.)

  (B) EFFECTOR RESISTANCE to suppression. NOD Tconv are intrinsically less suppressible (D'Alise 2008):
      parameter `res` raises the Treg level needed to restrain effectors.

  (C) anti-CD3 = durable-but-WANING, reversible effector hyporesponsiveness (state X): a partial-CD8-
      exhaustion program that prevents expansion of autoreactive CD8 memory (Long 2016 Sci Immunol;
      Lledo-Delgado 2024 JCI: persists ~18 mo, ~36% diabetes-free at 5 yr) and is breakable (rapamycin;
      Baeyens 2009). X builds while dosed, decays slowly, scales effector expansion+killing by (1-X).

  (D) THE TWO-CHANNEL TOLERANCE PLATFORM -- the key to reconciling the heterogeneous combination data:
      antigen-specific tolerance acts via (i) SUBSTRATE-DEPENDENT conversion of effectors to Tregs
      (`phi*u_tol*c*E`) -- which anti-CD3 UNDERCUTS by depleting E (-> Foster 2025 mRNA antagonism;
      Stewart 2020 microparticle no-synergy) -- and (ii) SUBSTRATE-INDEPENDENT peripheral Treg
      EXPANSION (`psi*u_tol*R*(1-R/Rmax)`, the TGF-beta/IL-10/IL-2-like boost) -- which anti-CD3 does
      NOT undercut, and which COMBINES with the X window (-> Salmonella & L. lactis synergy: Mbongue
      2019/Cobb 2021-24; Sassi 2023). The platform's `psi` (independence) is the regime axis.

The model's contribution is a REGIME MAP over (platform independence psi, anti-CD3 strength): it
predicts the combination ANTAGONIZES for pure-antigen platforms (low psi) and SYNERGIZES for
Treg-expansion platforms (high psi) -- reconciling the real positive AND negative studies, and
giving a design rule. Outcome is reported as found; nothing is assumed to work.

State (years): B beta-cell mass, E autoreactive effectors, R Tregs, X anti-CD3 hyporesponsiveness.
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    bE=0.08, VE=1.80, K=0.50, Ki=0.50, dE=0.80,
    bR=0.05, VR=1.40, dR=0.50,            # bR = normal peripheral Treg homeostatic source
    res=1.45,                              # (B) effector resistance to suppression (NOD Tconv)
    c=0.55,                                # (D-i) substrate-dependent conversion efficiency
    psi=0.0,                               # (D-ii) substrate-INDEPENDENT Treg-expansion boost (PLATFORM axis)
    Rmax=2.2,                              # Treg expansion ceiling
    phi=0.40, rho=0.90, rhoB=0.60, kappa=0.40,
    epsX=0.9, dX=1.10,                     # (C) anti-CD3 hyporesponsiveness imprint + waning
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
    B, E, R, X = (max(v, 0.0) for v in y)
    X = min(X, 1.0)
    n = N_HILL
    u_a3 = _pulse(t, sched.get("a3_t0", 1e9), A3_DUR, A3_RATE) if sched.get("a3") else 0.0
    u_tol = _pulse(t, sched.get("tol_t0", 1e9), TOL_DUR, TOL_RATE) if sched.get("tol") else 0.0
    psi = sched.get("psi", p["psi"])       # platform independence can be set per-scenario
    c = p["c"]
    selfE = p["VE"] * E**n / (p["K"]**n + E**n) / (1 + (R / (p["Ki"] * p["res"]))**n)
    selfR = p["VR"] * R**n / (p["K"]**n + R**n) / (1 + (E / p["Ki"])**n)
    conv = p["phi"] * u_tol * c * E                      # substrate-dependent (anti-CD3 undercuts via E)
    expand = psi * u_tol * R * (1 - R / p["Rmax"])       # substrate-INDEPENDENT peripheral Treg expansion
    dE = p["bE"] + (1 - X) * selfE - p["dE"] * E - u_a3 * E - u_tol * c * E
    dR = p["bR"] + selfR - p["dR"] * R + conv + expand - p["rho"] * u_a3 * R
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * (1 - X) * E * B
    dX = p["epsX"] * u_a3 * (1 - X) - p["dX"] * X
    return [dB, dE, dR, dX]


def stage2_ic(E0=1.10, p=None):
    p = p or P
    R0 = (p["bR"]) / p["dR"]
    return [0.60, E0, R0, 0.0]


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
    """psi sets the tolerance platform's substrate-independent Treg-expansion (the platform type)."""
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


def combo_effect(psi, p=None):
    """Synergy(+)/antagonism(-): best combination minus best monotherapy, at platform independence psi."""
    A = arms(psi)
    fr = {n: cure_fraction(s, p=p) for n, s in A.items()}
    best_combo = max(fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"])
    best_mono = max(fr["tolerance only"], fr["anti-CD3 only"])
    return best_combo - best_mono, fr


def main():
    base = time_to_dx(simulate(arms(0.0)["untreated"]))
    print(f"untreated median t_dx = {base:.2f} yr")
    print("\nThe combination outcome depends on the tolerance PLATFORM (psi = substrate-independent")
    print("Treg-expansion). Low psi = pure-antigen (mRNA/microparticle); high psi = Treg-boosting")
    print("(Salmonella/L. lactis secreting TGF-b/IL-10).\n")
    print(f"{'platform psi':>12} {'tol-only':>9} {'a3-only':>8} {'best combo':>11} {'synergy(+)/antag(-)':>20}")
    for psi in [0.0, 0.5, 1.0, 1.5, 2.0, 2.6]:
        eff, fr = combo_effect(psi)
        tag = "SYNERGY" if eff > 0.05 else ("ANTAGONISM" if eff < -0.05 else "neutral")
        print(f"{psi:>12.1f} {fr['tolerance only']*100:>8.0f}% {fr['anti-CD3 only']*100:>7.0f}% "
              f"{max(fr['simultaneous'],fr['anti-CD3 -> tol'],fr['tol -> anti-CD3'])*100:>10.0f}% "
              f"{eff*100:>+12.0f} pts  {tag}")
    print("\nLiterature placement: Foster 2025 (mRNA) & Stewart 2020 (microparticle) ~ low psi (antagonism);")
    print("Salmonella (Cobb/Mbongue) & L. lactis (Sassi 2023) ~ high psi (synergy).")


if __name__ == "__main__":
    main()
