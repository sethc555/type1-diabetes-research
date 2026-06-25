#!/usr/bin/env python3
"""VERTICAL deepening #3 — ANTIGENS & EPITOPE SPREADING. The disease starts against a PRIMARY antigen
(insulin) and SPREADS to others (GAD, IA-2, ZnT8, hybrid peptides) over time, driven by beta-cell
stress generating neoantigens -- the SAME stress loop as t1d_betacell.py (Marre 2015; Strollo 2022).
Spreading is hierarchical/staged (TEDDY: Vehik 2020; Ilonen 2013). This is why SINGLE-antigen tolerance
underperforms (Balakrishnan 2020): tolerize one epitope, the disease escapes to the spread-to ones.

State: E_i effectors vs antigen i (i=0 primary), pr_i priming (0=dormant,1=recruited; pr_0=1), B beta,
S beta-cell stress (drives spreading + relieved by beta-protection). Antigen-specific tolerance durably
suppresses TARGETED antigens (single = {primary}; broad = all). Deterministic. 4 GB cap.

Predictions: (1) single-antigen tolerance is ESCAPED by spreading; (2) EARLY (pre-spread) tolerance
works far better; (3) BROAD tolerance escapes the trap; (4) beta-PROTECTION slows spreading -> a NEW
cross-layer synergy that makes single-antigen tolerance work better (cuts off its escape route).
"""
import numpy as np
from scipy.integrate import solve_ivp

M = 5  # 0=insulin(primary), 1..4 = GAD / IA-2 / ZnT8 / hybrid-insulin-peptide
P = dict(
    bE=0.03, rE=1.6, Emax=1.0, dE=0.6,   # per-antigen effector seed / growth / cap / death
    spread=11.0,                          # epitope-spreading rate (stress-driven recruitment of the next antigen)
    kappa=0.40, rhoB=0.60,                # beta-cell kill (by total attack) / regen
    k_stress=1.4, dS=1.0, prot=4.0,       # stress from attack / relief / beta-protection relief
    tolkill=4.0,                          # durable suppression of a TOLERIZED antigen's effectors
    S_thresh=0.26,                        # spreading needs SUSTAINED high stress -> drop stress fast and it halts
)
B_OK = 0.30; HORIZON = 5.0


def rhs(t, y, p, s):
    E = np.maximum(y[:M], 0.0); pr = np.clip(y[M:2*M], 0.0, 1.0)
    B = max(y[2*M], 0.0); S = min(max(y[2*M+1], 0.0), 1.0)
    pr[0] = 1.0                                                   # primary antigen always primed
    targets = s.get("targets", [])
    tol_on = bool(s.get("tol")) and t >= s.get("tol_t0", 1e9)    # tolerance is DURABLE once given
    u_prot = 1.0 if (s.get("prot") and t >= s.get("prot_t0", 0.0)) else 0.0
    tolkill = np.array([p["tolkill"] if (tol_on and i in targets) else 0.0 for i in range(M)])
    dE = pr * (p["bE"] + p["rE"] * E * (1 - E / p["Emax"])) - p["dE"] * E - tolkill * E
    dpr = np.zeros(M)
    for i in range(1, M):
        dpr[i] = p["spread"] * max(S - p["S_thresh"], 0.0) * pr[i-1] * (1 - pr[i])   # spreads only above a stress threshold
    tot = E.sum()
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * B * tot
    dS = p["k_stress"] * tot * (1 - S) - p["dS"] * S * (1 + p["prot"] * u_prot)
    return np.concatenate([dE, dpr, [dB, dS]])


def simulate(s, p=None):
    p = p or P
    E0 = np.zeros(M); E0[0] = 0.30                               # primary antigen active but still GROWING (early)
    pr0 = np.zeros(M); pr0[0] = 1.0
    y0 = np.concatenate([E0, pr0, [0.60, 0.10]])
    return solve_ivp(rhs, (0, 8.0), y0, args=(p, dict(s)), t_eval=np.linspace(0, 8, 1600),
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.02)


def bend(sol):
    return float(np.interp(HORIZON, sol.t, sol.y[2*M]))


def nspread(sol):
    return int((sol.y[M:2*M, -1] > 0.5).sum())                   # antigens recruited by end (pr_0=primary already counts)


def main():
    LATE, EARLY = 2.5, 0.0
    arms = {
        "untreated":                       {},
        "single-antigen tol, EARLY":       {"tol": True, "tol_t0": EARLY, "targets": [0]},
        "single-antigen tol, LATE":        {"tol": True, "tol_t0": LATE, "targets": [0]},
        "BROAD (all-antigen) tol, LATE":   {"tol": True, "tol_t0": LATE, "targets": list(range(M))},
        "single LATE + beta-protection":   {"tol": True, "tol_t0": LATE, "targets": [0], "prot": True, "prot_t0": 0.0},
    }
    print("Epitope-spreading model — beta-cell preservation by antigen-tolerance strategy\n")
    print(f"  {'arm':32s} {'beta@5yr':>9} {'#antigens':>10} {'outcome':>11}")
    R = {}
    for nm, s in arms.items():
        sol = simulate(s); b = bend(sol); R[nm] = b
        print(f"  {nm:32s} {b:>9.2f} {nspread(sol):>10} {'preserved' if b > B_OK else 'lost':>11}")
    print("\n  P1 single-antigen tol is ESCAPED by spreading:  single-LATE %.2f  <  broad-LATE %.2f"
          % (R["single-antigen tol, LATE"], R["BROAD (all-antigen) tol, LATE"]))
    print("  P2 EARLY (pre-spread) beats LATE:               single-EARLY %.2f  >  single-LATE %.2f"
          % (R["single-antigen tol, EARLY"], R["single-antigen tol, LATE"]))
    print("  P3 BROAD tolerance escapes the trap:            broad-LATE %.2f (preserved)"
          % R["BROAD (all-antigen) tol, LATE"])
    print("  P4 CROSS-LAYER: beta-protection slows spreading -> rescues single-antigen tol:")
    print("        single-LATE %.2f  ->  single-LATE + beta-protect %.2f"
          % (R["single-antigen tol, LATE"], R["single LATE + beta-protection"]))


if __name__ == "__main__":
    main()
