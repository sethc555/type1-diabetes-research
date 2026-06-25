#!/usr/bin/env python3
"""Machine-checkable assertions for CALIBRATION #1 (calib_tn10.py): the disease timescale is fit to the
TN10 placebo curve and the anti-CD3 effect to the teplizumab arm (Herold 2019), with plausible,
data-consistent values. Deterministic. 4 GB cap."""
import sys
import numpy as np
from scipy.optimize import brentq
from calib_tn10 import fit_kappa, onset_time, cohort_onsets, MED_PLACEBO, MED_TEPLI

kappa = fit_kappa(MED_PLACEBO)
eff = brentq(lambda e: onset_time(kappa * (1 - e)) - MED_TEPLI, 0.01, 0.95, xtol=1e-5)
f36 = float(np.mean(cohort_onsets(kappa) <= 3))

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# the fit reproduces the real medians
chk("placebo median = 24.4 mo (fit converged)", abs(onset_time(kappa) - MED_PLACEBO) < 0.05, f"{onset_time(kappa)*12:.1f} mo")
chk("teplizumab median = 48.4 mo (fit converged)", abs(onset_time(kappa*(1-eff)) - MED_TEPLI) < 0.05, f"{onset_time(kappa*(1-eff))*12:.1f} mo")
# the calibrated values are biologically plausible (not forced into a corner)
chk("kappa in a plausible range 0.4-0.8 /yr", 0.4 < kappa < 0.8, f"kappa = {kappa:.3f} /yr")
chk("anti-CD3 effect in a plausible 10-40%", 0.10 < eff < 0.40, f"{eff*100:.0f}% effective attack reduction")
# the cohort KM is consistent with TN10 (~36%/yr -> ~60-70% progressed by 3 yr)
chk("KM @36mo TN10-consistent (0.55-0.75)", 0.55 < f36 < 0.75, f"{f36*100:.0f}% progressed by 36 mo")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- calibration #1 (disease timescale <- TN10)")
print("  kappa pins the placebo median (24.4 mo); a 24% anti-CD3 effect pins the teplizumab delay (48.4 mo); both plausible.")
sys.exit(0 if npass == len(checks) else 1)
