#!/usr/bin/env python3
"""P3 — calibration to clinical anchors.

Anchors (from analysis/MEMO.md / scan_results.md):
  - TN10 (Herold/Sims): a single 14-day teplizumab course in stage-2 relatives delayed
    progression to stage-3 (clinical) diabetes by a median of ~2 years (placebo median to
    diagnosis ~24-27 months; teplizumab ~48-50 months).
  - TrialNet staging consensus (Phillip 2024): stage 2 (multiple autoantibodies +
    dysglycemia) carries a high near-term risk -- roughly ~half progress to stage 3 within
    ~2 years.
  - Metabolic inflection (Montaser 2026): accelerated beta-cell decline begins ~1-2 yr
    before clinical diagnosis.

We sample a stage-2 cohort over a severity gradient (baseline effector burden E0) whose
UNTREATED median time-to-diagnosis is anchored to ~2 years, then read off the anti-CD3
monotherapy delay and the combination-sequencing fractions ON THE SAME COHORT.

Honest result up front: at the operating point the model reproduces the untreated ~2-year
median and the qualitative teplizumab delay, but UNDER-produces the ~2-year monotherapy delay
magnitude (single short course only transiently debulks effectors here). The robust, novel
contribution is the SEQUENCING antagonism, not the monotherapy-delay magnitude -- stated as a
known limitation, in the spirit of the project's audit.

Output: t1d_calibration.png, prints calibration table.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import t1d_model as M


# stage-2 cohort: heterogeneous in BOTH effector severity (E0) and residual beta-cell mass
# (B0) at entry, since real stage-2 relatives present across a range of both. Spread chosen so
# the untreated median t_dx ~2 yr AND ~half progress by ~2 yr (broad, TrialNet-like curve).
def cohort(n=500, seed=0):
    rng = np.random.default_rng(seed)
    E0 = np.clip(rng.normal(1.05, 0.22, n), 0.72, 1.7)
    B0 = np.clip(rng.normal(0.52, 0.12, n), 0.33, 0.85)
    return E0, B0


def km_curve(sched, E0s, B0s, t_end=6.0):
    """Fraction NOT yet diagnosed (B>B_DX) vs time -- a Kaplan-Meier-style progression curve."""
    ts = np.linspace(0, t_end, 121)
    tdx = np.array([M.time_to_dx(M.simulate(sched, y0=[b, e, 0.12], t_end=t_end + 2))
                    for e, b in zip(E0s, B0s)])
    surv = np.array([(tdx > t).mean() for t in ts])
    median = np.interp(-0.5, -surv, ts) if surv.min() <= 0.5 else np.inf
    return ts, surv, median, tdx


def main():
    E0s, B0s = cohort()
    ts_u, surv_u, med_u, _ = km_curve(M.arms()["untreated"], E0s, B0s)
    ts_a, surv_a, med_a, _ = km_curve(M.arms()["anti-CD3 only"], E0s, B0s)

    print("=== calibration: untreated stage-2 progression ===")
    print(f"  untreated median time-to-diagnosis : {med_u:.2f} yr   (TN10 placebo ~2.0 yr)")
    frac2 = 1 - np.interp(2.0, ts_u, surv_u)
    print(f"  untreated progressed by 2 yr       : {frac2*100:.0f}%      (TrialNet stage-2 ~50%)")
    print(f"  anti-CD3 monotherapy median        : {med_a:.2f} yr")
    delay = med_a - med_u if np.isfinite(med_a) else np.inf
    print(f"  anti-CD3 monotherapy DELAY         : {('+%.2f' % delay) if np.isfinite(delay) else 'censored'} yr"
          f"   (TN10 ~+2.0 yr)  [model under-produces magnitude -- see docstring]")

    print("\n=== same cohort, combination sequencing (durable-control fraction @5yr) ===")
    for name in ["tolerance only", "simultaneous", "anti-CD3 -> tol", "tol -> anti-CD3"]:
        fr = np.mean([M.banked_mass(M.simulate(M.arms()[name], y0=[b, e, 0.12])) > M.B_CURE
                      for e, b in zip(E0s, B0s)])
        print(f"  {name:18s} {fr*100:5.1f}%")

    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.plot(ts_u, surv_u * 100, lw=2.2, color="#999999", label=f"untreated (median {med_u:.1f} yr)")
    ax.plot(ts_a, surv_a * 100, lw=2.2, color="#b2182b",
            label=f"anti-CD3 monotherapy (median {med_a:.1f} yr)" if np.isfinite(med_a)
            else "anti-CD3 monotherapy")
    ax.axvline(2.0, ls=":", color="k", lw=1)
    ax.set_xlabel("years from stage 2")
    ax.set_ylabel("% not yet at stage-3 diagnosis")
    ax.set_title("Calibration: untreated stage-2 progression anchored to TN10 placebo (~2 yr median)")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 105)
    fig.tight_layout()
    fig.savefig("t1d_calibration.png", dpi=110)
    plt.close(fig)
    print("\nwrote t1d_calibration.png")


if __name__ == "__main__":
    main()
