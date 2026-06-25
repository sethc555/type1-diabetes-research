#!/usr/bin/env python3
"""P6 (discrete-clonal / stochastic) — the model class that CAN, in principle, reproduce Foster 2025.

The avidity-resolved continuum (P5, t1d_avidity.py) proved the antagonism is sub-continuum AND
sub-bistable: in any basin-flip model, anti-CD3 is intrinsically pro-flip, so it never *reduces*
tolerance efficacy. The structural-negative said Foster needs DISCRETE-CLONAL / STOCHASTIC dynamics.
This builds exactly that and tests it.

Mechanism (the Santamaria/infectious-tolerance logic made discrete & stochastic):
  - Antigen-specific tolerance converts targeted high-avidity effector clones into REGULATORY clones G
    that suppress the WHOLE repertoire by bystander suppression (global S = sum_k G).
  - anti-CD3 is non-selective debulking + PREFERENTIALLY kills the just-activated CONVERTING cells C
    (rate kAC). Because clones are DISCRETE and counts are small, killing C can drive a would-be
    regulatory clone to EXTINCTION (G_k -> 0, permanently lost) -> the bystander suppression that
    protected the rest of the repertoire is gone -> the surviving effectors (only transiently debulked)
    relapse -> COMBINATION < TOLERANCE-ALONE = the Foster antagonism.
  This is impossible in a continuum (density is fungible/regrows); it lives in the discreteness.

Tau-leaping (Poisson increments), vectorized over a stochastic virtual-patient cohort. 4 GB cap.
Reproducible (seeded). Key experiment: scan kAC (anti-CD3's clone-specific deletion of converters);
does the combination drop BELOW tolerance-alone as kAC rises?
"""
import numpy as np

PARAMS = dict(
    rE=3.2, dE=0.80, bE=0.6,          # effector proliferation (FAST -> relapse possible) / death / influx
    Ksupp=6.0, supp=3.0,              # bystander suppression: prolif * 1/(1+supp*S/Ksupp)
    conv=4.5, convr=4.0, dC=1.2,      # tolerance activation E->C (targeted) / C->G conversion / C loss
    dG=0.55,                          # regulatory (memory) death — BRITTLE: protection must be sustained
    kA=18.0, kAC=40.0, kAG=2.0,       # anti-CD3: kill E (flat) / kill converting C (preferential) / deplete G
    epsX=2.2, dX=1.6,                 # anti-CD3 durable hyporesponsiveness (scales effector prolif by 1/(1+X))
    kappa=0.022, rhoB=0.7,            # beta-cell avidity-weighted kill (HARDER) / regen
    k_tol=1.6, w_tol=0.50,            # tolerance targets a high-avidity band
    psi=0.0, psi_scale=9.0,           # PLATFORM AXIS: substrate-INDEPENDENT regulatory induction.
)                                     # psi=0 = CONVERSION platform (mRNA/peptide; Foster) ; high psi = EXPANSION platform (IL-10/TGF-b; AG019/Mathieu)
A3_DUR = 14/365.0; TOL_DUR = 30/365.0
B_CURE = 0.45; B_DX = 0.30; T_END = 6.0; DT = 0.012


def _on(t, t0, dur):
    return 1.0 if (t0 <= t < t0 + dur) else 0.0


