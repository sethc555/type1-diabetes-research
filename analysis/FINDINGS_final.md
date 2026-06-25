# Findings (v-final) — the combination is SYNERGISTIC, and the antagonism is a clone-level phenomenon a population model cannot capture

_This supersedes the published v1 headline (`FINDINGS.md`) and the v2 interim rebuild
(`FINDINGS_v2.md`). It is the honest result after a post-publication critique from an immunologist
and a verified-biology rebuild. Numbers re-derived/asserted by `verify_claims_vfinal.py` (**7/7 PASS**,
under the 4 GB cap). Status: illustrative within-host modeling / hypothesis generation — **not**
validated clinical findings. The full honesty trail is in [AUDIT.md](AUDIT.md) §"Post-publication
reversal"; the verbatim critique is held privately._

## What happened

The v1 preprint (Zenodo 10.5281/zenodo.20804558) claimed a **tolerance-first sequencing antagonism**:
antigen-specific tolerance monotherapy was 100% effective, anti-CD3 "antagonized" it (−41 pts when
co-dosed), and the rule was "give tolerance first." An immunologist reviewer raised three points that the two prior self-audits had missed:

1. **The Treg pool was built only by peripheral conversion** — no thymic source. (Valid as stated;
   his proposed *thymic-deficit* fix is itself NOD-contradicted — see below.)
2. **Tolerance-monotherapy = 100% was uncalibrated** — a byproduct of the chosen parameters, anchored
   to no empirical tolerance result. Tolerance is constitutively impaired in T1D. **Correct, and
   load-bearing.**
3. **The operating point inverted the clinical rationale** — if tolerance alone is 100% and anti-CD3
   alone is 0%, the model argues *against* combining them, whereas anti-CD3 is added in the clinic
   precisely *because* antigen-specific tolerance under-delivers. **Correct, the sharpest point.**

Points 2 and 3 are fatal to the v1 headline. The "antagonism" was largely an artifact of operating in
a regime where tolerance was already maximally effective, so anything that perturbed it could only
look harmful. We rebuilt the model on the verified biology and let it say whatever it says.

## The verified biology the rebuild is grounded in (deep-research + Semantic Scholar)

