# Findings — antigens & epitope SPREADING (vertical deepening #3), and the cross-layer synergy

_Makes antigens explicit: a PRIMARY autoantigen (insulin) and stress-driven SPREADING to others over
time. Code: `t1d_spreading.py` (deterministic). Grounded in `_scan/epitope_spreading.md`. Status:
illustrative modeling / hypothesis._

## The model
Per-antigen effector pools `E_i` (i=0 primary insulin; 1–4 = GAD/IA-2/ZnT8/hybrid peptide), each with a
priming state `pr_i` (0 dormant → 1 recruited). β-cell **stress `S`** (driven by the total attack) drives
**hierarchical, threshold-gated spreading** — the next antigen is recruited only while stress is
sustained-high. This is the SAME stress that generates neoantigens in `t1d_betacell.py` (Marré 2015;
Strollo 2022), so the β-cell layer *is* the spreading engine. Antigen-specific tolerance durably
suppresses TARGETED antigens (single = {primary}; broad = all), at an EARLY or LATE time. Grounding:
spreading is hierarchical/staged (TEDDY — Vehik 2020; Ilonen 2013); single-antigen tolerance is escaped
by neo/spread-epitopes (Balakrishnan 2020; Peakman & Santamaria 2024).

## Results (`t1d_spreading.py`) — the #antigens column shows the mechanism

| arm | β@5yr | #antigens recruited |
|---|---|---|
| untreated | 0.42 | 5 (full spread) |
| single-antigen tolerance, **EARLY** | **0.96** | **1** (spreading halted) |
| single-antigen tolerance, **LATE** | 0.64 | 5 (escaped) |
| **BROAD** (all-antigen) tolerance, LATE | 0.84 | 5 |
| single LATE **+ β-protection** | **0.86** | **1** (spreading prevented) |

**P1 — single-antigen tolerance is ESCAPED by spreading.** LATE single-antigen tol (0.64) < broad (0.84):
once the disease has spread to 5 antigens, tolerizing only the primary leaves 4 to escape. Reproduces the
documented clinical underperformance of single-antigen immunotherapy.

**P2 — EARLY (pre-spread) tolerance works far better.** single-EARLY (0.96, **1 antigen**) ≫ single-LATE
(0.64, 5): treating before spreading *halts* it — only the primary is ever active, so tolerizing it
suffices. The prevention-window rationale, mechanized.

**P3 — BROAD tolerance escapes the trap.** Covering all antigens (0.84) preserves β even when given late —
no escape route.

**P4 — CROSS-LAYER (the prize): β-protection slows spreading and RESCUES single-antigen tolerance.**
β-protection cut the recruited-antigen count from **5 → 1** (less stress → fewer neoantigens → no
spreading), turning a failing single-antigen LATE arm (0.64) into a success (0.86). **The β-cell-stress
layer and the spreading layer unify into one therapeutic synergy:** protect the target → cut off the
escape route → single-antigen tolerance becomes sufficient.

## Why this matters
It explains a real, nagging clinical fact (single-antigen tolerance keeps underperforming), and yields
three actionable, falsifiable strategies — **treat EARLY (before spreading), tolerize BROAD, or add
β-protection to single-antigen tolerance** — the last of which ties the whole T1D body together.

## Honest caveats
Illustrative; magnitudes illustrative (the robust outputs are the directions + the #antigens mechanism).
Spreading is modeled as **sequential** (hierarchical) and **stress-threshold-gated** — both are modeling
choices (real spreading is hierarchical-ish but not strictly sequential; the threshold abstracts
"sustained inflammation"). Antigen tolerance is a durable per-antigen suppression (lumped). The
cross-layer β-protection→spreading link is mechanistically grounded (stress→neoantigens) but the
*magnitude* of the rescue is illustrative.
