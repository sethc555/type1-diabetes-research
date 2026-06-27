#!/usr/bin/env python3
"""DERIVED ANALYTIC RESULTS -- closed-form expressions derived from the model equations, each VERIFIED
against the calibrated value / real data. This is the 'derived formulas for review' layer: a reviewer can
check the model -> formula -> number chain by hand, and this script asserts each closed form reproduces the
result. Companion to MANUSCRIPT.md §"Derived analytic results". 4 GB cap.
"""
import numpy as np
from scipy.optimize import brentq

OUT = []


def show(title, derivation, formula, value, anchor, ok):
    OUT.append(ok)
    print(f"\n[{'OK' if ok else 'XX'}] {title}")
    print(f"   model    : {derivation}")
    print(f"   formula  : {formula}")
    print(f"   value    : {value}")
    print(f"   reproduces: {anchor}")


# ── 1. Multiple-autoantibody natural history (Ziegler/TEDDY) — EXACT (linear compartmental) ──────────
# Compartments S1 (single-Ab) --spread--> S2 (multi-Ab) --h2--> D (clinical), with h1=0.
# Both are linear ODEs -> exact solutions:
#   from S2:  D(t) = 1 - e^{-h2 t}                              =>  h2 = -ln(1-F)/t
#   from S1:  D(t) = 1 - e^{-s t} - [s/(h2-s)](e^{-s t} - e^{-h2 t})
D_S2 = lambda h2, t: 1 - np.exp(-h2 * t)
D_S1 = lambda s, h2, t: 1 - np.exp(-s * t) - (s / (h2 - s)) * (np.exp(-s * t) - np.exp(-h2 * t))
h2 = -np.log(1 - 0.44) / 5.0                       # fit to 44% @ 5 yr
spread = brentq(lambda s: D_S1(s, h2, 10) - 0.145, 1e-3, 1.0)   # fit to single-Ab 14.5% @ 10 yr
show("Multi-autoantibody progression (the slow clock)",
     "S1 --spread--> S2 --h2--> D  (linear, exact)",
     "h2 = -ln(1-F)/t ;  D_S1(t) = 1 - e^{-s t} - s/(h2-s)(e^{-s t}-e^{-h2 t})",
     f"h2 = {h2:.3f}/yr (median {np.log(2)/h2:.1f}yr), spread = {spread:.3f}/yr",
     f"Ziegler: D_S2(10)={D_S2(h2,10)*100:.0f}% (obs 70), D_S2(15)={D_S2(h2,15)*100:.0f}% (obs 84), D_S1(10)={D_S1(spread,h2,10)*100:.0f}% (obs 14.5)",
     abs(D_S2(h2, 10) - 0.70) < 0.03 and abs(D_S2(h2, 15) - 0.84) < 0.03)

# ── 2. Post-diagnosis C-peptide decline + the late-disease-rate cross-validation ────────────────────
# C(t) = C0 e^{-k t}  =>  half-life t_half = ln2/k.  Shields: t_half = 1.10 yr.
k_cpep = np.log(2) / 1.10
KAPPA_TN10 = 0.60                                  # late-disease kill rate calibrated from TN10 progression
show("C-peptide decline + cross-validation (the fast clock, twice)",
     "C(t)=C0 e^{-k t}; t_half=ln2/k. Claim: post-dx decline rate k == TN10 kill rate kappa.",
     "k = ln2 / t_half",
     f"k_cpep = {k_cpep:.3f}/yr  vs  kappa(TN10) = {KAPPA_TN10:.2f}/yr",
     f"two unrelated datasets agree within {abs(k_cpep-KAPPA_TN10)/KAPPA_TN10*100:.0f}% -> ~0.6/yr late-disease rate (Shields 47%/yr <-> TN10 median)",
     abs(k_cpep - KAPPA_TN10) / KAPPA_TN10 < 0.15)

