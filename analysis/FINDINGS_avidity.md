# Findings (avidity-resolved, P5) — the structural-negative is robust AND sub-bistable

_Extends `FINDINGS_final.md`. Built on the Khadra/Pietropaolo avidity-continuum framework
(Jaberi-Douraki/Pietropaolo/Khadra, J Theor Biol 2015, PMC4567915) — the validated T1D model whose
central result is that onset is set by Treg-vs-Teff dominance **at specific high avidities**, not by
the population-averaged ratio. We extended it with the two therapies that framework explicitly does
**not** model, to test whether avidity resolution reproduces the Foster 2025 antagonism. Code:
`t1d_avidity.py` (runs under the 4 GB cap). Status: illustrative modeling, not clinical findings._

## The question
Does resolving T-cell **avidity** (the one dimension the lumped toggle lacked) let a continuum model
reproduce Foster 2025 (anti-CD3 *reduces* antigen-specific tolerance efficacy)? Our therapy asymmetry:
tolerance is **avidity-targeted** (acts on the high-avidity pathogenic clones it must convert);
anti-CD3 is **avidity-non-selective** (debulks across the spectrum) + durable hyporesponsiveness `X`.

## What we tested (all in `t1d_avidity.py`)
1. **Lumped (N=1) vs resolved (N=40)** across a tolerance-strength scan.
2. **Acute deletion** (mechanism 1): a converting pool `A_i`; anti-CD3 preferentially deletes the
   just-activated high-avidity converting clones (rate `delA`). Swept `delA` ∈ [0, 50].
3. **Weak durable window** (mechanism 2): swept `epsX` ∈ [0.05, 1.4] (where the v2 lumped model showed
   antagonism re-appear).

## Result — no antagonism, anywhere
- **Resolving avidity did the OPPOSITE of exposing antagonism**: targeted tolerance + anti-CD3 is
  *more* synergistic resolved than lumped (it rescues at lower tolerance strength). The model also
  reproduces Khadra's own "avidity-specific dominance" behaviour — a faithfulness check.
- **Acute deletion bites but cannot flip the sign**: high `delA` hurts the *simultaneous* and
  *tolerance-first* arms, but **anti-CD3-first is immune** (give anti-CD3, let it clear, then convert
  — no converting pool to delete), so the best achievable combination stays ≥ monotherapy → synergy.
- **Weak window only weakens**: low `epsX` slides the combination toward 0% but never below
  monotherapy. Less synergy, never antagonism.

## The deep reason (the sharpened structural-negative)
Foster's antagonism means **combination < tolerance-alone**, which requires tolerance-alone to be
*partially* effective. But a **bistable basin-flip framework — lumped OR avidity-resolved — has binary
cohort efficacy** (0% or 100%; you flip the basin or you don't). There is no graded middle for anti-CD3
to subtract from, and anti-CD3 is **intrinsically pro-flip**. Therefore:

> The antagonism is **sub-continuum AND sub-bistable.** It cannot appear in *any* basin-flip model
> (population or avidity), because anti-CD3 only ever helps the flip. Reproducing Foster requires
> leaving this model family entirely — **discrete-clonal / stochastic** dynamics, where anti-CD3
> stochastically removes the *specific* would-be-regulatory clones tolerance was building (a per-clone
> subtraction invisible to every continuum / cohort-fraction measure). This is the
> deterministic↔stochastic boundary.

Robust across **four model variants** (lumped v1–v4; avidity-resolved P5) and the two strongest
candidate mechanisms.

## Bonus — a falsifiable sequencing prediction (NEW, opposite to v1)
Acute deletion in avidity space yields a clean, testable rule **inside** an overall-synergistic
combination: because anti-CD3 deletes the just-activated converting clones, **anti-CD3-FIRST is optimal**
(let anti-CD3 clear, *then* give tolerance), while simultaneous / tolerance-first are degraded. This is
the *opposite* of v1's withdrawn "tolerance-first" rule, and it is mechanistically grounded.

## Honest meta-point
Across every resolution we have tried, the biology predicts **synergy** — consistent with the positive
Salmonella/L. lactis combination studies. Foster's antagonism, if robust (it is an ADA abstract,
limited detail), is therefore a **specific discrete-clonal phenomenon**, not a population effect.

## Next
`t1d_clonal.py` — the discrete-clonal/stochastic model: the model class that *can*, in principle,
produce Foster (anti-CD3 stochastically deleting the converting clones that would have become the
linchpin bystander-suppressive regulators). Settles whether Foster is reproducible at all.
