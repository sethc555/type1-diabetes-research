# Findings — sequencing antagonism between anti-CD3 and antigen-specific tolerance in T1D

> ⚠️ **SUPERSEDED (2026-06-22) — read [FINDINGS_final.md](FINDINGS_final.md) instead.**
> The "tolerance-first sequencing antagonism" headline below is **withdrawn as an artifact.** A
> post-publication critique from an immunologist (an immunologist reviewer) showed the
> tolerance-monotherapy = 100% operating point was uncalibrated and inverted the clinical rationale.
> A verified-biology rebuild **reverses** the conclusion: the combination is **synergistic**, and the
> Foster/Stewart antagonism is a **clone-level** effect a bistable population model cannot capture.
> See [FINDINGS_final.md](FINDINGS_final.md) and [AUDIT.md](AUDIT.md) §"Post-publication reversal".
> This file is retained, unaltered below, as the honesty record of the original claim.

_All numbers below are re-derived and asserted by `verify_claims.py` (24/24 PASS). Status:
illustrative within-host modeling / hypothesis generation — **not** validated clinical findings.
Read with [MEMO.md](MEMO.md) (the literature lane) and [AUDIT.md](AUDIT.md)._

## The question

Foster et al. 2025 (NOD mice, ADA abstract 2136-LB) reported an unexplained, unmodeled result:
**anti-CD3 monoclonal antibody (teplizumab-class) *reduces* the efficacy of antigen-specific
(mRNA/peptide) tolerance immunotherapy.** Both are being pushed toward combination use
(Greenbaum 2026; Wouters 2026), so *whether and how to combine them* is a live clinical
question. No mechanistic within-host model existed (the T1D "modeling" literature is statistical/ML
— Patil 2024, Montaser 2026). This is the open lane.

## The model (P1 — `t1d_model.py`)

A 3-state within-host ODE: beta-cell mass `B`, autoreactive effector burden `E`, antigen-specific
Treg burden `R`. `E` and `R` form a **mutual-repression bistable switch** (each self-promotes via
a Hill term, each represses the other) — the standard motif for immune cell-fate decisions. Two
stable basins:
- **autoimmune** (E high, R low → beta-cells killed): `verify` confirms B → 0.002;
- **tolerant** (E low, R high → beta-cells preserved): `verify` confirms B → 0.931.

Late stage 2 sits in the autoimmune basin. Two interventions, **same total drug, different order**:
- **antigen-specific tolerance** *converts* effectors to Tregs: flux `phi·u_tol·E` from E into R.
  It *needs effectors present to convert.*
- **anti-CD3** is *lymphodepleting*: removes effectors (`u_a3·E`) but also depletes Tregs
  (`rho·u_a3·R`); by itself it only transiently debulks E, so the switch reverts.

## Results

**1. The mechanism reproduces Foster, and resolves it into a sequencing rule.** Cohort
durable-control fraction (β-cell mass > 0.45 at 5 yr, across a severity gradient):

| arm | durable control |
|---|---|
| untreated | 0% |
| anti-CD3 monotherapy | 0% (delays only) |
| antigen-specific tolerance monotherapy | **100%** |
| simultaneous (both at once) | **59%**  — anti-CD3 antagonizes tolerance (−41 pts) |
| anti-CD3 → tolerance (anti-CD3 first) | **41%**  — worst (substrate deleted first) |
| tolerance → anti-CD3 (tolerance first) | **100%** — fully protected |

The ordering `tol-first ≥ tol-only > simultaneous > anti-CD3-first` is the mechanism's signature:
anti-CD3 given first/together removes the effector substrate tolerance must convert (and depletes
nascent Tregs), so the switch fails to flip; tolerance first builds and self-stabilizes the Treg
pool, after which an anti-CD3 course merely debulks residual effectors.

**2. The falsifiable prediction — an optimal inter-drug interval.** Gap sweep
(`t1d_gap.png`): tolerance-first is flat at ~97–100% for any gap; **anti-CD3-first recovers
monotonically with the gap** (59% at 0 → 100% at 1.5 yr) — i.e. if anti-CD3 must precede, you must
wait for the effector pool to recover before giving tolerance. Simultaneous dosing is the worst
protocol.

**3. Robustness — and a discovered two-channel caveat.** Over a 5-parameter grid:
- In the **Treg-sparing regime (`rho<1`)** — which matches teplizumab's documented Treg-sparing /
  expanding profile — **tolerance-first ≥ simultaneous in 171/171 (100%) viable sets, never
  negative** (strictly better in 26; the rest saturate, so order is irrelevant there).
