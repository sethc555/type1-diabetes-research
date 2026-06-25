#!/usr/bin/env python3
"""Cycle-2 ROBUSTNESS test — does the co-dosing antagonism survive the contestable assumptions
A6 (the vulnerable WINDOW) and A4 (which AVIDITY tolerance targets)? The cycle-2 S2 scan under-
delivered on A6, so we test the model's sensitivity directly instead of leaning on noisy literature.

A6 — vulnerable window: `convr` is the C->G conversion rate; LOW convr = WIDE window (slow conversion,
     long time for anti-CD3 to abort) ; HIGH convr = NARROW window (cells convert before anti-CD3
     catches them). The antagonism should fade as the window narrows. Biological anchor: effector->Treg
     conversion is a days-to-weeks process and anti-CD3 acts over ~2 weeks, so a non-trivial window is
     plausible — the test maps over what range the antagonism holds.
A4 — avidity: flip tolerance targeting from HIGH (k_tol=1.6, default) to LOW (k_tol=0.6) avidity. If
     the antagonism is avidity-agnostic, A4 does not threaten it.

Conversion platform (psi=0, the Foster regime), strong converter-abortion (kAC=120), marginal tolerance.
Reports tolerance-mono vs simultaneous (the Foster antagonism = sim << tol). 4 GB cap.
"""
import numpy as np
import t1d_clonal as M


def arm(name, p, seed):
    return M.run(M.ARMS[name], p, np.random.default_rng(seed))


def cell(p, seeds=(0, 1)):
    tol = float(np.mean([arm("tolerance only", p, s) for s in seeds]))
    sim = float(np.mean([arm("simultaneous", p, s) for s in seeds]))
    return tol * 100, sim * 100


def main():
    print("Cycle-2 robustness: does the co-dosing antagonism (sim << tol) survive A6 (window) and")
    print("A4 (avidity)? psi=0 (conversion/Foster regime), kAC=120, conv=2.5.\n")
    print(f"{'avidity':>8} {'convr':>6} {'window':>8} {'tol':>5} {'sim':>5} {'sim-tol':>8} {'antagonism?':>12}")
    held = []
    for k_tol, alab in [(1.6, "HIGH"), (0.6, "LOW")]:
        for convr in [1.0, 2.0, 4.0, 8.0, 16.0]:
            p = dict(M.PARAMS); p["psi"] = 0.0; p["conv"] = 2.5; p["kAC"] = 120.0
            p["k_tol"] = k_tol; p["convr"] = convr
            tol, sim = cell(p)
            gap = sim - tol
            antag = gap <= -15
            held.append(antag)
            win = "wide" if convr <= 2 else ("med" if convr <= 6 else "narrow")
            print(f"{alab:>8} {convr:6.1f} {win:>8} {tol:4.0f}% {sim:4.0f}% {gap:+7.0f} "
                  f"{'YES' if antag else 'faded':>12}")
    print(f"\nantagonism held in {sum(held)}/{len(held)} cells across both avidities and the window scan.")
    print("Read: if it holds for WIDE-to-MED windows at BOTH avidities, the result is robust to A4 and to")
    print("A6 within the plausible (non-instant) conversion-window range; it should fade only for a")
    print("NARROW window (near-instant conversion) — a falsifiable, biologically-checkable boundary.")


if __name__ == "__main__":
    main()
