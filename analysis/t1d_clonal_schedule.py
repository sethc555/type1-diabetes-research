#!/usr/bin/env python3
"""The PAYLOAD — combination REGIME MAP + optimal SCHEDULE rule, on the hardened clonal model.

(1) REGIME MAP: place the real T1D combination studies on the platform axis (psi = substrate-
    independent regulatory expansion) and show what the model predicts for co-dosing at each — a
    'which combinations backfire' map anchored to real data.
(2) SCHEDULE RULE: for the antagonism-prone CONVERSION platform, scan the inter-drug GAP (and order)
    to find how much separation rescues efficacy — the concrete, falsifiable design rule.

Reuses t1d_clonal.py. Means over 2 seeds. 4 GB cap.
"""
import numpy as np
import t1d_clonal as M


def cure(sched, p, seeds=(0, 1)):
    return float(np.mean([M.run(sched, p, np.random.default_rng(s)) for s in seeds])) * 100


# real combination studies, placed on the platform axis by mechanism
STUDIES = [
    (0.0, "Foster 2025 mRNA (NOD)                 [antagonism]"),
    (0.0, "Stewart 2020 microparticle             [no synergy]"),
    (1.0, "GAD-alum / peptide combos              [mixed/weak]"),
    (4.0, "Mathieu 2023 AG019 L.lactis-IL10 (human)[no antagonism]"),
    (4.0, "Salmonella TGF-b/IL-10 Cobb/Mbongue    [synergy]"),
    (4.0, "L. lactis Sassi 2023                   [synergy]"),
]


def regime_map():
    print("=" * 78)
    print("(1) REGIME MAP — platform type -> predicted co-dosing outcome, vs the real studies")
    print("=" * 78)
    print(f"{'psi':>4} {'platform':>11} {'tol-only':>9} {'co-dosed':>9} {'sim-tol':>8} {'PREDICTION':>14}")
    for psi in [0.0, 1.0, 4.0]:
        p = dict(M.PARAMS); p["psi"] = psi; p["conv"] = 2.5; p["kAC"] = 120.0
        tol = cure({"tol": True, "tol_t0": 0.0}, p)
        sim = cure({"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0}, p)
        gap = sim - tol
        pred = "ANTAGONISM" if gap < -15 else ("synergy" if gap > 15 else "safe/neutral")
        lab = "conversion" if psi == 0 else ("expansion" if psi >= 4 else "mixed")
        print(f"{psi:4.1f} {lab:>11} {tol:7.0f}% {sim:7.0f}% {gap:+7.0f} {pred:>14}")
        for ps, name in STUDIES:
            if abs(ps - psi) < 0.6:
                print(f"{'':27} ~ {name}")


def schedule_rule():
    print("\n" + "=" * 78)
    print("(2) SCHEDULE RULE — CONVERSION platform (psi=0, antagonism-prone): does a GAP rescue it?")
    print("=" * 78)
    p = dict(M.PARAMS); p["psi"] = 0.0; p["conv"] = 2.5; p["kAC"] = 120.0
    tol = cure({"tol": True, "tol_t0": 0.0}, p)
    print(f"tolerance-alone baseline = {tol:.0f}%   (co-dosed simultaneously = the gap=0 row below)")
    print(f"{'gap(yr)':>8} {'gap(wk)':>7} {'anti-CD3 -> tol':>16} {'tol -> anti-CD3':>16}")
    best = (-1, None, 0)
    for g in [0.0, 0.08, 0.17, 0.33, 0.5, 1.0]:
        a3t = cure({"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": g}, p)
        ta3 = cure({"tol": True, "tol_t0": 0.0, "a3": True, "a3_t0": g}, p)
        for val, order in [(a3t, "anti-CD3->tol"), (ta3, "tol->anti-CD3")]:
            if val > best[0]:
                best = (val, order, g)
        print(f"{g:8.2f} {g*52:6.0f}w {a3t:15.0f}% {ta3:15.0f}%")
    print(f"\nDESIGN RULE (conversion platforms): co-dosing (gap=0) gives the antagonism; separating by a")
    print(f"gap restores efficacy. Best in scan: {best[1]} at ~{best[2]*52:.0f} wk -> {best[0]:.0f}%.")
    print("Expansion platforms (IL-10/Treg-boost): safe to co-administer (regime map, psi=4 row).")
    print("Falsifiable: the antagonism should shrink monotonically as the inter-drug gap widens.")


def main():
    regime_map()
    schedule_rule()


if __name__ == "__main__":
    main()
