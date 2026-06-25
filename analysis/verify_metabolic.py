#!/usr/bin/env python3
"""Machine-checkable assertions for the METABOLIC / glucose layer (t1d_metabolic.py).
Deterministic. Asserts: the honeymoon (rise then fall), glucose control modest alone (weaker than
immunotherapy), the two levers are ~ADDITIVE (combo best, not super-additive), and the C-peptide vs
glycemia dissociation. 4 GB cap."""
import sys
import numpy as np
from t1d_metabolic import simulate, cAt, gAt

std = simulate({"u_insulin": 0.5})
tight = simulate({"u_insulin": 1.0})
imm = simulate({"u_insulin": 0.5, "u_imm": 0.4})
combo = simulate({"u_insulin": 1.0, "u_imm": 0.4})

dx = cAt(std, 0); peak = max(cAt(std, tt) for tt in np.linspace(0, 1.5, 60)); late = cAt(std, 3)
s2, t2, i2, c2 = cAt(std, 2), cAt(tight, 2), cAt(imm, 2), cAt(combo, 2)
g_eff, i_eff, c_eff = t2 - s2, i2 - s2, c2 - s2

checks = []
def chk(name, cond, detail):
    checks.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# P1 — the honeymoon: C-peptide rises above diagnosis, then declines
chk("P1  honeymoon rises above dx", peak > dx + 0.02, f"peak {peak:.2f} > dx {dx:.2f}")
chk("P1b then the attack wins",     late < peak - 0.02, f"3yr {late:.2f} < peak {peak:.2f}")
# P2 — glucose control is a modest lever alone, weaker than immunotherapy
chk("P2  tight > standard",         t2 > s2,        f"tight {t2:.2f} > standard {s2:.2f}")
chk("P2b glucose lever < immuno",   g_eff < i_eff,  f"glucose +{g_eff:.2f} < immuno +{i_eff:.2f}")
# P3 — the two levers are ~ADDITIVE (combo best, but NOT super-additive)
chk("P3  combo beats both singles", c2 > i2 and c2 > t2, f"combo {c2:.2f} > immuno {i2:.2f}, tight {t2:.2f}")
chk("P3b ~additive (honest)",       abs(c_eff - (g_eff + i_eff)) < 0.04, f"combo +{c_eff:.2f} vs sum +{g_eff+i_eff:.2f}")
# P4 — C-peptide vs glycemia DISSOCIATION (the two readouts move oppositely across therapies)
chk("P4  C-pep / glucose dissociate",
    cAt(imm, 2) > cAt(tight, 2) and gAt(imm, 2, 0.5) > gAt(tight, 2, 1.0),
    f"immuno: C-pep {cAt(imm,2):.2f} high / G {gAt(imm,2,0.5):.1f} high; tight: C-pep {cAt(tight,2):.2f} / G {gAt(tight,2,1.0):.1f}")

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass — metabolic / glucose layer")
print("  honeymoon reproduced; glucose control modest alone; metabolic+immune arms additive; C-peptide != glycemia.")
sys.exit(0 if npass == len(checks) else 1)
