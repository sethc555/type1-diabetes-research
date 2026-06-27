# Novelty & prior-art assessment

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> This document situates the model against the literature surfaced in
> [scan_results.md](scan_results.md) (126 papers, 12 topics, 2026-06-21) and reconciled in
> [MEMO.md](MEMO.md). It claims novelty of *approach and hypothesis*, not of clinical validation.

## Novelty of the corrected body (the multi-layer model)

> **Revised 2026-06-27** after a comparable-paper search (Semantic Scholar + web) that the v1 sweeps below had
> missed — they searched the *withdrawn sequencing* claim, not the corrected body's "calibrated within-host
> model + decision output" claims. The search surfaced an established **mechanistic within-host T1D modelling
> lineage** (including the very framework this repo's avidity layer is built on) and a 2024 T1D trial
> simulator. The honest novelty is **narrower** than first written, and is re-stated here.

**What this is NOT.** It is **not** the first mechanistic within-host model of T1D, and **not** the first model
used for T1D trial design. A real ODE/continuum lineage predates it, and this repo's avidity layer *extends*
that lineage rather than competing with it. Any claim of priority over those models would be false. The
individual mechanisms are established biology — none is discovered here.

### Closest prior art — the mechanistic within-host T1D modelling lineage (reconciled)
| Prior work | What it is | Relation to this model |
|---|---|---|
| **Khadra & Pietropaolo 2011** (*PLoS ONE*, [10.1371/journal.pone.0014796](https://doi.org/10.1371/journal.pone.0014796)) | T-cell avidity / killing-efficacy ODE model of T1D progression. | **The parent framework** — the avidity layer (`t1d_avidity.py`) is built directly on it. |
| **Jaberi-Douraki, Pietropaolo & Khadra 2015** (*J Theor Biol*, [10.1016/j.jtbi.2015.07.032](https://doi.org/10.1016/j.jtbi.2015.07.032)) | Continuum model of autoreactive + regulatory T-cell avidity. | Direct predecessor of our continuum treatment; mathematically **deeper** than our ODE layers. |
| **Jaberi-Douraki & Schnell 2014** (*J Theor Biol*, [10.1016/j.jtbi.2014.05.003](https://doi.org/10.1016/j.jtbi.2014.05.003)) | β-cell "suicide"/stress contribution to autoimmune T1D. | Overlaps the β-cell-stress layer (`t1d_betacell.py`); we add the spreading/therapy coupling. |
| **Jaberi-Douraki et al. 2014** (*PLoS ONE*, [10.1371/journal.pone.0093326](https://doi.org/10.1371/journal.pone.0093326)) | T-cell-cycle progression → autoantibody release. | Overlaps the B-cell/autoantibody layer (`t1d_bcell.py`). |
| Integrated metabolism⊗autoimmune β-cell-death model ([PMC3522595](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3522595/)); **Mahaffy & Edelstein-Keshet 2007** (T-cell dynamics via Hopf/homoclinic bifurcation); CD8–β-cell ABM ([PMC5761894](https://pmc.ncbi.nlm.nih.gov/articles/PMC5761894/)) | Metabolism+autoimmune integration; bifurcation structure; a discrete-agent precedent. | Precedents for the metabolic layer, the bistable/threshold behaviour, and the discrete-clonal layer. The *integration idea* is not claimed as new. |
| **Morales & Klose 2024** (*CPT:PSP*, [10.1002/psp4.13193](https://doi.org/10.1002/psp4.13193)) | T1D-prevention **trial-design simulator**: a *statistical* joint longitudinal + time-to-event model on **individual-level** TrialNet + TEDDY data, predicting time-to-onset and trial power. Drug effect is an **empirical dial** (DP50 scaling, no mechanism of action); no combination, no per-patient biomarker stratification, no out-of-sample validation (full-text read 2026-06-27). | **The nearest decision-output neighbour, better-resourced on the trial-design axis** (real per-patient data, published). **Complementary, not competing:** it sizes and powers a trial but does not say *why* a drug works or *who* responds — our mechanistic failure-mode explanation, the per-patient exhaustion-stratification, and the OOS boundary are exactly the *"trial enrichment, stratification"* inputs its authors call for. |

### What is genuinely novel (narrower, graded honestly)
1. **A re-analysis-testable stratification prediction** *(strongest)* — a baseline-CD8-exhaustion score → teplizumab response enrichment ~56%→~91%/~25%, checkable on **existing** TrialNet data (`responder_classifier.py`). It *extends* the Long 2016 / Wiedeman 2019 exhaustion biomarker into a quantitative, falsifiable enrichment; none of the models above makes a per-patient response prediction of this kind.
2. **Leave-one-trial-out validation with an explicit failure boundary** — calibrated to four trials, it predicts held-out trials' *natural history* to ~2% and **openly reports that cross-stage drug-effect extrapolation does not transfer** (39–132%). The surveyed mechanistic models are not OOS-cross-validated with a stated boundary; Morales fits a joint model rather than reporting where it breaks.
3. **One framework that reconciles contradictory combination trials** — Foster 2025 (antagonism) vs Mathieu 2023 (safe) via a platform axis (`t1d_clonal.py`). *A hypothesis resting partly on a conference abstract, not a finding* — but no prior model spans the pair.
4. **A knob-independent structural negative** — the avidity continuum (the Khadra/Jaberi-Douraki framework) *cannot* reproduce the Foster antagonism; only discrete-clonal resolution can. A mechanism-class constraint that holds regardless of tuning — and a negative result *about the lineage we build on*.
5. **The method, as a credibility (not scientific) contribution** — reproduce an unexplained published result → smallest model → falsifiable prediction → adversarial audit *with open retraction* → machine-verified attestation of every number. Distinctive as a practice; explicitly **not** a new biological result.

### Honest bottom line
This is **not a first or a best-in-class** T1D model. It is **broader in scope** than any single prior model
(innate → spreading → B-cell → metabolic → genetics in one body — scope trades against depth, it is not a win),
**more explicit about where it fails**, and it carries **one specific, testable, decision-relevant prediction**
the prior models do not. Its value does not rest on novelty or on beating those models — it rests on being
*calibrated, honestly bounded, and checkable against data a network already holds*. Framed that way (extension
+ a falsifiable prediction, never priority), it is a legitimate contribution and safe to post.

Cross-layer transfers (the exhaustion sign-flip to cancer/HIV; the β-cell-stress hub shared across the
spreading/metabolic/innate layers) are reasoning patterns, not new biology, and are presented as such.

---

> The assessment below is the original **v1 (sequencing)** novelty + the prior-art sweeps, retained as the
> record. Its prior-art landscape — *no mechanistic within-host model of the anti-CD3 × antigen-specific-
> tolerance combination* — still frames the combination layer (`t1d_clonal.py`).
>
> **Superseded:** the v1 table's broad characterisation of T1D modelling as "statistical/ML" is **corrected by
> the lineage reconciliation above** — a mechanistic within-host T1D modelling literature does exist (Khadra,
> Jaberi-Douraki, Mahaffy & Edelstein-Keshet). Only the *specific drug-combination* gap remains open.

## What is novel here (v1 — combination layer, retained as record)

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
