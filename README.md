# Sequencing antagonism between anti-CD3 and antigen-specific tolerance in type 1 diabetes

> 📄 **Read the manuscript:** [**rendered web version**](https://sethc555.github.io/type1-diabetes-research/) · [PDF](docs/manuscript.pdf) · [Zenodo DOI: 10.5281/zenodo.20804558](https://doi.org/10.5281/zenodo.20804558)

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> This repository contains a deliberately simplified mechanistic model built to *explain* one
> published, unexplained pre-clinical observation and to generate a falsifiable prediction. The
> parameters are illustrative beyond a single calibrated progression-timing anchor; "cure" means
> durable in-model β-cell preservation, not a clinical outcome. Nothing here is a validated clinical
> result. Read it as a quantitative hypothesis, not as evidence.

## The arc

Foster et al. 2025 (NOD mice, ADA abstract 2136-LB) reported an unexplained, unmodeled result:
anti-CD3 monoclonal antibody (teplizumab-class) *reduces* the efficacy of antigen-specific
(mRNA/peptide) tolerance immunotherapy — and both are being pushed toward combination use, so
*whether and how to combine them* is a live clinical question. The T1D "modeling" literature is
statistical/ML (Patil 2024, Montaser 2026); no mechanistic within-host model of this drug–drug
interaction existed. We built the first one: a 3-state ODE in which autoreactive effectors and
antigen-specific Tregs form a bistable switch driving β-cell mass. The model reproduces the Foster
antagonism and resolves it into a **sequencing rule** — give antigen-specific tolerance *first*,
let the Treg pool self-stabilize, *then* dose anti-CD3 — with a quantitative, falsifiable prediction
about the optimal inter-drug interval.

## What's here

```
type1-diabetes-research/
├── README.md                     ← this file
├── ABSTRACT.md                   ← citable one-page summary
└── analysis/
    ├── t1d_model.py              ← P1: the core 3-state within-host ODE + interventions + arms
    ├── t1d_experiments.py        ← P2: mechanism/cohort/gap-sweep/robustness; writes the .png + .npz
    ├── t1d_calibration.py        ← P3: stage-2 cohort calibrated to TN10 / TrialNet progression
    ├── t1d_analytic.py           ← P-analytic: DERIVED closed-form criterion (antagonism factor + ρ=1 inversion law) that replicates the ODE
    ├── verify_claims.py          ← machine-checkable re-derivation of every headline number (24/24)
    ├── FINDINGS.md               ← the verified results + exact numbers
    ├── MEMO.md                   ← the literature lane, citations, calibration anchors
    ├── METHODS.md                ← consolidated methods (equations, parameters, numerics)
    ├── NOVELTY.md                ← prior-art / novelty assessment
    ├── scan_results.md           ← 126-paper Semantic Scholar scan (12 topics, 2026-06-21)
    ├── t1d_mechanism.png         ← why order matters: only tolerance-first builds & keeps R
    ├── t1d_cohort.png            ← durable-control fraction by arm (the antagonism bar chart)
    ├── t1d_gap.png               ← the falsifiable prediction: cure fraction vs inter-drug interval
    ├── t1d_calibration.png       ← untreated stage-2 progression vs TN10 placebo (~2 yr median)
    ├── t1d_analytic.png          ← derived order-inversion law (A^ρ−A) vs ODE benefit, crossing 0 at ρ*=1
    ├── t1d_results.npz           ← cached numeric outputs of the experiment sweeps
    └── raw_cache.json            ← raw Semantic Scholar API payload backing scan_results.md
```

## Key results

All numbers below are re-derived and asserted by [`verify_claims.py`](analysis/verify_claims.py)
(24/24 PASS); see [FINDINGS.md](analysis/FINDINGS.md) for the full statement.

**The model is bistable.** Two stable basins: autoimmune (effectors high → β-cell mass → 0.002) and
tolerant (Tregs high → β-cell mass → 0.931). Late stage 2 sits in the autoimmune basin.

**The mechanism reproduces Foster and resolves it into a sequencing rule.** Cohort durable-control
fraction (β-cell mass > 0.45 at 5 yr, across a severity gradient):

| arm | durable control |
|---|---|
| untreated | 0% |
| anti-CD3 monotherapy | 0% (delays only) |
| antigen-specific tolerance monotherapy | **100%** |
| simultaneous (both at once) | **59%** — anti-CD3 antagonizes tolerance (−41 pts) |
| anti-CD3 → tolerance (anti-CD3 first) | **41%** — worst (substrate deleted first) |
| tolerance → anti-CD3 (tolerance first) | **100%** — fully protected |

The ordering `tol-first ≥ tol-only > simultaneous > anti-CD3-first` is the mechanism's signature.

**The falsifiable prediction — an optimal inter-drug interval.** In the gap sweep
([`t1d_gap.png`](analysis/t1d_gap.png)), tolerance-first is flat at ~97–100% for any gap, while
anti-CD3-first recovers monotonically with the gap (59% at 0 → 100% at 1.5 yr): if anti-CD3 must
precede, you have to wait for the effector pool to recover before giving tolerance. Simultaneous
dosing is the worst protocol.

**Robustness — and a two-channel caveat.** Over a 5-parameter grid: in the Treg-sparing regime
(`rho<1`, matching teplizumab's documented Treg-sparing/expanding profile) tolerance-first ≥
simultaneous in **171/171 (100%) viable sets, never negative** (strictly better in 26; the rest
saturate). Including strongly Treg-depleting anti-CD3 (`rho≤1.1`), the optimal order **can invert**
(17/228 sets, all at the highest `rho`) — there are two antagonism channels, substrate-depletion
(favors tolerance-first) and Treg-destruction (favors anti-CD3-first), and which dominates is set by
how Treg-depleting anti-CD3 is. This yields a **second falsifiable prediction**: if anti-CD3 is
strongly Treg-depleting in vivo, the optimal order flips.

**Calibration.** A stage-2 cohort heterogeneous in effector severity and residual β-cell mass
reproduces the untreated progression curve: median time-to-diagnosis **2.06 yr** (TN10 placebo ~2.0
yr), **~45% progressed by 2 yr** (TrialNet stage-2 ~50%). The sequencing antagonism persists on this
clinically-anchored cohort (tol-only 100% → simultaneous 65% → anti-CD3-first 35% → tol-first 97%).

## Verifying the claim chain

Every headline number above is re-derived from the model modules and asserted within tolerance:

```bash
cd analysis && python3 verify_claims.py
```

This prints each check and exits 0 only if all pass (**24/24 PASS**). A regression in any module
trips a FAIL. The checks cover bistability, untreated ~2-yr progression, anti-CD3 delay-only
behavior, the cohort antagonism + sequencing fractions, the gap-sweep direction, the Treg-sparing
robustness invariant, and the high-`rho` order-inversion caveat.

## Running it

```bash
pip install -r requirements.txt        # numpy, scipy, matplotlib

cd analysis
python3 t1d_model.py                    # single-patient + cohort table (P1)
python3 t1d_experiments.py              # figures + t1d_results.npz (P2)
python3 t1d_calibration.py             # calibration table + figure (P3)
python3 verify_claims.py                # re-derive & assert every headline number
```

Rebuilding the literature corpus ([scan_results.md](analysis/scan_results.md) /
[raw_cache.json](analysis/raw_cache.json)) is optional and requires a Semantic Scholar API key; the
scan driver lives one level above the project at `../_scan/scan_all.py`:

```bash
S2_API_KEY=... python3 ../_scan/scan_all.py
```

## Provenance & caveats

This work was produced in a single interactive modeling session (2026-06) and is **illustrative**.
Parameters are illustrative beyond the one calibrated anchor (untreated stage-2 progression timing),
and the bistable switch makes outcomes binary per patient, so results are framed as cohort fractions.
Two honest limitations carry from [FINDINGS.md](analysis/FINDINGS.md): (1) the model **under-produces
the teplizumab monotherapy delay magnitude** (+0.68 yr here vs TN10's ~+2 yr) — a single short
anti-CD3 course only transiently debulks effectors, so the robust contribution is the *sequencing
antagonism*, not the monotherapy-delay magnitude; and (2) the antagonism is visible only in the
marginal-efficacy regime and is neutral where tolerance is overwhelmingly effective. The originating
observation (Foster 2025) is itself a conference abstract. See [MEMO.md](analysis/MEMO.md) for the
literature lane and [NOVELTY.md](analysis/NOVELTY.md) for the prior-art reconciliation.
