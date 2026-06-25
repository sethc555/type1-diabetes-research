#!/usr/bin/env python3
"""Teplizumab RESPONDER vs NON-RESPONDER — the field's #1 open question, on our exhaustion model.

Mechanism (documented biology): teplizumab's durable effect is an induced CD8 hyporesponsiveness /
partial-exhaustion program (Long 2016; Lledo-Delgado) that wanes. A RESPONDER is a patient in whom the
autoreactive effectors are driven into durable exhaustion and DO NOT come back; a NON-RESPONDER either
exhausts weakly/transiently OR has a renewable stem-like source (TSCM; Dufort 2026) that REFILLS the
attack once exhaustion wanes. This predicts the two real biomarkers:
  - baseline exhausted-CD8 signature -> RESPONDER (Wiedeman 2019): start already partly exhausted (high X0).
  - high TSCM -> NON-RESPONDER (Dufort 2026): high renewable effector source `r_tscm`.

State (per patient): E autoreactive effectors (bistable self-activation), X exhaustion imprint, B beta.
Teplizumab MONOTHERAPY (the approved use). Deterministic cohort; patients differ in (r_tscm, X0, severity).
4 GB cap (trivial).
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    bE=0.04, VE=1.70, K=0.50, dE=0.70,   # effector influx / bistable self-activation / death
    nH=4.0,                               # effector-switch Hill cooperativity (AS1 robustness knob; n>=2 bistable, n=1 graded/non-bistable)
    sx=5.5,                               # exhaustion suppresses effector self-activation by 1/(1+sx*Xe)
    epsX=40.0, dX=0.46,                   # teplizumab exhaustion: builds to ~0.8 during the 14-day course,
                                          #   wanes with ~18-mo half-life (Lledo-Delgado); dX=durability (lower=more durable)
    rhoB=0.60, kappa=0.95, kx=3.0,        # beta regen / per-effector kill / exhaustion-reduces-killing
)
TEP_RATE = 16.0; TEP_DUR = 14/365.0
B_DX = 0.30; B_CURE = 0.45; HORIZON = 5.0


def rhs(t, y, p, tep):
    E, X, B = (max(v, 0.0) for v in y)
    X0 = p.get("X0", 0.0)
    Xe = min(max(X, X0), 1.0)                                          # baseline exhaustion = persistent floor (Wiedeman trait)
    u = TEP_RATE if (tep and 0 <= t < TEP_DUR) else 0.0
    nH = p["nH"]
    selfE = p["VE"] * E**nH / (p["K"]**nH + E**nH) / (1.0 + p["sx"] * Xe)  # Hill cooperativity nH (AS1 knob)
    dE = p["bE"] + p["r_tscm"] + selfE - p["dE"] * E - u * E           # r_tscm = TSCM renewal (exhaustion-resistant)
    dX = p["epsX"] * u * (1 - X) - p["dX"] * (X - X0)                  # teplizumab transient decays toward the X0 floor
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * E * B / (1.0 + p["kx"] * Xe)
    return [dE, dX, dB]


def simulate(tep, p, E0=1.0):
    y0 = [E0, p.get("X0", 0.0), 0.60]
    return solve_ivp(rhs, (0, 8.0), y0, args=(p, tep), t_eval=np.linspace(0, 8, 1400),
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.02)


def responds(p, E0=1.0):
    B = simulate(True, p, E0).y[2]
    return float(np.interp(HORIZON, np.linspace(0, 8, 1400), B)) > B_CURE


def patient(r_tscm, X0, base=None):
    p = dict(base or P); p["r_tscm"] = r_tscm; p["X0"] = X0; return p


def main():
    # calibration: untreated progresses; a baseline patient on teplizumab
    base = patient(0.10, 0.0)
    untr = float(np.interp(HORIZON, np.linspace(0, 8, 1400), simulate(False, base).y[2]))
    print(f"calibration: untreated B@5yr = {untr:.2f} (progresses, <{B_CURE}); teplizumab is monotherapy.\n")

    print("=" * 70)
    print("RESPONSE MAP — responder(R)/non-responder(.) over baseline-exhaustion X0 x TSCM-renewal r_tscm")
    print("=" * 70)
    X0s = [0.00, 0.10, 0.20, 0.30, 0.40]
    rts = [0.02, 0.06, 0.10, 0.15, 0.22]
    print(f"{'X0 \\ r_tscm':>12} " + " ".join(f"{r:>5.2f}" for r in rts) + "   (TSCM ->)")
    grid = []
    for X0 in X0s:
        row = [responds(patient(r, X0)) for r in rts]
        grid.append(row)
        print(f"{X0:>12.2f} " + " ".join(f"{'  R  ' if v else '  .  '}" for v in row))
    grid = np.array(grid)
    print("  (^ baseline exhaustion)")

    # response rate over a realistic cohort (random in the same ranges + severity spread)
    rng = np.random.default_rng(0)
    N = 240
    resp = []
    for _ in range(N):
        r = rng.uniform(0.02, 0.32); x0 = rng.uniform(0.0, 0.40); e0 = rng.uniform(0.8, 1.3)
        resp.append((r, x0, responds(patient(r, x0), E0=e0)))
    resp = np.array(resp)
    rate = resp[:, 2].mean()
    # biomarker directions: mean predictor value in responders vs non-responders
    R = resp[resp[:, 2] == 1]; NR = resp[resp[:, 2] == 0]
    print(f"\nCOHORT (n={N}): response rate = {rate*100:.0f}%  (teplizumab is ~partial -> realistic if ~30-60%)")
    print(f"  baseline exhaustion X0 : responders {R[:,1].mean():.2f}  vs  non-responders {NR[:,1].mean():.2f}"
          f"   -> {'HIGHER in responders (matches Wiedeman)' if R[:,1].mean()>NR[:,1].mean() else 'no'}")
    print(f"  TSCM renewal r_tscm    : responders {R[:,0].mean():.2f}  vs  non-responders {NR[:,0].mean():.2f}"
          f"   -> {'LOWER in responders (matches Dufort)' if R[:,0].mean()<NR[:,0].mean() else 'no'}")

    # actionable lever: convert non-responders by (a) more durable exhaustion (lower dX) or (b) blunting TSCM
    print("\n" + "=" * 70)
    print("ACTIONABLE — can we CONVERT non-responders? take the non-responder corner (high TSCM, low X0)")
    print("=" * 70)
    nr = patient(0.22, 0.03)
    print(f"  non-responder baseline (high TSCM, low exhaustion): responds? {responds(nr)}")
    durable = dict(nr); durable["dX"] = 0.25          # make the exhaustion ~2x more durable
    print(f"  + more DURABLE exhaustion (dX 0.46->0.25, e.g. a 2ND teplizumab course before it wanes): {responds(durable)}")
    bluntts = dict(nr); bluntts["r_tscm"] = 0.06      # blunt the TSCM renewal source
    print(f"  + BLUNT the TSCM renewal source (r_tscm 0.22->0.06): {responds(bluntts)}")
    print("\n-> model says non-response is the exhaustion-durability-vs-renewal balance; both levers are")
    print("   testable, biomarker-stratified predictions (treat high-TSCM/low-exhaustion patients differently).")


if __name__ == "__main__":
    main()
