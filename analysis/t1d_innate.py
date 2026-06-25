#!/usr/bin/env python3
"""VERTICAL deepening #6 — INNATE IMMUNITY / NEUTROPHILS. Closes the last AS3 residual. Adds the UPSTREAM
trigger the other layers assumed away: innate inflammation N (neutrophils/NETs + IFN-a). N does two things
grounded in the literature: (a) it FEEDS the beta-stress hub -- IFN-a drives HLA-I + ER stress (Marroqui
2017), the same AB1 loop; and (b) it PRIMES the adaptive attack E (Lombardi 2018: IFN-a is the priming
trigger). E has a Hill self-amplification, so once PRIMED past a threshold it becomes SELF-SUSTAINING and
innate-INDEPENDENT.

That bistability is the point: innate-targeted therapy (anti-IL-1 / anti-IFN) suppresses N, so it
PREVENTS if given EARLY (before E ignites) but FAILS if given at clinical onset (E already self-sustaining).
This reproduces why anti-IL-1 failed at onset (Moran 2013 Lancet; Cabrera 2016 -- it moderated inflammation
but did NOT preserve C-peptide) and predicts it would work as PREVENTION. Deterministic. 4 GB cap.

State: N innate, E adaptive attack, B beta-mass, S stress (adaptive + innate IFN).
Predictions: (1) innate-targeting has a narrow EARLY window; (2) the adaptive attack goes innate-INDEPENDENT
once established; (3) innate is UPSTREAM of the stress hub (early control throttles it); (4) innate activation
PRECEDES the adaptive attack and beta-loss (a pre-onset biomarker).
"""
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    k_dam=1.5, dN=0.6,                              # innate: beta-damage (DAMP/stress) feedback + decay
    a_prime=0.8, Kh=0.30, rE=1.4, Emax=1.0, dE=0.5, sf=0.6,   # adaptive: innate PRIMING + Hill self-amplification
    rhoB=0.5, kappa=0.6, amp=0.6, kappa_N=0.05,     # beta: regen / adaptive kill / stress-amp / small direct innate kill
    k_imm=1.0, k_ifn=0.8, dS=1.0,                   # stress: adaptive attack + innate IFN-a (Marroqui 2017)
)
HOR = 6.0; B_OK = 0.30


def rhs(t, y, p, s):
    N = max(y[0], 0.0); E = max(y[1], 0.0); B = max(y[2], 0.0); S = min(max(y[3], 0.0), 1.0)
    ui = s.get("u_innate", 0.0) if t >= s.get("innate_t0", 1e9) else 0.0
    um = s.get("u_imm", 0.0) if t >= s.get("imm_t0", 1e9) else 0.0
    dN = p["k_dam"] * S * (1 - N) - p["dN"] * N - ui * N
    hill = E**4 / (p["Kh"]**4 + E**4)                            # SHARP cooperative self-amplification (needs E past Kh)
    dE = (p["a_prime"] * N + p["rE"] * hill * (1 - E / p["Emax"])) * (1 + p["sf"] * S) - p["dE"] * E - um * E
    dB = p["rhoB"] * B * (1 - B) - p["kappa"] * E * B * (1 + p["amp"] * S) - p["kappa_N"] * N * B
    dS = (p["k_imm"] * E + p["k_ifn"] * N) * (1 - S) - p["dS"] * S
    return [dN, dE, dB, dS]


def simulate(s, p=None):
    p = p or P
    y0 = [0.70, 0.02, 1.00, 0.10]                   # innate TRIGGER fired (e.g. viral), ~no adaptive yet, healthy beta, low stress
    return solve_ivp(rhs, (0, HOR), y0, args=(p, dict(s)), t_eval=np.linspace(0, HOR, 1500),
                     method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.01)


def bend(sol):
    return float(np.interp(HOR, sol.t, sol.y[2]))


def first_t(sol, idx, thresh, rising=True):
    y = sol.y[idx]
    hit = np.where(y > thresh if rising else y < thresh)[0]
    return float(sol.t[hit[0]]) if len(hit) else float("nan")


def main():
    print("Innate-immunity layer — the upstream trigger that primes the adaptive attack\n")

    untr = simulate({})
    early = simulate({"u_innate": 8.0, "innate_t0": 0.0})       # innate therapy from the start (prevention)
    late = simulate({"u_innate": 8.0, "innate_t0": 2.5})        # innate therapy at clinical onset (Moran 2013 setting)

    print("P1  Innate-targeting has a narrow EARLY WINDOW (explains why anti-IL-1 failed at onset; Moran 2013):")
    print(f"      untreated            beta@6yr {bend(untr):.2f}  ({'lost' if bend(untr)<B_OK else 'preserved'})")
    print(f"      anti-innate EARLY    beta@6yr {bend(early):.2f}  ({'preserved' if bend(early)>B_OK else 'lost'})  <- prevention")
    print(f"      anti-innate LATE     beta@6yr {bend(late):.2f}  ({'lost' if bend(late)<B_OK else 'preserved'})  <- fails (Moran 2013)\n")

    print("P2  The adaptive attack goes INNATE-INDEPENDENT once established (why LATE fails):")
    print(f"      anti-innate EARLY  E@6yr {float(np.interp(HOR,early.t,early.y[1])):.2f} (never ignited)")
    print(f"      anti-innate LATE   E@6yr {float(np.interp(HOR,late.t,late.y[1])):.2f} (self-sustaining -- suppressing innate no longer matters)\n")

    peakS_u = float(untr.y[3].max()); peakS_e = float(early.y[3].max())
    print("P3  Innate is UPSTREAM of the stress hub (early control throttles the stress->neoantigen engine):")
    print(f"      peak beta-cell stress S:  untreated {peakS_u:.2f}  ->  anti-innate EARLY {peakS_e:.2f}\n")

    tN = float(untr.t[np.argmax(untr.y[0])]); tE = first_t(untr, 1, 0.5); tB = first_t(untr, 2, 0.5, rising=False)
    print("P4  Innate activation PRECEDES adaptive attack and beta-loss (a pre-onset biomarker):")
    print(f"      innate N peaks @ {tN:.2f}yr  <  adaptive E established @ {tE:.2f}yr  <  beta<50% @ {tB:.2f}yr")


if __name__ == "__main__":
    main()
