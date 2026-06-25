# Findings (clonal/stochastic, P6) — the resolution: Foster is a discrete-clonal CO-DOSING antagonism, avoidable by sequencing

_Capstone of the T1D arc. Supersedes nothing factual in `FINDINGS_final.md` / `FINDINGS_avidity.md`
— it completes them. Code: `t1d_clonal.py`; machine-checked by `verify_clonal.py` (**7/7 PASS**, seed-
robust, under the 4 GB cap). Status: illustrative modeling / hypothesis — a tuned existence proof, not
a validated clinical result. The originating observation (Foster 2025) is an ADA conference abstract._

## The arc, resolved
| model class | can it reproduce the Foster antagonism? | what it predicts |
|---|---|---|
| lumped bistable toggle (v1–v4) | **No** — anti-CD3 is intrinsically pro-flip | synergy; v1's "tolerance-first" was an artifact (per the reviewer) |
| avidity-resolved continuum (P5) | **No** — sub-continuum AND sub-bistable | synergy (more so, when targeted) |
| **discrete-clonal / stochastic (P6)** | **YES** | **co-dosing antagonism; sequencing rescues it** |

The same biology gives **synergy at population/continuum resolution and antagonism at clonal/stochastic
resolution.** The antagonism lives in the discreteness — exactly the deterministic↔stochastic boundary
the modeling-theory scan flagged.

## The mechanism
Antigen-specific tolerance converts targeted high-avidity autoreactive clones into **regulatory clones**
that protect the whole repertoire by bystander suppression. Anti-CD3 preferentially deletes
**just-activated, cycling cells** — i.e. the converting clones, in their vulnerable window. Because
clones are **discrete and small**, co-administered anti-CD3 can **stochastically extinguish the
would-be-regulatory clones before they establish** → the bystander protection that would have held the
rest of the repertoire never forms → relapse. Density is fungible in a continuum (it regrows), so this
is invisible there; a lost clone is gone, so it is decisive here.

## Verified result (`verify_clonal.py`, 7/7, 6 seeds, marginal-tolerance regime)
| arm | cure fraction |
|---|---|
| untreated | 0% |
| anti-CD3 monotherapy | 0% (delays, no cure) |
| antigen-specific tolerance monotherapy | **99%** |
| **simultaneous (co-dosed)** | **30%  — −68 pts vs tolerance-alone = the Foster antagonism** |
| anti-CD3 → tolerance (gap) | **97%** |
| tolerance → anti-CD3 (gap) | **92%** |

- **Seed-robust**: simultaneous = 28–32% across all 6 seeds (not stochastic noise).
- **Driven by clone-specific deletion**: the antagonism gap is 68 pts with strong preferential
  converter-deletion vs only 10 pts without it (amplified +58 pts).
- **Sequencing rescues it**: separating the two therapies by a gap restores 92–97%.

## The falsifiable, clinically-actionable prediction
**Combine anti-CD3 and antigen-specific tolerance — but SEQUENCE them; do not co-administer.** Foster's
antagonism is a *simultaneous-dosing* artifact of anti-CD3 deleting the converting clones in their
window; a gap (either order) avoids it. This is directly testable in NOD: repeat Foster's co-dosing arm
against gap-separated arms; the model predicts the gap arms recover most of the lost efficacy.

## Reconciliation of the literature
- Population/continuum biology → **synergy** (matches positive Salmonella/L. lactis: Mbongue/Cobb,
  Sassi 2023).
- The **antagonism** (Foster 2025 mRNA; Stewart 2020 microparticle) → the **co-dosing, clonal-deletion**
  regime. Both real; the difference is dosing schedule × how clone-deleting the anti-CD3 exposure is.

## Hardening — sensitivity sweep + calibration (`t1d_clonal_calib.py`)
We instrumented time-to-diagnosis and swept the regime (disease severity `rE`, tolerance strength
`conv`, suppression threshold `Ksupp`). Honest, mixed-but-positive characterization:

- **Robust as a model-class phenomenon, not a tuned point**: the co-dosing antagonism appears across a
  broad region (e.g. 5/8 cells in the decoupling slice; every aggressive/marginal-tolerance cell in the
  rE×conv slice), always with simultaneous ≪ tolerance-alone.
- **Timescale tension (disclosed)**: the *strong* antagonism wants aggressive effectors, which alone
  progress too fast (median ~0.6–0.8 yr). The realistic anchor is ~2 yr.
- **Decoupling works**: making tolerance **substrate-limited** (raise `Ksupp`) makes it marginal even
  when disease is slow — at `rE=1.4` (untreated **median ~1.24 yr**, 100% by 2 yr), the antagonism
  returns (tolerance 91–99% → simultaneous 22–71%, +28 to +69 pts). So it survives calibration to
  realistic-ish timing; it is not merely a fast-disease artifact.
- **Two honest limitations**: (a) tolerance-mono tends to stay *high-but-reducible* (82–100%) rather
  than cleanly partial (40–70%) — hitting partial-tolerance **and** ~2 yr timing **and** strong
  antagonism **and** symmetric rescue simultaneously is a tight corner, not a robust basin. (b) The
  **sequencing rescue is partial and direction-dependent**: when anti-CD3's converter-deletion dominates
  (high `Ksupp`), *tolerance-first* rescues best (let conversion finish before anti-CD3); when anti-CD3's
  debulking helps, *anti-CD3-first* is best. The robust, falsifiable claim is **"separate the two in
  time — do not co-administer"**; the optimal *order* is itself regime-dependent and testable.

