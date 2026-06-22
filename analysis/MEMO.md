# T1D modeling-lane memo — where the momentum is, and the open lane

_Derived from `scan_results.md` (126 papers, 12 topics, scanned 2026-06-21)._

## 1. Where the momentum is

- **Teplizumab response heterogeneity is the field's live obsession.** The 2025–26 frontier is no longer "does anti-CD3 work" but "who responds, and why." See Sassi et al. 2025 (_JCI_, neutrophil-enriched signature → teplizumab **resistance**), Lledó-Delgado et al. 2025 (_Nat Commun_, latent EBV **enhances** anti-CD3 efficacy), Roma-Wilson & Pozzilli 2025 (_JDC_, "which endotype is most suitable for anti-CD3 trials"), and Sims et al. 2023 (_Diabetologia_, high proinsulin:C-peptide ratio marks high-progression-risk responders).
- **Combination/sequencing of immunotherapies is producing surprising antagonism that nobody has explained.** Foster et al. 2025 ("2136-LB", NOD mice): **anti-CD3 mAb REDUCES the efficacy of antigen-specific mRNA/RNA immunotherapy.** Greenbaum et al. 2026 and Denroche et al. 2025 push antigen-specific tolerance (PPI + TGF-β/IL-10/IL-2 plasmid; tolerogenic LNP) as combination partners. Wouters et al. 2026 frames the whole problem as "stage-specific challenges."
- **The pre-clinical β-cell decline curve is being quantitatively pinned down.** Montaser et al. 2026 (_Diabetes_): a metabolic **inflection point ~1–2 yr before diagnosis** of accelerated β-cell decline, from TrialNet OGTTs. Carr et al. 2026 ("2382-P"): stage-specific β-cell responsiveness (φtotal, Oral Minimal Model) trajectories aligned to S1/S2 transitions.
- **Staging is being made probabilistic and individualized.** Sims et al. 2025 (IA-2A positivity → faster progression within stages); Ghalwash et al. 2024 (data-driven autoantibody phenotypes); Steck/Triolo 2025 (genetic risk modulates stage transitions). Staging is heterogeneous, not deterministic.
- **"Modeling" in this field is statistical/ML, not mechanistic.** Patil et al. 2024 (gradient-boosting on single-cell islets), Montaser 2026 (survival/ML), Ghalwash 2024 (similarity clustering). The only mechanistic-dynamics mention is Karaoglu et al. 2025 (review-level, immune-evasive β-cell computational modeling). **No within-host ODE of Treg/effector/β-cell coupled to clinical C-peptide exists in the scan.**
- **CD8 effector exhaustion sets progression rate.** Wiedeman et al. 2019 (most-cited, 138) — autoreactive CD8 exhaustion distinguishes slow progressors; Schroderus et al. 2024 — temporal CD8 shifts S1→S3. Exhaustion state is a tunable model variable.

## 2. Candidate open modeling lanes

**Lane A — Sequencing antagonism between anti-CD3 and antigen-specific tolerance.**
Joins (i) anti-CD3 pharmacodynamics literature (Mamidi 2026; Sassi 2025) with (ii) antigen-specific Treg-induction literature (Greenbaum 2026; Serr 2016; Cabello-Kindelan 2019). _Open:_ Foster 2025 shows anti-CD3 BLUNTS antigen-specific immunotherapy in NOD, but no mechanistic model explains it (hypothesis: anti-CD3 transiently deletes/cycles the very effectors-in-transit that antigen therapy needs to re-educate into Tregs). _Calibrate to:_ NOD combination diabetes-incidence curves + TN10 stage-2 delay.

**Lane B — Window optimization: when in the silent prodrome does teplizumab bank the most β-cell mass?**
Joins (i) TrialNet staging/progression-rate literature (Montaser 2026; Sims 2025) with (ii) teplizumab PD/response literature (Sims 2023; Mathieu 2025). _Open:_ the inflection point (Montaser) and φtotal trajectories (Carr) now give a calibratable decline curve, but no model couples Treg/effector dynamics to it to ask the **timing** question mechanistically. _Calibrate to:_ TN10 (~2 yr median delay), Montaser inflection ~1–2 yr pre-dx, Carr φtotal S1/S2 curves.

**Lane C — Responder/non-responder bistability from exhaustion + immune-context.**
Joins (i) CD8 exhaustion literature (Wiedeman 2019; Schroderus 2024) with (ii) teplizumab-response-modifier literature (Lledó-Delgado EBV 2025; Sassi neutrophil 2025). _Open:_ no model treats "response vs resistance" as an exhaustion-driven bistable attractor. _Calibrate to:_ slow- vs fast-progressor C-peptide slopes; EBV+ vs EBV− response split.

## 3. Recommended lane

**Lane A (sequencing antagonism), absorbing Lane B's timing axis.** It attaches to a concrete, published, *unexplained* result (Foster 2025), sits squarely at the un-joined intersection of two active drug literatures, and is purely computational. **Falsifiable prediction:** _a coupled Treg/effector/β-cell ODE+stochastic model will show that anti-CD3 given **before** antigen-specific tolerance therapy nets less banked β-cell mass than the reverse order or a delay/gap — with a predicted optimal inter-drug interval that maximizes Treg conversion, recovering the Foster antagonism only in the simultaneous/anti-CD3-first arm._

## 4. Closest prior art to reconcile/extend

- Carr et al. 2026 ("2382-P") — Oral Minimal Model φtotal stage-specific β-cell trajectories (calibration backbone for β-cell compartment).
- Montaser et al. 2026 — ML inflection-point model (provides decline-acceleration timing; my model must reproduce it mechanistically).
- Patil et al. 2024 (_Cell Rep Med_) — ML progression model (statistical baseline to beat with mechanism).
- Wiedeman et al. 2019 — CD8 exhaustion as progression-rate determinant (sets effector-state variable).
- Karaoglu et al. 2025 — the one computational-modeling review in T1D (situate against).
- Cabello-Kindelan 2019 / Serr 2016 — Treg-induction kinetics (parameterize Treg conversion term).

## 5. Key calibration anchors

- **TN10 teplizumab (stage 2):** ~2-year median delay to stage 3; single 14-day course. (Mathieu 2025; Zaitoon 2025; TEPLI-REAL real-world cohort, Gitelman 2026.)
- **Metabolic inflection point:** accelerated β-cell decline begins **~1–2 yr before diagnosis** (Montaser 2026, TNPTP OGTTs).
- **Stage-specific β-cell decline:** φtotal trajectories aligned to 4 yr pre-S1 and S1→S2 transition (Carr 2026); MMTT/DBS C-peptide slopes (Hendriks 2025; Dunseath 2026 USTEKID).
- **Progression-rate modifiers:** IA-2A+ accelerates within/across stages (Sims 2025); PI:C ratio marks high-risk teplizumab responders (Sims 2023); EBV+ enhances response (Lledó-Delgado 2025).
- **Combination antagonism (target to reproduce):** anti-CD3 reduces antigen-specific-immunotherapy efficacy in NOD incidence curves (Foster 2025, "2136-LB").
- **Stage-2 baseline progression:** ~11%/yr to stage 3 (multiple-autoantibody+dysglycemia) per TrialNet staging (Phillip et al. 2024 consensus).
