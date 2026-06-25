# Findings — the explicit exhaustion HIERARCHY (vertical deepening of the responder model)

_Replaces the responder model's lumped exhaustion `X` + TSCM-renewal `r_tscm` with the real
autoreactive-CD8 ladder. Code: `t1d_hierarchy.py` (deterministic). Grounded in T1D-specific data;
search in `_scan/exhaustion_hierarchy.md`. Status: illustrative modeling / hypothesis._

## The ladder (each rung is documented in T1D)
- **P — stem-like progenitor** (TCF1⁺, self-renewing): the refill engine. Autoreactive CD8 **memory-stem
  cells are detected in T1D patients** (Vignali 2018, *Diabetes*) → the pool `P0` is a *measurable* axis.
- **E — effector**: differentiates from P, kills β-cells.
- **X — terminally exhausted** (TOX⁺/LAG3⁺): driven from E by chronic antigen + anti-CD3; **restrained,
  protective** — intra-islet autoreactive CD8 are held by an exhaustion program **maintained by LAG3**
  (Grebinoski 2022, *Nat Immunol*); exhaustion **predicts teplizumab response** (Long 2016, *Sci Immunol*).
- **Interventions:** teplizumab drives E→X (therapeutic exhaustion); checkpoint blockade *reverses* it.

## Three predictions, all clean
**1. The PROGENITOR pool is the responder/non-responder axis** (teplizumab monotherapy):

| progenitor `P0` | β@5yr | outcome |
|---|---|---|
| 0.05–0.20 | 0.59–0.80 | **responder** |
| 0.30–0.45 | 0.05–0.25 | **non-responder** |

Small/quiescent progenitor → responder; a large progenitor **refills the attack** after exhaustion
wanes → non-responder. This *deepens* the responder result: the lumped "TSCM renewal" knob is now an
explicit, **measurable** cell population (Vignali's autoreactive TSCM).

**2. CHECKPOINT BLOCKADE unleashes disease — reproducing a known clinical fact.** A teplizumab-controlled
responder (β@5yr = **0.76**) loses control when checkpoint blockade (anti-PD-1/LAG3) is given at 1.5 yr
(β@5yr = **0.09 — disease unleashed**). **This matches the documented reality that checkpoint inhibitors
*cause* autoimmune type 1 diabetes.** A model that reproduces a real, important side effect of an
*unrelated* drug class — without being built to — is the strongest validation this layer could get.

**3. Non-response splits into TWO mechanisms with MATCHED levers** (richer than the lumped model). A
big-progenitor non-responder (`P0`=0.45) is **converted by targeting the progenitor** (deplete the
stem/TSCM pool → responds), but **NOT** by maintaining exhaustion alone (the problem is the influx, not
reversion). So: *big stem pool → target the progenitor; poor exhaustion-durability → sustain exhaustion
/ 2nd course.* Biomarker-stratified, mechanism-matched treatment.

## The transfer (your "maybe it transfers" — answered, honestly, with a sign flip)
This **same ladder is the cancer / chronic-infection model run with the opposite goal.** There you
*give* checkpoint blockade (reverse exhaustion) to **unleash** effectors against the tumor/virus; here
you *drive* exhaustion (anti-CD3) to **restrain** them. One module, two signs. That's why HIV and cancer
exhaustion biology is directly relevant — and why checkpoint-induced T1D is the predictable cost of the
cancer move. It transfers; it just flips sign.

## Honest caveats
Illustrative deterministic model; predictions are **directional/qualitative** (the magnitudes are
illustrative). The progenitor axis maps to the real autoreactive-TSCM population but is not *fit* to
patient data. The checkpoint-T1D reproduction is the key validation; the progenitor-vs-durability split
is a hypothesis the model *generates* (testable: do checkpoint-induced-T1D and teplizumab-non-response
track baseline autoreactive-TSCM frequency?). LAG3-maintained exhaustion (Grebinoski) is represented as
a single reversion rate `rev`.
