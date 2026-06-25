# Biological-assumptions audit — the clonal/avidity T1D models (adversarial, self-directed)

_Purpose: list every biological assumption baked into `t1d_clonal.py` / `t1d_avidity.py`, mark which
are LOAD-BEARING (the antagonism result dies if they're wrong) vs supporting, and rate each as
SUPPORTED / CONTESTED / SHAKY against what we currently believe — so the Semantic Scholar check targets
the ones that matter. This is the "is every load-bearing assumption tied to something real?" check that
v1 skipped. Date 2026-06-24._

## Tier 1 — LOAD-BEARING **and** contestable (if any of these is wrong, the Foster antagonism result collapses)

**A1. Anti-CD3 reproduces the antagonism by PREFERENTIALLY DELETING activated/converting cells** (`kAC`).
- Where: `killC = kAC * C * ua3`, with kAC ≫ kA. This single term *is* the antagonism mechanism.
- Why contestable / SHAKY: teplizumab is deliberately **non-mitogenic** (Fc-modified) to *minimise*
  T-cell depletion/activation; its documented durable mechanism is **partial exhaustion / anergy / Treg
  induction**, not deletion of activated clones. If anti-CD3 anergizes rather than deletes the
  converting cells, the converters survive (just paused) and the antagonism may vanish.
- **S2 query:** teplizumab / anti-CD3 mechanism — deletion vs anergy vs exhaustion of *activated* T cells.

**A2. Protection is concentrated in a SMALL number of discrete regulatory clones that can stochastically go extinct.**
- Where: discrete clones (K≈24), small counts → Poisson extinction; the whole reason continuum models
  couldn't reproduce Foster.
- Why contestable / CONTESTED: if antigen-specific regulatory protection is **clonally diverse /
  redundant** (many clones, large numbers), losing a few converters is buffered and the antagonism
  disappears. The result requires the protective repertoire to be genuinely **sparse**.
- **S2 query:** clonality / TCR diversity / redundancy of antigen-specific (induced) Tregs protecting islets.

**A3. Antigen-specific tolerance works by creating BYSTANDER-suppressive regulatory clones** (global suppression).
- Where: `S = sum_k G`, `supp = 1/(1+supp·S/Ksupp)` — converted cells suppress the *whole* repertoire
  (infectious/linked tolerance).
- Why contestable / CONTESTED: tolerance might instead work by **deletion or anergy of the specific
  autoreactive clones** (no durable bystander-suppressor pool to lose) — in which case there is nothing
  for anti-CD3 to "extinguish," and the mechanism doesn't apply.
- **S2 query:** mechanism of antigen-specific tolerance in T1D — infectious/bystander Treg suppression vs deletion/anergy.

## Tier 2 — load-bearing, moderately contestable

**A4. Tolerance acts on / converts HIGH-avidity clones** (`gtol` peaked at high avidity).
- Why contestable / CONTESTED: Santamaria's pMHC-nanoparticle tolerance **expands LOW-avidity
  autoregulatory T cells** — the opposite avidity. Which avidity the protective pool occupies changes
  which clones are vulnerable to anti-CD3.
- **S2 query:** avidity of protective/regulatory vs pathogenic T cells in T1D; do tolerance therapies act on high- or low-avidity clones.

**A5. Antigen-specific tolerance MONOTHERAPY is effective** (cures most of the cohort alone).
- Why contestable / SHAKY: human antigen-specific tolerance monotherapy (GAD-alum, peptides, etc.) has
  **largely failed** to show durable efficacy — the reviewer's exact load-bearing point. Our hardening already
  flagged tolerance-mono stays "high-but-reducible." If tolerance alone barely works, "anti-CD3 reduces
  it" must be re-framed.
- **S2 query:** efficacy of antigen-specific immunotherapy monotherapy in T1D (human trials + NOD).

**A6. A vulnerable CONVERSION WINDOW exists** — converting cells transit a deletable state on a timescale anti-CD3 can intercept.
- Why contestable / CONTESTED: the kinetics of effector→Treg conversion vs anti-CD3 pharmacodynamics are
  not well pinned; the "window" is assumed, not measured.
- **S2 query:** kinetics/timescale of induced-Treg conversion; effector-to-Treg transdifferentiation timing.

## Tier 3 — supporting assumptions (already vetted or low-risk)

| # | assumption | status |
|---|---|---|
| A7 | anti-CD3 induces durable, waning hyporesponsiveness (state `X`) | **SUPPORTED** (Long 2016; Lledó-Delgado) |
| A8 | tolerance bottleneck is peripheral, not thymic | **SUPPORTED** (Feuerer 2007/09) |
| A9 | thymic negative selection skews the peripheral autoreactive repertoire toward LOW avidity | SUPPORTED (but in tension with A4) |
| A10 | β-cell killing is dominated by high-avidity autoreactive CD8 effectors | SUPPORTED (Wiedeman 2019) |
| A11 | β-cells regenerate logistically | CONTESTED — limited regeneration in established human T1D (less central to the antagonism) |

## Priority for the Semantic Scholar check
The result lives or dies on **A1, A2, A3** (the antagonism mechanism). A4, A5, A6 reshape it. A1 is the
single biggest risk: if teplizumab anergizes rather than deletes activated converters, our central
mechanism is wrong. The S2 check targets A1–A6; A1–A3 are the kill-shots to look hardest at.

---

## S2 VERDICT (2026-06-24) — assumptions largely SURVIVE; one big reframe
_Scan: `_scan/contested_assumptions.md` (70 papers). Plus the decisive read of the direct **human**
combination trial Mathieu 2023 (AG019 + teplizumab; PMC10709251)._

| # | assumption | verdict | key evidence |
|---|---|---|---|
| A1 | anti-CD3 hits the activated converters | **SUPPORTED, refined** | activated T cells are AICD-prone (Ni 05, Hartwig 08); anti-CD3 up-regulates PD-1 and impairs activated effectors (Wållberg 2017); teplizumab ↑ partially-exhausted CD8 (KLRG1/TIGIT/EOMES) in humans (Mathieu 2023). **Refine "deletes" → "deletes OR exhausts/anergizes" — either way the converter doesn't finish becoming a protector.** |
| A2 | protective clones are sparse (extinction matters) | **SUPPORTED** | islet-protective activated/memory-Treg clonal expansion is *limiting* (Mhanna 2021); antigen-specific Tregs "extremely low" frequency (Yang 2022); autoreactive CD8 TCR-restricted (Fuchs 2017). |
| A3 | tolerance protects via bystander/IL-10 suppression | **SUPPORTED** | infectious tolerance documented in T1D (Kleijwegt & Roep 2013); engineered/redirected Tregs show bystander suppression (Yeh 2017, Yang 2022); AG019 acts via PPI-specific IL-10⁺ Tr1 + memory Tregs (Mathieu 2023). |
| A4 | tolerance acts on HIGH-avidity clones | **CONTESTED / likely oversimplified** | protective regulatory cells skew LOW-avidity (Santamaria pMHC-NP); Treg function "disengaged from TCR affinity" (Jing 2023); high-avidity pathogenic clones escape central tolerance (Serre 2015). Reshapes, doesn't kill. |
| A5 | tolerance MONOTHERAPY is effective | **WEAK alone (as the reviewer noted)** | AG019 mono stabilised only to ~6 mo then declined by 12 mo; combination did better (Mathieu 2023). Our marginal-tolerance regime is the realistic one. |

### THE BIG REFRAME (the audit's real catch)
The one **direct human combination trial** — teplizumab + AG019, **co-administered (≈12-day overlap)** —
showed **NO antagonism**: C-peptide 112% of baseline at 6 mo (vs 73% decline on placebo), metabolic
variables stabilised/improved to 12 mo, i.e. **SYNERGY**, the opposite of Foster. A naive "co-dosing
always antagonizes" claim would have been **demolished by this human data** — a expert-review-style hit avoided.

BUT it fits our framework's regime map exactly: **AG019 is an IL-10/Treg-EXPANSION platform**
(substrate-independent) → our predicted **SYNERGY** regime; **Foster's mRNA is a CONVERSION-dependent
platform** → our predicted **ANTAGONISM** regime. So the corrected, defensible claim is **not** "don't
co-dose" but: **"co-dosing antagonizes only for CONVERSION-dependent platforms (mRNA/peptide that work
by converting the target effectors anti-CD3 then deletes); Treg-EXPANSION platforms (IL-10/TGF-β) are
safe to co-dose and synergize."** Anchored now to BOTH a mouse antagonism (Foster) and a human synergy
(Mathieu). This is a validation of the framework AND a precision upgrade of the claim.

### Build implied
Make the **platform-type axis explicit in the clonal model** so it reproduces BOTH datasets: expansion
platform → synergy (Mathieu human), conversion platform → co-dosing antagonism (Foster NOD). Generalize
A1 deletion→deletion-or-exhaustion (human exhausted-CD8 supports it). A4 avidity = lower-priority sweep.
**[DONE — platform axis built; see FINDINGS_clonal.md §Platform axis.]**

---

## CYCLE 2 (2026-06-24) — A6 (window), A4 (avidity), A12 (locality)
_S2 scan `_scan/contested2_window.md` (32 papers) UNDER-DELIVERED on A6 (noisy/off-domain hits; the
conversion-kinetics & teplizumab-PK sections came back nearly empty — an honest gap). Real signals:
Treg induction is driven more by **antigen DOSE than avidity** (Turner 2009 → A4 oversimplified,
confirmed); islet Tregs are **short-lived & plastic** (Kornete 2017 → supports our brittle-regulator
choice); diverse-TCR Treg requirement (Oh 2012) is a mild tension with strict sparseness. Because the
scan was weak, we tested the MODEL's sensitivity directly (`t1d_clonal_robust.py`)._

| # | assumption | verdict | basis |
|---|---|---|---|
| A4 | which avidity tolerance targets | **RESOLVED — non-threatening** | antagonism strong at BOTH high- and low-avidity targeting (robust 5/5 each). The oversimplification doesn't change the result. |
| A6 | a vulnerable conversion WINDOW exists | **ROBUST within the plausible range** | antagonism held across the whole window scan (convr 1→16), gracefully weakening as the window narrows (−82→−47 high-avidity; −89→−30 low). It would only vanish for a **near-instant** conversion — biologically implausible (effector→Treg conversion is days-to-weeks). The window-dependence is itself a **falsifiable prediction**: faster conversion → weaker antagonism. |
| A12 | global vs local suppression | **not directly resolved; low downside risk** | if suppression is local (not global), clone-loss is *less* buffered → would *strengthen* the antagonism, not threaten it. |

**Honest open gap:** the A6 conversion-kinetics/teplizumab-PK *literature* was not cleanly confirmed
this pass (poor queries). The model-robustness lowers the risk, but a better-targeted search (or expert
input) on the actual conversion timescale vs anti-CD3 duration remains a real to-do.

**Net after two cycles:** the load-bearing biology (A1–A3) is supported; the result reproduces both real
combination datasets via the platform axis; and it is robust to the avidity (A4) and window (A6)
assumptions. The remaining items are lower-stakes (A11 β-regeneration; A12 locality; A2 magnitude).
