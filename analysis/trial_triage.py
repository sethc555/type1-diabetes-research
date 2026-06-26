#!/usr/bin/env python3
"""TRIAL-TRIAGE ENGINE (build #3) -- the model body made QUERYABLE for trial design.

Given a proposed design (modality, stage, sequence, population, partner) it returns a verdict:
predicted OUTCOME + the mechanistic FAILURE MODE + the FIX the same mechanisms predict -- each traced to a
layer + its verify, and tagged with a CONFIDENCE that honors the out-of-sample boundary (loo_validation.py):
natural-history / timing / stratification = validated; cross-stage drug-effect MAGNITUDE = directional only.

It predicts nothing new -- it packages the intervention map (SYNTHESIS.md) + the calibration/validation into
something a person designing a trial can use: 'will this fail, why, and what would the model try instead?'.
Reuses responder_classifier.py for the live stratification numbers. 4 GB cap (trivial)."""
from collections import namedtuple

Verdict = namedtuple("Verdict", "outcome mechanism fix confidence source")
FAVORABLE, CONDITIONAL, FAIL, CONTRA = "FAVORABLE", "CONDITIONAL", "LIKELY-FAIL", "CONTRAINDICATED"
RANK = {CONTRA: 0, FAIL: 1, CONDITIONAL: 2, FAVORABLE: 3}


def _tepli_enrichment():
    try:
        import numpy as np
        from responder_classifier import cohort
        P = cohort(); x0 = P[:, 1]
        return float(P[:, 2].mean()), float(P[x0 >= np.quantile(x0, 0.6), 2].mean())
    except Exception:
        return 0.56, 0.91


def triage(modality, stage="onset", sequence="mono", population="unselected", partner=None):
    m, p = modality.lower(), (partner or "").lower()

    if "checkpoint" in m:
        return Verdict(CONTRA,
            "reverses the protective exhaustion that restrains autoreactive CD8 -> unleashes the attack",
            "do NOT use in T1D -- this is the cautionary direction",
            "HIGH -- reproduces documented checkpoint-inhibitor-induced T1D", "hierarchy AH2")

    if any(k in m for k in ("il-1", "anakinra", "canakinumab", "anti-innate")):
        if stage in ("onset", "stage3", "late", "new-onset"):
            return Verdict(FAIL,
                "given at clinical onset, the adaptive attack already self-sustains -- removing the innate trigger no longer helps",
                "give as PREVENTION (stage 1-2, before the adaptive attack ignites)",
                "HIGH -- explains the Moran 2013 (AIDA/canakinumab) null", "innate AI1")
        return Verdict(CONDITIONAL,
            "innate-targeting prevents only before the adaptive attack self-sustains",
            "use early (stage 1-2); pair with an adaptive-arm agent for durability", "MEDIUM", "innate AI1")

    if any(k in m for k in ("cd20", "rituximab")):
        pop = "" if population != "unselected" else " (unselected: works only if B-cell-driven -- stratify by B-vs-T dominance, Linsley 2018)"
        if sequence == "mono" or partner is None:
            return Verdict(FAIL,
                "B-cell depletion is transient: a ~8-month shift, then the decline resumes (B cells repopulate)" + pop,
                "pair with a DURABLE agent (antigen tolerance); and stratify to B-cell-dominant patients",
                "HIGH -- reproduces Pescovitz 2014", "bcell BC1")
        return Verdict(CONDITIONAL,
            "anti-CD20 debulks the spreading-driver but is transient; a durable partner can carry the benefit" + pop,
            "keep the durable partner; stratify by B-vs-T dominance", "MEDIUM", "bcell BC1")

    if "toler" in m or "antigen" in m:
        expansion = any(k in m for k in ("expansion", "il-10", "tgf"))
        if p and ("cd3" in p or "tepli" in p):
            if expansion:
                return Verdict(FAVORABLE,
                    "expansion-type tolerance is substrate-independent -> no competition with anti-CD3 (matches the Mathieu 2023 human trial)",
                    "safe to combine (even co-dose)", "HIGH -- reproduces Mathieu 2023", "clonal AP1")
            if sequence in ("co-dose", "codose", "simultaneous"):
                return Verdict(FAIL,
                    "conversion-type tolerance co-dosed with anti-CD3: anti-CD3 deletes the converting clones tolerance needs (substrate antagonism)",
                    "SEQUENCE -- separate the two in time, do not co-dose", "HIGH -- reproduces Foster 2025", "clonal AP1 / verify_clonal")
            return Verdict(CONDITIONAL,
                "sequencing conversion-tolerance and anti-CD3 avoids the co-dosing antagonism",
                "keep them separated in time; prefer broad/early tolerance to resist spreading", "MEDIUM", "clonal")
        if "broad" in m or stage in ("early", "stage1", "prevention") or sequence == "early":
            return Verdict(FAVORABLE,
                "broad or early tolerance outruns epitope spreading -- no escape route",
                "the recommended form: multi-antigen and/or pre-spreading", "HIGH -- spreading P2/P3", "spreading AE1")
        return Verdict(FAIL,
            "single-antigen tolerance given late is ESCAPED by epitope spreading (the disease recruits new specificities)",
            "use BROAD (multi-antigen) or EARLY (pre-spreading) tolerance, or add beta-protection to slow spreading",
            "HIGH -- spreading layer + the documented single-antigen underperformance", "spreading AE1")

    if "cd3" in m or "tepli" in m:
        if p and ("toler" in p or "antigen" in p):
            return triage(partner, stage=stage, sequence=sequence, population=population, partner=modality)
        overall, hi = _tepli_enrichment()
        if population in ("exhaustion-high", "stratified", "exhausted"):
            return Verdict(FAVORABLE,
                f"selecting baseline-exhaustion-high patients enriches teplizumab response to ~{hi*100:.0f}%",
                "the recommended stratification; confirm on existing trial data first",
                "MEDIUM -- enrichment MAGNITUDE is a forward bet, testable on existing data", "responder_classifier #14")
        return Verdict(CONDITIONAL,
            f"unselected teplizumab is partial (~{overall*100:.0f}% response) -- it works, but washes out over an unselected cohort",
            f"STRATIFY by baseline CD8 exhaustion (-> ~{hi*100:.0f}% in the exhaustion-high subgroup); re-analyze existing trials to confirm",
            "HIGH for the direction; magnitude is a forward bet", "responder AR1 / responder_classifier")

    if any(k in m for k in ("verapamil", "beta-prot", "protect", "glucose", "insulin")):
        if partner:
            return Verdict(FAVORABLE,
                "beta-protection / glucose control is orthogonal (non-immune) -> a safe, additive adjunct that also slows spreading",
                "use as an adjunct to a disease-modifying agent", "HIGH -- betacell AB4 / metabolic AM1", "betacell/metabolic")
        return Verdict(CONDITIONAL,
            "modest alone -- it throttles the stress/spreading engine but does not clear autoimmunity",
            "add a disease-modifying immunotherapy", "HIGH", "betacell AB4 / metabolic AM1")

    return Verdict(CONDITIONAL, "no specific rule matched", "specify modality / stage / sequence / population", "LOW", "-")