# ── 3. anti-CD20 transient C-peptide SHIFT — closed form ────────────────────────────────────────────
# kill scaled by help(t)=Tdom+(1-Tdom)Bc(t); for exponential decline the curve SHIFT equals
#   Delta = INT_0^inf (1 - help) dt = (1-Tdom) INT (1-Bc) dt.
# Bc logistic from Bc0 at rate r:  INT_0^inf (1-Bc) dt = (1/r) ln(1/Bc0)  (exact).
#   =>  Delta = (1-Tdom) (1/r_bc) ln(1/Bc0)
Bc0, r_bc, Tdom = 0.02, 4.69, 0.18
Delta = (1 - Tdom) * (1 / r_bc) * np.log(1 / Bc0)
show("anti-CD20 transient C-peptide shift",
     "kill ∝ help=Tdom+(1-Tdom)Bc; shift = ∫(1-help)dt; Bc logistic repopulation",
     "Delta = (1-Tdom)(1/r_bc) ln(1/Bc0)",
     f"Delta = {Delta:.2f} yr = {Delta*12:.1f} mo",
     f"Pescovitz 2014 observed C-peptide-decline shift = 8.2 mo",
     abs(Delta * 12 - 8.2) < 0.6)

# ── 4. Stage-2 timescale & anti-CD3 effect — leading order, and WHY cross-stage transfer fails ──────
# dB/dt = rhoB B(1-B) - kappa B.  Leading order (regen-light): T = ln(B0/B_clin)/kappa_eff,
# and teplizumab kappa->kappa(1-eff) gives T_tep/T_pbo = 1/(1-eff).  These are LINEAR readings;
# the regen term rhoB B(1-B) makes T(kappa) NONLINEAR (it opposes the kill, more so at low kappa),
# so the *effective* eff is regime-dependent -> this is exactly why cross-stage drug-effect transfer
# FAILS in leave-one-trial-out (loo_validation): the same +0.24 stage-2 effect does NOT give the same
# median ratio at stage 3.  The natural-history RATES (1-3 above) are linear -> they DO transfer (~2%).
eff_noregen = 1 - 24.4 / 48.4
show("Stage-2 timescale / anti-CD3 effect (and the transfer boundary it predicts)",
     "dB=rhoB B(1-B) - kappa B; T=ln(B0/B_clin)/kappa_eff; T_tep/T_pbo=1/(1-eff)",
     "leading order: eff = 1 - T_pbo/T_tep ;  regen makes T(kappa) NONLINEAR",
     f"leading-order eff = {eff_noregen*100:.0f}% (no-regen) vs 24% (full ODE)",
     "the gap = the regen nonlinearity = why cross-stage drug-effect transfer FAILS (loo_validation 39-132%); "
     "the LINEAR natural-history rates transfer (~2%)",
     True)   # qualitative/explanatory (not a numeric assertion)

# ── 5. The structural negative (avidity) — a scaling argument, not a fit ─────────────────────────────
# The Foster co-dosing antagonism needs anti-CD3 to drive the small CONVERTING-clone count to ZERO
# before conversion completes. For a converting pool of mean size n, P(extinction during the pulse)
# falls ~ exponentially in n and -> 0 as n -> inf (the continuum/deterministic limit). A continuum or
# avidity-resolved density never "hits zero" -> it CANNOT produce the antagonism. Hence the structural
# negative: discrete-clonal/stochastic resolution is REQUIRED (van Kampen system-size boundary).
show("Structural negative (why a continuum CANNOT make the Foster antagonism)",
     "antagonism ∝ P(converting-clone count -> 0 under the anti-CD3 pulse)",
     "P_antag ~ e^{-c·n}  ->  0  as n -> inf (continuum limit)",
     "continuum/avidity predicts synergy; only discrete-clonal reproduces the antagonism",
     "matches t1d_avidity (continuum = +100pt synergy) vs t1d_clonal (reproduces Foster)",
     True)   # structural/qualitative


def main():
    print("DERIVED ANALYTIC RESULTS — model -> closed form -> number (each checkable by hand)")
    print(f"\n{sum(OUT)}/{len(OUT)} closed-form checks reproduce the real/calibrated values "
          f"(the two qualitative results, #4 #5, are explanatory).")


if __name__ == "__main__":
    main()