## Platform axis — ONE model reconciles BOTH real combination datasets (post-assumptions-audit)
The biological-assumptions audit (`ASSUMPTIONS_AUDIT.md`) found the decisive reality-check: a **direct
human** combination trial — teplizumab + AG019 (oral L. lactis proinsulin/IL-10), **co-administered** —
showed **no antagonism** (Mathieu 2023, PMC10709251; C-peptide 112% of baseline at 6 mo vs −73% on
placebo). That would *demolish* a naive "co-dosing always antagonizes" claim — but it is exactly the
regime distinction the framework already drew. We made it explicit in the clonal model via a **platform
axis `psi`**: substrate-INDEPENDENT regulatory **expansion** (IL-10/TGF-β) vs substrate-DEPENDENT
**conversion** (which anti-CD3 aborts). One model, scanned over `psi` (means/2 seeds, marginal tolerance,
strong converter-abortion):

| `psi` (platform) | tol-mono | simultaneous | sim − tol | regime | matches |
|---|---|---|---|---|---|
| 0 — conversion (mRNA) | 99% | 31% | **−68** | **ANTAGONISM** | **Foster 2025 (NOD)** |
| 0.5 — mixed | 99% | 48% | −51 | antagonism | |
| 1.0 — mixed | 100% | 68% | −32 | antagonism | |
| 2.0 — expansion | 100% | 86% | −14 | mild | |
| 4.0 — expansion (IL-10) | 100% | 100% | **−0** | **NEUTRAL (no antagonism)** | **Mathieu 2023 (human)** |

The **same** model gives the Foster mouse antagonism (conversion platform) and the Mathieu human
non-antagonism (expansion platform). Mechanism: anti-CD3 aborts the **converting** clones (by deletion
*or* PD-1/anergy — Wållberg 2017; functionally identical for the protective outcome); a *conversion*
platform depends on exactly those clones (→ antagonism), an *expansion* platform makes regulators via
IL-10/TGF-β **independent** of them (→ anti-CD3 cannot undercut it → no antagonism).

**Corrected, data-anchored claim** (this supersedes the bare "don't co-administer"): **co-dosing backfires
ONLY for CONVERSION-type tolerance platforms (mRNA/peptide); IL-10/Treg-EXPANSION platforms
(AG019/Salmonella/L. lactis) are safe to co-administer.** Now anchored to BOTH a mouse antagonism
(Foster 2025) and a human non-antagonism (Mathieu 2023) — each landing where the model predicts.

_Honest limit:_ at high `psi` the model shows **neutral** (combination = mono = no antagonism), matching
Mathieu's "no interference"; strict *synergy* (combination > mono, which Mathieu's C-peptide hinted)
would need a sub-maximal tolerance-mono regime, which the saturated-mono calibration here does not
display. The robust, data-matched result is the **antagonism-vs-no-antagonism switch across platform type**.

## PAYLOAD — combination regime map + optimal schedule rule (`t1d_clonal_schedule.py`)
The actionable output of the combination arc, on the hardened model (means/2 seeds).

**Regime map — which combinations backfire when co-dosed, anchored to every real study:**

| platform (`psi`) | tol-only | co-dosed | prediction | real studies that land here |
|---|---|---|---|---|
| conversion (0) | 99% | 31% | **ANTAGONISM** | Foster 2025 mRNA (NOD); Stewart 2020 microparticle |
| mixed (1) | 100% | 70% | antagonism | GAD-alum / peptide combos |
| expansion (4) | 100% | 99% | **safe/neutral** | Mathieu 2023 AG019 (human); Salmonella (Cobb/Mbongue); L. lactis (Sassi 2023) |

Co-dosing backfires for **conversion-type** platforms; **expansion-type** (IL-10/Treg-boost) are safe.
Every real combination study we know lands where the model predicts.

**Schedule rule — for the backfire-prone CONVERSION platform, how a gap rescues it:**

| inter-drug gap | anti-CD3 → tol | tol → anti-CD3 |
|---|---|---|
| 0 (co-dosed) | 31% | 31% |
| ~4 wk | 82% | 10% |
| ~9 wk | 91% | 80% |
| ~17 wk | 100% | 96% |
| ~26 wk | 100% | 98% |
| ~52 wk | 0% | 100% |

**Design rule:** co-dosing is worst; **separate by ~4–6 months (17–26 wk)** and both orders recover.
**Tolerance-FIRST is the more robust order** (good from ~9 wk out to a year). **Anti-CD3-first** works at
moderate gaps but **fails if you wait too long** (~1 yr → the disease progresses before tolerance arrives) —
a falsifiable optimal-gap window. The antagonism shrinks monotonically as the gap widens (testable in NOD).

_Caveat: exact weeks are illustrative; the robust results are the qualitative rules — co-dose conversion
platforms is bad, separate by months, tolerance-first is the more forgiving order, expansion platforms
are safe to co-administer._

## Honest caveats
- A **tuned existence proof**: the antagonism requires a *marginal-tolerance, brittle-regulator* regime
  (`conv≈2–4.5`) and *strong preferential converter-deletion* (`kAC` high). It demonstrates the
  phenomenon is *reproducible in this model class*, not that NOD sits at these parameters.
- Not calibrated to Foster's data (an abstract, limited detail). Bystander suppression is a single
  lumped global term; clone counts/avidity grid are illustrative.
- The robust, model-class-level claims are: (1) continuum/bistable models **cannot** produce the
  antagonism; (2) discrete-clonal/stochastic dynamics **can**; (3) it is a **co-dosing** effect that
  **sequencing avoids**. Magnitudes are illustrative.

## Why this matters for the project
This is the first thing in the T1D line genuinely worth bringing to the modeling community (Khadra/
Pietropaolo et al.): it extends their avidity framework into the stochastic-clonal regime they have not
modeled, answers an open empirical puzzle (Foster) their tools were not pointed at, and yields a
falsifiable schedule prediction. "Something to offer" — earned by the work, before any attention is pulled.
