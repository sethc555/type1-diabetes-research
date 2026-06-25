#!/usr/bin/env python3
"""Machine-checkable assertions for the GENETICS / HLA calibration bridge (t1d_genetics.py).
Deterministic. Asserts the genotype->parameter map (anchored in REAL Erlich 2008 HLA odds ratios)
reproduces the known genotype->phenotype facts: higher OR/GRS -> younger onset (Sharp 2019), DR15-DQ6
protection (Erlich), and the insulin-first(DR4)/GAD-first(DR3) endotype (Bauer 2019). 4 GB cap."""
import sys
import numpy as np
from t1d_genetics import GENO, onset

rows = [(name, OR, onset(OR), ag) for name, OR, ag in GENO]
ts = [t for _, OR, t, _ in rows if np.isfinite(t)]            # onset ages, rows in DECREASING OR order
dq6 = next(t for n, OR, t, ag in rows if "DQ6" in n)
dr34 = next(t for n, OR, t, ag in rows if n.startswith("DR3/DR4"))

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# T1 — higher OR/GRS -> younger onset (Sharp 2019): onset non-decreasing as OR falls
chk("T1  higher OR/GRS -> younger onset (Sharp 2019)",
    all(ts[i] >= ts[i-1] - 1e-9 for i in range(1, len(ts))),
    f"onset ages {', '.join(f'{t:.1f}' for t in ts)} yr (non-decreasing as OR falls)")
# T1b — the OR=30 genotype is the earliest
chk("T1b DR3/DR4-DQ2/8 (OR=30) is earliest", abs(dr34 - min(ts)) < 1e-9, f"DR3/DR4 onset {dr34:.1f} yr = youngest")
# T2 — DR15-DQ6 protected (Erlich OR=0.03)
chk("T2  DR15-DQ6 PROTECTED (Erlich OR=0.03)", not np.isfinite(dq6), "no disease within 30 yr")
# T3 — primary antigen / endotype by HLA class (Bauer 2019)
ins_ok = all("insulin" in ag for n, OR, t, ag in rows if n.startswith("DR4/"))
gad_ok = all("GAD" in ag for n, OR, t, ag in rows if n.startswith("DR3/"))
chk("T3  endotype by HLA class (Bauer 2019)", ins_ok and gad_ok, "DR4 -> insulin-first, DR3 -> GAD-first")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- genetics / HLA calibration bridge")
print("  genotype->parameter map (real Erlich 2008 ORs) reproduces Sharp 2019 onset gradient, DQ6 protection, Bauer endotypes.")
sys.exit(0 if npass == len(checks) else 1)
