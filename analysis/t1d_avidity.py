#!/usr/bin/env python3
"""P5 (avidity-resolved) — does the Khadra/Pietropaolo avidity framework reproduce the Foster 2025
antagonism once we add the two therapies it never modeled, including the strongest candidate
mechanisms? Definitive test of whether the antagonism is sub-continuum (needs discrete-clonal /
stochastic resolution) or capturable by avidity-resolved continuum dynamics.

Framework: Jaberi-Douraki/Pietropaolo/Khadra (J Theor Biol 2015, PMC4567915) — Teff & Treg
distributed over an avidity axis k; T1D onset set by Treg-vs-Teff dominance at SPECIFIC high avidities.
Therapy asymmetry (our extension): tolerance is AVIDITY-TARGETED (peaked g_tol(k), high avidity);
anti-CD3 is AVIDITY-NON-SELECTIVE (flat over k) + durable hyporesponsiveness X.

Two candidate antagonism mechanisms, both tested here:
  (1) ACUTE DELETION (state A): tolerance first ACTIVATES targeted high-avidity effectors into a
      converting pool A_i en route to Treg; anti-CD3 PREFERENTIALLY deletes cycling A (rate delA).
      If anti-CD3 hits A before conversion completes -> aborts it -> candidate antagonism.
  (2) WEAK durable window (low epsX): where the v2 lumped model showed the antagonism re-appear.

State: B, X, then E_i (effectors), A_i (activated/converting), R_i (Tregs) over avidity. 4 GB cap.
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    bE=0.08, VE=1.80, Khill=0.50, Ki=0.50, dE=0.80,
    bR=0.05, VR=1.40, dR=0.50,
    conv=0.45,                   # tolerance activation rate E->A (the strength knob; marginal band)
    convr=4.0, dA_decay=0.8,     # A->R conversion rate / A reversion
    delA=0.0,                    # anti-CD3 PREFERENTIAL deletion of activated A (0=off; mechanism 1)
    phi=0.80, rho=0.90,
    rhoB=0.60, kappa=0.55,
    epsX=0.9, dX=1.10,           # anti-CD3 durable hyporesponsiveness imprint (mechanism-2 knob) + waning
    k_tol=1.6, w_tol=0.35, a_escape=1.2,
)
N_HILL = 2
A3_RATE = 22.0;  A3_DUR = 14/365.0
TOL_RATE = 12.0; TOL_DUR = 30/365.0
B_CURE = 0.45; HORIZON = 5.0


def grid(N):
    if N == 1:
        o = np.array([1.0]); return o, o.copy(), o.copy(), o.copy()
    k = np.linspace(0.30, 2.00, N)
    pE = np.exp(-P["a_escape"] * (k - k[0]));            pE /= pE.mean()
    gtol = np.exp(-((k - P["k_tol"])**2) / (2*P["w_tol"]**2)); gtol /= gtol.mean()
    wkill = k / k.mean()
    return k, pE, gtol, wkill


def _pulse(t, t0, dur, rate):
    return rate if (t0 <= t < t0 + dur) else 0.0


def rhs(t, y, p, sched, G):
    k, pE, gtol, wkill = G
    N = k.size
    B = max(y[0], 0.0); X = min(max(y[1], 0.0), 1.0)
    E = np.maximum(y[2:2+N], 0.0); A = np.maximum(y[2+N:2+2*N], 0.0); R = np.maximum(y[2+2*N:2+3*N], 0.0)
    n = N_HILL
    u_a3 = _pulse(t, sched.get("a3_t0", 1e9), A3_DUR, A3_RATE) if sched.get("a3") else 0.0
    u_tol = _pulse(t, sched.get("tol_t0", 1e9), TOL_DUR, TOL_RATE) if sched.get("tol") else 0.0
    selfE = p["VE"] * E**n / (p["Khill"]**n + E**n) / (1 + (R / p["Ki"])**n)
    selfR = p["VR"] * R**n / (p["Khill"]**n + R**n) / (1 + (E / p["Ki"])**n)
    activate = p["conv"] * u_tol * gtol * E
    convflux = p["convr"] * A
    dE = p["bE"]*pE + (1 - X)*selfE - p["dE"]*E - u_a3*E - activate
    dA = activate - convflux - p["delA"]*u_a3*A - p["dA_decay"]*A      # anti-CD3 preferentially deletes A
    dR = p["bR"] + selfR - p["dR"]*R + p["phi"]*convflux - p["rho"]*u_a3*R
    kill = p["kappa"] * (1 - X) * B * np.mean(wkill * E)
    dB = p["rhoB"] * B * (1 - B) - kill
    dX = p["epsX"] * u_a3 * (1 - X) - p["dX"] * X
    return np.concatenate(([dB, dX], dE, dA, dR))


def stage2_ic(N, G, E0=1.10):
    k, pE, gtol, wkill = G
    E = E0 * pE; A = np.zeros(N); R = (P["bR"]/P["dR"]) * np.ones(N) * 0.3
    return np.concatenate(([0.60, 0.0], E, A, R))


def simulate(sched, N, p=None, E0=1.10, t_end=6.0, npts=1000):
    p = p or P; G = grid(N); sched = dict(sched or {})
    y0 = stage2_ic(N, G, E0)
    return solve_ivp(rhs, (0, t_end), y0, args=(p, sched, G), t_eval=np.linspace(0, t_end, npts),
                     method="LSODA", rtol=1e-7, atol=1e-9, max_step=0.02)


def banked(sol):
    return float(np.interp(HORIZON, sol.t, sol.y[0]))


def arms(gap=0.25):
    return {
        "untreated":       {},
        "anti-CD3 only":   {"a3": True, "a3_t0": 0.0},
        "tolerance only":  {"tol": True, "tol_t0": 0.0},
        "simultaneous":    {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0},
        "anti-CD3 -> tol": {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": gap},
        "tol -> anti-CD3": {"tol": True, "tol_t0": 0.0, "a3": True, "a3_t0": gap},
    }


def cure_fraction(sched, N, p=None, cohort=None):
    cohort = cohort if cohort is not None else np.linspace(0.70, 1.50, 9)
    return float(np.mean([banked(simulate(sched, N, p=p, E0=E0)) > B_CURE for E0 in cohort]))


def combo_effect(p, N=40):
    A = arms()
    fr = {nm: cure_fraction(s, N, p=p) for nm, s in A.items()}
    bc = max(fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"])
    bm = max(fr["tolerance only"], fr["anti-CD3 only"])
    return bc - bm, fr


def reg(eff):
    return "ANTAG" if eff < -0.05 else ("SYN" if eff > 0.05 else "neut")


def scan_acute():
    print("== EXPERIMENT 1: ACUTE DELETION in avidity space (anti-CD3 deletes converting clones A) ==")
    print("   does preferential deletion of the just-activated high-avidity converting pool flip it?")
    print(f"   {'conv':>5} {'delA':>5} {'tol':>4} {'a3':>4} {'sim':>4} {'a3>t':>5} {'t>a3':>5} {'combo-mono':>10} {'regime':>6}")
    found = False
    for conv in [0.35, 0.45, 0.55]:
        for delA in [0.0, 3.0, 8.0, 20.0, 50.0]:
            p = dict(P); p["conv"] = conv; p["delA"] = delA
            eff, fr = combo_effect(p)
            if eff < -0.05: found = True
            print(f"   {conv:5.2f} {delA:5.1f} {fr['tolerance only']*100:3.0f}% {fr['anti-CD3 only']*100:3.0f}% "
                  f"{fr['simultaneous']*100:3.0f}% {fr['anti-CD3 -> tol']*100:4.0f}% {fr['tol -> anti-CD3']*100:4.0f}% "
                  f"{eff*100:+9.0f} {reg(eff):>6}")
    print(f"   -> antagonism found via acute deletion? {'YES' if found else 'NO'}")


def scan_X():
    print("\n== EXPERIMENT 2: WEAK durable window (sweep epsX; v2 showed antagonism re-appears low) ==")
    print(f"   {'conv':>5} {'epsX':>5} {'tol':>4} {'a3':>4} {'sim':>4} {'a3>t':>5} {'t>a3':>5} {'combo-mono':>10} {'regime':>6}")
    found = False
    for conv in [0.45, 0.55]:
        for epsX in [0.05, 0.20, 0.45, 0.90, 1.40]:
            p = dict(P); p["conv"] = conv; p["epsX"] = epsX
            eff, fr = combo_effect(p)
            if eff < -0.05: found = True
            print(f"   {conv:5.2f} {epsX:5.2f} {fr['tolerance only']*100:3.0f}% {fr['anti-CD3 only']*100:3.0f}% "
                  f"{fr['simultaneous']*100:3.0f}% {fr['anti-CD3 -> tol']*100:4.0f}% {fr['tol -> anti-CD3']*100:4.0f}% "
                  f"{eff*100:+9.0f} {reg(eff):>6}")
    print(f"   -> antagonism found via weak window? {'YES' if found else 'NO'}")


def main():
    print("Definitive test: can the avidity-resolved CONTINUUM reproduce the Foster antagonism?\n")
    scan_acute()
    scan_X()
    print("\nIf both NO across the marginal band, the antagonism is sub-continuum -> demands discrete-")
    print("clonal / stochastic resolution (the deterministic<->stochastic boundary), not avidity alone.")


if __name__ == "__main__":
    main()
