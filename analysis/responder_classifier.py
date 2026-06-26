#!/usr/bin/env python3
"""STRATIFIED RESPONDER CLASSIFIER — the decision-relevant output: turn the model's responder mechanism
into a score over a MEASURABLE biomarker, and predict the ENRICHMENT a trial/re-analysis would get by
stratifying on it. This is the artifact a network (e.g. TrialNet) could act on: 'stratify your existing
teplizumab data by baseline exhaustion and the response rate should move like THIS.'

Real anchors (teplizumab, AbATE):
  * Response rate ~50% teplizumab vs 22% placebo remained insulin-independent / C-peptide-preserved (Herold AbATE).
  * Responders carry MORE partially-exhausted CD8 (TIGIT+KLRG1+/EOMES+) -- Long 2016 (Sci Immunol); the
    baseline exhausted-CD8 signature predicts response -- Wiedeman 2019.

The model's responder axis is baseline exhaustion X0 (a persistent trait) traded off against TSCM renewal
r_tscm. Here we: (1) check the unselected response rate vs AbATE, (2) check the biomarker direction/size vs
Long/Wiedeman, then (3) PREDICT the enrichment from stratifying on baseline exhaustion -- the falsifiable,
not-tuned part. Reuses t1d_responder.py. 4 GB cap.
"""
import numpy as np
from t1d_responder import responds, patient

ABATE_RATE = 0.50            # ~50% teplizumab responders (Herold AbATE)


def cohort(n=400, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        r = rng.uniform(0.02, 0.32)      # TSCM renewal
        x0 = rng.uniform(0.0, 0.40)      # BASELINE exhaustion (the measurable biomarker)
        e0 = rng.uniform(0.8, 1.3)       # severity
        rows.append((r, x0, responds(patient(r, x0), E0=e0)))
    return np.array(rows)


def main():
    P = cohort()
    r_tscm, x0, resp = P[:, 0], P[:, 1], P[:, 2]
    overall = resp.mean()
    R, NR = P[resp == 1], P[resp == 0]

    print("STRATIFIED RESPONDER CLASSIFIER — teplizumab, baseline-exhaustion biomarker\n")
    print("  (1) unselected response rate  -- vs AbATE ~50%")
    print(f"      model {overall*100:.0f}%   AbATE ~{ABATE_RATE*100:.0f}%   -> {'match' if abs(overall-ABATE_RATE)<0.10 else 'off'} (within {abs(overall-ABATE_RATE)*100:.0f} pts)\n")

    print("  (2) biomarker direction/size -- responders should carry MORE baseline exhaustion (Long/Wiedeman)")
    print(f"      baseline exhaustion X0: responders {R[:,1].mean():.2f}  vs  non-responders {NR[:,1].mean():.2f}"
          f"   ({R[:,1].mean()/max(NR[:,1].mean(),1e-9):.1f}x higher in responders)\n")

    print("  (3) PREDICTED ENRICHMENT from stratifying on baseline exhaustion  (the falsifiable, not-tuned output)")
    q40, q60 = np.quantile(x0, 0.4), np.quantile(x0, 0.6)
    lo = P[x0 <= q40, 2].mean(); hi = P[x0 >= q60, 2].mean()
    print(f"      exhaustion-LOW  (bottom 40%): response {lo*100:.0f}%")
    print(f"      unselected                  : response {overall*100:.0f}%")
    print(f"      exhaustion-HIGH (top 40%)   : response {hi*100:.0f}%")
    print(f"      -> enrichment HIGH-vs-LOW = {(hi-lo)*100:+.0f} pts; HIGH-vs-unselected = {(hi-overall)*100:+.0f} pts\n")

    print("  THE DECISION-RELEVANT CLAIM (testable on existing trial data, no new trial):")
    print(f"   * Stratifying a teplizumab cohort by BASELINE exhausted-CD8 should raise the response rate from")
    print(f"     ~{overall*100:.0f}% (unselected) to ~{hi*100:.0f}% (exhaustion-high) and drop it to ~{lo*100:.0f}% (exhaustion-low).")
    print(f"   * If a re-analysis of AbATE/TN10/PROTECT by the baseline exhaustion (or TSCM) signature recovers")
    print(f"     an enrichment of this SIZE, the stratifier is validated -- and 'teplizumab works, in the")
    print(f"     exhaustion-high subgroup' becomes an evidenced, actionable claim. If not, the stratifier is wrong.")
    print("   NOTE: the rate (~50%) and direction are consistency-with-construction; the ENRICHMENT MAGNITUDE")
    print("   is the genuine forward prediction (not tuned) -- that is the part worth testing.")


if __name__ == "__main__":
    main()
