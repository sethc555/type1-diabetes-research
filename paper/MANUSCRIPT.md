# A calibrated, trial-validated within-host model of type 1 diabetes immunotherapy: failure modes, mechanism, and a testable stratification prediction

**Author:** Seth Cope¹  _(¹ Independent researcher. ORCID: [0009-0000-5520-915X](https://orcid.org/0009-0000-5520-915X))_

_Preprint draft — illustrative modeling study / hypothesis generation. Not validated experimental or
clinical findings. Convert to PDF (e.g. `pandoc MANUSCRIPT.md -o manuscript.pdf`) for posting._

> **Correction history.** This project's first public headline — a tolerance-first *sequencing antagonism*
> (Zenodo [10.5281/zenodo.20804558](https://doi.org/10.5281/zenodo.20804558)) — was **withdrawn** as an
> uncalibrated-operating-point artifact (external reviewer critique; [../analysis/AUDIT.md](../analysis/AUDIT.md)
> §"Post-publication reversal"). It was rebuilt from verified biology into the body reported here. The
> reversal is kept visible on purpose. A formal figure set is to be generated at publication; results below
> are reproduced from the per-layer `FINDINGS_*.md` and re-derived by the `verify_*.py` harness.

---

## Abstract

**Background.** Multiple disease-modifying immunotherapies are advancing in type 1 diabetes (T1D), yet most
trials fail, often in ways that are predictable in hindsight (wrong stage, wrong combination, wrong timing),
and no mechanistic framework spans them. **Methods.** We build a within-host model of the T1D immune attack,
grown layer by layer — each the smallest dynamical model reproducing a specific *unexplained, published*
result, then pushed to a falsifiable prediction, adversarially audited, and machine-verified — and then
calibrate its load-bearing parameters to trial data and validate them out-of-sample. **Results.** The body
spans the full disease arc (innate trigger → self-amplifying β-cell-stress→spreading loop → adaptive attack →
B-cell arm → metabolic readout, with genetics setting boundary conditions). The *same* framework reconciles
the contradictory Foster 2025 (co-dosing antagonism) and Mathieu 2023 (safe combination) results via a
platform axis; reproduces the teplizumab response biomarkers; predicts checkpoint-inhibitor-induced T1D; and
**explains why** anti-IL-1, single-antigen tolerance, and anti-CD20 trials failed (timing, escape,
transience). Calibration to TN10, TEDDY/Ziegler, Shields/PROTECT and Pescovitz reveals a two-clock
accelerating disease and cross-dataset consistency. In leave-one-trial-out validation the model predicts the
**natural history of held-out trials within ~2%**, while honestly bounding cross-stage drug-effect
extrapolation as unreliable. It yields one re-analysis-testable prediction: stratifying teplizumab by
baseline CD8 exhaustion should raise the response rate from ~56% to ~91%. **Conclusions.** A disciplined,
self-auditing within-host model can reconcile contradictory trials, explain failures, and produce a
falsifiable, decision-relevant stratification — without curing or validating anything. Illustrative modeling
hypothesis, conditional on the stated assumptions.

## 1. Introduction
T1D results from autoimmune destruction of insulin-producing β-cells, with a long pre-symptomatic prodrome
(stages 1–2) during which intervention can delay clinical (stage 3) disease. The field now has several
disease-modifying levers — anti-CD3 (teplizumab, the first approved), antigen-specific tolerance, anti-CD20,
anti-IL-1, β-protective agents — but trials mostly disappoint, and a growing list of "failures" looks, in
retrospect, like the *right drug at the wrong stage* or the *wrong combination*. Mechanistic within-host T1D
models exist — a T-cell-avidity / β-cell ODE lineage (Khadra & Pietropaolo 2011; Jaberi-Douraki et al.
2014–2015; Mahaffy & Edelstein-Keshet 2007) — and a recent prevention-trial simulator (Morales & Klose 2024)
informs trial design. What is missing is a single mechanistic framework that *spans these disease-modifying
interventions*, reconciles their contradictory results, says *why* specific trials failed, and is validated
out-of-sample with a stated boundary. We build on that lineage to do this — not to add a model, but to turn
scattered, contradictory trial results into a coherent, falsifiable, *calibrated* design rationale, honest
about exactly how far it can be trusted.

## 2. Model and methods (summary)
Each layer is the smallest within-host dynamical model reproducing a specific unexplained published result;
full equations, parameters, numerics, calibration, and validation protocols are in
[`../analysis/METHODS.md`](../analysis/METHODS.md), and each layer's results + caveats in its
`FINDINGS_*.md`. Models are deterministic ODEs (`solve_ivp`, LSODA) except the combination layer, which is
discrete-clonal/stochastic because the Foster antagonism is *sub-continuum*. Recurring motifs: an
effector↔Treg / self-activation n-Hill switch; a β-cell-stress feedback loop (stress → HLA/neoantigen →
amplified attack); a waning anti-CD3 exhaustion imprint; threshold-gated spreading and ignition. Every model
runs under a 4 GB cap; **19 `verify_*.py` scripts** assert every headline number; a standing assumption
registry (`assumptions.json` + `validate.py`) catalogs every assumption and surfaces blind spots.

## 3. Results

**3.1 A connected arc that lands real data.** Built independently, the layers reproduce or predict ~8
independent datasets/trials. The **combination** layer (discrete-clonal) reproduces the Foster 2025 co-dosing
antagonism as a stochastic substrate-depletion effect that *sequencing avoids*, and a **platform axis**
reconciles it with the safe Mathieu 2023 human trial (conversion-type platforms antagonize; expansion-type do
not); the **avidity** layer shows the continuum *cannot* produce the antagonism — a structural negative. The
**responder** layer reproduces both teplizumab biomarkers (baseline exhaustion → responder, Wiedeman 2019;
TSCM renewal → non-responder, Dufort 2026). The **hierarchy** layer predicts checkpoint-inhibitor-induced T1D
(a documented clinical fact) and carries the cancer/HIV sign-flip. The **β-cell**, **spreading**, **B-cell**,
**metabolic**, and **innate** layers add the self-amplifying stress hub, epitope spreading, the anti-CD20
arm, the C-peptide/glucose readout, and the upstream innate trigger; **genetics** sets the boundary
conditions from real HLA odds ratios.

**3.2 A convergent thesis: why interventions fail, and what would work.** The layers independently arrive at
one shape of answer — single-agent immunotherapy is structurally limited (n-fragile, escaped, transient, or
partial), and durable benefit needs (i) cutting the shared β-cell-stress→spreading engine, (ii) pairing
orthogonal modalities, (iii) timing/sequencing. Concretely, the model **explains documented failures**:
anti-IL-1 failed because given at clinical onset, after the adaptive attack self-sustains (Moran 2013) — and
is predicted to work as *prevention*; single-antigen tolerance is *escaped by epitope spreading* (rescued by
early or broad tolerance, or β-protection); anti-CD20 is *transient* because B cells repopulate
(Pescovitz 2014), needing a durable partner; co-dosed anti-CD3 + conversion-tolerance *antagonize* by
substrate competition. These are failure-mode *explanations*, each checkable.

**3.3 Calibration: a two-clock, accelerating disease, with cross-validation.** Fitting the load-bearing
parameters to four trials (TN10, TEDDY/Ziegler, Shields/PROTECT, Pescovitz) pins a pre-clinical clock
(~0.12/yr) and a final-approach clock (~0.6/yr) — the disease *accelerates ~3–5×* as it progresses, as the
self-amplifying hub predicts. Two cross-validations a free-knob model could not produce: the ~0.6/yr late
rate emerges from *two unrelated cohorts* (TN10 progression and the post-diagnosis C-peptide decline,
agreeing within 6%), and the anti-CD3 effect fit on stage-2 prevention *predicts* the PROTECT stage-3
C-peptide preservation. Identifiability is reported honestly: the timescale is pinned, the
`kappa`-vs-effector-burden split is not.

**3.4 Out-of-sample validation, and an honest boundary.** In leave-one-trial-out validation, the model
predicts the **natural history of trials it was never fit to within ~2%** (the C-peptide half-life from the
TN10 progression rate; the Ziegler 15-year progression from the 5-year point). But **cross-stage drug-effect
extrapolation fails** (39–132%): the anti-CD3 effect is not the same in stage 2 vs stage 3. The measured
verdict — *quantitative for natural history; a per-stage tool, not an extrapolator, for therapy* — is the
decision-grade boundary, and is itself a useful negative result.

**3.5 A decision-relevant, re-analysis-testable prediction.** Formalizing the responder mechanism into a
baseline-exhaustion score reproduces the AbATE response rate (~56% vs ~50% observed) and the Long 2016 /
Wiedeman 2019 biomarker direction, and predicts the **enrichment from stratification**: ~56% (unselected) →
~91% (exhaustion-high) / ~25% (exhaustion-low). This is testable on *existing* AbATE/TN10/PROTECT data
without a new trial: if a re-analysis by the baseline-exhaustion (or TSCM) signature recovers an enrichment
of this size, *"teplizumab works, in the exhaustion-high subgroup"* becomes an evidenced, actionable claim.

## 4. Derived analytic results (the model → closed-form → number chain)
Several headline results follow in *closed form* from the model equations, so a reviewer can check the
model→formula→number chain by hand; `analytic.py` (asserted by `verify_analytic.py`, 7/7) re-derives each
and verifies it against the real value.

**(i) The two clocks, exactly.** The pre-clinical natural history is a *linear* compartmental chain
S₁ →(s) S₂ →(h₂) D (single → multiple autoantibody → clinical; direct single-Ab progression h₁=0), with exact
solutions — from the multiple-Ab state, D(t)=1−e^(−h₂t) ⟹ **h₂ = −ln(1−F)/t**; from the single-Ab state,
D(t)=1−e^(−st)−[s/(h₂−s)](e^(−st)−e^(−h₂t)). Fitting h₂ to 44% at 5 yr (Ziegler) gives h₂=0.116/yr and
reproduces 69%/82% at 10/15 yr (obs 70/84); fitting s to single-Ab 14.5% at 10 yr gives the spreading rate
s≈0.04/yr. The final-approach clock is the post-diagnosis C-peptide decline C(t)=C₀e^(−kt), half-life
**t½ = ln2/k**; Shields' t½=1.10 yr gives k=0.63/yr — equal within 6% to the late-disease kill rate κ=0.60/yr
calibrated *independently* from the TN10 median. The same ~0.6/yr rate from two unrelated datasets is a
closed-form cross-validation.

**(ii) The anti-CD20 transient shift, in closed form.** With β-cell kill scaled by B-cell help
help(t)=T_dom+(1−T_dom)B_c(t) and exponential C-peptide decline, the net curve shift is the integrated loss
of help, Δ=∫₀^∞(1−help)dt=(1−T_dom)∫₀^∞(1−B_c)dt. For logistic repopulation from B_c0 at rate r_bc,
∫₀^∞(1−B_c)dt=(1/r_bc)·ln(1/B_c0) exactly, giving **Δ = (1−T_dom)·(1/r_bc)·ln(1/B_c0)**. With the calibrated
T_dom=0.18, r_bc=4.7/yr, B_c0=0.02 this is **Δ = 8.2 months** — the exact shift Pescovitz 2014 reported.

**(iii) Why the validation boundary exists, analytically.** Stage-2 progression is dB/dt=ρ_B·B(1−B)−κ·B; to
leading order the onset time is T=ln(B₀/B_clin)/κ and teplizumab (κ→κ(1−eff)) gives T_tep/T_pbo=1/(1−eff) —
*linear* readings. But the logistic regeneration term makes T(κ) nonlinear, so the *effective* drug effect is
regime-dependent (no-regen eff=50% vs full-ODE 24%). That is precisely why cross-stage drug-effect transfer
fails in leave-one-trial-out (39–132%) while the *linear* natural-history rates in (i) transfer to ~2%: the
analytic structure predicts the empirical trust boundary.

**(iv) The structural negative, as a scaling argument.** The Foster co-dosing antagonism requires anti-CD3 to
drive the small converting-clone count to *zero* before conversion completes; for a converting pool of mean
size n, P(extinction during the pulse) ~ e^(−c·n) → 0 in the continuum (n→∞) limit. A continuum / avidity-
resolved density never reaches zero, so it *cannot* produce the antagonism — discrete-clonal/stochastic
resolution is required (the van Kampen system-size boundary). Hence the avidity continuum predicts synergy
while only the discrete-clonal model reproduces Foster.

## 5. Discussion
Building on the mechanistic within-host T1D lineage (Khadra/Jaberi-Douraki avidity; the β-cell and
autoantibody ODE models), what we add is a single framework that spans these disease-modifying interventions,
reconciles their contradictory trial results, explains specific failures mechanistically, and is validated
out-of-sample with an explicit failure boundary — a combination we did not find in the surveyed literature.
Its value is not a cure or a discovery — every constituent mechanism is established biology — but a *reasoning
and prioritization layer*: a falsifiable map of why interventions fail and what to test next.
The strongest "more than parameter-fitting" evidence is two-fold: a **knob-independent structural negative**
(the avidity continuum cannot make Foster's antagonism) and **cross-dataset consistency** (the same rate from
two cohorts; a drug effect fit on one stage predicting another) — neither of which free parameters can
produce. The single most actionable output is the stratification prediction (§3.5), which a network holding
the trial data (e.g. TrialNet) could check directly.

**Limitations.** This is illustrative throughout. (i) Magnitudes are illustrative beyond the calibrated
spine; the robust outputs are directions, structural results, and the validated *rates*. (ii) Calibration is
to *summary* trial statistics, not individual-level data; not all parameters are identifiable (the timescale
is pinned, its decomposition is not). (iii) The model is a per-stage tool — cross-stage therapy effects do
**not** extrapolate (§3.4), measured at 39–132% error. (iv) The conscious structural simplifications (a
single severity knob; the still-excluded environmental trigger) and the conceptual-frame limit (the
validator's own caveat: it cannot see unknown-unknowns) are stated in `validate.py` and the registry. (v) One
prior headline was already wrong and withdrawn — the reason the framing throughout is hypothesis-level, and
the reason the audit trail and machine-verification are part of the contribution, not an afterthought.

## 6. Data and code availability
All code, the literature corpus, the verification harness, the assumption registry/validator, and the audit
trail are openly available: https://github.com/sethc555/type1-diabetes-research (the withdrawn v1 is archived
at Zenodo DOI 10.5281/zenodo.20804558; a corrected-version DOI is pending the publish decision). Running
`cd analysis && python3 validate.py --run` re-derives every headline number (the full `verify_*.py` harness),
and `python3 analytic.py` re-derives the closed forms of §4.

## 7. Disclosures
**Status:** illustrative within-host modeling / hypothesis generation; not validated experimental or clinical
findings, not medical advice. **AI assistance:** developed with substantial help from an AI
coding/analysis assistant (Anthropic Claude) for implementation, derivation, audit, and drafting, under the
author's direction; AI tools are not authors. **Competing interests:** none. **Funding:** none.

## 8. References (key — full prior-art assessment in [`../analysis/NOVELTY.md`](../analysis/NOVELTY.md))

1. Foster J, et al. Anti-CD3 reduces the efficacy of antigen-specific immunotherapy in NOD mice. *Diabetes* 2025; 74(Suppl 1), 2136-LB.
2. Mathieu C, et al. (AG019 ± teplizumab, antigen-specific tolerance, human). 2023.
3. Herold KC, et al. (TN10) An anti-CD3 antibody, teplizumab, in relatives at risk for type 1 diabetes. *N Engl J Med* 2019; 381:603–613.
4. Ramos EL, et al. (PROTECT) Teplizumab and β-cell function in newly diagnosed type 1 diabetes. *N Engl J Med* 2023.
5. Ziegler AG, et al. Seroconversion to multiple islet autoantibodies and risk of progression to diabetes. *JAMA* 2013; 309:2473–2479.
6. Vehik K, et al. Hierarchical order of autoantibody spreading and progression to T1D (TEDDY). *Diabetes Care* 2020; 43:2066.
7. Shields BM, et al. C-peptide decline in type 1 diabetes has two phases. *Diabetes Care* 2018; 41:1486–1492.
8. Pescovitz MD, et al. Rituximab, B-lymphocyte depletion, and β-cell function (and 2-year results). *N Engl J Med* 2009; *Diabetes Care* 2014.
9. Moran A, et al. Interleukin-1 antagonism in type 1 diabetes of recent onset (AIDA/TN-14). *Lancet* 2013; 381:1905–1915.
10. Long SA, et al. Partial exhaustion of CD8 T cells and clinical response to teplizumab. *Sci Immunol* 2016; 1:eaai7793.
11. Erlich H, et al. HLA DR-DQ haplotypes and genotypes and type 1 diabetes risk (T1DGC). *Diabetes* 2008; 57:1084–1092.
12. Sharp SA, et al. Development and standardization of an improved T1D genetic risk score (GRS2). *Diabetes Care* 2019; 42:200–207.

*Prior within-host T1D models (the lineage this work builds on):*
13. Khadra A, Pietropaolo M, et al. Investigating the role of T-cell avidity and killing efficacy in relation to type 1 diabetes progression. *PLoS ONE* 2011; 6:e14796. doi:10.1371/journal.pone.0014796.
14. Jaberi-Douraki M, Schnell S, Pietropaolo M, Khadra A. Unraveling the contribution of pancreatic β-cell suicide in autoimmune type 1 diabetes. *J Theor Biol* 2014. doi:10.1016/j.jtbi.2014.05.003.
15. Jaberi-Douraki M, et al. Predictive models of type 1 diabetes progression: T-cell cycles and their implications on autoantibody release. *PLoS ONE* 2014; 9:e93326. doi:10.1371/journal.pone.0093326.
16. Jaberi-Douraki M, Pietropaolo M, Khadra A. Continuum model of T-cell avidity: autoreactive and regulatory T-cell responses in type 1 diabetes. *J Theor Biol* 2015. doi:10.1016/j.jtbi.2015.07.032.
17. Mahaffy JM, Edelstein-Keshet L. Modeling cyclic waves of circulating T cells in autoimmune diabetes. *Bull Math Biol* 2007.
18. Morales JF, Klose M, et al. Type 1 diabetes prevention clinical trial simulator: case reports of a model-informed drug development tool. *CPT Pharmacometrics Syst Pharmacol* 2024. doi:10.1002/psp4.13193.
