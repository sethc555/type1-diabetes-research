#!/usr/bin/env python3
"""VERTICAL deepening — the explicit autoreactive-CD8 EXHAUSTION HIERARCHY under T1D.

Replaces the responder model's lumped exhaustion `X` + TSCM-renewal `r_tscm` with the real ladder
(grounded in T1D-specific data):
  P  stem-like PROGENITOR (TCF1+, self-renewing) -- the refill engine; autoreactive CD8 memory-stem
     cells are detected in T1D patients (Vignali 2018). Patient pool size P0 = the responder axis.
  E  EFFECTOR -- differentiates from P, kills beta cells.
  X  terminally-EXHAUSTED (TOX+/LAG3+) -- driven from E by chronic antigen + anti-CD3; RESTRAINED,
     low-killing, PROTECTIVE (intra-islet autoreactive CD8 are held by an exhaustion program
     maintained by LAG3 -- Grebinoski 2022; exhaustion predicts teplizumab response -- Long 2016).
  H  exhaustion-program intensity (the durable, ~18-mo teplizumab imprint that drives E->X).

Interventions:
  teplizumab (anti-CD3): boosts E->X exhaustion (therapeutic — restrains the attack).
  checkpoint blockade (anti-PD-1/LAG3): REVERSES exhaustion (boosts X->E reversion) — the CANCER/HIV
     move. In autoimmunity it should UNLEASH disease => predicts checkpoint-inhibitor-induced T1D (a
     documented clinical fact -> built-in validation). SAME ladder, OPPOSITE therapeutic sign = the transfer.

Deterministic. 4 GB cap (trivial).
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    diff=1.2,                  # progenitor -> effector influx scale (s_P = diff * P0) — strong: progenitor re-ignites
    a=1.7, K=0.5, dE=0.70,     # effector self-activation (n=4 switch) / half-sat / death
    exh0=0.25, exhH=5.0,       # baseline E->X exhaustion / boosted by program H
    rev=0.12, dX=0.25,         # X->E reversion (low = exhaustion maintained, LAG3) / X death (low: persistent reservoir)
    epsH=40.0, dH=0.46,        # teplizumab exhaustion-program imprint / ~18-mo waning
    cpi_rev=6.0, cpi_block=0.9,# checkpoint: ADD to X->E reversion AND BLOCK the exhaustion program (reverse exhaustion)
    kappa=1.10, rhoB=0.60,     # effector kills beta / beta regen
)
TEP_DUR = 14/365.0; CPI_DUR = 60/365.0
B_CURE = 0.45; HORIZON = 5.0


def _pulse(t, t0, dur):
    return 1.0 if (t0 <= t < t0 + dur) else 0.0


def rhs(t, y, p, s):
    E, X, H, B = (max(v, 0.0) for v in y); H = min(H, 1.0)
    u_tep = _pulse(t, s.get("tep_t0", 1e9), TEP_DUR) if s.get("tep") else 0.0
    u_cpi = _pulse(t, s.get("cpi_t0", 1e9), CPI_DUR) if s.get("cpi") else 0.0
    sP = p["diff"] * s.get("P0", 0.3)                       # progenitor -> effector influx (patient axis)
    exh = (p["exh0"] + p["exhH"] * H) * (1.0 - p["cpi_block"] * u_cpi)   # E->X; checkpoint BLOCKS the program
    rev = p["rev"] + p["cpi_rev"] * u_cpi                   # X->E (checkpoint blockade reverses exhaustion)
    selfE = p["a"] * E**4 / (p["K"]**4 + E**4)              # n=4 switch -> a low "controlled" basin exists
    dE = sP + selfE - p["dE"] * E - exh * E + rev * X
    dX = exh * E - rev * X - p["dX"] * X
    dH = p["epsH"] * u_tep * (1 - H) - p["dH"] * H
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * E * B
    return [dE, dX, dH, dB]


def simulate(sched, p=None, E0=1.1, t_end=8.0):
    p = p or P
    y0 = [E0, 0.0, 0.0, 0.60]
    return solve_ivp(rhs, (0, t_end), y0, args=(p, dict(sched)), t_eval=np.linspace(0, t_end, 1600),
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.02)


def bend(sol):
    return float(np.interp(HORIZON, sol.t, sol.y[3]))


def controls(P0, p=None, **extra):
    s = {"tep": True, "tep_t0": 0.0, "P0": P0, **extra}
    return bend(simulate(s, p)) > B_CURE


def main():
    untr = bend(simulate({"P0": 0.3}))
    print(f"calibration: untreated B@5yr = {untr:.2f} (progresses).\n")

    print("=" * 72)
    print("PREDICTION 1 — the PROGENITOR pool (P0) is the responder/non-responder axis (teplizumab mono)")
    print("=" * 72)
    print(f"  {'progenitor P0':>14} {'B@5yr':>7} {'outcome':>14}")
    for P0 in [0.05, 0.12, 0.20, 0.30, 0.45]:
        b = bend(simulate({"tep": True, "tep_t0": 0.0, "P0": P0}))
        print(f"  {P0:>14.2f} {b:>7.2f} {'RESPONDER' if b > B_CURE else 'non-responder':>14}")
    print("  -> small/quiescent progenitor = responder; large progenitor refills the attack = non-responder.")
    print("     (P = the autoreactive memory-stem pool detected in T1D patients, Vignali 2018 -> measurable.)")

    print("\n" + "=" * 72)
    print("PREDICTION 2 — CHECKPOINT BLOCKADE (reverse exhaustion) UNLEASHES disease (=> checkpoint-T1D)")
    print("=" * 72)
    resp = {"tep": True, "tep_t0": 0.0, "P0": 0.08}        # a teplizumab-controlled responder
    b_ctrl = bend(simulate(resp))
    b_cpi = bend(simulate({**resp, "cpi": True, "cpi_t0": 1.5}))   # then anti-PD-1/LAG3 at 1.5 yr
    print(f"  controlled responder (teplizumab, small progenitor): B@5yr = {b_ctrl:.2f}  ({'OK' if b_ctrl>B_CURE else 'lost'})")
    print(f"  + checkpoint blockade at 1.5 yr (reverse the protective exhaustion): B@5yr = {b_cpi:.2f}  "
          f"({'DISEASE UNLEASHED' if b_cpi < B_CURE else 'no effect'})")
    print("  -> matches the documented clinical fact: checkpoint inhibitors CAUSE autoimmune type 1 diabetes.")

    print("\n" + "=" * 72)
    print("PREDICTION 3 — non-response has TWO causes, each with a MATCHED, biomarker-stratified lever")
    print("=" * 72)
    print(f"  big-progenitor non-responder (P0=0.45):                          responds? {controls(0.45)}")
    print(f"   + TARGET THE PROGENITOR (deplete the stem/TSCM pool, P0 0.45->0.08): responds? {controls(0.08)}")
    p_maint = dict(P); p_maint["rev"] = 0.03
    print(f"   + maintain exhaustion alone (LAG3, rev 0.12->0.03): responds? {controls(0.45, p=p_maint)}"
          f"   <- does NOT fix a progenitor-driven non-responder (the influx is the problem)")
    print("  -> the hierarchy SPLITS non-response into two mechanisms: a big stem pool (target the")
    print("     progenitor) vs poor exhaustion-durability (sustain exhaustion / 2nd course). Matched levers.")

    print("\nTRANSFER (the sign flip): this SAME ladder is the cancer/chronic-infection model run with the")
    print("OPPOSITE goal -- there you GIVE checkpoint blockade (reverse exhaustion) to UNLEASH effectors")
    print("against the tumor/virus; here you DRIVE exhaustion (anti-CD3) to RESTRAIN them. One module, two signs.")


if __name__ == "__main__":
    main()
