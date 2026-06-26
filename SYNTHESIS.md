# Synthesis — what the whole model says

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> This is the capstone of a nine-layer exploration ([README.md](README.md) is the per-layer tour). It
> states the one thesis the layers converged on, maps every modality onto it, and tiers every claim by
> how much it is actually backed. It is run honesty-first: machine-checkable claims, a standing assumption
> registry ([analysis/assumptions.json](analysis/assumptions.json) + [validate.py](analysis/validate.py)),
> Semantic-Scholar grounding, and one publicly-reversed headline kept visible on purpose
> ([AUDIT.md](analysis/AUDIT.md) §reversal). The value here is a *coherent, falsifiable framework*, not proof.

---

## The thesis

Built one at a time — each to answer a different clinical question, each grounded in different papers —
the six layers kept arriving at the **same shape of answer**:

> **Single-agent immunotherapy is structurally limited in type 1 diabetes — each agent fails in a
> characteristic way — and durable benefit emerges from (1) cutting the shared engine that drives the
> disease, (2) pairing modalities that act on orthogonal axes, and (3) timing/sequencing to avoid
> antagonism and pre-empt epitope spreading.**

Nothing forced this. The convergence *emerged* from independently-built layers, which is why it is worth
stating as a result rather than a framing.

---

## The shared engine (the hub)

The layers are not independent diseases — they are views of **one feedback loop**:

```
   β-cell STRESS ──► neoantigens / HLA-I up ──► new T-cell specificities (SPREADING)
        ▲                                              │
        │                                              ▼
        └──────────  effector attack on β  ◄──  B cells present the new antigens
```

- The **β-cell-stress loop** (`t1d_betacell.py`, AB1) generates the neoantigens that…
- …drive **epitope spreading** (`t1d_spreading.py`, AE1), which…
- …**B cells present** as APCs (`t1d_bcell.py`, BC1), feeding the effector attack that stresses β-cells.

This is why one intervention — **β-protection** (verapamil; AB4) — keeps reappearing as helpful across
layers: it throttles the *engine*, not just one output. Cutting stress slows spreading (5→1 antigens) and
rescues single-antigen tolerance. The hub is the reason the layers cohere.

**Glucose feeds the same hub.** Hyperglycemia generates the *same* oxidative/ER stress (`t1d_metabolic.py`,
AM1; Gerber & Rutter 2017), so **glucotoxicity** is another input to the loop — making glucose control a
(modest) throttle on it, and letting the body finally read out in **C-peptide and glucose**, the units trials
actually report.

**And innate IFN-α lights the loop.** Upstream of everything, the innate trigger (neutrophils/NETs/IFN-α;
`t1d_innate.py`, AI1) drives β-stress (IFN-α → HLA-I + ER stress; Marroqui 2017) *and* primes the adaptive
attack — which then self-sustains. So the full arc is **innate trigger → β-stress hub → adaptive attack →
spreading → metabolic collapse**, one connected loop from initiation to clinical readout.

---

## The intervention map

Every modality, its axis, how it fails *alone*, and what rescues it:

| modality | acts on | characteristic single-agent failure | rescue (from the model) |
|---|---|---|---|
| **anti-CD3** (teplizumab) | debulks/exhausts effectors | durable but **wanes**; **co-dosing** with conversion-tolerance **antagonizes** (deletes the converting clones) | **sequence** it (tolerance→anti-CD3); re-dose |
| **antigen tolerance, conversion-type** (mRNA) | converts effector→Treg | weak alone; **escaped by spreading**; antagonized by co-dosed anti-CD3 | **broad** + **early** + **β-protection**; don't co-dose anti-CD3 |
| **antigen tolerance, expansion-type** (IL-10/TGF-β) | expands Tregs (substrate-independent) | weak alone | **safe** with anti-CD3 (no substrate competition → no antagonism) |
| **β-protection** (verapamil) | protects β; **cuts stress→neoantigen→spreading** | doesn't clear autoimmunity | orthogonal & safe **adjunct**; rescues single-antigen tolerance |
| **anti-CD20** (rituximab) | depletes B-cell APCs; cuts spreading-driver | **transient** (B cells repopulate); fails if **T-dominated** | pair with a **durable** agent (tolerance) |
| **insulin / glucose control** | the metabolic arm (cuts glucotoxicity) | **modest alone** — the immune attack dominates (McVean 2023) | an **independent, additive** adjunct to disease-modifying therapy |
| **anti-IL-1 / anti-innate** (anakinra, canakinumab) | the upstream innate trigger | **fails at onset** — the adaptive attack already self-sustains (Moran 2013) | give as **prevention** (stage 1–2), *before* ignition |
| **checkpoint inhibitors** | *reverse* protective exhaustion | **precipitate T1D** (the cautionary direction — validated) | — (this is the "what not to do") |

