# Type 1 diabetes immunotherapy — a within-host modeling exploration

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> Every result here is a quantitative *hypothesis* from a deliberately simplified mechanistic model,
> labeled with its evidence and its caveats. Nothing is a validated clinical result. The repo is run
> **honesty-first**: machine-checkable claims, adversarial self-audits that retract overclaims (one
> headline was publicly reversed — see below), a standing assumption registry, and Semantic-Scholar
> grounding at every step.

> ## ⚠️ Correction history — the honesty trail
> The original published headline (Zenodo [10.5281/zenodo.20804558](https://doi.org/10.5281/zenodo.20804558))
> claimed a **"tolerance-first sequencing antagonism."** It was **withdrawn** after an immunologist
> (an immunologist reviewer) showed it rested on an **uncalibrated** operating point that
> inverted the clinical rationale. The corrected result and the post-mortem are in
> [analysis/FINDINGS_final.md](analysis/FINDINGS_final.md) and [analysis/AUDIT.md](analysis/AUDIT.md)
> §"Post-publication reversal". That reversal is kept visible on purpose — it is how this work is
> supposed to behave, and it is what the rest of the model was rebuilt to deserve.

## What this is
A within-host model of the type 1 diabetes immune attack that grew, layer by layer, to answer a
connected set of immunotherapy questions — each grounded in the literature, machine-checked, and
honestly bounded. It grew to **nine mechanistic layers** — the full disease arc from the innate trigger to
the C-peptide readout — and its load-bearing knobs are now **calibrated to trial data and validated
out-of-sample** (it predicts the natural history of trials it was *never fit to* within ~2%). It reproduces
or predicts **~8 real-world datasets/trials** plus the HLA genotype→phenotype map, and yields one
re-analysis-testable clinical prediction. The arc:

---

## ★ The capstone — read this first
**[SYNTHESIS.md](SYNTHESIS.md)** — the one thesis all the layers converged on, the full **intervention map**
(which pairings backfire, which are safe, which need a partner), the **patient-response axes**, the
consolidated **testable predictions**, and an honest tier of what's backed by how much. Read that for
*what the whole body says*. **[CALIBRATION.md](CALIBRATION.md)** — how the load-bearing knobs were *fit to
trial data* (TN10, TEDDY/Ziegler, Shields/PROTECT, Pescovitz), the two-clock structure, and the
cross-validations. Then read on for the per-layer tour.

---

## Results — each in its own FINDINGS doc

### 1 · Combination — which immunotherapy pairings backfire, and how to schedule them
→ [FINDINGS_clonal.md](analysis/FINDINGS_clonal.md) · [FINDINGS_avidity.md](analysis/FINDINGS_avidity.md) · code `t1d_clonal.py`, checked by `verify_clonal.py` (**7/7, seed-robust**)
- Population/bistable models predict **synergy** and *structurally cannot* reproduce the Foster 2025
  antagonism; **avidity** resolution doesn't rescue it either → the antagonism is **sub-continuum**.
- A **discrete-clonal/stochastic** model *does* reproduce it: a **co-dosing antagonism** (anti-CD3
  stochastically extinguishes the just-activated converting clones), which **sequencing avoids**.
- A **platform axis** reconciles *both* real datasets: **conversion-type** platforms (mRNA; Foster)
  antagonize when co-dosed; **expansion-type** (IL-10; the Mathieu 2023 human AG019+teplizumab trial)
  are safe. The model lands every known combination study where it actually fell.
- **Payload** (`t1d_clonal_schedule.py`): a **regime map** (which combos backfire) + a **schedule rule**
  (separate conversion-type drugs by ~4–6 months; tolerance-first is the more robust order).

### 2 · Teplizumab responder vs non-responder
→ [FINDINGS_responder.md](analysis/FINDINGS_responder.md) · code `t1d_responder.py`
- A **durable-exhaustion vs TSCM-renewal balance** reproduces the ~50% response split **and both real
  biomarkers**: baseline exhausted-CD8 → responder (Wiedeman 2019); high TSCM → non-responder (Dufort 2026).
- **Actionable:** predicted non-responders are *converted* by a 2nd course or by targeting TSCM —
  and the model correctly flags that **rapamycin would backfire** (it breaks the exhaustion; Baeyens 2009).

### 3 · The exhaustion hierarchy (vertical deepening)
→ [FINDINGS_hierarchy.md](analysis/FINDINGS_hierarchy.md) · code `t1d_hierarchy.py`
- Explicit **progenitor (TCF1) → effector → terminally-exhausted (TOX)** ladder. The **progenitor pool**
  is the responder axis — a *measurable* population (Vignali 2018).
- **Predicts checkpoint-inhibitor-induced T1D** — a documented clinical fact (built-in validation).
- **Transfer:** the *same* ladder run with the *opposite* sign is the cancer/HIV model.

### 4 · The β-cell as an active participant (vertical deepening)
→ [FINDINGS_betacell.md](analysis/FINDINGS_betacell.md) · code `t1d_betacell.py`
- A **stress → HLA/neoantigen feedback loop** makes the disease self-amplifying.
- **β-protection** (verapamil-type) works *orthogonally* and combines with immunotherapy as a **safe,
  antagonism-free axis** — a new combination prediction. *(Honest non-result: the β-fragility
  lever-switch did **not** emerge; reported as-is.)*

### 5 · Epitope spreading — why single-antigen tolerance keeps failing
→ [FINDINGS_spreading.md](analysis/FINDINGS_spreading.md) · `t1d_spreading.py`, `verify_spreading.py` (**7/7**)
- A **primary antigen (insulin)** that **spreads** to others, stress-driven. Single-antigen tolerance is
  **escaped** by spreading; **early**, **broad**, or **β-protection** each defeat the escape — the last
  unifying the β-cell and antigen layers.

### 6 · B cells & autoantibodies — why anti-CD20 is transient
→ [FINDINGS_bcell.md](analysis/FINDINGS_bcell.md) · `t1d_bcell.py`, `verify_bcell.py` (**6/6**)
- B cells as APCs that drive spreading and sustain the attack. **Anti-CD20 (rituximab) is transient**
  (B cells repopulate — Pescovitz 2014), with a **responder axis** (fails when T-dominated — Linsley 2018);
  pairing with durable tolerance beats either alone. #autoantibodies = the measurable biomarker.

### 7 · The metabolic / glucose readout
→ [FINDINGS_metabolic.md](analysis/FINDINGS_metabolic.md) · `t1d_metabolic.py`, `verify_metabolic.py` (**7/7**)
- Converts β-mass into **C-peptide + glucose** (trial units); **glucotoxicity** feeds the stress hub.
  Reproduces the **honeymoon** (Mortensen 2009); glucose control alone is modest (honest McVean 2023 match)
  and is **additive, not synergistic**, with immunotherapy (reported as-is).

### 8 · Innate immunity — the upstream trigger
→ [FINDINGS_innate.md](analysis/FINDINGS_innate.md) · `t1d_innate.py`, `verify_innate.py` (**7/7**)
- Innate inflammation (neutrophils/NETs/IFN-α) **primes** the adaptive attack (bistable → self-sustaining).
  **Explains why anti-IL-1 failed at onset** (Moran 2013 — too late) and predicts it works as *prevention*.

### 9 · Genetics / HLA — the calibration bridge
→ [FINDINGS_genetics.md](analysis/FINDINGS_genetics.md) · `t1d_genetics.py`, `verify_genetics.py` (**4/4**)
- A genotype→parameter map anchored in **real HLA odds ratios** (Erlich 2008) that reproduces — *unfit* —
  the onset-age gradient (Sharp 2019), DQ6 protection, and the insulin-first/GAD-first endotype (Bauer 2019).

### Calibration, validation & the decision-relevant output
→ **[CALIBRATION.md](CALIBRATION.md)** · `calib_*.py`, `loo_validation.py`, `responder_classifier.py`
- **Calibration (4 fits)**: disease timescale ← TN10; spreading ← TEDDY/Ziegler; C-peptide ← Shields/PROTECT;
  anti-CD20 transience ← Pescovitz. Reveals a **two-clock accelerating disease** + two **cross-validations**.
- **Out-of-sample validation** (`loo_validation.py`, **5/5**): predicts held-out trials' **natural history to
  ~2%**; cross-stage drug effects do **not** transfer — an honest, measured trust boundary.
- **The actionable prediction** (`responder_classifier.py`, **4/4**): stratifying teplizumab by **baseline
  exhaustion** should raise response ~56% → **~91% (high) / ~25% (low)** — testable on *existing* trial data.

---

## Integrity infrastructure
- **19 `verify_*.py` scripts** (one per layer + the 4 calibrations + the out-of-sample validation + the responder classifier) — machine-checkable re-derivation of every headline number (exit 0 ⇔ pass); `validate.py --run` executes them all under the 4 GB cap.
- **[AUDIT.md](analysis/AUDIT.md)** — adversarial audits, including the public reversal post-mortem.
- **[ASSUMPTIONS_AUDIT.md](analysis/ASSUMPTIONS_AUDIT.md)** — two cycles of self-directed assumption audits + literature checks.
- **`assumptions.json` + `validate.py`** — a **standing assumption registry + validator**: catalogs every
  assumption (status / controversy / evidence / the parameters it governs), prints a *dig-here* queue of
  load-bearing-but-unsettled assumptions, and **surfaces blind spots** (model parameters with no
  catalogued assumption). It prints its own limit: it cannot see conceptual-frame unknown-unknowns.
  ```bash
  cd analysis && python3 validate.py          # dashboard + dig-here queue + blind-spot surfacer
  python3 validate.py --run                   # also re-execute the verify_*.py scripts (4 GB cap)
  ```

## Map of the repo
```
type1-diabetes-research/
├── README.md            ← this overview (the tour)
├── SYNTHESIS.md         ← the cross-layer thesis + intervention map (read first)
├── CALIBRATION.md       ← the data-anchoring: 4 calibrations, out-of-sample validation, cross-validations
└── analysis/
    ├── t1d_clonal.py  t1d_avidity.py          ← combination: clonal/stochastic + avidity (sub-continuum)
    ├── t1d_responder.py  t1d_hierarchy.py     ← teplizumab responder / exhaustion hierarchy (+checkpoint-T1D)
    ├── t1d_betacell.py  t1d_spreading.py      ← β-cell stress feedback / epitope spreading
    ├── t1d_bcell.py  t1d_metabolic.py         ← B-cell + anti-CD20 / metabolic C-peptide+glucose readout
    ├── t1d_innate.py  t1d_genetics.py         ← innate trigger / genetics-HLA calibration bridge
    ├── calib_{tn10,teddy,cpeptide,pescovitz}.py   ← the 4 trial calibrations
    ├── loo_validation.py  responder_classifier.py ← out-of-sample validation + the stratified prediction
    ├── t1d_model.py + _v2/_v3/_v4             ← the original (withdrawn v1) + verified-biology rebuilds
    ├── FINDINGS_*.md                          ← the results, one per layer (final/clonal/avidity/responder/
    │                                            hierarchy/betacell/spreading/bcell/metabolic/innate/genetics)
    ├── verify_*.py  (19)                      ← machine-checks (one per layer + calibrations + validation)
    ├── assumptions.json  validate.py          ← standing assumption registry + validator (blind-spot surfacer)
    └── AUDIT.md  ASSUMPTIONS_AUDIT.md  METHODS.md  NOVELTY.md  ← audits + methods + literature lane
        (Semantic-Scholar scans for each step live one level up in ../_scan/*.md)
```

## Running it
```bash
pip install -r requirements.txt           # numpy, scipy, (matplotlib for the v1 figures)
cd analysis
# every model runs under a 4 GB cap per project policy, e.g.:
bash -c 'ulimit -v 4194304; timeout 595 python3 t1d_clonal.py'
python3 t1d_spreading.py    # any layer's main() prints its predictions (most deterministic + fast)
python3 calib_tn10.py       # a calibration (fit to a trial) + its identifiability
python3 loo_validation.py   # out-of-sample: predict held-out trials (natural history ~2%)
python3 responder_classifier.py   # the stratified teplizumab enrichment prediction
python3 validate.py         # the standing assumption audit (dashboard + dig-here + blind spots)
python3 validate.py --run   # ALSO re-execute all 19 verify_*.py (the full regression, 4 GB cap)
```

## Honest caveats
Illustrative throughout — magnitudes are illustrative; the robust outputs are *directions and
structural results*, not numbers. The qualitative claims are anchored to real data (Foster 2025,
Mathieu 2023, the response biomarkers, checkpoint-induced T1D), but **none is a validated clinical
result**, and one prior headline was already wrong and withdrawn. The earlier kill-the-result dig-here
items (bistable switch; conversion window; β-protection combination) have since been resolved/grounded;
what remains in the `validate.py` queue are two **conscious structural simplifications** (a single severity
knob; the still-excluded environmental trigger). The calibrated spine is **validated out-of-sample for
*natural history* (~2%) but only per-stage — not extrapolating — for *therapy*** (see
[CALIBRATION.md](CALIBRATION.md)). Detailed per-result caveats live in each `FINDINGS_*.md`. Originating
observations include conference abstracts (Foster 2025; Dufort 2026).
