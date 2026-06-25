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
honestly bounded. It now reproduces or predicts **three independent real-world datasets** (Foster 2025,
Mathieu 2023, and the teplizumab response biomarkers) and one documented drug side effect
(checkpoint-induced T1D). The arc:

---

## ★ The capstone — read this first
**[SYNTHESIS.md](SYNTHESIS.md)** — the one thesis all six layers converged on, the full **intervention map**
(which pairings backfire, which are safe, which need a partner), the **patient-response axes**, the
consolidated **testable predictions**, and an honest tier of what's backed by how much. Read that for
*what the whole body says*; read on for the per-layer tour.

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

---

## Integrity infrastructure
- **`verify_claims*.py`, `verify_clonal.py`** — machine-checkable re-derivation of headline numbers (exit 0 ⇔ pass).
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
├── README.md                       ← this overview
└── analysis/
    ├── t1d_clonal.py               ← discrete-clonal/stochastic model (Foster + platform axis)
    ├── t1d_clonal_{schedule,robust,calib}.py  ← regime map + schedule rule / robustness / calibration
    ├── t1d_avidity.py              ← avidity-continuum model (the sub-continuum negative result)
    ├── t1d_responder.py            ← teplizumab responder/non-responder
    ├── t1d_hierarchy.py            ← progenitor→effector→exhausted ladder (+ checkpoint-T1D)
    ├── t1d_betacell.py             ← the β-cell as active participant (stress feedback)
    ├── t1d_model.py + _v2/_v3/_v4  ← the original (withdrawn v1) toggle + verified-biology rebuilds
    ├── FINDINGS_{final,clonal,avidity,responder,hierarchy,betacell}.md  ← the results, one per layer
    ├── FINDINGS.md                 ← the original v1 result (SUPERSEDED, kept as the record)
    ├── verify_*.py / verify_clonal.py  ← machine-checks
    ├── AUDIT.md / ASSUMPTIONS_AUDIT.md  ← audits
    ├── assumptions.json / validate.py   ← the standing assumption registry + validator
    └── MEMO.md / METHODS.md / NOVELTY.md / scan_results.md  ← literature lane
        (Semantic-Scholar scans for each step live one level up in ../_scan/*.md)
```

## Running it
```bash
pip install -r requirements.txt           # numpy, scipy, (matplotlib for the v1 figures)
cd analysis
# every model runs under a 4 GB cap per project policy, e.g.:
bash -c 'ulimit -v 4194304; timeout 595 python3 t1d_clonal.py'
python3 t1d_responder.py    # deterministic, fast
python3 t1d_hierarchy.py
python3 t1d_betacell.py
python3 verify_clonal.py    # machine-check the clonal antagonism (7/7)
python3 validate.py         # the standing assumption audit
```

## Honest caveats
Illustrative throughout — magnitudes are illustrative; the robust outputs are *directions and
structural results*, not numbers. The qualitative claims are anchored to real data (Foster 2025,
Mathieu 2023, the response biomarkers, checkpoint-induced T1D), but **none is a validated clinical
result**, and one prior headline was already wrong and withdrawn. Open gaps are tracked live in the
`validate.py` dig-here queue (currently: the bistable-switch structural assumption; the conversion
"window" whose literature is unconfirmed; the β-protection+immunotherapy combination, model-predicted
not confirmed). The detailed per-result caveats live in each `FINDINGS_*.md`. Originating observations
include conference abstracts (Foster 2025; Dufort 2026).
