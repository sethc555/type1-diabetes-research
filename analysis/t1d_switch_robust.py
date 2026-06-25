#!/usr/bin/env python3
"""DIG-HERE: AS1 robustness -- does the responder result depend on the BISTABLE switch (and its
steepness)? Scan the effector-switch Hill cooperativity nH (n>=2 = bistable; n=1 = graded/non-bistable)
on a FIXED virtual cohort and check whether the two validated biomarker DIRECTIONS survive:
  baseline exhaustion X0  -> higher in responders (Wiedeman 2019)
  TSCM renewal r_tscm     -> lower  in responders (Dufort 2026)
If the directions hold across nH (esp. at n=1), the result does NOT hinge on the bistable assumption.
4 GB cap (deterministic, trivial).
"""
import numpy as np
import t1d_responder as M

rng = np.random.default_rng(0)
N = 220
COHORT = [(rng.uniform(0.02, 0.32), rng.uniform(0.0, 0.40), rng.uniform(0.8, 1.3)) for _ in range(N)]


def main():
    print("AS1 robustness — responder result vs effector-switch steepness nH (same cohort throughout)\n")
    print(f"  {'nH':>4} {'bistable?':>9} {'response':>9} {'X0: R>NR?':>11} {'TSCM: R<NR?':>12} {'both biomarkers?':>17}")
    for nH in [1.0, 2.0, 3.0, 4.0, 6.0, 8.0]:
        rows = []
        for r, x0, e0 in COHORT:
            p = M.patient(r, x0); p["nH"] = nH
            rows.append((r, x0, M.responds(p, E0=e0)))
        a = np.array(rows)
        rate = a[:, 2].mean()
        R, NR = a[a[:, 2] == 1], a[a[:, 2] == 0]
        if len(R) and len(NR):
            x0_ok = R[:, 1].mean() > NR[:, 1].mean()          # Wiedeman direction
            ts_ok = R[:, 0].mean() < NR[:, 0].mean()          # Dufort direction
            both = "YES" if (x0_ok and ts_ok) else "no"
            xs, ts = ("YES" if x0_ok else "no"), ("YES" if ts_ok else "no")
        else:
            xs = ts = both = "n/a (saturated)"
        print(f"  {nH:>4.0f} {('bistable' if nH>=2 else 'GRADED'):>9} {rate*100:>7.0f}% {xs:>11} {ts:>12} {both:>17}")
    print("\nRead: if both biomarker directions hold for nH>=2 (and ideally at n=1), the responder result")
    print("does NOT hinge on a steep/specific switch -- AS1 is a sound, non-fragile structural choice")
    print("(and bistable T-cell fate is itself well-supported: Tbet/GATA3 toggle, Delgoffe 2009 Teff/Treg).")


if __name__ == "__main__":
    main()
