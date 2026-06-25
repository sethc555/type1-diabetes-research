#!/usr/bin/env python3
"""VERTICAL deepening #4 — B CELLS & AUTOANTIBODIES. Closes blind spot AS3 (T-cell-centric scope) and
connects UP to the spreading layer. B cells are antigen-presenting cells that (a) DRIVE epitope spreading
(present new determinants -- McLaughlin 2015; Wan 2018 Nature) and (b) AMPLIFY autoreactive T-cell
activation (Pescovitz 2009 NEJM; Herold 2011). Anti-CD20 (rituximab) depletes them -> preserves C-peptide
~1 yr, then WANES as B cells repopulate (Pescovitz 2014; Chamberlain 2016 = tolerance not reset).

State adds Bc (B-cell APC level) to the spreading model. Spreading needs B cells (spread x Bc); effector
activation = Tdom (T-autonomous fraction) + (1-Tdom)*Bc -> anti-CD20 cuts the (1-Tdom) part. Anti-CD20
depletes Bc; Bc repopulates logistically (transience). Autoantibody count = #antigens recruited (Felton
2024 staging biomarker). Deterministic. 4 GB cap.

Predictions: (1) anti-CD20 is TRANSIENT (repopulation reopens spreading); (2) RESPONDER axis -- works when
B-cell-driven (low Tdom), fails when T-dominated (high Tdom; Linsley 2018); (3) anti-CD20 + single-antigen
tolerance SYNERGY (a 2nd route -- besides beta-protection -- to defeat the spreading escape); (4)
#autoantibodies = the measurable spreading-extent biomarker.
"""
import numpy as np
from scipy.integrate import solve_ivp

M = 5  # 0=insulin(primary), 1..4 = GAD / IA-2 / ZnT8 / hybrid-insulin-peptide
P = dict(
    bE=0.03, rE=1.6, Emax=1.0, dE=0.6,    # per-antigen effectors
    spread=30.0, S_thresh=0.26, tolkill=4.0,   # spreading (fast: complete <1yr) + antigen tolerance
    kappa=0.40, rhoB=0.60,                 # beta kill / regen
    k_stress=1.4, dS=1.0, prot=4.0,        # stress / beta-protection
    Bc0=1.0, bBc=0.30, r_bc=1.5, cd20=10.0,  # B-cell capacity / marrow influx / repopulation / anti-CD20 depletion
    Tdom=0.20,                             # T-cell AUTONOMY fraction (0=B-cell-dependent, 1=T-autonomous): responder axis
)
CD20_DUR = 1.0; B_OK = 0.30               # anti-CD20 depletes B cells ~1 yr (rituximab), then they repopulate


def rhs(t, y, p, s):
    E = np.maximum(y[:M], 0.0); pr = np.clip(y[M:2*M], 0.0, 1.0)
    B = max(y[2*M], 0.0); S = min(max(y[2*M+1], 0.0), 1.0); Bc = max(y[2*M+2], 0.0)
    pr[0] = 1.0
    bc = min(Bc / p["Bc0"], 1.0)
    Tdom = s.get("Tdom", p["Tdom"])
    targets = s.get("targets", [])
    tol_on = bool(s.get("tol")) and t >= s.get("tol_t0", 1e9)
    u_prot = 1.0 if (s.get("prot") and t >= s.get("prot_t0", 0.0)) else 0.0
    c0 = s.get("cd20_t0", 1e9); u_cd20 = 1.0 if (s.get("cd20") and c0 <= t < c0 + CD20_DUR) else 0.0
    tolk = np.array([p["tolkill"] if (tol_on and i in targets) else 0.0 for i in range(M)])
    helpf = Tdom + (1 - Tdom) * bc                                          # B-cell APC help SUSTAINS the attack
    dE = pr * (p["bE"] + p["rE"] * E * (1 - E / p["Emax"])) - p["dE"] * E - tolk * E   # effectors persist (memory T cells; not B-cell-targeted)
    dpr = np.zeros(M)
    for i in range(1, M):
        dpr[i] = p["spread"] * bc * max(S - p["S_thresh"], 0.0) * pr[i-1] * (1 - pr[i])   # spreading NEEDS B cells (APC)
    tot = E.sum()
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * B * tot * helpf             # anti-CD20 -> less B help -> attack PAUSES (transient)
    dS = p["k_stress"] * tot * (1 - S) - p["dS"] * S * (1 + p["prot"] * u_prot)
    dBc = p["bBc"] + p["r_bc"] * Bc * (1 - Bc / p["Bc0"]) - p["cd20"] * Bc * u_cd20   # marrow influx + logistic; anti-CD20 depletes -> repopulates (transience)
    return np.concatenate([dE, dpr, [dB, dS, dBc]])


