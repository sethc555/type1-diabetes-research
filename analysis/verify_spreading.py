#!/usr/bin/env python3
"""Machine-checkable assertions for the epitope-SPREADING layer (t1d_spreading.py).
Deterministic (no seeds) -> exact, reproducible. Asserts the 4 predictions hold, including the
mechanism (the #antigens-recruited count). 4 GB cap.  python3 verify_spreading.py"""
import sys
from t1d_spreading import simulate, bend, nspread

LATE = 2.5
def arm(s):
    sol = simulate(s); return bend(sol), nspread(sol)

untr_b, untr_n = arm({})
se_b, se_n = arm({"tol": True, "tol_t0": 0.0,  "targets": [0]})
sl_b, sl_n = arm({"tol": True, "tol_t0": LATE, "targets": [0]})
br_b, br_n = arm({"tol": True, "tol_t0": LATE, "targets": [0, 1, 2, 3, 4]})
sp_b, sp_n = arm({"tol": True, "tol_t0": LATE, "targets": [0], "prot": True, "prot_t0": 0.0})

checks = []
def chk(name, cond, detail):
    checks.append(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# P1 — single-antigen tolerance is ESCAPED by spreading (and spreading really did complete by LATE)
chk("P1  single-LATE escaped by spreading", sl_b < br_b - 0.05, f"single-LATE {sl_b:.2f} < broad-LATE {br_b:.2f}")
chk("P1b spreading completed before LATE",  sl_n >= 4,           f"#antigens at single-LATE = {sl_n} (>=4)")
# P2 — EARLY (pre-spread) beats LATE, by HALTING spreading
chk("P2  EARLY beats LATE",                 se_b > sl_b + 0.10,  f"single-EARLY {se_b:.2f} > single-LATE {sl_b:.2f}")
chk("P2b EARLY halts spreading",            se_n <= 2,           f"#antigens at single-EARLY = {se_n} (<=2)")
# P3 — BROAD tolerance escapes the trap
chk("P3  BROAD preserves beta",             br_b > 0.30,         f"broad-LATE {br_b:.2f} preserved")
# P4 — CROSS-LAYER: beta-protection rescues single-antigen tol AND cuts the antigen count
chk("P4  beta-protect rescues single-LATE", sp_b > sl_b + 0.10,  f"single-LATE {sl_b:.2f} -> +protect {sp_b:.2f}")
chk("P4b beta-protect cuts spreading",      sp_n < sl_n,         f"#antigens {sl_n} -> {sp_n} with protection")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass — epitope-spreading layer")
print("  single-antigen tolerance is escaped by spreading; EARLY/BROAD/beta-protection each defeat the escape.")
sys.exit(0 if npass == len(checks) else 1)
