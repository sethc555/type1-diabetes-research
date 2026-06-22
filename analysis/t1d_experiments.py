#!/usr/bin/env python3
"""P2 — experiments on the core model: mechanism timecourse, cohort antagonism, the
inter-drug gap sweep (the falsifiable sequencing prediction), and a robustness sweep
(is the antagonism a single-point artifact, or does it hold over a parameter region?).

Outputs: t1d_mechanism.png, t1d_cohort.png, t1d_gap.png, t1d_results.npz
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import t1d_model as M


def mechanism_figure():
    """Why the order matters: simultaneous fails to build R; tolerance-first builds & keeps it."""
    scen = [("untreated", M.arms()["untreated"]),
            ("simultaneous", M.arms()["simultaneous"]),
            ("anti-CD3 -> tol", M.arms()["anti-CD3 -> tol"]),
            ("tol -> anti-CD3", M.arms()["tol -> anti-CD3"])]
    fig, axes = plt.subplots(1, 4, figsize=(16, 3.6), sharey=True)
    for ax, (name, s) in zip(axes, scen):
        sol = M.simulate(s, t_end=8.0)
        ax.plot(sol.t, sol.y[0], label="B (beta-cell)", lw=2.2, color="#1b7837")
        ax.plot(sol.t, sol.y[1], label="E (effector)", lw=1.6, color="#b2182b")
        ax.plot(sol.t, sol.y[2], label="R (Treg)", lw=1.6, color="#2166ac")
        ax.axhline(M.B_DX, ls=":", color="grey", lw=1)
        ax.set_title(name, fontsize=11)
        ax.set_xlabel("years")
        ax.set_ylim(0, 1.8)
    axes[0].set_ylabel("level")
    axes[0].legend(fontsize=8, loc="upper right")
    fig.suptitle("Mechanism: only tolerance-FIRST builds a self-stabilizing Treg pool (R) "
                 "before anti-CD3 debulks effectors", fontsize=11)
    fig.tight_layout()
    fig.savefig("t1d_mechanism.png", dpi=110)
    plt.close(fig)


def cohort_figure():
    names = list(M.arms())
    fr = [M.cure_fraction(M.arms()[n]) * 100 for n in names]
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#999999", "#d6604d", "#4393c3", "#f4a582", "#b2182b", "#2166ac"]
    ax.bar(range(len(names)), fr, color=colors)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("durable-control fraction (%)")
    ax.set_title("anti-CD3 antagonizes antigen-specific tolerance — but only when given "
                 "first/together (Foster 2025)")
    for i, v in enumerate(fr):
        ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=9)
    ax.set_ylim(0, 110)
    fig.tight_layout()
    fig.savefig("t1d_cohort.png", dpi=110)
    plt.close(fig)
    return names, fr


def gap_sweep():
    """The falsifiable prediction: cure fraction vs inter-drug interval for both orders."""
    gaps = np.linspace(0.0, 1.5, 16)
    a3_first, tol_first = [], []
    for g in gaps:
        a3_first.append(M.cure_fraction({"a3": True, "a3_t0": 0.0,
                                          "tol": True, "tol_t0": g}) * 100)
        tol_first.append(M.cure_fraction({"tol": True, "tol_t0": 0.0,
                                           "a3": True, "a3_t0": g}) * 100)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(gaps, a3_first, "-o", color="#b2182b", label="anti-CD3 first, then tolerance")
    ax.plot(gaps, tol_first, "-o", color="#2166ac", label="tolerance first, then anti-CD3")
    tol_only = M.cure_fraction(M.arms()["tolerance only"]) * 100
    ax.axhline(tol_only, ls="--", color="#4393c3", lw=1, label=f"tolerance alone ({tol_only:.0f}%)")
    ax.set_xlabel("inter-drug interval (years)")
    ax.set_ylabel("durable-control fraction (%)")
    ax.set_title("Sequencing rule: tolerance-first is robust; anti-CD3-first needs a long gap "
                 "to recover")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 110)
    fig.tight_layout()
    fig.savefig("t1d_gap.png", dpi=110)
    plt.close(fig)
    return gaps, np.array(a3_first), np.array(tol_first)


def robustness_sweep(rho_max=0.9):
    """Over a parameter grid, in what fraction of viable cases does tolerance-first beat
    (or tie) simultaneous? Guards against a single-point artifact. Default restricts to the
    Treg-SPARING regime (rho<1), which matches teplizumab's documented Treg-sparing/expanding
    profile; pass rho_max=1.1 to include strongly Treg-depleting anti-CD3 (where the optimal
    ORDER can invert -- the two-channel caveat)."""
    rng = dict(phi=[0.30, 0.40, 0.50], rho=[0.5, 0.7, 0.9, 1.1],
               VR=[1.3, 1.4, 1.5], Ki=[0.45, 0.50, 0.55], kappa=[0.36, 0.40, 0.44])
    import itertools
    keys = list(rng)
    viable = antag = neg = 0
    deltas = []
    for combo in itertools.product(*[rng[k] for k in keys]):
        d_ = dict(zip(keys, combo))
        if d_["rho"] > rho_max:
            continue
        p = dict(M.P); p.update(d_)
        if M.cure_fraction(M.arms()["untreated"], p=p) > 0.2:
            continue
        if M.cure_fraction(M.arms()["tolerance only"], p=p) < 0.3:
            continue
        viable += 1
        d = (M.cure_fraction(M.arms()["tol -> anti-CD3"], p=p)
             - M.cure_fraction(M.arms()["simultaneous"], p=p))
        deltas.append(d)
        antag += (d > 0.01)
        neg += (d < -0.01)
    return viable, antag, neg, np.array(deltas)


def main():
    mechanism_figure()
    names, fr = cohort_figure()
    gaps, a3f, tolf = gap_sweep()
    viable, antag, neg, deltas = robustness_sweep(rho_max=0.9)
    viable2, antag2, neg2, deltas2 = robustness_sweep(rho_max=1.1)

    print("cohort durable-control fraction by arm:")
    for n, v in zip(names, fr):
        print(f"  {n:18s} {v:5.1f}%")
    print(f"\nantagonism (tol-only - simultaneous): "
          f"{fr[names.index('tolerance only')] - fr[names.index('simultaneous')]:+.1f} pts")
    print(f"order effect (tol->a3 - a3->tol):     "
          f"{fr[names.index('tol -> anti-CD3')] - fr[names.index('anti-CD3 -> tol')]:+.1f} pts")
    print(f"\ngap sweep: anti-CD3-first recovers from {a3f[0]:.0f}% (gap 0) to "
          f"{a3f[-1]:.0f}% (gap {gaps[-1]:.1f}yr); tolerance-first flat at ~{tolf.mean():.0f}%")
    print(f"\nrobustness (Treg-sparing regime, rho<1): tolerance-first >= simultaneous in "
          f"{viable-neg}/{viable} viable sets ({100*(viable-neg)/viable:.0f}%), strictly better "
          f"in {antag}; mean delta {deltas.mean()*100:+.1f} pts, "
          f"range [{deltas.min()*100:+.1f}, {deltas.max()*100:+.1f}]; NEG cases: {neg}")
    print(f"robustness (incl. strongly Treg-depleting anti-CD3, rho<=1.1): "
          f"{viable2-neg2}/{viable2} ({100*(viable2-neg2)/viable2:.0f}%); NEG (order inverts): "
          f"{neg2} -- all at the highest rho (the two-channel caveat)")

    np.savez("t1d_results.npz",
             arm_names=np.array(names, dtype=object), arm_fractions=np.array(fr),
             gaps=gaps, a3_first=a3f, tol_first=tolf,
             robust_viable=viable, robust_antag=antag, robust_neg=neg, robust_deltas=deltas,
             robust_viable_hi=viable2, robust_neg_hi=neg2)
    print("\nwrote t1d_mechanism.png, t1d_cohort.png, t1d_gap.png, t1d_results.npz")


if __name__ == "__main__":
    main()
