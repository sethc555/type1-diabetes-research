# Methods

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> This documents the *current* multi-layer body. Each model's exact equations live in its own file's
> `rhs()` (the source of truth) and are described in the matching `FINDINGS_*.md`; this file gives the
> shared methodology, the model inventory, the numerics, and the calibration/validation/verification
> protocols. The original (withdrawn) v1 3-state model is documented separately in §8.

## 1. Modeling approach
Each layer is the **smallest within-host dynamical model** that reproduces a specific *unexplained,
published* result, then is pushed to a falsifiable prediction, adversarially audited, and machine-verified
(the cluster method, `../../METHOD.md`). Models are deterministic ODEs (`scipy.integrate.solve_ivp`) except
the combination layer, which is discrete-clonal/stochastic (tau-leaping) because the Foster antagonism is a
*sub-continuum* effect. Recurring motifs: an effector↔Treg / effector self-activation **n-Hill switch**; a
**β-cell-stress feedback loop** (stress → HLA/neoantigen → amplified attack); a durable-but-waning
**exhaustion imprint** (anti-CD3); and **threshold-gated** processes (spreading, ignition). Time is in
**years**; β-cell mass `B`∈[0,1] (∝ C-peptide). Every model runs under a hard **4 GB cap**
(`ulimit -v 4194304; timeout 595`).

## 2. Model inventory
Each model is a standalone `t1d_*.py` with a `main()` that prints its predictions and a `verify_*.py` that
asserts them (exit 0 ⇔ pass). Equations: see each file's `rhs()`; results + caveats: the `FINDINGS_*.md`.

| model | captures | reproduces (real anchor) | verify |
|---|---|---|---|
| `t1d_clonal.py` | discrete-clonal/stochastic combination + platform axis | Foster 2025 antagonism; Mathieu 2023 safety | `verify_clonal.py` 7/7 |
| `t1d_avidity.py` | avidity-resolved continuum (the structural negative) | Foster antagonism is **sub-continuum** | `verify_avidity.py` 2/2 |
| `t1d_responder.py` | teplizumab responder = exhaustion-vs-TSCM balance | Wiedeman 2019 + Dufort 2026 biomarkers | `verify_responder.py` 6/6 |
| `t1d_hierarchy.py` | progenitor→effector→exhausted ladder | checkpoint-inhibitor-induced T1D | `verify_hierarchy.py` 6/6 |
| `t1d_betacell.py` | β-cell stress feedback; β-protection axis | self-amplifying loop; safe combination | `verify_betacell.py` 4/4 |
| `t1d_spreading.py` | primary antigen + stress-driven spreading | why single-antigen tolerance is escaped | `verify_spreading.py` 7/7 |
| `t1d_bcell.py` | B cells as APCs; anti-CD20 + repopulation | Pescovitz 2014 transience; Linsley 2018 axis | `verify_bcell.py` 6/6 |
| `t1d_metabolic.py` | C-peptide + glucose readout; glucotoxicity | Mortensen 2009 honeymoon; McVean 2023 | `verify_metabolic.py` 7/7 |
| `t1d_innate.py` | innate trigger primes the adaptive attack | Moran 2013 anti-IL-1 failure (timing) | `verify_innate.py` 7/7 |
| `t1d_genetics.py` | genotype→parameter map (calibration bridge) | Erlich 2008 / Sharp 2019 / Bauer 2019 | `verify_genetics.py` 4/4 |

Helper/robustness scripts (`t1d_clonal_{calib,robust,schedule}.py`, `t1d_switch_robust.py`) explore the
clonal regime/robustness; their claims fold into `verify_clonal.py` and the FINDINGS.

## 3. Numerics
`solve_ivp`, method **LSODA**, `rtol=1e-8`, `atol=1e-10`, bounded `max_step` (≈0.01–0.02 yr); states floored
at 0 in the RHS; intervention courses are square pulses (anti-CD3 ~14 d, tolerance ~30 d, β-protection
sustained). Deterministic models give exact, reproducible numbers (verify asserts values, not just
direction). The clonal model uses Poisson tau-leaping and is checked for **seed-robustness**. Outcomes:
β-mass / C-peptide at a horizon; cohort fractions where a switch makes per-patient outcomes binary;
median time-to-clinical for progression curves.

