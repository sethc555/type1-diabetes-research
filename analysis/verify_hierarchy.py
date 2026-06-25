#!/usr/bin/env python3
"""Machine-checkable assertions for the HIERARCHY layer (t1d_hierarchy.py): the stem-like PROGENITOR pool
is the responder axis (P1); CHECKPOINT blockade reverses the protective exhaustion and UNLEASHES disease
(P2 -> reproduces checkpoint-inhibitor-induced T1D, the built-in validation); non-response splits into two
matched-lever mechanisms (P3). Deterministic. 4 GB cap."""
import sys
from t1d_hierarchy import simulate, bend, controls, P, B_CURE

b_small = bend(simulate({"tep": True, "tep_t0": 0.0, "P0": 0.05}))
b_large = bend(simulate({"tep": True, "tep_t0": 0.0, "P0": 0.45}))
resp = {"tep": True, "tep_t0": 0.0, "P0": 0.08}
b_ctrl = bend(simulate(resp))
b_cpi = bend(simulate({**resp, "cpi": True, "cpi_t0": 1.5}))
p_maint = dict(P); p_maint["rev"] = 0.03

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

chk("P1 small progenitor -> RESPONDER", b_small > B_CURE, f"B@5yr {b_small:.2f}")
chk("P1 large progenitor -> non-responder", b_large < B_CURE, f"B@5yr {b_large:.2f}")
chk("P2 teplizumab-controlled responder is OK", b_ctrl > B_CURE, f"B@5yr {b_ctrl:.2f}")
chk("P2 CHECKPOINT blockade UNLEASHES disease (checkpoint-T1D)", b_cpi < B_CURE, f"B@5yr {b_cpi:.2f}")
chk("P3 targeting the progenitor converts a non-responder", controls(0.08), "deplete stem pool -> R")
chk("P3 maintaining exhaustion alone does NOT fix a progenitor-driven non-responder", not controls(0.45, p=p_maint), "the influx is the problem")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- hierarchy layer (checkpoint-T1D validation holds)")
sys.exit(0 if npass == len(checks) else 1)
