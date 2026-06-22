# Methods

> **Status — illustrative within-host modeling / hypothesis generation, NOT clinical findings.**
> Consolidated methods for the model in [`t1d_model.py`](t1d_model.py), the experiments in
> [`t1d_experiments.py`](t1d_experiments.py), and the calibration in
> [`t1d_calibration.py`](t1d_calibration.py). Results: [FINDINGS.md](FINDINGS.md). Literature lane
> and calibration anchors: [MEMO.md](MEMO.md).

## 1. Model

A 3-state within-host ODE. State (time in **years**): β-cell mass `B` (fraction of healthy, ~
proportional to C-peptide, 0..1); autoreactive effector burden `E` (a.u.); antigen-specific Treg
burden `R` (a.u.). The effector and Treg pools form a **mutual-repression bistable switch** (each
self-promotes via a Hill term of order `n=2`, each represses the other — the standard motif for
immune cell-fate decisions). β-cell mass grows logistically and is killed in proportion to effector
burden.

### Equations (n = 2 Hill)

```
dE/dt = bE + VE * E^n/(K^n+E^n) / (1+(R/Ki)^n)  - dE*E - u_a3(t)*E - u_tol(t)*E
dR/dt = bR + VR * R^n/(K^n+R^n) / (1+(E/Ki)^n)  - dR*R + phi*u_tol(t)*E - rho*u_a3(t)*R
dB/dt = rhoB * B*(1-B) - kappa * E * B
```

`u_a3(t)` and `u_tol(t)` are the time-dependent intervention rates (square pulses; see §3). The
switch is biased toward autoimmunity because `VR < VE`. There are two stable basins:

- **autoimmune** (E high, R low → β-cells killed): in [`verify_claims.py`](verify_claims.py), from
  IC `[0.60, 1.10, 0.12]` over 20 yr, `B → 0.002`;
- **tolerant** (E low, R high → β-cells preserved): from IC `[0.60, 0.10, 1.20]`, `B → 0.931`.

Late stage 2 sits in the autoimmune basin. The two interventions, **same total drug, different
order**: antigen-specific tolerance *converts* effectors to Tregs (flux `phi*u_tol*E` from `E` into
`R`; it needs effectors present to convert); anti-CD3 is lymphodepleting — it removes effectors
(`u_a3*E`) but also depletes Tregs (`rho*u_a3*R`), so by itself it only transiently debulks `E` and
the switch reverts.

## 2. Parameters

Operating point (the `P` dict in [`t1d_model.py`](t1d_model.py)). Illustrative; the antagonism is
robust over a region (§6).

| param | value | meaning |
|---|---|---|
| `bE` | 0.08 | baseline effector influx |
| `VE` | 1.80 | effector self-activation max rate |
| `K` | 0.50 | half-saturation of self-activation |
| `Ki` | 0.50 | cross-repression half-saturation |
| `dE` | 0.80 | effector loss (1/yr) |
| `bR` | 0.04 | baseline Treg influx |
| `VR` | 1.40 | Treg self-activation max rate (< `VE`: switch biased toward autoimmunity) |
| `dR` | 0.50 | Treg loss (1/yr) |
| `phi` | 0.40 | tolerance conversion efficiency (fraction of removed E that becomes R) |
| `rho` | 0.90 | anti-CD3 Treg-depletion factor (relative to its effector-depletion rate) |
| `rhoB` | 0.60 | β-cell logistic regeneration rate (1/yr) |
| `kappa` | 0.40 | per-effector β-cell kill rate |
| `n` (`N_HILL`) | 2 | Hill coefficient |

Intervention strengths / durations (effective per-year rates during a short clinical course):

