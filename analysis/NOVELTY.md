# Novelty & prior-art assessment

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> This document situates the model against the literature surfaced in
> [scan_results.md](scan_results.md) (126 papers, 12 topics, 2026-06-21) and reconciled in
> [MEMO.md](MEMO.md). It claims novelty of *approach and hypothesis*, not of clinical validation.

## What is novel here

| # | Novel piece | Why it is new |
|---|---|---|
| 1 | **First mechanistic within-host model of the anti-CD3 × antigen-specific-tolerance combination.** | The T1D "modeling" literature is statistical/ML (Patil 2024, Montaser 2026, Ghalwash 2024). No coupled Treg/effector/β-cell ODE of this drug pair exists in the scan. The one computational-modeling mention (Karaoglu 2025) is review-level on immune-evasive β-cells, not this combination. |
| 2 | **A sequencing rule that explains the Foster antagonism.** | Foster 2025 reported anti-CD3 *reduces* antigen-specific tolerance efficacy but offered no mechanism. We show a bistable effector↔Treg switch is sufficient to reproduce it and orders the protocols `tol-first ≥ tol-only > simultaneous > anti-CD3-first`, with a falsifiable optimal inter-drug interval. |
| 3 | **A two-channel mechanism resolving when the rule holds vs inverts.** | We identify two distinct antagonism channels — substrate-depletion (anti-CD3 deletes the effectors tolerance must convert → favors tolerance-first) and Treg-destruction (anti-CD3 destroys freshly-built Tregs → favors anti-CD3-first) — and show which dominates is set by how Treg-depleting anti-CD3 is (`rho`). This yields a second, sharper falsifiable prediction (order inverts at high `rho`). |

## Closest prior art to reconcile (from [MEMO.md](MEMO.md) §4)

None of the nearest neighbors is a mechanistic-dynamical model of this drug combination; each is
statistical/ML or review-level, and our model is positioned to extend or be calibrated against them.

| Prior work | What it is | Relation to this model |
|---|---|---|
| **Foster et al. 2025** ("2136-LB", NOD mice) | The originating empirical observation: anti-CD3 reduces antigen-specific immunotherapy efficacy. | The unexplained result this model exists to *explain* and convert into a sequencing hypothesis. |
| **Carr et al. 2026** ("2382-P") | Oral Minimal Model φtotal stage-specific β-cell trajectories. | Calibration backbone for the β-cell compartment; descriptive, not mechanistic-dynamical. |
| **Montaser et al. 2026** (*Diabetes*) | ML inflection-point model of accelerated β-cell decline ~1–2 yr pre-dx. | Provides decline-acceleration timing the model should reproduce; statistical, not mechanistic. |
| **Patil et al. 2024** (*Cell Rep Med*) | Gradient-boosting ML progression model on single-cell islets. | The statistical baseline to beat with mechanism. |
| **Wiedeman et al. 2019** (*JCI*) | Autoreactive CD8 exhaustion distinguishes slow progressors. | Sets the effector-state variable; not a dynamical model. |
| **Karaoglu et al. 2025** | The one computational-modeling *review* in T1D (immune-evasive β-cells). | Nearest "modeling" neighbor; review-level, different question. |
| **Cabello-Kindelan 2019 / Serr 2016** | Treg-induction kinetics (PPI plasmid; humanized-mouse Foxp3+ Treg induction). | Parameterize the tolerance conversion term; experimental, not whole-system dynamics. |

**Net:** the un-joined intersection is real. Two active drug literatures (anti-CD3
pharmacodynamics and antigen-specific Treg induction) meet at a published, *unexplained*
combination result, and no mechanistic within-host model spans them.

## Honest bottom line

This is a **modeling hypothesis built on a conference abstract** (Foster 2025, ADA "2136-LB"). The
contribution is a sufficient, falsifiable mechanism and a testable sequencing rule — not a validated
clinical finding. The model is deliberately simple, its parameters are illustrative beyond a single
calibrated progression-timing anchor, and it openly under-produces the teplizumab monotherapy delay
magnitude (the robust, novel claim is the *sequencing antagonism*, not that magnitude). The value is
that it turns an unexplained observation into a concrete, disprovable prediction with a stated
inversion condition.

## Key references

