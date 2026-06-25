# Findings — B cells & autoantibodies (vertical deepening #4)

_Closes catalogued blind spot AS3 (T-cell-centric scope) by adding B cells, and connects to the spreading
layer. Code: `t1d_bcell.py` (deterministic). Grounded in `_scan/bcell_axis.md`. Status: illustrative
modeling / hypothesis._

## The model
Adds a B-cell APC compartment `Bc` to the spreading model. B cells do two things grounded in the
literature: (a) they **sustain the autoreactive attack** as antigen-presenting cells — so the β-cell kill
is scaled by B-cell help `helpf = Tdom + (1-Tdom)·Bc` (Pescovitz 2009 *NEJM*; Herold 2011); and (b) they
**drive epitope spreading** (spreading ∝ Bc — McLaughlin 2015; Wan 2018 *Nature*). Crucially the autoreactive
**T effectors persist** (memory) — rituximab targets B cells, *not* T cells — so depletion only *pauses* the
attack. **Anti-CD20** depletes Bc; a marrow influx + logistic term **repopulates** it (the transience).
`Tdom` (T-cell autonomy) is the responder axis. Autoantibody count = #antigens recruited (Felton 2024).

## Results (`t1d_bcell.py`, `verify_bcell.py` 6/6)

**P1 — anti-CD20 is TRANSIENT (Pescovitz 2014, *2-yr results*).** β under anti-CD20: **0.71 @3yr (peak) →
0.45 @5yr → 0.01 @11yr**; the benefit **+0.12 @3yr fades to +0.00 @11yr**. Because the T effectors persist
and B cells repopulate, the attack resumes — the model *reproduces* why rituximab's 1-yr benefit is gone by
year 2.

**P2 — RESPONDER axis (Linsley 2018).** anti-CD20 benefit is **+0.12 in a B-cell-driven patient** (Tdom=0.20)
vs **+0.05 when T-dominated** (Tdom=0.65) — 2.4×. "Elevated T cells predict poor response": the model gives
the mechanism (a T-autonomous attack doesn't need the B-cell help anti-CD20 removes).

**P3 — anti-CD20 + single-antigen tolerance > either alone.** At 6 yr: **combo 0.39 > single-tol 0.31 >
anti-CD20 0.27 > untreated 0.18.** Anti-CD20 adds debulking/attack-pause; tolerance adds durable primary
control. Honestly modest: because anti-CD20 is *transient* and single-antigen tolerance is *escaped by
spreading*, the combination **delays rather than cures** a fully-spread disease — consistent with the
spreading layer's lesson that a durable fix needs BROAD/EARLY tolerance or β-protection.

**P4 — #autoantibodies = the measurable biomarker (Felton 2024).** The model's hidden spreading extent
(#antigens recruited) is exactly what islet-autoantibody staging measures — so every prediction above is
checkable in blood.

## Why this matters
It folds the landmark anti-CD20 trial (Pescovitz 2009/2014) into the same framework, *explains its
transience and its responders*, and shows where a B-cell agent fits: as **debulking that needs a durable
partner**. Combined with the spreading and β-cell layers, the picture converges — single agents are
transient (anti-CD20) or escaped (single-antigen tolerance); durability comes from cutting the spreading
engine (broad/early tolerance, β-protection) and pairing modalities.

## Honest caveats
Illustrative; magnitudes illustrative (robust outputs are the four directions). "B-cell help scales the
kill, effectors persist" is a modeling choice (captures rituximab targeting B-not-T); the repopulation
timescale is stylized (the qualitative peak-then-fade is the robust feature, not the exact 11-yr tail).
Autoantibodies are treated as a *readout* of spreading, not as primary effectors (consistent with
T1D being T-cell-mediated). Innate immunity and microbiome remain out of scope (AS3 residual).