| const | value | meaning |
|---|---|---|
| `A3_RATE` | 18.0 (1/yr) | anti-CD3 effector-depletion rate while dosing |
| `A3_DUR` | 14/365 yr | anti-CD3 course length ~14 days (TN10 single course) |
| `TOL_RATE` | 12.0 (1/yr) | antigen-specific tolerance conversion rate while dosing |
| `TOL_DUR` | 30/365 yr | tolerance course length ~30 days |
| `B_DX` | 0.30 | stage-3 diagnosis threshold (fraction of healthy β-cell mass) |
| `B_CURE` | 0.45 | "durable control" threshold at the evaluation horizon |
| `HORIZON` | 5.0 yr | evaluation horizon |

## 3. Intervention schedules (arms)

All arms deliver the **same total drug**; only order/overlap differs (`arms(gap)` in
[`t1d_model.py`](t1d_model.py)). `gap` is the inter-drug interval (years) for the two sequential
arms. Each agent is a square pulse of its rate over its duration starting at the scheduled time.

| arm | anti-CD3 start | tolerance start |
|---|---|---|
| untreated | — | — |
| anti-CD3 only | 0.0 | — |
| tolerance only | — | 0.0 |
| simultaneous | 0.0 | 0.0 |
| anti-CD3 → tol | 0.0 | `gap` (default 0.25 yr) |
| tol → anti-CD3 | `gap` | 0.0 |

## 4. Cohort / severity sampling

The per-patient severity knob is the baseline effector burden `E0` in the late-stage-2 initial
condition `stage2_ic(E0) = [0.60, E0, 0.12]` (β-cell mass partly reduced, effectors winning, Tregs
low). Higher `E0` = sicker.

- **Cohort durable-control fraction** (`cure_fraction`, P1/P2): severity gradient
  `E0 ∈ linspace(0.70, 1.50, 17)`; fraction with banked β-cell mass > `B_CURE` at `HORIZON`.
- **Calibration cohort** (P3, [`t1d_calibration.py`](t1d_calibration.py)): n = 500, seeded;
  heterogeneous in *both* effector severity and residual β-cell mass —
  `E0 ~ Normal(1.05, 0.22)` clipped to [0.72, 1.7] and `B0 ~ Normal(0.52, 0.12)` clipped to
  [0.33, 0.85], with Tregs fixed at 0.12. Spread chosen so the untreated median time-to-diagnosis
  ~2 yr and ~half progress by ~2 yr (a broad, TrialNet-like curve).

## 5. Outcome metrics

- **`time_to_dx`** — first time `B` crosses below `B_DX` (0.30), linearly interpolated between
  solver samples; `inf` if never crossed.
- **`banked_mass`** — `B` interpolated at the horizon (5 yr).
- **`cure_fraction`** — fraction of the severity cohort with `banked_mass > B_CURE` (0.45) at the
  horizon (durable control). Because the switch is bistable, per-patient outcomes are binary, so
  results are reported as cohort fractions and the antagonism is visible in the marginal-efficacy
  regime.
- **Kaplan-Meier-style progression** (P3) — fraction not yet diagnosed (`B > B_DX`) vs time;
  median read off the survival curve.

## 6. Numerics and robustness-sweep design

**Integration.** `scipy.integrate.solve_ivp`, method **LSODA**, `rtol=1e-8`, `atol=1e-10`,
`max_step=0.012`; default `t_end = 8.0` yr, 2500 evaluation points. States are floored at 0 inside
the RHS. The system is deterministic (no stochastic component), so verification checks assert actual
values, not just direction.