def simulate(s, p=None):
    p = p or P
    E0 = np.zeros(M); E0[0] = 0.30
    pr0 = np.zeros(M); pr0[0] = 1.0
    y0 = np.concatenate([E0, pr0, [0.60, 0.10, p["Bc0"]]])
    return solve_ivp(rhs, (0, 12.0), y0, args=(p, dict(s)), t_eval=np.linspace(0, 12, 2000),
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.02)


def bAt(sol, t):
    return float(np.interp(t, sol.t, sol.y[2*M]))


def nAt(sol, t):
    idx = int(np.argmin(np.abs(sol.t - t)))
    return int((sol.y[M:2*M, idx] > 0.5).sum())


def main():
    print("B-cell / autoantibody layer — anti-CD20 (rituximab) on the spreading disease\n")

    untr = simulate({})
    cd20 = simulate({"cd20": True, "cd20_t0": 2.0})            # dose on ESTABLISHED (post-spread) disease
    print("P1  anti-CD20 is TRANSIENT (effectors persist; B cells repopulate -> attack resumes; Pescovitz 2014):")
    print(f"      untreated   beta:  3yr {bAt(untr,3):.2f}  5yr {bAt(untr,5):.2f}  11yr {bAt(untr,11):.2f}")
    print(f"      anti-CD20   beta:  3yr {bAt(cd20,3):.2f}  5yr {bAt(cd20,5):.2f}  11yr {bAt(cd20,11):.2f}   (peak then relapse)")
    print(f"      -> benefit PEAKS then FADES: +{bAt(cd20,3)-bAt(untr,3):.2f} @3yr  ->  +{bAt(cd20,11)-bAt(untr,11):.2f} @11yr\n")

    print("P2  RESPONDER axis (works when B-cell-driven, fails when T-dominated; Linsley 2018):")
    for tag, td in [("B-cell-driven  (Tdom=0.20)", 0.20), ("T-dominated    (Tdom=0.65)", 0.65)]:
        u = simulate({"Tdom": td}); c = simulate({"Tdom": td, "cd20": True, "cd20_t0": 2.0})
        print(f"      {tag:26s} peak benefit @3yr  untreated {bAt(u,3):.2f} -> anti-CD20 {bAt(c,3):.2f}"
              f"  (+{bAt(c,3)-bAt(u,3):.2f})")
    print()

    LATE = 2.5
    arms = {
        "untreated":                  {},
        "single-antigen tol, LATE":   {"tol": True, "tol_t0": LATE, "targets": [0]},
        "anti-CD20 alone":            {"cd20": True, "cd20_t0": LATE},
        "anti-CD20 + single-tol":     {"tol": True, "tol_t0": LATE, "targets": [0], "cd20": True, "cd20_t0": LATE},
    }
    print("P3  anti-CD20 + single-antigen tolerance SYNERGY (deplete spreading-drivers + tolerize primary):")
    R = {}
    for nm, s in arms.items():
        sol = simulate(s); R[nm] = bAt(sol, 6)
        print(f"      {nm:26s} beta@6yr {bAt(sol,6):.2f}  (#ab {nAt(sol,6)})")
    print(f"      -> combo {R['anti-CD20 + single-tol']:.2f}  >  single-tol {R['single-antigen tol, LATE']:.2f}"
          f"  and  anti-CD20 {R['anti-CD20 alone']:.2f}\n")

    print("P4  #autoantibodies = #antigens recruited (Felton 2024) -- the model's hidden spreading")
    print("    extent is the MEASURABLE staging biomarker, so every prediction above is checkable in blood.")


if __name__ == "__main__":
    main()