- Including **strongly Treg-depleting anti-CD3 (`rho≤1.1`)**, the optimal **order can invert**
  (17/228 sets, all at the highest `rho`). Mechanistically there are *two* antagonism channels:
  (i) **substrate-depletion** (anti-CD3 deletes the effectors tolerance needs → don't give it
  first → favors tolerance-first) and (ii) **Treg-destruction** (anti-CD3 destroys freshly-built
  Tregs → don't give it last → favors anti-CD3-first). Which dominates is set by how Treg-depleting
  anti-CD3 is. This yields a **second falsifiable prediction**: if anti-CD3 turns out strongly
  Treg-depleting in vivo, the optimal order flips.

**4. Calibration (P3 — `t1d_calibration.py`).** A stage-2 cohort heterogeneous in effector
severity and residual β-cell mass reproduces the untreated progression curve: **median
time-to-diagnosis 2.06 yr (TN10 placebo ~2.0 yr), ~45% progressed by 2 yr (TrialNet stage-2
~50%).** The sequencing antagonism persists on this clinically-anchored cohort (tol-only 100% →
simultaneous 65% → anti-CD3-first 35% → tol-first 97%).

**5. A derived criterion that replicates the model (P-analytic — `t1d_analytic.py`).** Because the
courses (~2–4 weeks) are near-impulsive relative to the year-scale switch, each integrates exactly
to a linear map on `(E, R)`: tolerance `E→T·E, R→R+φ(1−T)E` and anti-CD3 `E→A·E, R→A^ρ·R`, with
`T=e^{−σ_tol·τ_tol}=0.373`, `A=e^{−σ_a3·τ_a3}=0.501`. Two closed-form results follow, both verified
against the full ODE (and asserted in `verify_claims.py`):
- **Antagonism factor.** Co-administering anti-CD3 retains only a fraction of the tolerogenic Treg
  yield, `𝒜 = Y_sim/Y_tol = A^ρ · σ_tol/(σ_tol+(1−ρ)σ_a3) = 0.467` (measured from the exact maps:
  0.51). It **factorizes into the two channels**: `A^ρ=0.54` (Treg-destruction) × `0.87`
  (substrate-competition) — i.e. the antagonism is, in closed form, "co-dosing keeps ~half the
  converted Tregs."
- **Order-inversion law.** Tolerance-first nets `~A^ρ·φ(1−T)E₀` Tregs vs anti-CD3-first's
  `~A·φ(1−T)E₀`, so **tolerance-first is optimal ⟺ A^ρ > A ⟺ ρ < 1**, crossover **ρ* = 1**. This
  *predicts* the numerically-discovered two-channel inversion: the ODE benefit
  `Δ(tol-first − simultaneous)` flips from +41 pts at ρ=0.9 to −6 pts at ρ=1.1, straddling ρ=1
  (`t1d_analytic.png`). The saddle-ratio criterion `Q=R/E > Q_crit` (Q_crit=0.89) additionally
  reproduces the cure *ordering* (clear arms exactly; exact marginal-arm fractions still need the
  ODE — the proxy is blunt near the separatrix). This is the T1D analogue of the HIV project's
  single derived reproduction number.

## Honest limitations (the audit upholds these)

- **The model under-produces the teplizumab *monotherapy* delay magnitude** (+0.68 yr vs TN10's
  ~+2 yr): a single short anti-CD3 course only transiently debulks effectors here. The robust,
  novel contribution is the **sequencing antagonism**, not the monotherapy-delay magnitude.
- Outcomes are framed as **cohort fractions** because the underlying switch is bistable (binary
  per patient); the antagonism is visible in the **marginal-efficacy regime** and is neutral where
  tolerance is overwhelmingly effective.
- Parameters are illustrative beyond the calibrated progression timing; "cure" is durable
  β-cell preservation in-model, not a clinical claim. The Foster result is a conference abstract.

### Audit corrections (2026-06-22 — see [AUDIT.md](AUDIT.md))

An adversarial audit confirmed `verify_claims.py` (24/24) and that every number above reproduces,
and that the antagonism/sequencing ordering survives sweeps over the cure threshold (B_CURE
0.30–0.60), five cohort ranges, and horizons 3–10 yr. Two scope caveats it added:
- **The antagonism (tolerance-only > simultaneous) is conditional on the Hill coefficient n=2**:
  at n≥3 the cross-repression sharpens and the antagonism can reverse; the robustness sweep did
  not vary n. The result should be read as holding for the moderate-cooperativity (n=2) switch.
- **"tolerance-first = 100% fully protected" is specific to the 5-yr horizon** — it remains the
  best arm at 6–10 yr but is not exactly 100% there.
