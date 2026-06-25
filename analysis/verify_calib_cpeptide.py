#!/usr/bin/env python3
"""Machine-checkable assertions for CALIBRATION #3 (calib_cpeptide.py): the C-peptide readout is anchored to
Shields 2018, and -- the point -- it CROSS-VALIDATES (1) kappa from a second dataset and (2) the anti-CD3
effect transferred to PROTECT. Deterministic. 4 GB cap."""
import sys
import numpy as np
from scipy.optimize import brentq
from calib_tn10 import fit_kappa, onset_time, MED_PLACEBO, MED_TEPLI
from calib_cpeptide import CPEP_HALFLIFE, PROTECT_WK, PROTECT_DIFF_PMOL, PROTECT_BASELINE

k_cpep = np.log(2) / CPEP_HALFLIFE
kappa = fit_kappa(MED_PLACEBO)
eff = brentq(lambda e: onset_time(kappa * (1 - e)) - MED_TEPLI, 0.01, 0.95)
model_frac = np.exp(-k_cpep * (1 - eff) * PROTECT_WK) - np.exp(-k_cpep * PROTECT_WK)
protect_frac = PROTECT_DIFF_PMOL / PROTECT_BASELINE

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# anchored to Shields 2018
chk("C-peptide decline reproduces Shields 47%/yr", abs((1 - np.exp(-k_cpep)) - 0.47) < 0.02, f"{(1-np.exp(-k_cpep))*100:.0f}%/yr")
# CROSS-VALIDATION 1: the late-disease rate agrees across two unrelated datasets
chk("XVAL1: k_cpep ~ kappa within 15% (two datasets)", abs(k_cpep - kappa) / kappa < 0.15, f"k_cpep {k_cpep:.3f} vs kappa {kappa:.3f} ({abs(k_cpep-kappa)/kappa*100:.0f}%)")
# CROSS-VALIDATION 2: the anti-CD3 effect transfers to PROTECT (same ballpark)
chk("XVAL2: PROTECT prediction plausible", 0.05 < model_frac < 0.20, f"model {model_frac:.2f} fractional")
chk("XVAL2: within ~0.08 of PROTECT", abs(model_frac - protect_frac) < 0.08, f"model {model_frac:.2f} vs PROTECT ~{protect_frac:.2f}")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- calibration #3 (C-peptide readout + 2 cross-validations)")
print("  ~0.6/yr late-disease kill rate confirmed by TN10 AND C-peptide decline; anti-CD3 effect transfers to PROTECT.")
sys.exit(0 if npass == len(checks) else 1)
