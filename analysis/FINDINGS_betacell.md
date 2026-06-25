# Findings — the β-cell as an ACTIVE participant (vertical deepening #2)

_Adds the missing half of the disease: β-cells stop being a passive target. Code: `t1d_betacell.py`
(deterministic). Grounded in the β-cell-stress literature (`_scan/betacell_side.md`). Status:
illustrative modeling / hypothesis._

## The model
A β-cell **stress** state `S` driven up by the immune attack and by metabolic load, which then closes a
**feedback loop**: stress → (a) HLA/neoantigen **amplification** of the attack, (b) **dedifferentiation**
(functional `Bf` → dedifferentiated `Bd`, *recoverable*), (c) more killing. Grounded in: "an accomplice
more than a mere victim" (Sahin & Engin 2021); IFN-α → HLA-I hyperexpression + neoantigens (Colli 2020,
Carré 2025); immune-*independent* β-cell **fragility** (Dooley 2016); β-cell **rest is protective**
(van Tienhoven 2025). Two patient axes (immune attack + β-fragility `phi`); two therapy axes (immune /
β-protective, e.g. verapamil/ER-stress reduction).

## Results
**P1 — the stress feedback makes the disease SELF-AMPLIFYING.** Untreated functional β@5yr: **0.12
without** the feedback vs **0.04 with** it — the β-cell "provoking its own attack" makes the disease ~3×
worse. The vicious cycle is real in-model.

**P2 — β-protection works ORTHOGONALLY.** β-protective therapy *alone* (no immune action) preserves
functional β (**0.26** vs 0.04 untreated) — by lowering stress it breaks the loop, blunts
dedifferentiation, and lets dedifferentiated cells **recover**. Predicts verapamil-type efficacy via a
purely β-intrinsic route.

**P3 — the combination is SAFE SYNERGY (no antagonism) — a NEW antagonism-free axis.** immune-only 0.14,
β-protect-only 0.26, **combination 0.48** (best monotherapy +0.22). Because the two mechanisms are
**orthogonal** (calm the attack vs protect/de-stress the target), they combine with **no antagonism** —
unlike the conversion-platform antagonism in the immune-immune combination work. This **extends the
combination/regime framework with a new, safe-to-co-administer axis** (e.g. verapamil + teplizumab).

**P4 — fragility stratification: HONEST PARTIAL.** The hypothesis (robust-β → immune lever; fragile-β →
protection) **did NOT cleanly flip**: β-protection is **broadly dominant at every fragility level**
(it breaks the loop at its source). The immune lever is only *relatively* more competitive for robust β
(low `phi`: immune/protect 0.24/0.33; high `phi`: 0.05/0.14) — a **directional** trend, not a switch.
Reported as-is; not forced.

## What's genuinely new here
- The **β-cell side as an active accomplice** with a self-amplifying stress→neoantigen→attack loop.
- A **second therapy axis** (protect the target) that works without touching the immune system.
- The headline actionable result: **β-protection + immunotherapy is a clean, antagonism-free
  combination** — extending our combination framework beyond the immune-immune (Foster/Mathieu) axis.

## Honest caveats
Illustrative deterministic model; magnitudes illustrative; the robust results are **P1–P3** (the
feedback loop, orthogonal β-protection, safe combination). **P4 (the fragility lever-switch) did not
emerge** — the model says β-protection is broadly valuable rather than fragility-stratified, and we
report that honestly. The stress→neoantigen amplification is a single lumped term; dedifferentiation is
two compartments; not fit to patient data (β-fragility maps to Dooley's genetic axis qualitatively).