The map *is* the actionable output: it says which pairs backfire (co-dosed anti-CD3 + mRNA tolerance),
which are safe (anti-CD3 + IL-10 tolerance; anything + β-protection), and which need a partner (anti-CD20).

---

## The patient axes (who responds to what)

The body also identified the **dimensions of heterogeneity** that decide response — each a measurable trait:

| axis | predicts | source layer |
|---|---|---|
| **HLA / genetic risk** (genotype) | *who* gets disease, *how young*, *which* primary antigen | genetics (AG1) — the **upstream determinant** of the axes below |
| baseline **exhausted-CD8** / low **TSCM** renewal | teplizumab **responder** | responder (AR1), hierarchy (AH3) |
| tolerance **platform type** (conversion vs expansion) | whether anti-CD3 co-dosing **antagonizes** | combination (AP1) |
| **β-cell fragility** (immune-independent) | β-loss despite immune control | β-cell (AB2) |
| **T-vs-B dominance** (T-autonomous attack) | anti-CD20 **non-response** | B-cell (BC1) |
| **#autoantibodies** (spreading extent) | disease stage; escape risk for single-antigen tolerance | spreading/B-cell (AE1, BC1) |

---

## Consolidated testable predictions

What the framework actually sticks its neck out on (falsifiable; ★ = already matches real data):