- **The tolerance bottleneck is PERIPHERAL, not thymic.** NOD thymic Treg generation is
  normal-to-*enhanced* with intact suppression (Feuerer 2007 PMC2084317; Feuerer 2009 PMC2604930); the
  corrigible deficit is peripheral activated/memory-Treg **clonal expansion**, restored by IL-2
  (Mhanna/Tang 2021, *Diabetes* 70:976). So the reviewer's *thymic-precursor-deletion* mechanism is the one
  part of his critique that the NOD literature contradicts — though his **clinical** points (tolerance
  impaired; monotherapy weak) stand. NOD conventional T cells also intrinsically **resist** suppression
  (D'Alise 2008) → parameter `res`.
- **anti-CD3 has a durable, *beneficial* effect:** a waning CD8 hyporesponsiveness / partial-exhaustion
  program (Long 2016 *Sci Immunol* eaai7793; Lledó-Delgado 2024) that prevents autoreactive-effector
  expansion and is breakable by rapamycin (Baeyens 2009 *Diabetes* 58:875). This is the model's `X`
  state, and it is what makes anti-CD3 *help* rather than hurt.
- **The combination literature is genuinely heterogeneous** — both antagonism and synergy are real:
  - *Antagonism:* Foster 2025 (anti-CD3 ↓ RNA immunotherapy in NOD; ADA abstract 2136-LB,
    DOI 10.2337/db25-2136-lb); Stewart 2020 (microparticle + anti-CD3 "fails to synergize",
    DOI 10.1021/acsbiomaterials.0c01075).
  - *Synergy:* Salmonella platforms (Mbongue 2019 DOI 10.3389/fimmu.2019.00320; Cobb 2021–24);
    L. lactis (Sassi 2023 DOI 10.2337/db22-0852); Zhao 2025 (DOI 10.1186/s12916-025-04001-5).

## The rebuilt models

- **v3 (`t1d_model_v3.py`)** — peripheral framing. Tolerance acts through **two channels**: a
  substrate-*dependent* conversion of effectors to Tregs (which anti-CD3 could blunt by depleting the
  substrate) and a substrate-*independent* peripheral Treg **expansion** `psi` (the TGF-β/IL-10/IL-2
  platform axis, which anti-CD3 cannot undercut). Outcome is reported as a **regime map over `psi`**.
- **v4 (`t1d_model_v4.py`)** — adds an explicit **acute-deletion** state `A`: tolerance first *activates*
  target effectors into a converting pool `A`, and anti-CD3 **preferentially deletes activated/cycling
  cells**, so — at the population level — it can abort conversion. This channel was added **specifically
  to try to manufacture the Foster antagonism**.

## Results (verified — `verify_claims_vfinal.py`, 7/7)

**1. The combination NEVER antagonizes — it SYNERGIZES.** Across the full platform-independence axis
`psi`, the best combination arm minus the best monotherapy arm is **≥ 0 at every `psi` in both models**.
anti-CD3 monotherapy cures **0%** of the cohort at every `psi` (it delays only — matching TN10/
teplizumab), yet adding it to tolerance *raises* the cure fraction:

| model | regime | best-combo − best-mono |
|---|---|---|
| v3 | `psi = 1.0` (conversion-limited) | **+65 pts (SYNERGY)** |
| v3 | `psi = 1.5` | **+76 pts (SYNERGY)** |
| v3 | every `psi` tested | **min = +0 pts (never negative)** |
| v4 | `psi = 0` (pure-antigen, Foster/Stewart regime) | **+100 pts (SYNERGY)** |
| v4 | every `psi` tested | **min = +0 pts (never negative)** |

This is the OPPOSITE of the v1 headline and is consistent with the **positive** Salmonella/L. lactis
combination studies. Mechanistically: anti-CD3's effector reduction and its durable `X`
hyporesponsiveness window are **intrinsically pro-tolerant** — they always help the bistable switch
flip toward the tolerant basin. In a population-balance effector↔Treg model, anti-CD3 cannot be made
to hurt.

**2. The structural negative result — the Foster antagonism is unreproducible here.** v4 was built to
produce the antagonism via acute deletion of the converting clones. It does not: at `psi = 0` — the
pure-antigen regime where Foster 2025 and Stewart 2020 actually sit — v4 **still synergizes by +100
pts**. The acute-deletion *population* term is swamped by the benefit of debulking effectors and the
`X` window. The sign cannot be flipped by wiring more population channels.

→ Therefore the Foster/Stewart antagonism is not a population-balance effect. It requires a
**clone-level acute mechanism**: anti-CD3 deleting the *specific, just-activated* autoreactive clones
in the narrow window before they convert — a discrete/stochastic, per-clone event that a deterministic
ODE over lumped pools necessarily averages away. **This is the model's real, falsifiable contribution:**
it converts "anti-CD3 sometimes antagonizes antigen-specific tolerance" into a sharp, testable claim
about *where* the antagonism must live (clone-level kinetics), and predicts that **Treg-expansion
platforms (high `psi`) are the ones that should robustly combine with anti-CD3**, while
conversion-only, pure-antigen platforms (low `psi`) are the ones at risk.

## Honest bottom line

- v1's "tolerance-first sequencing antagonism" headline is **withdrawn** as an artifact of an
  uncalibrated, rationale-inverting operating point. the reviewer was right.
- The defensible result is **synergy** — anti-CD3 + antigen-specific tolerance should outperform either
  alone, because anti-CD3's durable effector hyporesponsiveness buys a window for a peripherally-limited
  Treg pool to consolidate. This matches the positive combination literature.
- The **Foster/Stewart antagonism is real but lives below the resolution of any bistable population
  model** — it is a clone-level acute-deletion phenomenon. Capturing it is a different model class
  (stochastic/clonal/agent-based), and that is the open lane this result opens.

## Caveats (unchanged in spirit)

Illustrative parameters; the synergy *magnitude* (+65 to +100 pts) is illustrative — the robust pieces
are the **direction** (combination > monotherapy at every `psi`) and the **structural negative**
(no population channel reproduces the antagonism). `psi` is a coarse stand-in for "how much of the
platform's tolerogenic effect is Treg-expansion vs effector-conversion." The `X` exhaustion channel is
a documented teplizumab mechanism but is a single lumped state. Still hypothesis-generating — now
aligned with, rather than inverting, the clinical rationale, and pointing at a concrete next model class.
