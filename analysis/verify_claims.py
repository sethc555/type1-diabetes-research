#!/usr/bin/env python3
"""Machine-checkable verification of every load-bearing claim in this repo.

Re-derives each headline number from the model modules and asserts it within tolerance.
A regression in any module trips a FAIL. Run:  python3 verify_claims.py   (-> exit 0 if all pass)

Stochastic-free (deterministic ODEs), so checks are on actual values, not just direction --
except the robustness sweep, where we assert the qualitative invariant (no order-inversion in
the Treg-sparing regime) on a reduced grid for speed.
"""
import sys, itertools
import numpy as np
import t1d_model as M

checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


# --- 1. bistability: two stable fixed points exist (tolerant: B high; autoimmune: B low) ---
sol_auto = M.simulate({}, y0=[0.60, 1.10, 0.12], t_end=20)
sol_tol  = M.simulate({}, y0=[0.60, 0.10, 1.20], t_end=20)
B_auto, B_tol = sol_auto.y[0, -1], sol_tol.y[0, -1]
check("bistable: autoimmune basin collapses beta-cells (B_end<0.1)", B_auto < 0.10, f"B={B_auto:.3f}")
check("bistable: tolerant basin preserves beta-cells (B_end>0.7)", B_tol > 0.70, f"B={B_tol:.3f}")

# --- 2. untreated representative progresses to stage-3 in ~2 yr ---
tdx_u = M.time_to_dx(M.simulate(M.arms()["untreated"]))
check("untreated reaches diagnosis (finite t_dx)", np.isfinite(tdx_u), f"t_dx={tdx_u:.2f} yr")
check("untreated t_dx in [1.8, 2.8] yr (TN10 placebo ~2 yr)", 1.8 <= tdx_u <= 2.8, f"{tdx_u:.2f}")

# --- 3. anti-CD3 monotherapy only DELAYS (does not cure the representative patient) ---
tdx_a = M.time_to_dx(M.simulate(M.arms()["anti-CD3 only"]))
check("anti-CD3 monotherapy delays but does not cure (finite t_dx > untreated)",
      np.isfinite(tdx_a) and tdx_a > tdx_u, f"t_dx={tdx_a:.2f} vs {tdx_u:.2f}")

# --- 4-6. cohort fractions: antagonism + sequencing rule ---
fr = {n: M.cure_fraction(M.arms()[n]) for n in M.arms()}
check("tolerance monotherapy cures the cohort (=100%)", fr["tolerance only"] >= 0.99,
      f"{fr['tolerance only']*100:.0f}%")
check("untreated & anti-CD3 monotherapy do not bank durable control @5yr (=0%)",
      fr["untreated"] == 0 and fr["anti-CD3 only"] == 0,
      f"untr={fr['untreated']*100:.0f}%, a3={fr['anti-CD3 only']*100:.0f}%")
check("ANTAGONISM: simultaneous < tolerance-only (anti-CD3 blunts tolerance)",
      fr["simultaneous"] < fr["tolerance only"] - 0.1,
      f"sim={fr['simultaneous']*100:.0f}% vs tol={fr['tolerance only']*100:.0f}%")
check("SEQUENCING: tol->anti-CD3 >= anti-CD3->tol (order matters)",
      fr["tol -> anti-CD3"] >= fr["anti-CD3 -> tol"] + 0.1,
      f"tol-first={fr['tol -> anti-CD3']*100:.0f}% vs a3-first={fr['anti-CD3 -> tol']*100:.0f}%")
check("SEQUENCING: tol->anti-CD3 fully rescues (>=95%, == tol-only)",
      fr["tol -> anti-CD3"] >= 0.95, f"{fr['tol -> anti-CD3']*100:.0f}%")

