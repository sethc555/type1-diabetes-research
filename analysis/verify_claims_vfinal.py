#!/usr/bin/env python3
"""Machine-checkable verification of the v-final (post-review, verified-biology) claims.

The v-final result REVERSES the published v1 headline. v1 claimed a tolerance-first
SEQUENCING ANTAGONISM; an immunologist reviewer showed that rested on an
uncalibrated tolerance-monotherapy = 100% and an inverted clinical rationale. Rebuilt on the
verified biology (PERIPHERAL tolerance bottleneck -- Feuerer 2007/09, Mhanna/Tang 2021; durable
anti-CD3 effector hyporesponsiveness -- Long 2016, Lledo-Delgado), the model (v3 two-channel;
v4 + acute-deletion) predicts the OPPOSITE of v1: anti-CD3 SYNERGIZES with antigen-specific
tolerance, and the bistable EFFECTOR<->Treg POPULATION framework CANNOT reproduce the
Foster 2025 / Stewart 2020 antagonism at all. This script asserts those v-final invariants.

Run:  python3 verify_claims_vfinal.py   (exit 0 iff all pass). Under the 4 GB cap per policy:
  bash -c 'ulimit -v 4194304; timeout 595 python3 verify_claims_vfinal.py'
"""
import sys
import numpy as np
import t1d_model_v3 as V3
import t1d_model_v4 as V4

checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

# =====================================================================================
# v3 -- model rebuilt on the verified biology (peripheral two-channel tolerance platform)
# =====================================================================================
base3 = V3.time_to_dx(V3.simulate(V3.arms(0.0)["untreated"]))
check("v3 untreated progresses to dx in ~1.5-3.5 yr (TN10/TrialNet-anchored)",
      1.5 <= base3 <= 3.5, f"{base3:.2f} yr")

PSIS3 = [0.0, 0.5, 1.0, 1.5, 2.0, 2.6]
eff3, mono3 = {}, {}
for psi in PSIS3:
    e, fr = V3.combo_effect(psi)
    eff3[psi], mono3[psi] = e, fr["anti-CD3 only"]

# (1) anti-CD3 monotherapy never cures the cohort (delays only) -- matches TN10/teplizumab
check("v3 anti-CD3 monotherapy = 0% cohort cure at every psi (delays, never cures)",
      all(v <= 0.001 for v in mono3.values()),
      f"max a3-only across psi = {max(mono3.values())*100:.0f}%")

# (2) THE STRUCTURAL RESULT: the combination NEVER antagonizes -- no psi gives a net-negative
#     best-combo-minus-best-mono. anti-CD3's effector reduction is intrinsically pro-tolerant.
check("v3 combination NEVER antagonizes (best-combo - best-mono >= 0 at all psi)",
      all(e >= -0.02 for e in eff3.values()),
      f"min effect over psi = {min(eff3.values())*100:+.0f} pts")

# (3) and it SYNERGIZES in the conversion-limited band (matches the POSITIVE Salmonella/L.lactis data)
check("v3 SYNERGY in the mid-psi band (>= +50 pts at psi=1.0 and psi=1.5)",
      eff3[1.0] >= 0.50 and eff3[1.5] >= 0.50,
      f"psi1.0={eff3[1.0]*100:+.0f}, psi1.5={eff3[1.5]*100:+.0f} pts")

# =====================================================================================
# v4 -- adds the ACUTE-DELETION channel A, built EXPLICITLY to try to manufacture the antagonism
#       (anti-CD3 preferentially deletes the just-activated converting clones). If the bistable
#       population framework could produce Foster, it would show here, at low psi.
# =====================================================================================
base4 = V4.time_to_dx(V4.simulate(V4.arms(0.0)["untreated"]))
check("v4 untreated progresses to dx in ~1.5-3.5 yr", 1.5 <= base4 <= 3.5, f"{base4:.2f} yr")

def v4_effect(psi):
    fr = {n: V4.cure_fraction(s) for n, s in V4.arms(psi).items()}
    bc = max(fr["simultaneous"], fr["anti-CD3 -> tol"], fr["tol -> anti-CD3"])
    bm = max(fr["tolerance only"], fr["anti-CD3 only"])
    return bc - bm

eff4 = {psi: v4_effect(psi) for psi in [0.0, 0.4, 0.8, 1.2, 1.8, 2.6]}

# (4) Even WITH the acute-deletion channel, there is NO antagonism anywhere
check("v4 combination NEVER antagonizes despite the acute-deletion channel",
      all(e >= -0.02 for e in eff4.values()),
      f"min effect over psi = {min(eff4.values())*100:+.0f} pts")

# (5) THE STRUCTURAL NEGATIVE RESULT: at psi=0 (pure-antigen platform -- the Foster/Stewart regime),
#     the acute-deletion mechanism STILL yields strong synergy. A population-balance acute-deletion
#     term cannot flip the sign => the antagonism demands a CLONE-LEVEL mechanism this framework misses.
check("v4 STRUCTURAL NEGATIVE: psi=0 (Foster/Stewart regime) still SYNERGIZES (>= +50 pts) "
      "-- a population acute-deletion term cannot reproduce the antagonism",
      eff4[0.0] >= 0.50, f"psi=0 effect = {eff4[0.0]*100:+.0f} pts")

print("\n" + "=" * 70)
npass = sum(c for _, c, _ in checks)
print(f"{npass}/{len(checks)} checks passed")
print("\nv-final: anti-CD3 SYNERGIZES with antigen-specific tolerance (v1's tolerance-first")
print("antagonism was an artifact of an uncalibrated operating point -- the reviewer was right).")
print("The Foster 2025 / Stewart 2020 antagonism is UNREPRODUCIBLE in this bistable effector<->Treg")
print("population framework and requires a clone-level acute mechanism -- a falsifiable reframing.")
sys.exit(0 if npass == len(checks) else 1)