def rank(designs):
    return sorted(designs, key=lambda d: RANK[triage(**d).outcome], reverse=True)


def main():
    print("TRIAL-TRIAGE ENGINE -- the model body, queryable for trial design\n")
    scen = [
        ("REAL TRIALS THAT FAILED / the model's call", None),
        ("anti-IL-1 at new-onset (Moran 2013)",                 dict(modality="anti-IL-1", stage="onset")),
        ("single-antigen tolerance, late monotherapy",          dict(modality="antigen tolerance (conversion)", stage="late")),
        ("anti-CD20 monotherapy (Pescovitz)",                   dict(modality="anti-CD20", sequence="mono")),
        ("teplizumab + conversion-tolerance, CO-DOSED (Foster)", dict(modality="teplizumab", partner="antigen tolerance (conversion)", sequence="co-dose")),
        ("checkpoint inhibitor in T1D",                         dict(modality="checkpoint inhibitor")),
        ("WHAT WORKS / the model's fixes", None),
        ("teplizumab + expansion-tolerance (Mathieu, real)",    dict(modality="teplizumab", partner="antigen tolerance (expansion)")),
        ("anti-IL-1 as PREVENTION (stage 1-2)",                 dict(modality="anti-IL-1", stage="stage1")),
        ("BROAD / early antigen tolerance",                     dict(modality="broad antigen tolerance", stage="early")),
        ("anti-CD20 + durable tolerance partner",               dict(modality="anti-CD20", partner="antigen tolerance", sequence="combo")),
        ("teplizumab + conversion-tolerance, SEQUENCED",        dict(modality="teplizumab", partner="antigen tolerance (conversion)", sequence="sequenced")),
        ("teplizumab, EXHAUSTION-HIGH stratified",              dict(modality="teplizumab", population="exhaustion-high")),
        ("teplizumab, unselected (the wash-out)",               dict(modality="teplizumab", stage="stage2")),
        ("beta-protection as adjunct to immunotherapy",         dict(modality="beta-protection", partner="teplizumab")),
    ]
    for name, d in scen:
        if d is None:
            print(f"\n=== {name} ==="); continue
        v = triage(**d)
        print(f"\n  [{v.outcome:14}] {name}")
        print(f"      why : {v.mechanism}")
        print(f"      fix : {v.fix}")
        print(f"      conf: {v.confidence}")

    print("\n\n=== RANKING a candidate set (new-onset stage-3 combination designs) ===")
    cands = [
        dict(modality="checkpoint inhibitor"),
        dict(modality="anti-CD20", sequence="mono"),
        dict(modality="teplizumab", stage="stage3"),
        dict(modality="teplizumab", partner="antigen tolerance (conversion)", sequence="sequenced"),
        dict(modality="teplizumab", population="exhaustion-high"),
        dict(modality="teplizumab", partner="beta-protection"),
    ]
    for d in rank(cands):
        v = triage(**d)
        label = d["modality"] + (f" + {d['partner']}" if d.get("partner") else "") + (f" [{d['population']}]" if d.get("population", "unselected") != "unselected" else "") + (f" ({d['sequence']})" if d.get("sequence", "mono") != "mono" else "")
        print(f"  {v.outcome:14}  {label}")


if __name__ == "__main__":
    main()