# --- 7. gap sweep: anti-CD3-first recovers as the inter-drug interval grows ---
g0 = M.cure_fraction({"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0})
g1 = M.cure_fraction({"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 1.5})
check("gap sweep: anti-CD3-first improves with a longer gap", g1 > g0 + 0.1,
      f"gap0={g0*100:.0f}% -> gap1.5yr={g1*100:.0f}%")

# --- 8. robustness invariant: in the Treg-sparing regime, tol-first never < simultaneous ---
rng = dict(phi=[0.30, 0.50], rho=[0.5, 0.9], VR=[1.3, 1.5], Ki=[0.45, 0.55], kappa=[0.36, 0.44])
keys = list(rng)
neg = viable = 0
for combo in itertools.product(*[rng[k] for k in keys]):
    p = dict(M.P); p.update(dict(zip(keys, combo)))
    if M.cure_fraction(M.arms()["untreated"], p=p) > 0.2:
        continue
    if M.cure_fraction(M.arms()["tolerance only"], p=p) < 0.3:
        continue
    viable += 1
    d = M.cure_fraction(M.arms()["tol -> anti-CD3"], p=p) - M.cure_fraction(M.arms()["simultaneous"], p=p)
    neg += (d < -0.01)
check("robustness: NO order-inversion in Treg-sparing regime (rho<1)",
      neg == 0 and viable >= 8, f"{neg} inversions / {viable} viable sets")

# --- 9. two-channel caveat: strongly Treg-depleting anti-CD3 (rho=1.1) CAN invert the order ---
p_hi = dict(M.P); p_hi.update(phi=0.5, rho=1.1, VR=1.3, Ki=0.5, kappa=0.44)
d_hi = (M.cure_fraction(M.arms()["tol -> anti-CD3"], p=p_hi)
        - M.cure_fraction(M.arms()["simultaneous"], p=p_hi))
check("two-channel caveat: order inverts at high rho (tol-first worse there)", d_hi < 0,
      f"delta={d_hi*100:+.0f} pts at rho=1.1")

# --- 10. EXACT-VALUE pins: the headline cohort fractions cited in the paper (within tolerance) ---
exact = {"untreated": 0.0, "anti-CD3 only": 0.0, "tolerance only": 1.0,
         "simultaneous": 0.588, "anti-CD3 -> tol": 0.412, "tol -> anti-CD3": 1.0}
for nm, v in exact.items():
    check(f"cohort fraction pinned: {nm} = {v*100:.1f}%", abs(fr[nm] - v) < 0.03,
          f"{fr[nm]*100:.1f}% vs {v*100:.1f}%")

# --- 11. EXACT calibration figures (paper: median 2.06 yr, ~45% by 2 yr, anti-CD3 delay +0.68 yr) ---
import t1d_calibration as C
E0s, B0s = C.cohort(n=500, seed=0)   # n=500/seed=0 reproduces the exact cited figures
ts_u, surv_u, med_u, _ = C.km_curve(M.arms()["untreated"], E0s, B0s)
_, _, med_a, _ = C.km_curve(M.arms()["anti-CD3 only"], E0s, B0s)
prog2 = 1 - np.interp(2.0, ts_u, surv_u)
check("calibration: untreated median t_dx ~2.06 yr (TN10 placebo ~2.0)", 1.85 <= med_u <= 2.30,
      f"{med_u:.2f} yr")
check("calibration: ~45% progressed by 2 yr (TrialNet stage-2 ~50%)", 0.35 <= prog2 <= 0.55,
      f"{prog2*100:.0f}%")
check("calibration: anti-CD3 monotherapy delay +~0.68 yr (under-produces TN10 ~+2)",
      0.4 <= (med_a - med_u) <= 0.95, f"+{med_a - med_u:.2f} yr")

# NB: the EXACT full-grid robustness counts (171/171 viable, 0 inversions, 26 strictly better in
# the Treg-sparing regime; 17 order-inversions at rho<=1.1) are reproduced by
#   `python3 t1d_experiments.py`  (robustness_sweep)
# and were independently re-confirmed in the adversarial audit (AUDIT.md). They are NOT asserted
# here because the full sweep (~38k integrations) exceeds the per-claim 595 s attestation cap;
# check 12 above asserts the robustness INVARIANT (no inversion in rho<1) on a reduced grid, which
# is the load-bearing claim. (Same policy as the HIV exemplar for its expensive sweeps.)

# --- 13. DERIVED criteria (t1d_analytic.py): the closed-form impulsive-limit results ---
import t1d_analytic as AN
# (a) antagonism factor: closed form ~ measured-from-exact-maps, and both show co-admin keeps ~half
af_closed = AN.antagonism_factor()
af_meas = AN.apply_simultaneous(1.10, 0.0)[1] / AN.apply_tol(1.10, 0.0)[1]
check("derived: antagonism factor A^rho*sigT/(sigT+(1-rho)sigA) ~ measured Y_sim/Y_tol",
      0.40 <= af_closed <= 0.55 and abs(af_closed - af_meas) < 0.08,
      f"closed={af_closed:.3f}, measured={af_meas:.3f}")
# (b) order-inversion law: sign(A^rho - A) flips at rho=1, and the ODE order agrees on both sides
inv = lambda r: AN.A**r - AN.A
def ode_delta(r):
    p = dict(M.P); p["rho"] = r
    return (M.cure_fraction(M.arms()["tol -> anti-CD3"], p=p)
            - M.cure_fraction(M.arms()["simultaneous"], p=p))
check("derived: order-inversion crossover at rho*=1 (sign A^rho-A flips, ODE agrees)",
      inv(0.9) > 0 and inv(1.1) < 0 and ode_delta(0.9) >= 0 and ode_delta(1.1) < 0,
      f"A^.9-A={inv(0.9):+.3f}(ODE{ode_delta(0.9)*100:+.0f}), A^1.1-A={inv(1.1):+.3f}(ODE{ode_delta(1.1)*100:+.0f})")

print("\n" + "=" * 60)
npass = sum(c for _, c, _ in checks)
print(f"{npass}/{len(checks)} checks passed")
sys.exit(0 if npass == len(checks) else 1)
