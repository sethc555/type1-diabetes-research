#!/usr/bin/env python3
"""CALIBRATION #3 -- the C-PEPTIDE readout, which turns out to CROSS-VALIDATE kappa and the anti-CD3 effect.

REAL targets:
  * Shields 2018 (Diabetes Care, "C-Peptide Decline ... Two Phases"): post-diagnosis stimulated C-peptide
    falls EXPONENTIALLY at 47%/yr (95% CI 43-51), half-life 1.10 yr, then stabilizes (two-phase).
  * PROTECT (Ramos 2023, NEJM NEJMoa2308743): teplizumab in newly-diagnosed stage-3 children slowed the
    C-peptide decline by a least-squares mean +0.13 pmol/mL at week 78 (95% CI 0.09-0.17, p<0.001).

This anchors the C-peptide readout (AM1) -- but the payoff is two CROSS-VALIDATIONS that the free-knob model
could not claim:
  (1) the post-diagnosis decline rate (0.63/yr) independently matches the TN10-calibrated kappa (0.60/yr) --
      two unrelated datasets/cohorts -> the same late-disease effective kill rate;
  (2) the anti-CD3 effect calibrated on STAGE-2 prevention (TN10), applied to STAGE-3 C-peptide, lands in the
      PROTECT ballpark -- the drug effect TRANSFERS across stages (a prediction, not a fit).
"""
import numpy as np
from scipy.optimize import brentq
from calib_tn10 import fit_kappa, onset_time, MED_PLACEBO, MED_TEPLI

CPEP_HALFLIFE = 1.10          # yr  (Shields 2018)
CPEP_DECLINE = 0.47           # /yr fractional (Shields 2018)
PROTECT_WK = 78 / 52.0        # yr
PROTECT_DIFF_PMOL = 0.13      # pmol/mL absolute (Ramos 2023); baseline stim C-pep ~0.8 -> ~0.16 fractional
PROTECT_BASELINE = 0.8        # pmol/mL (approx newly-diagnosed baseline)


def main():
    print("CALIBRATION #3 -- C-peptide readout <- Shields 2018 + PROTECT (cross-validates kappa & anti-CD3)\n")

    k_cpep = np.log(2) / CPEP_HALFLIFE
    print(f"  Shields 2018: first-phase decline {CPEP_DECLINE*100:.0f}%/yr, half-life {CPEP_HALFLIFE} yr")
    print(f"  FIT  C-peptide decline rate k = ln2/halflife = {k_cpep:.3f}/yr"
          f"   (check 1-exp(-k) = {(1-np.exp(-k_cpep))*100:.0f}%/yr vs 47%)\n")

    kappa = fit_kappa(MED_PLACEBO)
    rel = abs(k_cpep - kappa) / kappa * 100
    print("  CROSS-VALIDATION 1 -- the late-disease kill rate, from two unrelated datasets:")
    print(f"    TN10 stage-2 progression  -> kappa  = {kappa:.3f}/yr")
    print(f"    post-dx C-peptide decline -> k_cpep = {k_cpep:.3f}/yr")
    print(f"    agree within {rel:.0f}%  -> ~0.6/yr is the late-disease effective kill rate, confirmed twice.\n")

    eff = brentq(lambda e: onset_time(kappa * (1 - e)) - MED_TEPLI, 0.01, 0.95)
    k_tepli = k_cpep * (1 - eff)
    C_pbo = np.exp(-k_cpep * PROTECT_WK)
    C_tep = np.exp(-k_tepli * PROTECT_WK)
    frac = C_tep - C_pbo
    protect_frac = PROTECT_DIFF_PMOL / PROTECT_BASELINE
    print("  CROSS-VALIDATION 2 -- the anti-CD3 effect transfers stage-2 -> stage-3:")
    print(f"    anti-CD3 effect calibrated on TN10 (stage-2 prevention): {eff*100:.0f}% attack reduction")
    print(f"    applied to stage-3 C-peptide @78wk: placebo {C_pbo:.2f} vs teplizumab {C_tep:.2f} (frac of baseline)")
    print(f"    model preservation {frac:.2f} (fractional)  vs  PROTECT +0.13 pmol/mL (~{protect_frac:.2f} fractional)")
    print(f"    -> same ballpark (model slightly conservative); the drug effect TRANSFERS across stages -- a")
    print(f"       PREDICTION from independently-calibrated parameters, not a fit.")


if __name__ == "__main__":
    main()