## 4. Calibration (fit to trial summary data)
Load-bearing, outcome-determining parameters are fit to **published summary statistics** (not
individual-level data). Four calibrations (`calib_*.py`, each machine-checked):

| parameter | anchor | fit |
|---|---|---|
| disease timescale `kappa` | TN10 placebo median 24.4 mo (Herold 2019); teplizumab 48.4 mo | 0.60/yr; anti-CD3 effect 24% |
| spreading rate | Ziegler 2013 / TEDDY (44/70/84%; single-Ab 14.5%) | 0.04/yr; multi-Ab hazard 0.12/yr |
| C-peptide decline | Shields 2018 (47%/yr, t½ 1.10 yr) | 0.63/yr |
| anti-CD20 transience | Pescovitz 2009/2014 (69%@12mo; 8.2-mo shift) | r_bc 4.7/yr, Tdom 0.18 |

Calibration reveals a **two-clock accelerating disease** (pre-clinical ~0.12/yr → final ~0.6/yr) and two
**cross-validations** (the ~0.6/yr late rate from TN10 *and* the C-peptide decline, agreeing within 6%; the
anti-CD3 effect transferring TN10→PROTECT). **Identifiability is reported honestly**: the timescale is
pinned, but `kappa`-vs-effector-burden is not (the median fixes their product); see `CALIBRATION.md`.

## 5. Out-of-sample validation (leave-one-trial-out)
`loo_validation.py` predicts each held-out trial endpoint from parameters calibrated only on the others.
**Natural-history RATE predictions validate to ~2%** (e.g. the C-peptide half-life predicted from the TN10
progression rate; Ziegler 15-yr from the 5-yr point). **Cross-stage DRUG-EFFECT extrapolation fails**
(39–132%): the anti-CD3 effect differs between stage 2 and stage 3. Verdict: *quantitative for natural
history; a per-stage tool, not an extrapolator, for therapy* — a measured trust boundary (`verify_loo.py`).

## 6. Decision-relevant output
`responder_classifier.py` formalizes the responder mechanism into a baseline-exhaustion score and predicts
the **enrichment** from stratifying teplizumab on it: ~56% (unselected) → ~91% (exhaustion-high) / ~25%
(exhaustion-low). The rate (~50%, AbATE) and direction (Long 2016/Wiedeman 2019) are reproduced; the
enrichment *magnitude* is the forward, re-analysis-testable bet (`verify_responder_classifier.py`).

## 7. Verification and the assumption registry
**19 `verify_*.py` scripts** re-derive and assert every headline number; `validate.py --run` executes them
all under the cap. **`assumptions.json` + `validate.py`** are a standing registry: every assumption is
tagged (role/status/controversy/evidence/governed-parameters); the validator prints a dashboard, a
*dig-here* queue (load-bearing-but-unsettled), and a **blind-spot surfacer** (model parameters with no
catalogued assumption — and it flags, not silently skips, any model it cannot parse). It prints its own
limit: it cannot see conceptual-frame unknown-unknowns. Audits and retractions: `AUDIT.md`,
`ASSUMPTIONS_AUDIT.md`.

## 8. The original (withdrawn) v1 model — kept for the record
The first study was a **3-state ODE** (β-mass `B`, effectors `E`, antigen-specific Tregs `R`) forming a
mutual-repression bistable switch, in `t1d_model.py` (+ `t1d_experiments.py`, `t1d_calibration.py`,
`t1d_analytic.py`, and the verified-biology rebuilds `t1d_model_v2/v3/v4.py`), verified by
`verify_claims*.py`. Its headline — a tolerance-first *sequencing antagonism* — was **withdrawn** as an
uncalibrated-operating-point artifact (`AUDIT.md` §reversal). It is retained because the correction trail is
part of the work's integrity, and because the discrete-clonal `t1d_clonal.py` later reproduced the *real*
(Foster) antagonism as a sub-continuum, co-dosing effect — superseding the v1 explanation.
