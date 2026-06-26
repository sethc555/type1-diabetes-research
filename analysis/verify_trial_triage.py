#!/usr/bin/env python3
"""Machine-checkable assertions for the TRIAL-TRIAGE ENGINE (trial_triage.py): it must reproduce the model
body's verdicts -- the real trials that FAILED get LIKELY-FAIL (with the matching fix), the cautionary
direction gets CONTRAINDICATED, and the model's fixes get FAVORABLE; and the ranker orders them correctly.
4 GB cap."""
import sys
from trial_triage import triage, rank, FAVORABLE, CONDITIONAL, FAIL, CONTRA

checks = []
def chk(name, got, want):
    ok = got == want; checks.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {got}" + ("" if ok else f"  (expected {want})"))

# real trials that failed -> LIKELY-FAIL
chk("anti-IL-1 at onset (Moran 2013)", triage("anti-IL-1", stage="onset").outcome, FAIL)
chk("single-antigen tolerance, late", triage("antigen tolerance (conversion)", stage="late").outcome, FAIL)
chk("anti-CD20 monotherapy (Pescovitz)", triage("anti-CD20", sequence="mono").outcome, FAIL)
chk("teplizumab + conversion-tolerance CO-DOSED (Foster)", triage("teplizumab", partner="antigen tolerance (conversion)", sequence="co-dose").outcome, FAIL)
# the cautionary direction -> CONTRAINDICATED
chk("checkpoint inhibitor", triage("checkpoint inhibitor").outcome, CONTRA)
# the model's fixes -> FAVORABLE
chk("teplizumab + expansion-tolerance (Mathieu)", triage("teplizumab", partner="antigen tolerance (expansion)").outcome, FAVORABLE)
chk("broad/early tolerance", triage("broad antigen tolerance", stage="early").outcome, FAVORABLE)
chk("teplizumab, exhaustion-high stratified", triage("teplizumab", population="exhaustion-high").outcome, FAVORABLE)
chk("beta-protection adjunct", triage("beta-protection", partner="teplizumab").outcome, FAVORABLE)
# timing/sequence rescues flip the verdict off FAIL
chk("anti-IL-1 as prevention (stage 1-2)", triage("anti-IL-1", stage="stage1").outcome, CONDITIONAL)
chk("teplizumab + conversion-tolerance SEQUENCED", triage("teplizumab", partner="antigen tolerance (conversion)", sequence="sequenced").outcome, CONDITIONAL)
chk("teplizumab unselected (wash-out)", triage("teplizumab", stage="stage2").outcome, CONDITIONAL)

# the ranker orders correctly (best is FAVORABLE, worst is CONTRAINDICATED)
ranked = rank([dict(modality="checkpoint inhibitor"), dict(modality="teplizumab", population="exhaustion-high"), dict(modality="anti-CD20", sequence="mono")])
chk("ranker: best = stratified teplizumab", triage(**ranked[0]).outcome, FAVORABLE)
chk("ranker: worst = checkpoint", triage(**ranked[-1]).outcome, CONTRA)

npass = sum(checks)
print(f"\n{npass}/{len(checks)} checks pass -- trial-triage engine reproduces the body's verdicts")
sys.exit(0 if npass == len(checks) else 1)