- Foster et al. 2025 — ADA abstract "2136-LB" (NOD): anti-CD3 reduces antigen-specific immunotherapy efficacy.
- Carr et al. 2026 — ADA "2382-P": Oral Minimal Model φtotal stage-specific β-cell trajectories.
- Montaser et al. 2026 — *Diabetes*: ML metabolic inflection point ~1–2 yr before diagnosis.
- Patil et al. 2024 — *Cell Rep Med*: ML progression model on single-cell islets.
- Wiedeman et al. 2019 — *JCI*: autoreactive CD8 exhaustion in slow progressors.
- Karaoglu et al. 2025 — computational-modeling review (immune-evasive β-cells).
- Cabello-Kindelan 2019 / Serr 2016 — antigen-specific Treg-induction kinetics.
- Phillip et al. 2024 — *Diabetologia*: TrialNet staging consensus (stage-2 progression rates).
- Greenbaum et al. 2026; Wouters et al. 2026 — push antigen-specific tolerance as combination partners / stage-specific framing.

---

## Prior-art re-sweep (2026-06-22) — targeted nearest-neighbour search

A second, *targeted* Semantic Scholar sweep (`_scan/prior_art_t1d.md`) aimed squarely at the
specific claim and its adjacents. It **strengthened the honesty of the assessment** by surfacing
an earlier precedent for the *phenomenon*:

- **The antagonism is independently anticipated — Stewart, Posgai et al. 2020** (*ACS Biomater.
  Sci. Eng.*, doi:10.1021/acsbiomaterials.0c01075): "Combination treatment with antigen-specific
  dual-sized microparticle system plus anti-CD3 immunotherapy **fails to synergize**... in NOD
  mice" — the *same* empirical antagonism, five years before Foster 2025. So the empirical
  phenomenon is **PARTIALLY ANTICIPATED** (Stewart 2020 + Foster 2025), not first reported here.
- **What remains novel:** no paper in the sweep gives a mechanistic/mathematical *explanation* of
  the antagonism or a **sequencing rule** (tolerance-first), nor the substrate-depletion-vs-
  Treg-destruction two-channel structure. The closest bistable-immune ODE is **Alexander & Wahl
  2011** (*Bull. Math. Biol.*, "Self-tolerance and Autoimmunity in a Regulatory T Cell Model") —
  establishes the Treg/effector toggle-switch motif but with no β-cells, no therapy, no ordering.
  The mechanistic model + sequencing rule are novel within the corpus.
- **Supports our assumptions:** Miyahara/Khattar 2012 (anti-CD3-class agents reduce
  antigen-reactive T cells while *sparing* Tregs) backs the Treg-sparing ρ<1 regime; Rafiqi/
  Aldasouqi 2025 backs the effector→Treg conversion flux.
- **Could challenge us:** Valle/Barbagiovanni 2015 (heterogeneous CD3 expression → variable
  anti-CD3 T-cell modulation) — if Tregs are modulated comparably to effectors in vivo, that is
  the high-ρ regime where our model predicts the optimal order **inverts** (the disclosed caveat).

**Updated verdict:** phenomenon PARTIALLY ANTICIPATED (Stewart 2020); the explanatory toggle-switch
model and the tolerance-first sequencing rule remain NOVEL.

---

## Pre-publication novelty recheck (2026-06-22, before preprint)

A second, sharper Semantic Scholar sweep (`_scan/prior_art_t1d_recheck.md`, 61 papers, query
phrasings aimed squarely at catching a duplicate) was run as a publication gate and assessed
against the claims. **Result: no same-finding paper exists** — neither a mechanistic/mathematical
model of the anti-CD3 × antigen-specific-tolerance antagonism nor a tolerance-first sequencing rule
appears anywhere in either sweep. The priors are unchanged: Stewart 2020 and Foster 2025 anticipate
the *phenomenon*; Alexander & Wahl 2011 supplies the bistable-Treg *motif*; all are cited above.

Newly surfaced adjacents (none displaces the priors, none closer to the core claim):
- **Dalton, Asante-Asamani et al. 2025** (bioRxiv, "APCs determine response to Treg therapy in
  T1D") — the nearest T1D Treg-therapy *model*, but single-therapy, no anti-CD3 antagonism / no order.
- **Brown, Thirawatananond et al. 2024** (CD226 inhibition) — augments Tregs / diminishes effectors,
  supporting the effector↔Treg axis; no combination / sequencing.
- **Messenheimer et al. 2017** ("Timing of PD-1 blockade is critical... anti-OX40") — a
  *sequencing-matters* precedent, but in **cancer** immunotherapy with different drug classes; cited
  here as a conceptual analogy (not the same finding) so reviewers don't surface it as undisclosed
  prior art.

On the `rho<1` (Treg-sparing) assumption: Lledó-Delgado 2024 and the EBV/Nat Commun 2025
characterization of teplizumab as repertoire-shifting / Treg-sparing *support* the headline regime;
no 2024–26 paper shows teplizumab *strongly depleting* Tregs in vivo, so the inverted-order caveat
remains appropriately hedged. **Verdict: core contribution (explanatory model + sequencing rule)
NOVEL and safe to post, with the phenomenon framed as anticipated.**