def run(sched, p, rng, P=140, K=24, return_full=False):
    a = np.linspace(0.30, 2.00, K)                       # avidity spectrum
    pE = np.exp(-0.6 * (a - a[0])); pE /= pE.mean()      # thymic escape: low-avidity heavy (mild)
    gtol = np.exp(-((a - p["k_tol"])**2)/(2*p["w_tol"]**2)); gtol /= gtol.mean()  # tolerance targeting
    actE = a / a.mean()                                  # high-avidity effectors proliferate/kill more
    sev = rng.uniform(0.7, 1.6, (P, 1))                  # per-patient severity
    E = rng.poisson(np.clip(34.0 * sev * pE[None, :], 0, None)).astype(float)
    C = np.zeros((P, K)); G = np.zeros((P, K))
    B = np.full(P, 0.62); X = np.zeros(P)
    tdx = np.full(P, np.inf); tgrid = []; Bmean = []
    for t in np.arange(0, T_END, DT):
        ua3 = _on(t, sched.get("a3_t0", 1e9), A3_DUR) if sched.get("a3") else 0.0
        ut = _on(t, sched.get("tol_t0", 1e9), TOL_DUR) if sched.get("tol") else 0.0
        S = G.sum(axis=1, keepdims=True)                  # bystander suppression (global)
        supp = 1.0 / (1.0 + p["supp"] * S / p["Ksupp"])
        hypo = 1.0 / (1.0 + X[:, None])                   # anti-CD3 durable hyporesponsiveness
        def pois(lam):
            return rng.poisson(np.clip(lam, 0, None) * DT).astype(float)
        prolif = pois(p["rE"] * E * actE[None, :] * supp * hypo)
        edeath = pois(p["dE"] * E)
        influx = pois(p["bE"] * pE[None, :] * np.ones((P, 1)))
        act = np.minimum(E, pois(p["conv"] * gtol[None, :] * E * ut))      # tolerance activates E->C
        cconv = np.minimum(C, pois(p["convr"] * C))                        # C->G: CONVERSION channel (substrate-dependent; anti-CD3-vulnerable via C)
        expand = pois(p["psi"] * p["psi_scale"] * gtol[None, :] * ut * np.ones((P, 1)))  # EXPANSION channel (IL-10/TGF-b): substrate-INDEPENDENT regulatory induction, NOT routed through deletable C
        closs = np.minimum(C - cconv, pois(p["dC"] * C))
        killE = np.minimum(E, pois(p["kA"] * E * ua3))
        killC = np.minimum(C, pois(p["kAC"] * C * ua3))                    # anti-CD3 ABORTS converting clones — by deletion OR PD-1/anergy (Wallberg 2017); either way they never become protectors
        killG = np.minimum(G, pois(p["kAG"] * G * ua3))
        gdeath = np.minimum(G - killG, pois(p["dG"] * G))
        E = np.clip(E + influx + prolif - edeath - act - killE, 0, None)
        C = np.clip(C + act - cconv - closs - killC, 0, None)
        G = np.clip(G + cconv + expand - killG - gdeath, 0, None)
        X = np.clip(X + DT*(p["epsX"]*ua3 - p["dX"]*X), 0, None)
        kill = p["kappa"] * (actE[None, :] * E).sum(axis=1) / K * hypo[:, 0]
        B = np.clip(B + DT*(p["rhoB"]*B*(1-B) - kill*B), 0, 1.0)
        newly = (B < B_DX) & ~np.isfinite(tdx); tdx[newly] = t
        if return_full:
            tgrid.append(t); Bmean.append(B.mean())
    if return_full:
        return float(np.mean(B > B_CURE)), tdx, np.array(tgrid), np.array(Bmean)
    return float(np.mean(B > B_CURE))


ARMS = {
    "untreated":       {},
    "anti-CD3 only":   {"a3": True, "a3_t0": 0.0},
    "tolerance only":  {"tol": True, "tol_t0": 0.0},
    "simultaneous":    {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.0},
    "anti-CD3 -> tol": {"a3": True, "a3_t0": 0.0, "tol": True, "tol_t0": 0.25},
    "tol -> anti-CD3": {"tol": True, "tol_t0": 0.0, "a3": True, "a3_t0": 0.25},
}


def arms_fractions(p, seed=0):
    rng = np.random.default_rng(seed)
    return {nm: run(s, p, rng) for nm, s in ARMS.items()}


def main():
    print("PLATFORM-AXIS model — does ONE model reproduce BOTH real combination results?")
    print("psi = substrate-INDEPENDENT regulatory induction (the IL-10/TGF-b 'expansion' channel):")
    print("  psi=0   -> CONVERSION platform (mRNA/peptide; Foster 2025 NOD -> antagonism)")
    print("  psi>>0  -> EXPANSION platform  (IL-10/TGF-b; AG019/Mathieu 2023 human -> synergy)")
    print("anti-CD3 strongly aborts converters (kAC=120) throughout; tolerance marginal (conv=2.5);")
    print("means over 2 seeds.\n")
    print(f"   {'psi':>4} {'platform':>11} {'tol':>5} {'a3':>4} {'sim':>5} {'a3>t':>5} {'t>a3':>5} "
          f"{'sim-tol':>8} {'regime':>20}")
    for psi in [0.0, 0.5, 1.0, 2.0, 4.0]:
        p = dict(PARAMS); p["psi"] = psi; p["conv"] = 2.5; p["kAC"] = 120.0
        rows = [[arms_fractions(p, seed=s)[k] for k in ARMS] for s in range(2)]
        a = np.array(rows).mean(0) * 100
        d = {k: a[i] for i, k in enumerate(ARMS)}
        gap = d["simultaneous"] - d["tolerance only"]
        reg = "ANTAGONISM (Foster)" if gap < -5 else ("SYNERGY (Mathieu)" if gap > 5 else "neutral")
        lab = "conversion" if psi == 0 else ("expansion" if psi >= 2 else "mixed")
        print(f"   {psi:4.1f} {lab:>11} {d['tolerance only']:4.0f}% {d['anti-CD3 only']:3.0f}% "
              f"{d['simultaneous']:4.0f}% {d['anti-CD3 -> tol']:4.0f}% {d['tol -> anti-CD3']:4.0f}% "
              f"{gap:+7.0f} {reg:>20}")
    print("\nIf low-psi gives antagonism and high-psi gives synergy, the SAME clonal model reproduces BOTH")
    print("the Foster mouse antagonism (conversion platform) AND the Mathieu human synergy (expansion")
    print("platform) -- anchored to real data: 'co-dosing backfires only for conversion-type platforms'.")


if __name__ == "__main__":
    main()