**Robustness sweep** (`robustness_sweep` in [`t1d_experiments.py`](t1d_experiments.py)). A
5-parameter grid: `phi ∈ {0.30, 0.40, 0.50}`, `rho ∈ {0.5, 0.7, 0.9, 1.1}`,
`VR ∈ {1.3, 1.4, 1.5}`, `Ki ∈ {0.45, 0.50, 0.55}`, `kappa ∈ {0.36, 0.40, 0.44}`. A parameter set is
**viable** only if untreated cure fraction ≤ 0.2 *and* tolerance-only ≥ 0.3 (i.e. the regime is
disease-progressing and tolerance-responsive). For each viable set we record
`delta = cure(tol→anti-CD3) − cure(simultaneous)`. The default run restricts to the **Treg-sparing
regime** `rho < 1` (matching teplizumab's documented Treg-sparing/expanding profile); passing
`rho_max=1.1` includes strongly Treg-depleting anti-CD3, where the optimal order can invert (the
two-channel caveat). [`verify_claims.py`](verify_claims.py) asserts the qualitative invariant — no
order-inversion in the Treg-sparing regime — on a reduced 2-level grid for speed, plus a single
high-`rho` point demonstrating inversion.

## 7. Calibration anchors (from [MEMO.md](MEMO.md))

- **TN10 teplizumab (stage 2):** single 14-day course; placebo median to diagnosis ~24–27 months,
  teplizumab ~48–50 months → ~2-year median delay (Mathieu 2025; Zaitoon 2025; Gitelman 2026
  TEPLI-REAL).
- **TrialNet staging consensus (Phillip 2024):** stage 2 carries high near-term risk — roughly half
  progress to stage 3 within ~2 years; ~11%/yr baseline.
- **Metabolic inflection (Montaser 2026):** accelerated β-cell decline begins ~1–2 yr before
  diagnosis.
- **β-cell decline backbone (Carr 2026):** Oral Minimal Model φtotal trajectories aligned to S1→S2.
- **Treg-induction kinetics (Cabello-Kindelan 2019; Serr 2016):** parameterize the tolerance
  conversion term.
- **Combination antagonism to reproduce (Foster 2025, "2136-LB"):** anti-CD3 reduces
  antigen-specific-immunotherapy efficacy in NOD incidence curves.

## 8. Derived criterion (P-analytic — `t1d_analytic.py`)

The intervention courses (~2–4 weeks) are near-impulsive relative to the year-scale switch, so in
the impulsive limit each integrates **exactly** to a linear map on `(E, R)` (the slow baseline /
self-activation / decay terms contribute `O(rate·τ) ≈ 0.04–0.07` over a course and are dropped):

```
T = exp(-sigma_tol * tau_tol) = 0.373      A = exp(-sigma_a3 * tau_a3) = 0.501
tolerance:  E -> T*E ,        R -> R + phi*(1-T)*E          (convert effectors to Tregs)
anti-CD3:   E -> A*E ,        R -> A**rho * R               (delete effectors; deplete Tregs)
```

For **simultaneous** co-administration the two act on the same decaying effector pool, integrated in
two phases (both over `[0, tau_a3]`, tolerance alone over `[tau_a3, tau_tol]`); composing the maps
is incorrect because it over-credits the substrate. From these maps:

- **Antagonism factor** `A_antag = Y_sim/Y_tol = A**rho * sigma_tol/(sigma_tol+(1-rho)*sigma_a3)`
  (= 0.467; measured from the exact maps, 0.51) — factorizes into Treg-destruction `A**rho` and
  substrate-competition `sigma_tol/(sigma_tol+(1-rho)sigma_a3)`.
- **Order-inversion law** `tol-first optimal <=> A**rho > A <=> rho < 1`, crossover `rho* = 1`.
- **Separatrix criterion** `Q = R_f/E_f > Q_crit` with `Q_crit = 0.886` the `R/E` ratio at the
  toggle's saddle (located by bisection on the basin of the intervention-free (E,R) subsystem);
  reproduces the cure *ordering* but not exact marginal-arm fractions (the proxy is blunt near the
  separatrix — those need the full ODE).

Validation: `verify_claims.py` asserts the antagonism factor (closed-form ≈ measured) and the
order-inversion crossover (sign of `A**rho - A` flips at rho=1 and the ODE benefit flips with it).
The only non-closed-form step is a short relaxation of the (E,R) subsystem across the inter-drug
gap for the sequential arms.
