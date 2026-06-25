#!/usr/bin/env python3
"""Machine-checkable assertions for the RESPONDER layer (t1d_responder.py): reproduces a partial
teplizumab response rate and BOTH real biomarker directions (baseline exhaustion -> responder, Wiedeman
2019; TSCM renewal -> non-responder, Dufort 2026), plus the two conversion levers. Seeded cohort. 4 GB cap."""
import sys
import numpy as np
from t1d_responder import responds, patient

rng = np.random.default_rng(0); N = 240; rows = []
for _ in range(N):
    r = rng.uniform(0.02, 0.32); x0 = rng.uniform(0.0, 0.40); e0 = rng.uniform(0.8, 1.3)
    rows.append((r, x0, responds(patient(r, x0), E0=e0)))
rows = np.array(rows); rate = rows[:, 2].mean()
R = rows[rows[:, 2] == 1]; NR = rows[rows[:, 2] == 0]

nr = patient(0.22, 0.03)
durable = dict(nr); durable["dX"] = 0.25         # a 2nd course before exhaustion wanes
blunt = dict(nr); blunt["r_tscm"] = 0.06         # blunt the renewal source

checks = []
def chk(n, c, d):
    checks.append(c); print(f"  [{'PASS' if c else 'FAIL'}] {n}: {d}")

chk("response rate is PARTIAL (30-65%)", 0.30 <= rate <= 0.65, f"{rate*100:.0f}%")
chk("baseline exhaustion HIGHER in responders (Wiedeman)", R[:, 1].mean() > NR[:, 1].mean(), f"R {R[:,1].mean():.2f} vs NR {NR[:,1].mean():.2f}")
chk("TSCM renewal LOWER in responders (Dufort)", R[:, 0].mean() < NR[:, 0].mean(), f"R {R[:,0].mean():.2f} vs NR {NR[:,0].mean():.2f}")
chk("clear responder responds (high exhaustion, low TSCM)", responds(patient(0.02, 0.40)), "-> R")
chk("durable exhaustion CONVERTS a non-responder", (not responds(nr)) and responds(durable), "2nd course rescues the high-TSCM corner")
chk("blunting TSCM CONVERTS a non-responder", responds(blunt), "blunt renewal rescues")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- responder layer (both teplizumab biomarkers reproduced)")
sys.exit(0 if npass == len(checks) else 1)