1. ★ **Co-dosed** anti-CD3 + conversion-type antigen tolerance **antagonize** (Foster 2025); **sequencing rescues** *(the testable rescue)*.
2. ★ **Expansion-type** tolerance (IL-10/TGF-β) does **not** antagonize anti-CD3 (Mathieu 2023 AG019+teplizumab).
3. ★ **Baseline exhaustion / low TSCM → teplizumab responder** (Wiedeman 2019; Dufort 2026).
4. ★ **Checkpoint inhibitors reverse protective exhaustion → T1D** (documented drug side effect).
5. **β-protection (verapamil) is a safe orthogonal adjunct** that **slows epitope spreading** *(no head-to-head trial yet)*.
6. **Single-antigen tolerance is escaped by spreading**; **broad or early** tolerance, or a **β-protection** adjunct, rescues it.
7. **Anti-CD20 benefit is transient and B-cell-dominance-dependent**; pairing with durable tolerance extends it.
8. **#autoantibodies ≈ spreading extent** → a usable **staging/monitoring biomarker** for all of the above.
9. ★ **The honeymoon is a *function* recovery** — insulin lifts glucotoxic stress, transiently restoring C-peptide (Mortensen 2009).
10. ★ **Glucose control is a modest, *independent* lever** — additive with immunotherapy, **not** synergistic (honest match to McVean/CLVer 2023's null).
11. **C-peptide and glycemia dissociate** — preserving β-mass needn't normalize glucose; report both.
12. ★ **Innate-targeting (anti-IL-1) has a narrow early window** — *fails at onset* (Moran 2013, established) because the adaptive attack self-sustains; predicted to **work as prevention** (the open half).
13. ★ **Genotype sets the patient axes** — an HLA odds-ratio→escape map reproduces the onset-age gradient (Sharp 2019), DQ6 protection (Erlich 2008), and the insulin-first/GAD-first endotype (Bauer 2019), none of them fit to.

14. ⚑ **(testable now, on existing data) Baseline-exhaustion stratification enriches teplizumab response** —
    the model predicts ~56% unselected → **~91% (exhaustion-high) / ~25% (exhaustion-low)**, a +66-pt
    enrichment a re-analysis of AbATE/TN10/PROTECT could confirm or kill (`responder_classifier.py`). The
    rate (~50%, AbATE) and direction (Long/Wiedeman) are reproduced; the *enrichment magnitude* is the
    forward bet. **The single most actionable prediction here** — and the natural one to bring to TrialNet.

Predictions 1–4, 9–10, 13, and the onset-failure of 12 already land on published data (that the *same* model
lands all of them is the point); 5–8, 11, the prevention-half of 12, and the **enrichment magnitude of 14**
are the open, falsifiable bets.

---

## Honest tiering — what's backed by how much

- **Reproduces published data** (the model lands where reality fell): Foster 2025 antagonism, Mathieu 2023
  safety, teplizumab response biomarkers, checkpoint-induced T1D — and, **semi-quantitatively anchored in real
  effect sizes**, the genotype→phenotype map (HLA onset-age gradient, DQ6 protection, insulin/GAD endotype;
  Erlich 2008 / Sharp 2019 / Bauer 2019) — the first **calibrated** plank, vs the free knobs below.
- **Fit to trial data** (calibration, not just reproduction): the disease **timescale** is fit to the TN10
  placebo curve (median 24.4 mo) and teplizumab's ~2-yr delay to a **24% anti-CD3 effect** (Herold 2019);
  identifiability reported — the median pins the *timescale* (and `kappa×E`), not `kappa` alone (`calib_tn10.py`).
  And the **spreading clock** is fit to the Ziegler 2013 / TEDDY natural history (multiple-Ab → T1D 70%@10yr;
  single-Ab 14.5%@10yr) — spreading ~0.04/yr, and *clinical progression requires spreading* (`calib_teddy.py`).
  And the C-peptide readout **cross-validates** the model: the post-diagnosis decline rate (Shields 2018)
  independently matches `kappa` within 6% — **~0.6/yr confirmed by two unrelated datasets** — and the anti-CD3
  effect calibrated on *stage 2* **predicts** the PROTECT *stage-3* C-peptide preservation (`calib_cpeptide.py`).
  That cross-dataset consistency is something the free-knob model could not claim. **→ The full calibration
  phase (4 fits, the two-clock structure, both cross-validations, and identifiability) is in
  [CALIBRATION.md](CALIBRATION.md).**
- **Mechanistically grounded predictions** (literature supports the premise, outcome untested): β-protection
  as spreading-brake + safe adjunct; broad/early tolerance beats single; anti-CD20 + tolerance combination.
- **Modeling abstractions** (conscious, catalogued): bistable cell-fate switch (AS1, robustness-checked),
  sequential/threshold spreading (AE1), B-help-scales-kill (BC1), single severity knob (AS2).
- **Out of scope** (named, not hidden): innate immunity/neutrophils, gut microbiome (AS3 residual).

The registry holds **26 assumptions across 7 models, every parameter catalogued**; `validate.py` prints the
dig-here queue and flags any uncatalogued parameter as a candidate blind spot. Run it — the model audits itself.

---

## The method, and its honest limit

This grew by **continual expansion + Semantic-Scholar grounding + adversarial self-audit**: each layer
opened by a literature scan, built to reproduce a real result, then run through the validator, which
*caught its own new blind spots* (e.g. an uncatalogued switch-steepness parameter) for cataloguing. That
loop is why the body got *more* trustworthy as it grew, not less.

Its limit is stated in the registry's own metadata: the validator catches *written-but-uncatalogued* and
*catalogued-but-unchecked* assumptions — it **cannot** catch what is missing from the conceptual frame
entirely (true unknown-unknowns). Those need exactly what reversed the v1 headline: external expert
critique. **Microscope, not oracle.** This synthesis is a map of a well-explored region, drawn honestly,
with its edges marked — not a claim to have found the territory's end.
