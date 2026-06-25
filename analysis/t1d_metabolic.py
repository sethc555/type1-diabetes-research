#!/usr/bin/env python3
"""VERTICAL deepening #5 — METABOLIC / GLUCOSE READOUT. Converts abstract beta-MASS into the readouts
trials actually report: C-PEPTIDE (= mass x secretory function) and GLUCOSE. Adds a NEW arm to the
beta-cell-stress hub: GLUCOTOXICITY -- hyperglycemia generates the same oxidative/ER stress (Gerber &
Rutter 2017) that mediates autoimmune beta-destruction (Dinic 2022), so glucose feeds the AB1 loop and
glucose control becomes a lever on the engine. Reproduces the HONEYMOON (Mortensen 2009) and the honest
modesty of glucose control alone (McVean/CLVer 2023: tight control did NOT robustly preserve C-peptide).

State: E immune attack, B beta-mass, S beta-cell stress (immune + GLUCOTOXIC). Glucose is QUASI-STEADY
(it equilibrates in hours vs the years-long beta/immune dynamics): G = p_in/(p_si*Ins_eff + p_b).
C-peptide = B*(1 - sigma*S): stress suppresses secretory function REVERSIBLY (mass preserved but function
down -> the dissociation). Insulin therapy raises Ins_eff -> lowers G -> relieves glucotoxic stress -> the
honeymoon. Deterministic.

Predictions: (1) HONEYMOON; (2) glucose control is a MODEST lever alone (immune attack dominates -- McVean);
(3) glucose control + immunotherapy give ADDITIVE, INDEPENDENT benefits (combo best -- both arms needed; the
model says ADDITIVE, not super-additive -- an honest sub-result vs the synergy I'd hypothesized); (4)
C-peptide vs GLYCEMIA dissociation.
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    bE=0.02, rE=1.2, Emax=1.0, dE=0.5, sf=0.8,    # immune attack; sf = stress AMPLIFIES the attack (Dinic 2022)
    rhoB=0.5, kappa=0.5, amp=0.7,                  # beta regen / kill / stress-amplified kill (AB1)
    k_imm=1.2, k_gluc=1.5, G_thresh=1.1, dS=1.0,   # stress sources: immune + GLUCOTOXIC (G above threshold)
    sigma=0.85,                                    # stress -> secretory dysfunction (REVERSIBLE: mass vs function)
    p_in=1.2, p_si=1.0, p_b=0.2,                   # glucose appearance / insulin sensitivity / basal clearance
)
HOR = 4.0


def cpep(B, S, p):
    return max(B * (1 - p["sigma"] * S), 0.0)      # C-peptide = mass x secretory function


def glucose(B, S, u_ins, p):
    return p["p_in"] / (p["p_si"] * (cpep(B, S, p) + u_ins) + p["p_b"])   # quasi-steady (fast vs beta/immune)


def rhs(t, y, p, s):
    E = max(y[0], 0.0); B = max(y[1], 0.0); S = min(max(y[2], 0.0), 1.0)
    u_ins = s.get("u_insulin", 0.0); u_imm = s.get("u_imm", 0.0)
    G = glucose(B, S, u_ins, p)
    gluctox = max(G - p["G_thresh"], 0.0)
    dE = (p["bE"] + p["rE"] * E * (1 - E / p["Emax"])) * (1 + p["sf"] * S) - p["dE"] * E - u_imm * E
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * E * B * (1 + p["amp"] * S)
    dS = (p["k_imm"] * E + p["k_gluc"] * gluctox) * (1 - S) - p["dS"] * S
    return [dE, dB, dS]


def simulate(s, p=None):
    p = p or P
    y0 = [0.60, 0.40, 0.80]                        # at DIAGNOSIS: established attack, ~40% mass, severely stressed (hyperglycemic)
    return solve_ivp(rhs, (0, HOR), y0, args=(p, dict(s)), t_eval=np.linspace(0, HOR, 1200),
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.01)


def cAt(sol, t, p=None):
    p = p or P
    B = np.interp(t, sol.t, sol.y[1]); S = np.interp(t, sol.t, sol.y[2])
    return cpep(B, S, p)


def gAt(sol, t, u_ins, p=None):
    p = p or P
    B = np.interp(t, sol.t, sol.y[1]); S = np.interp(t, sol.t, sol.y[2])
    return glucose(B, S, u_ins, p)


def main():
    print("Metabolic / glucose layer — C-peptide + glucose readouts on the immune attack\n")

    std = simulate({"u_insulin": 0.5})            # standard care: insulin, imperfect control
    print("P1  HONEYMOON -- insulin relieves glucotoxic stress -> transient C-peptide recovery (Mortensen 2009):")
    print(f"      C-peptide:  dx {cAt(std,0):.2f} -> 3mo {cAt(std,0.25):.2f} -> 6mo {cAt(std,0.5):.2f} -> 1yr {cAt(std,1):.2f} -> 3yr {cAt(std,3):.2f}")
    peak = max(cAt(std, tt) for tt in np.linspace(0, 1.5, 60))
    print(f"      peak C-peptide {peak:.2f} (a honeymoon rise above dx {cAt(std,0):.2f}), then the immune attack wins\n")

    tight = simulate({"u_insulin": 1.0})          # tight glycemic control
    print("P2  Glucose control is a MODEST lever ALONE (McVean/CLVer 2023 -- tight control didn't robustly preserve C-peptide):")
    print(f"      standard control   C-peptide@2yr {cAt(std,2):.2f}   (glucose@1yr {gAt(std,1,0.5):.1f})")
    print(f"      tight control      C-peptide@2yr {cAt(tight,2):.2f}   (glucose@1yr {gAt(tight,1,1.0):.1f})")
    print(f"      -> tight adds only +{cAt(tight,2)-cAt(std,2):.2f} C-peptide: relieves glucotoxicity, but the immune attack dominates\n")

    imm = simulate({"u_insulin": 0.5, "u_imm": 0.4})      # PARTIAL immunotherapy (realistic: slows, doesn't stop)
    combo = simulate({"u_insulin": 1.0, "u_imm": 0.4})
    print("P3  Glucose control + immunotherapy: ADDITIVE, INDEPENDENT benefits (combo best -- both arms needed):")
    for nm, sol in [("standard control only", std), ("tight control only", tight),
                    ("immunotherapy only", imm), ("immunotherapy + tight control", combo)]:
        print(f"      {nm:30s} C-peptide@2yr {cAt(sol,2):.2f}")
    g_eff = cAt(tight, 2) - cAt(std, 2); i_eff = cAt(imm, 2) - cAt(std, 2); c_eff = cAt(combo, 2) - cAt(std, 2)
    print(f"      -> combo {cAt(combo,2):.2f} > immuno {cAt(imm,2):.2f} > tight {cAt(tight,2):.2f} > standard {cAt(std,2):.2f}")
    print(f"      HONEST: glucose +{g_eff:.2f}, immuno +{i_eff:.2f}, combo +{c_eff:.2f} = ~ADDITIVE (not super-additive):")
    print(f"      two INDEPENDENT levers (metabolic + immune), so you need BOTH -- not a synergy, an addition.\n")

    print("P4  C-peptide vs GLYCEMIA dissociation (two readouts -- preserving mass != normalizing glucose):")
    print(f"      tight insulin only:  glucose NORMALIZED (G@2yr {gAt(tight,2,1.0):.1f}) but C-peptide low ({cAt(tight,2):.2f}) -- mass still lost")
    print(f"      immunotherapy:       C-peptide PRESERVED ({cAt(imm,2):.2f}) but glucose still high (G@2yr {gAt(imm,2,0.5):.1f}) -- needs insulin too")


if __name__ == "__main__":
    main()
