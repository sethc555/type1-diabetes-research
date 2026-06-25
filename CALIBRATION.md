# Calibration — pinning the knobs to data, and what it revealed

> Companion to [SYNTHESIS.md](SYNTHESIS.md). The synthesis is the *mechanism* capstone; this is the
> *data-anchoring* capstone. After the model body was built, the **load-bearing, outcome-determining knobs
> were fit to published trial/natural-history curves** — turning a "consistency engine with free knobs" into
> something whose quantitative claims carry weight *and* cross-validate. Status: illustrative modeling;
> fits are to **summary** data (not individual-level), honestly bounded below.

## The four calibrations
Each fits a load-bearing parameter to a real curve, and is machine-checked (`verify_calib_*.py`).

| # | parameter | real anchor | fitted value | verify |
|---|---|---|---|---|
| 1 | disease **timescale** `kappa` | TN10 placebo median 24.4 mo (Herold 2019) | **0.60/yr**; anti-CD3 effect **24%** → teplizumab 48.4 mo | 5/5 |
| 2 | **spreading** rate | Ziegler 2013 / TEDDY (44/70/84% multi-Ab; 14.5% single) | **0.04/yr**; multi-Ab hazard **0.12/yr** | 5/5 |
| 3 | **C-peptide** decline | Shields 2018 (47%/yr, t½ 1.10 yr) + PROTECT | **0.63/yr** | 4/4 |
| 4 | anti-CD20 **transience** | Pescovitz 2009/2014 (69%@12mo; 8.2-mo shift) | `r_bc` **4.7/yr**, `Tdom` **0.18** | 5/5 |

## What calibration *revealed* (beyond pinning numbers)

**1 — The disease has two clocks, and it accelerates.** The pre-clinical clock (multiple-Ab → clinical,
TEDDY/Ziegler) is **~0.12/yr** (median ~5.8 yr); the final-approach clock (stage 2 → clinical, TN10) is
**~0.6/yr** (median ~2 yr). The disease **accelerates ~3–5× as it progresses** — exactly what the
self-amplifying stress hub predicts. The acceleration is now *measured*, not assumed.

**2 — Cross-validation #1: the same late-disease rate from two unrelated datasets.** `kappa` from TN10
stage-2 progression (0.60/yr) and the post-diagnosis C-peptide decline rate from Shields (0.63/yr) agree
**within 6%** — two different cohorts, two different measurements, one rate. A free-knob model can't claim
this; free knobs absorb each dataset separately.

**3 — Cross-validation #2: a drug effect that transfers across stages.** The anti-CD3 effect fit on TN10
*stage-2 prevention* (24%) **predicts** the PROTECT *stage-3* C-peptide preservation (model 0.10 vs ~0.16
fractional, same ballpark). A prediction, not a fit.

**4 — Mechanism-confirming fits.** "Clinical progression *requires* spreading" (`h1=0` fits the single-Ab
14.5% only via spreading-then-progress). The anti-CD20 benefit is a **finite ~8.2-month shift** then a
parallel decline (Pescovitz 2014) — so it must be paired with a durable agent. And the Pescovitz-fit
`Tdom`≈0.18 independently matches the bcell layer's illustrative 0.20.

## Identifiability — what the data pins vs what it can't (honest)
- **Pinned:** the disease *timescale(s)*, the spreading *rate*, the C-peptide *decline rate*, the anti-CD20
  *transience window* — and the cross-dataset *consistency* of the late rate.
- **Not pinned:** `kappa` in isolation (the median fixes the product `kappa×E` and the ratio `B0/B_clin`;
  `kappa`=0.50–0.70/yr across those assumptions). The `kappa`-vs-effector-burden split is unidentifiable
  from these data. Stated, not hidden.
- **Still free:** only the *load-bearing* rates were calibrated; many secondary parameters remain
  illustrative. This is calibration of the spine, not the whole skeleton.

## The epistemic upgrade — the honest answer to "is it just knobs?"
Before calibration the honest "more than knobs" residue was **one** knob-*independent* result (the structural
negative: Foster's antagonism is sub-continuum). Calibration added a second, stronger kind: **cross-dataset
consistency** — the same rate from two cohorts, and a drug effect fit on one stage predicting another. That
is something free knobs *cannot* produce. So the model is no longer "known biology with free dials": its
spine is **fit to data and cross-validated**, with the un-identifiable parts clearly labeled.

It is still illustrative, still hypothesis-level, still fit to *summary* curves. But "just knobs" is no
longer the right description of the calibrated spine — and the places where it *is* still knobs are named.
