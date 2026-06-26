#!/usr/bin/env python3
"""Machine-checkable assertions for the STRATIFIED RESPONDER CLASSIFIER (responder_classifier.py):
the unselected response rate matches AbATE (~50%), responders carry more baseline exhaustion (Long/
Wiedeman direction), and stratifying on baseline exhaustion yields a large, monotonic ENRICHMENT (the
falsifiable, re-analysis-testable output). Deterministic cohort. 4 GB cap."""
import sys
import numpy as np
from responder_classifier import cohort, ABATE_RATE

P = cohort()
x0, resp = P[:, 1], P[:, 2]
overall = resp.mean()
R, NR = P[resp == 1], P[resp == 0]
q40, q60 = np.quantile(x0, 0.4), np.quantile(x0, 0.6)
lo = P[x0 <= q40, 2].mean()
hi = P[x0 >= q60, 2].mean()

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

chk("unselected rate matches AbATE (~50%, within 10 pts)", abs(overall - ABATE_RATE) < 0.10, f"model {overall*100:.0f}% vs ~{ABATE_RATE*100:.0f}%")
chk("responders carry MORE baseline exhaustion (Long/Wiedeman)", R[:, 1].mean() > 1.3 * NR[:, 1].mean(), f"{R[:,1].mean():.2f} vs {NR[:,1].mean():.2f}")
chk("stratification is MONOTONIC (low < unselected < high)", lo < overall < hi, f"{lo*100:.0f}% < {overall*100:.0f}% < {hi*100:.0f}%")
chk("ENRICHMENT is large (high - low > 30 pts)", (hi - lo) > 0.30, f"+{(hi-lo)*100:.0f} pts high-vs-low")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- stratified responder classifier")
print(f"  predicted, falsifiable: baseline-exhaustion stratification raises teplizumab response ~{overall*100:.0f}% -> ~{hi*100:.0f}% (testable on existing trial data).")
sys.exit(0 if npass == len(checks) else 1)
