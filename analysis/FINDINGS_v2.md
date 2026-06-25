# Findings v2 — model rebuilt after the reviewer critique (supersedes the v1 headline)

_Post-publication revision. The v1 preprint (Zenodo 10.5281/zenodo.20804558) made a **sequencing**
claim that does **not** survive a biologically-corrected model. This v2 is the honest result. Numbers
re-derived/asserted by `verify_claims_v2.py`. Status: illustrative modeling hypothesis, not clinical
findings. Verbatim critique held privately; honesty trail in [AUDIT.md](AUDIT.md)._

## What the critique was (an immunologist reviewer — 2026-06-22)
1. No thymic Treg source — the Treg pool was built only by peripheral conversion; NOD thymic-selection
   defects impair islet-protective Tregs and may delete the very precursors conversion depends on.
2. Tolerance-monotherapy = 100% was **uncalibrated** — a byproduct of parameters, not any measured
   result; tolerance is constitutively impaired in T1D (islet transplants need lifelong immunosuppression).
3. **Self-contradiction**: if tolerance alone is 100% and anti-CD3 alone is 0%, the model argues
   *against* combining them — inverting the real rationale (anti-CD3 is added *because* tolerance
   underdelivers). The efficacy gap that motivates combination was assumed away.

## The rebuilt model (`t1d_model_v2.py`)
Adds (1) a **thymic Treg source** `sig_thy` (impaired-but-nonzero in NOD → R has a floor independent
of conversion); (2) a **convertible-precursor fraction** `c` — tolerance can convert only `c·E`, so it
is *intrinsically* limited (NOD precursor deletion → small `c`); (3) **calibrated efficacies** — and
anti-CD3's real **durable benefit**: a 4th state `X`, an anti-CD3-induced effector-hyporesponsiveness
("exhaustion/anergy") imprint (documented teplizumab biology) that builds during dosing, decays
slowly, and scales down effector expansion *and* killing by `(1−X)`.

## Results (operating point: c=0.60, epsX=0.9, dX=1.10)

| arm | time-to-dx | cohort durable control |
|---|---|---|
| untreated | 2.66 yr | 0% |
| anti-CD3 only | +2.03 yr delay | **0%** (delays, does not cure — matches TN10/teplizumab) |
| tolerance only | — | **53%** (partial — calibrated, *not* 100%) |
| simultaneous | — | 100% |
| anti-CD3 → tolerance | — | 100% |
| tolerance → anti-CD3 | — | 100% |

**1. The robust finding — combination beats monotherapy (NEW; v1 could not produce this).** The
combination exceeds the best monotherapy by **+47 points** (100% vs 53%), and this held in **every**
case across an imprint-strength sweep (epsX 0.3→1.4). Mechanism: anti-CD3's exhaustion window holds
effectors down long enough for the *thymically-limited* Treg pool (which tolerance alone cannot raise
above ~half the cohort) to establish durable control. This is exactly the clinical rationale for
combining them — which the v1 model inverted.

**2. The v1 sequencing claim is downgraded.** Tolerance-first vs anti-CD3-first differs by **+0
points** across almost all of parameter space; the ~+24-point tolerance-first advantage re-appears
**only** when anti-CD3's durable benefit is weak/transient (epsX≈0.3). So the v1 headline
("anti-CD3 antagonises tolerance → give tolerance first") is a **second-order, regime-dependent**
effect, not a robust result. It survives only as a hedge: *if* anti-CD3's exhaustion benefit turns
out weak, the substrate-depletion antagonism dominates and order matters; otherwise it does not.

## Honest bottom line
The biologically-corrected model **reverses the emphasis** of the published v1 preprint. The
defensible claim is **synergy** — anti-CD3 + antigen-specific tolerance should outperform either alone
because anti-CD3's durable effector hyporesponsiveness buys a window for a thymically-limited Treg
pool — with **sequencing a minor effect** that matters only if that durable benefit is weak. The v1
"tolerance-first" sequencing rule should not be cited as a primary finding.

## Caveats (unchanged in spirit)
Illustrative parameters; the synergy *magnitude* (+47 pts) is illustrative, the robust piece is the
*direction* (combination > monotherapy) and that sequencing is second-order. Tolerance's 53% is a
NOD-partial-prevention calibration; pushing it weaker (lower `c`, the human-like regime) only widens
the combination's advantage. The exhaustion channel is a documented teplizumab mechanism but is here
a single lumped state. Still hypothesis-generating, now aligned with — not inverting — clinical rationale.
