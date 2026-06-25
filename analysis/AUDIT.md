# AUDIT — adversarial review of the T1D sequencing-antagonism model

_Date: 2026-06-22. Auditor role: adversarial scientific reviewer (tried to BREAK the claims,
then report honestly). Scope: `t1d_model.py`, `t1d_experiments.py`, `t1d_calibration.py`,
`verify_claims.py`, against `FINDINGS.md` / `MEMO.md`. Status of the work under audit:
illustrative within-host modeling / hypothesis generation — **not** validated clinical findings._

## (i) What I verified

**`verify_claims.py`: 13/13 PASS (exit 0).** Reproduced verbatim. Notable asserted values:
bistability B→0.002 (autoimmune) / 0.931 (tolerant); untreated t_dx=2.28 yr; anti-CD3
monotherapy t_dx=2.91 yr (delays, no cure); cohort fractions tol-only 100% / sim 59% /
a3→tol 41% / tol→a3 100%; gap sweep 59%→100%; robustness 0 inversions / 20 viable (rho<1);
two-channel inversion -24 pts at rho=1.1.

**Module re-runs match FINDINGS exactly:**

| quantity | FINDINGS | re-run | match |
|---|---|---|---|
| cohort fractions (untr/a3/tol/sim/a3→tol/tol→a3) | 0/0/100/59/41/100 | 0/0/100/58.8/41.2/100 | ✓ |
| antagonism (sim − tol-only) | −41 pts | −41.2 pts | ✓ |
| gap sweep a3-first 0→1.5 yr | 59→100% | 59→100% | ✓ |
| tol-first flat | ~97–100% | ~97% | ✓ |
| robustness rho<1 | 171/171 (100%), 26 strictly better | 171/171, 26 | ✓ |
| robustness rho≤1.1 | 17/228 invert, all at highest rho | 17/228 | ✓ |
| calibration untreated median | 2.06 yr | 2.06 yr | ✓ |
| % progressed by 2 yr | ~45% | 45% | ✓ |
| anti-CD3 monotherapy delay | +0.68 yr | +0.68 yr | ✓ |
| calibration sequencing (tol/sim/a3→tol/tol→a3) | 100/65/35/97 | 100/64.8/34.8/96.8 | ✓ |

No mismatches. Every load-bearing number in FINDINGS is reproduced.

## (ii) Adversarial probes and results

### A. Is the antagonism an artifact of B_CURE / cohort / horizon? — LARGELY NO (ordering survives)

I swept `B_CURE ∈ {0.30…0.60}`, five cohort E0 ranges (mild→sick, narrow→wide), and horizons
`{3,4,5,6,8,10}` yr. **The ordering `tol-first ≥ simultaneous ≥ anti-CD3-first` held in 100% of
the conditions tested — it never inverted.** What *does* depend on the choices is the *magnitude*:

