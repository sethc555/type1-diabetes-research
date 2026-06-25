#!/usr/bin/env python3
"""Machine-checkable assertions for CALIBRATION #2 (calib_teddy.py): the spreading rate + multiple-Ab
progression hazard fit to the TEDDY/Ziegler natural history, with plausible values and a tight fit.
Deterministic. 4 GB cap."""
import sys
from scipy.optimize import least_squares
from calib_teddy import progressed, resid

fit = least_squares(resid, [0.04, 0.12], bounds=([1e-3, 1e-3], [1.0, 1.0]))
spread, h2 = fit.x
worst = max(abs(r) for r in resid(fit.x))

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# the fit is tight to the real natural-history curve
chk("fit reproduces all 4 Ziegler/Vehik points", worst < 0.03, f"worst residual {worst*100:.1f} pp")
# the canonical anchor numbers come out right
chk("multiple-Ab -> T1D ~70% @10yr (Ziegler)", abs(progressed(spread, h2, "multiple", 10) - 0.70) < 0.03, f"{progressed(spread,h2,'multiple',10)*100:.0f}%")
chk("single-Ab -> T1D ~14.5% @10yr (Ziegler)", abs(progressed(spread, h2, "single", 10) - 0.145) < 0.03, f"{progressed(spread,h2,'single',10)*100:.0f}%")
# the calibrated rates are plausible
chk("spreading rate plausible 0.02-0.08 /yr", 0.02 < spread < 0.08, f"spread = {spread:.3f} /yr")
chk("multiple-Ab hazard plausible 0.08-0.16 /yr", 0.08 < h2 < 0.16, f"h2 = {h2:.3f} /yr (median {0.693/h2:.1f} yr)")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- calibration #2 (spreading rate <- TEDDY/Ziegler)")
print("  spreading ~0.04/yr (single->multiple); multiple-Ab clock ~0.12/yr; progression requires spreading.")
sys.exit(0 if npass == len(checks) else 1)
