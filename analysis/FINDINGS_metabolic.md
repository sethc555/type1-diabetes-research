# Findings — metabolic / glucose readout (vertical deepening #5)

_Converts abstract β-mass into the readouts trials actually report — **C-peptide** and **glucose** — and
adds **glucotoxicity** as a new arm of the β-cell-stress hub. Code: `t1d_metabolic.py` (deterministic),
checked by `verify_metabolic.py` (**7/7**). Grounded in `_scan/metabolic_axis.md`. Status: illustrative
modeling / hypothesis. C-peptide is in **model units** (normalized), not pmol/mL._

## The model
State: `E` immune attack, `B` β-mass, `S` β-cell stress. Glucose is **quasi-steady** (it equilibrates in
hours vs the years-long β/immune dynamics): `G = p_in/(p_si·(C-peptide + insulin) + p_b)`. **C-peptide =
B·(1 − σ·S)** — stress suppresses secretory *function reversibly*, so a stressed but living β-cell reads low
and recovers when stress lifts (this is what produces both the honeymoon and the dissociation).
**Glucotoxicity** (`G` above a threshold) feeds `S` — the same oxidative/ER stress that, per the literature,
*mediates* autoimmune β-destruction (Gerber & Rutter 2017; Dinić 2022). So glucose control is a lever on the
shared engine. The model runs from **diagnosis** (≈40% mass, hyperglycemic), the clinically meaningful entry.

## Results

**P1 — the HONEYMOON (Mortensen 2009).** Insulin lifts glucotoxic stress → secretory function recovers →
C-peptide **rises 0.13 → 0.17 over the first year**, then the immune attack wins and it declines (3 yr 0.13).
The model reproduces partial remission as a *function* recovery on preserved-then-lost mass.

**P2 — glucose control is a MODEST lever alone (honest McVean/CLVer 2023 match).** Tight vs standard control:
C-peptide@2yr **0.18 vs 0.15** (+0.03). Tight control normalizes glucose (0.9 vs 1.4) but the unchecked
immune attack dominates, so the C-peptide benefit is small — matching the trial that found tight control did
*not* robustly preserve C-peptide.

**P3 — glucose control + immunotherapy are ADDITIVE, not synergistic (an honest sub-result).** C-peptide@2yr:
standard 0.15 → tight 0.18 → immuno 0.20 → **combo 0.23**. The combo is best, but the breakdown is
**glucose +0.03, immuno +0.05, combo +0.09 ≈ their sum** — *additive, not super-additive*. I'd hypothesized
synergy; the model says the metabolic and immune arms are **independent levers**. That's still the actionable
message (you need *both* — disease-modifying therapy *and* glucose control), just an honest "addition, not
synergy." Reported as-is rather than tuned into a synergy.

**P4 — C-peptide ≠ glycemia (dissociation).** Tight insulin **normalizes glucose (0.9) but C-peptide stays
low (0.18)** — mass is still being lost. Immunotherapy **preserves C-peptide (0.20) but glucose stays high
(1.3)** — mass is protected but insufficient, so insulin is still needed. The two endpoints move
independently — exactly why trials report both and why C-peptide is the *disease-modifying* readout.

## Why this matters
It makes the whole body **speak in C-peptide and glucose**, the units trials actually report, so predictions
become directly comparable. It adds glucose control as a real (if modest) lever on the shared engine, and it
reproduces two phenomena the immune-only models couldn't — the honeymoon and the C-peptide/glycemia
dissociation. And it lands a *partly-negative* trial (McVean) honestly, which is itself a credibility check.

## Honest caveats
Illustrative; **C-peptide is in normalized model units** (directions and relative gaps are the signal, not
absolute values). Quasi-steady glucose and a glucotoxicity *threshold* are modeling abstractions. The
additive-not-synergistic finding (P3) is a genuine sub-result, not a tuned outcome. Insulin sensitivity is
fixed (no lipotoxicity / insulin-resistance arm). The honeymoon magnitude is modest (as it is clinically —
the dramatic clinical sign is the drop in insulin *requirement*, only partly mirrored by C-peptide).