- At `B_CURE ≤ 0.40` or horizon ≤ 4 yr, all combination arms saturate at 100% and the gap
  vanishes (order is irrelevant — exactly FINDINGS' "neutral where tolerance is overwhelmingly
  effective" caveat).
- At `B_CURE ≥ 0.50` or horizon ≥ 6 yr the separation is *larger*, not smaller.
- **Caveat surfaced:** the "tol-first = 100%, fully protected" claim is **horizon-specific**.
  At a 6/8/10-yr horizon tol-first falls to 65/41/41% (still the best arm, but not 100%). The
  5-yr "100%" should be read as "best arm at the 5-yr evaluation horizon," not "permanent cure."

**Verdict:** the antagonism/ordering is a genuine property of the dynamics in the n=2,
tolerance-effective regime, *not* a threshold/horizon artifact. The chosen B_CURE=0.45 / 5-yr
horizon sit in the marginal-efficacy window where the effect is maximally *visible* — which
FINDINGS explicitly discloses.

### B. Two-channel inversion at high rho — CONFIRMED and honestly disclosed

Sweeping rho: inversion (tol-first worse than simultaneous) begins at **rho=1.10** (−5.9 pts in a
single-parameter sweep; −24 pts on the specific high-rho set used by `verify_claims`) and grows at
rho=1.20. For rho ≤ 1.0 tol-first ≥ simultaneous. This matches FINDINGS §3 ("optimal order can
invert … all at the highest rho") and the second falsifiable prediction. Honest.

### C. Parameter sensitivity — RATES robust; HILL COEFFICIENT is a genuine fragility

- **Intervention strengths:** order survives `A3_RATE ∈ {9,18,27,36}` and `TOL_RATE ∈ {6,12,18,24}`
  unchanged. Robust.
- **Hill coefficient `n` (NEW caveat — not disclosed in FINDINGS):** the *antagonism* claim is
  **fragile to n**. At n=2 tol-only (100%) > simultaneous (59%) = antagonism. But at **n=3 simultaneous
  (41%) > tol-only (24%)** and at **n=4 simultaneous (82%) >> tol-only (18%)** — the antagonism
  *reverses* (anti-CD3 *helps* tolerance). Mitigating fact: at n=3/n=4 tolerance monotherapy falls
  below the model's own "viable" threshold (≥30% cured), so these sets would be filtered out of the
  robustness sweep; "antagonism" is only well-defined when tolerance is an effective monotherapy,
  which requires n≈2 here. The **order sub-claim** (`tol-first ≥ anti-CD3-first`) is more robust — it
  held at n=1,2,3,4. **Recommendation:** FINDINGS/robustness sweep fix n=2 throughout and never vary
  it; a one-line caveat should state that the *antagonism magnitude/sign depends on the switch
  steepness n, and the result is asserted for the n=2 (tolerance-effective) regime.*

### D. Calibration honesty — CONFIRMED honest, robust to seed

Across seeds 0–5 the cohort gives untreated median 2.06–2.11 yr, ~42–45% progressed by 2 yr,
anti-CD3 monotherapy delay +0.68–0.69 yr (not cherry-picked at seed=0). FINDINGS plainly states
the model **under-produces** the TN10 ~2-yr monotherapy delay (+0.68 vs ~2 yr) and `verify_claims`
asserts anti-CD3 monotherapy banks **0%** durable control. No claim overstates monotherapy.

### E. Biological plausibility of the mechanism — CONFIRMED

Trajectory spot-check (marginal patient E0=1.30): in **tol-first**, R jumps to 0.45 by t=0.1 yr as
E is converted down (1.30→0.51), and R stays elevated (0.40 at 5 yr) → more banked B (0.50). In
**anti-CD3-first**, R is *depleted below baseline* at t=0.1 yr (0.066 vs 0.12 start) while E is
debulked → the "substrate + nascent Tregs destroyed" story. The ODEs behave exactly as the prose
describes (tolerance converts E→R; anti-CD3 deletes E and partly R).

## (iii) Overclaims to retract / caveats to add

1. **ADD caveat (Hill coefficient):** the antagonism's sign/magnitude depends on the bistable-switch
   steepness `n`; it is asserted for `n=2`. At steeper switches (n≥3) tolerance monotherapy is no
   longer strongly effective in-model and the antagonism does not hold. The *sequencing order rule*
   is the more `n`-robust claim. (No sweep varies n; recommend stating the result is conditional on
   n=2.)
2. **CLARIFY (horizon-specificity of "100%"):** "tolerance-first = 100%, fully protected" is the
   best arm *at the 5-yr horizon*; at 6–10 yr tol-first declines (to ~41–65%) though it remains the
   best arm. Suggest phrasing "best arm / fully protected at the 5-yr evaluation horizon."

No numerical claim in FINDINGS was found to be wrong or non-reproducible. No retraction of a stated
number is required; the two items above are scope-narrowing caveats, not corrections of values.

## (iv) Per-claim verdict table

| # | Claim (FINDINGS) | Verdict |
|---|---|---|
| 1 | Bistable switch with autoimmune (B→0.002) & tolerant (B→0.931) basins | **SUPPORTED** |
| 2 | Untreated stage-2 reaches dx ~2 yr; anti-CD3 monotherapy delays only, no cure | **SUPPORTED** |
| 3 | Tolerance monotherapy → 100% durable control (cohort) | **SUPPORTED** (at n=2, 5-yr, B_CURE=0.45) |
| 4 | Antagonism: simultaneous (59%) < tol-only (100%), −41 pts | **SUPPORTED** for n=2; **conditional** — reverses at n≥3 where tolerance is weak (add caveat) |
| 5 | Sequencing rule: tol-first ≥ simultaneous > anti-CD3-first | **SUPPORTED** — survived all B_CURE, cohort, horizon, rate, and n perturbations tested |
| 6 | "tol-first fully protects (100%)" | **SUPPORTED but horizon-specific** (best arm; not 100% beyond 5 yr) |
| 7 | Falsifiable gap prediction: anti-CD3-first recovers with gap (59→100%); tol-first flat | **SUPPORTED** |
| 8 | Robustness rho<1: tol-first ≥ simultaneous in 171/171 viable sets | **SUPPORTED** |
| 9 | Two-channel caveat: order inverts for strongly Treg-depleting anti-CD3 (rho≥1.1), 17/228 | **SUPPORTED & honestly disclosed** |
| 10 | Calibration: median 2.06 yr, ~45% by 2 yr; antagonism persists on clinical cohort | **SUPPORTED** (seed-robust) |
| 11 | Model under-produces teplizumab monotherapy delay (+0.68 vs ~2 yr) | **SUPPORTED** (honest self-limitation) |

## (v) Bottom line

The repo is **reproducible and largely honest**. `verify_claims.py` passes 13/13 and every
load-bearing number in FINDINGS is reproduced to the digit. The headline **sequencing rule —
don't give anti-CD3 first; tolerance-first is best — is robust**: it survived variation of the cure
threshold (0.30–0.60), five cohort ranges, six horizons, intervention-strength changes, and the
Hill coefficient (n=1–4), inverting only when anti-CD3 is made strongly Treg-depleting (rho≥1.1),
which FINDINGS already discloses as the second falsifiable prediction. The mechanism behaves as
described at the trajectory level, and the calibration limitation is disclosed plainly.

Two caveats should be **added** (not retractions of any value): (a) the *antagonism* (tol-only >
simultaneous) is conditional on the n=2 / tolerance-effective regime and reverses at steeper
switches where tolerance is a weak monotherapy — and no sweep varies n; (b) "tolerance-first =
100%, fully protected" is specific to the 5-yr evaluation horizon (it is the best arm, but not 100%,
at 6–10 yr). With those two scope caveats the work stands as a sound illustrative hypothesis-
generation model — explicitly not a validated clinical result.

---

## Re-audit (2026-06-22, pre-publication)

_Second adversarial pass, triggered by the addition of a manuscript (`paper/MANUSCRIPT.md`), an
attestation (`attestation.json`), a publication config (`pub.yaml`/`CITATION.cff`), and a
pre-publication novelty recheck (`NOVELTY.md` §"Pre-publication novelty recheck"). Goal: catch any
overclaim before the preprint goes public._

### A. Re-verification (capped runs)

- **`verify_claims.py`: 13/13 PASS, exit 0** (re-run under `ulimit -v 4194304; timeout 595`). Asserted
  values reproduced verbatim: bistability B→0.002 / 0.931; untreated t_dx=2.28 yr; anti-CD3 mono
  t_dx=2.91 yr (delay-only); cohort tol-only 100% / sim 59% / a3→tol 41% / tol→a3 100%; gap 59→100%;
  Treg-sparing robustness 0 inversions / 20 viable; high-rho inversion −24 pts at rho=1.1.
- **`attestation.json`** shows `summary.all_passed: true`, `results[0].status: "pass"`, exit_code 0,
  `working_tree_dirty: false`, stdout_tail "13/13 checks passed". Consistent with the live run.
- **`claims.yaml`** (single claim `all`, `expect.exit_code: 0`): its prose statement accurately
  enumerates exactly what `verify_claims.py` asserts (bistability, ~2-yr progression, anti-CD3
  delay-only, tol 100%, antagonism sim 59% < tol 100%, sequencing rule, gap prediction, no inversion
  rho<1, two-channel inversion at high rho). **No overstatement** — it does not claim clinical
  validity, only re-derivation of FINDINGS numbers.

### B. Adversarial re-probe of the two load-bearing robustness facts (capped, FULL grid)

`verify_claims.py` only checks a reduced 2-level grid (20 viable sets). I re-ran the **full**
5-parameter grid (`/tmp/reprobe.py`, capped):
- **(a) Treg-sparing regime rho<1: 0 inversions / 171 viable sets, 26 strictly better** — reproduces
  the headline "171/171 (100%), strictly better in 26" claim in FINDINGS/README/MANUSCRIPT to the
  digit. No inversion anywhere.
- **(b) Order DOES invert at rho≥1.1:** delta(tol-first − sim) = +0 pts at rho=0.9, +0 at rho=1.0,
  **−24 pts at rho=1.1**, −18 at rho=1.2. The inversion onset at rho=1.1 and the −24 pts magnitude
  match the disclosed two-channel caveat exactly. Both load-bearing facts hold.

### C. Manuscript audit (the new surface)

Every quantitative claim in `paper/MANUSCRIPT.md` was checked against FINDINGS / verify output:

| manuscript claim | value | matches source? |
|---|---|---|
| bistable basins | B→0.002 / 0.931 | ✓ |
| tol-only / sim / a3-first / tol-first | 100 / 59 / 41 / 100 | ✓ |
| antagonism | −41 pts | ✓ (sim 59 − tol 100) |
| gap sweep a3-first | 59→100% to ~1.5 yr; tol-first flat ~97–100% | ✓ |
| robustness rho<1 | 171/171, strictly better in 26 | ✓ (full-grid re-probe) |
| two-channel | 17/228 invert, all highest rho | ✓ |
| calibration | median 2.06 yr, ~45% by 2 yr, tol/sim/a3→tol/tol→a3 = 100/65/35/97 | ✓ |
| monotherapy under-production | +0.68 yr vs ~2 yr | ✓ |

**No number in the manuscript is unsupported or inconsistent with FINDINGS/verify.**

- **Falsifiable-prediction ordering check.** §4 states the model predicts **(a) tolerance-first >
  (b) simultaneous > (c) anti-CD3-first**. Cohort numbers: 100% > 59% > 41% — **strictly consistent**.
  The abstract's "(a)>(b)>(c)" and §3.2's `tol-first ≥ tol-only > simultaneous > anti-CD3-first` agree.
- **"First mechanistic within-host model" — defensible.** The abstract/§4 hedge it ("To our knowledge")
  and NOVELTY.md's two independent S2 sweeps (126-paper + 61-paper recheck) found no mechanistic/ODE
  model of this drug pair; nearest neighbours (Alexander & Wahl 2011 motif; Dalton 2025 single-therapy
  Treg model) do not state the combination or a sequencing rule. Acceptable as a hedged novelty claim.
- **Phenomenon framed as ANTICIPATED, not discovered — correct.** §4 explicitly: "It does not claim to
  discover the antagonism — the *phenomenon* was anticipated empirically (Stewart 2020; Foster 2025) —
  but to **explain** it." Stewart 2020 and Foster 2025 are both cited in the intro and references.
  Messenheimer 2017 (cancer sequencing analogy) is disclosed, not passed off as the same finding.
- **All three honest limitations are carried into the manuscript** (§4 Limitations): (i) n=2-dependence
  of the antagonism ("at n≥3 ... can reverse; the robustness sweep did not vary n"); (ii) "100%" is
  5-yr-horizon-specific ("not exactly 100%, at 6–10 yr"); (iii) under-produced monotherapy delay
  (+0.68 vs ~2 yr). The manuscript even names the self-audit as the reason for the "rule for a known
  antagonism, not a discovery" framing. **The caveats are not stranded in FINDINGS.**

### D. Cross-document consistency

README, ABSTRACT, FINDINGS, METHODS, MANUSCRIPT, claims.yaml, pub.yaml, CITATION.cff, and the
attestation all tell the same story with the same numbers (0/0/100/59/41/100; −41 pts; 59→100% gap;
171/171; 17/228 at high rho; 2.06 yr / ~45%; calibration 100/65/35/97; +0.68 vr ~2 yr). The
illustrative/hypothesis-generation, not-clinical-findings disclaimer is present in every doc. No
retracted or caveated claim reappears unqualified anywhere.

### E. NEW issues found

1. **(NON-SCIENTIFIC, must-fix-before-post) Broken figure reference in `pub.yaml`.** `pub.yaml`
   `figures.og_image: "analysis/fig1.png"` — **that file does not exist**. The actual figures are
   `analysis/t1d_mechanism.png`, `t1d_cohort.png`, `t1d_gap.png`, `t1d_calibration.png`. The
   manuscript's own figure list uses the correct filenames, so this is only a publishing-config
   typo, not a scientific overclaim, but it will produce a broken social-card/OG image on posting.
   Fix: point `og_image` at a real file (e.g. `analysis/t1d_cohort.png`). *(Not fixed here — task
   scope restricts edits to AUDIT.md.)*
2. **No new overclaim.** No quantitative claim in the manuscript, abstract, README, or claims.yaml
   overstates what verify asserts or what FINDINGS supports. The two scope caveats flagged in the
   first audit (n=2-dependence; 5-yr-horizon "100%") are now explicitly in the manuscript.

### F. Recommendation

**GO-WITH-FIXES.** The science is reproducible (13/13, both robustness facts confirmed on the full
grid), the manuscript is numerically clean and consistent with every other document, the novelty is
appropriately hedged, the phenomenon is correctly framed as anticipated (Stewart 2020 / Foster 2025)
rather than discovered, and all three honest limitations are carried through. The **only** blocker is
cosmetic: the dangling `pub.yaml` `og_image: analysis/fig1.png` reference should be repointed to an
existing figure before the preprint/social card is generated. With that one-line fix, this is a GO to
post — explicitly as an illustrative within-host modeling hypothesis, not a validated clinical result.

## Post-audit hardening (2026-06-22, after the re-audit above)

After the re-audit's GO-WITH-FIXES, two changes were applied: (1) the dangling `pub.yaml`
`og_image` was repointed to a real figure (`analysis/t1d_cohort.png`); (2) **`verify_claims.py`
was strengthened from 13 → 24 checks** so every cited figure is machine-asserted, not just the
qualitative invariants. The seven added checks PIN, within tolerance, the exact cohort
durable-control fractions (0/0/100/58.8/41.2/100 %) and the exact calibration figures (untreated
median 2.06 yr, ~45% progressed by 2 yr, anti-CD3 monotherapy delay +0.68 yr). The full-grid
robustness exact counts (171/171; 17/228) were deliberately NOT added to verify — the ~38k-integration
sweep exceeds the per-claim 595 s attestation cap — they remain reproduced by `t1d_experiments.py`
and re-confirmed in the re-audit, with verify asserting the no-inversion invariant on a reduced grid
(same policy as the HIV exemplar for its expensive sweeps). Re-run capped: **24/24 PASS, 58 s, 110 MB
peak**; re-attested.

---

## Post-publication reversal (2026-06-22) — the v1 headline is WITHDRAWN as an artifact

_This is the most important entry in this file. After the preprint was published (GitHub / Zenodo
10.5281/zenodo.20804558 / Pages / social) we sent the result to an immunologist for review; his
critique, plus a verified-biology rebuild, overturned the headline. Both audits above — which passed
the repo as "reproducible and largely honest" — **missed it**, and it is worth being precise about why._

### The critique (an immunologist reviewer)

1. **No thymic Treg source** — the therapeutic Treg pool was built entirely by peripheral conversion.
   *Valid as stated.* (His proposed fix — a NOD thymic-precursor *deletion* deficit — is itself
   contradicted by the NOD literature: thymic Treg output is normal-to-enhanced, Feuerer 2007/09. The
   real bottleneck is peripheral expansion, Mhanna/Tang 2021. So we corrected the gap, not via his
   mechanism.)
2. **Tolerance-monotherapy = 100% was uncalibrated** — a byproduct of the parameters, anchored to no
   measured tolerance result; tolerance is constitutively impaired in T1D. **Correct and load-bearing.**
3. **The operating point inverted the clinical rationale** — with tolerance alone = 100% and anti-CD3
   alone = 0%, the model argues *against* combining; the real reason anti-CD3 is added is that
   antigen-specific tolerance under-delivers. **Correct — the fatal point.**

### Why both prior audits missed it (the honest post-mortem)

The audits above were **internal-consistency and reproducibility** audits. They confirmed every number
re-derived (24/24), that the docs agreed, that the ordering survived threshold/cohort/horizon/`n`
sweeps, and that the disclosed caveats were carried. **None of that can catch the actual error**, which
was not a reproducibility failure but a **calibration / framing failure**: the *operating point itself*
(tolerance-monotherapy ≈ 100%, anti-CD3 ≈ 0%) was never anchored to an empirical number, and in that
regime an "antagonism" is nearly forced — anything perturbing an already-maximal monotherapy can only
look harmful. An adversarial-reproduction audit re-derives the math inside the chosen regime; it does
not ask *"is this regime the right one, and does it invert the clinical rationale?"* That question
needed a domain expert, and is exactly the gap the reviewer filled. **Lesson for the method: a verify/audit
pass that re-derives numbers is necessary but not sufficient — every load-bearing operating point needs
an explicit empirical calibration anchor (or a stated `UNCALIBRATED` flag), and a "does this invert the
known clinical rationale?" check, before publication.**

### The verified-biology rebuild and the structural result (v2 → v3 → v4)

Rebuilt on retrieved primary literature (peripheral bottleneck; durable beneficial anti-CD3
hyporesponsiveness; effector resistance), the model **reverses** the v1 conclusion and produces a
clean negative result:

- **v3** (peripheral two-channel) and **v4** (v3 + an explicit acute-deletion channel added *to try to
  manufacture the antagonism*) both predict the combination **never antagonizes**: best-combo −
  best-mono **≥ 0 at every platform-independence `psi`**, and **synergizes** (+65/+76 pts at mid `psi`
  in v3; **+100 pts at `psi`=0 in v4**, the pure-antigen Foster/Stewart regime).
- **The structural negative result:** anti-CD3's effector-reduction + durable hyporesponsiveness are
  intrinsically pro-tolerant in a bistable population model, so **no population channel can flip the
  sign**. The Foster 2025 / Stewart 2020 antagonism therefore requires a **clone-level acute mechanism**
  (deleting the specific just-activated converting clones) that a deterministic lumped-pool ODE averages
  away. This is now `FINDINGS_final.md`, asserted by **`verify_claims_vfinal.py` (7/7 PASS, capped)**.

### Status of the published artifacts

The public v1 (README/FINDINGS/MANUSCRIPT/Zenodo/Pages/social) still asserts the withdrawn
tolerance-first headline. A post-publication revision is **owed and pending sign-off**: README +
FINDINGS now carry a SUPERSEDED banner pointing here and to `FINDINGS_final.md`; a Zenodo new version
and a reply to the reviewer are prepared but **not yet sent** (held deliberately until the v-final is
reviewed). v1's files are retained, clearly marked superseded, as the honesty record.
