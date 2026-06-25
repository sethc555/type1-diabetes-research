# Findings — genetics / HLA, as the CALIBRATION BRIDGE (vertical deepening #7)

_Genetics is the knob-setting layer, so the only worthwhile version maps **genotype → a model parameter
using real published effect sizes**, then **tests whether that map reproduces the known
genotype→phenotype facts**. Code: `t1d_genetics.py`, checked by `verify_genetics.py` (**4/4**). Grounded in
`_scan/genetics_hla.md` + pulled effect sizes. Status: the first step from *free* knobs toward
*genetically-anchored* knobs — semi-quantitative calibration, not individual-level fitting._

## Real anchors (pulled, cited)
- **HLA genotype odds ratios — Erlich 2008, T1DGC** (*Diabetes* db07-1331): DR3/DR4-DQ2/8 **OR = 30**
  (highest); DR15-DQ6 (DRB1\*1501-DQB1\*0602) **OR = 0.03** (dominant protection).
- **T1D-GRS2 — Sharp 2019** (*Diabetes Care*, AUC 0.92, 67 SNPs): **higher GRS → younger onset**;
  DR3-DQ2 homozygous → onset <2 yr.
- **Endotype — Bauer 2019** (*JCEM*): insulin-first (IAA) ~ DR4-DQ8; GAD-first (GADA) ~ DR3-DQ2.

## The map and the result
Genotype **OR → autoreactive escape** (saturating: `escape = OR/(OR+K)`) → ignition speed of the attack →
**onset age**; HLA class → which antigen is **primary**.

| genotype | HLA-OR (real) | onset age | primary antigen |
|---|---|---|---|
| DR3/DR4-DQ2/8 | 30 | **3.2 yr** | insulin+GAD |
| DR3/DR3-DQ2 | 6 | 4.6 yr | GAD |
| DR4/DR4-DQ8 | 5 | 5.0 yr | insulin |
| DR4/x | 1.5 | 15.6 yr | insulin |
| DR3/x | 1.5 | 15.6 yr | GAD |
| general population | 1.0 | protected | — |
| DR15-DQ6 carrier | 0.03 | **protected** | — |

## Calibration tests — all pass (against real genotype→phenotype facts)
- **T1 — higher OR/GRS → younger onset** (Sharp 2019): onset ages 3.2 → 4.6 → 5.0 → 15.6 yr fall
  monotonically as OR rises. **T1b**: the OR=30 genotype is the earliest (3.2 yr).
- **T2 — DR15-DQ6 protected** (Erlich OR=0.03): no disease within 30 yr.
- **T3 — endotype by HLA class** (Bauer 2019): DR4 → insulin-first, DR3 → GAD-first.

## Why this one is different (the epistemic point)
Every prior layer was *internally consistent* but its knobs were *free*. This is the first layer whose
central parameter is **anchored in a real, published, large-dataset effect size** (the HLA ORs / GRS2) and
**tested against an external genotype→phenotype map** it was not fit to. The patient axes that were free
dials (who gets disease, how young, which antigen) now fall out of **genotype**. That is the move from
"knobs on known biology" toward "knobs the data constrains" — the direction flagged as the only thing that
turns this body from a consistency engine into something calibrated.

## Honest caveats (what it is NOT)
This is **semi-quantitative**: real *aggregate* ORs → reproduced *ordering* of onset/endotype. It is **not**
individual-level GRS fitting — that needs controlled-access genotype+phenotype data (dbGaP/EGA: T1DGC,
TEDDY), which was not used. The **OR→parameter map itself** (`escape`, `seed`, `g`, `K_or`) is a modeling
choice, and onset ages are in model-scaled years (the *ordering and protection are robust; the absolute
ages are illustrative*). Only the HLA component is dynamically driven (it dominates GRS); non-HLA loci
(INS-VNTR, PTPN22, IL2RA, IFIH1) are named, not separately parameterized. So: a real bridge, honestly a
*first plank* of it — not a calibrated model.
