# Findings — innate immunity / neutrophils (vertical deepening #6)

_Adds the UPSTREAM trigger the other layers assumed away, and closes the last AS3 residual. Code:
`t1d_innate.py` (deterministic), checked by `verify_innate.py` (**7/7**). Grounded in `_scan/innate_axis.md`.
Status: illustrative modeling / hypothesis._

## The model
State: `N` innate inflammation (neutrophils/NETs/IFN-α), `E` adaptive attack, `B` β-mass, `S` stress. `N`
does two literature-grounded things: it **feeds the β-stress hub** (IFN-α → HLA-I + ER stress — Marroqui
2017, the same AB1 loop) and it **primes** the adaptive attack `E` (Lombardi 2018: IFN-α is the priming
trigger). `E` has a **sharp Hill self-amplification**, so once primed past a threshold it is **self-sustaining
and innate-independent**. Anti-innate therapy (anti-IL-1 / anti-IFN) suppresses `N`. The disease runs from
**health** (an innate trigger fires, e.g. a viral insult), so the full arc — innate → β-stress → adaptive →
β-loss — is visible.

## Results (`t1d_innate.py`, `verify_innate.py` 7/7)

**P1 — innate-targeting has a narrow EARLY WINDOW (explains Moran 2013).** β@6yr: untreated **0.06**,
anti-innate **EARLY 0.96 (prevented)**, anti-innate **LATE 0.13 (fails)**. Suppressing innate inflammation
*before* the adaptive attack ignites prevents disease; giving it at clinical onset is futile. This reproduces
why **anti-IL-1 failed at onset** (Moran 2013 *Lancet*; Cabrera 2016 — it *moderated inflammation* but did
*not* preserve C-peptide) and predicts the same drug would **work as prevention**.

**P2 — the adaptive attack goes INNATE-INDEPENDENT once established (why LATE fails).** E@6yr: early **0.02**
(never ignited) vs late **0.81** (self-sustaining). Once `E` is past the Hill threshold it no longer needs the
innate trigger — so removing the trigger late changes nothing. This *is* the mechanism behind the failed trials.

**P3 — innate is UPSTREAM of the stress hub.** Peak β-cell stress **0.61 → 0.13** with early innate control:
throttling the trigger throttles the stress→neoantigen→spreading engine the whole body runs on.

**P4 — innate activation PRECEDES the adaptive attack and β-loss.** Timeline: innate `N` active at **0.0 yr**
< adaptive `E` established **0.64 yr** < β<50% **1.79 yr**. The innate/IFN signature is a **pre-onset
biomarker** — consistent with the IFN signature preceding seroconversion clinically.

## Why this matters
It **completes the disease arc** — innate trigger → β-stress hub → adaptive attack → spreading → metabolic
collapse — so the model now spans initiation to clinical readout. And it turns a *major negative trial*
(anti-IL-1, Moran 2013) from an anomaly into a **prediction**: right drug, wrong time. That sharpens the
prevention/early-intervention theme running through the spreading and metabolic layers — innate-targeting
belongs in **stage 1–2 prevention**, not stage-3 rescue.

## Honest caveats
Illustrative. The **sharp Hill ignition threshold** (the bistable "needs priming, then self-sustains"
structure) is the load-bearing modeling choice — the early-window *direction* is robust to it, but the exact
threshold timing is not calibrated. The innate compartment is **lumped** (neutrophils + NETs + IFN-α +
macrophages as one `N`), not resolved. The environmental *cause* of the initial trigger (virus, microbiome)
is still out of scope — only its downstream innate response is modeled (the remaining AS3 residual).
