#!/usr/bin/env python3
"""Standing VALIDATOR for the T1D model assumptions. Reads assumptions.json and prints:
 (1) DASHBOARD     -- counts by status / role / controversy.
 (2) DIG-HERE QUEUE -- load-bearing/structural assumptions that are NOT 'supported' (prioritized by
     'kills_result_if_wrong'). This is the research backlog.
 (3) BLIND-SPOT SURFACER -- scans each model's parameter dict and flags parameters with NO catalogued
     assumption: a written-but-uncatalogued modeling choice = a candidate blind spot. Catalog it or cut it.
 (4) HONEST UNKNOWNS -- the explicitly-acknowledged gaps + the conceptual-frame limit the tool can't see.
 (5) --run -- also execute the verify_*.py scripts (4 GB cap) and report pass/fail.

Run after every model change.  python3 validate.py [--run]
"""
import json, re, os, glob, subprocess, argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "assumptions.json")
CORE_MODELS = ["t1d_clonal.py", "t1d_responder.py", "t1d_hierarchy.py", "t1d_betacell.py", "t1d_avidity.py",
               "t1d_spreading.py", "t1d_bcell.py", "t1d_metabolic.py", "t1d_innate.py", "t1d_genetics.py"]


def model_params(fn):
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        return []
    src = open(path).read()
    m = re.search(r'^(?:P|PARAMS)\s*=\s*dict\((.*?)^\)', src, re.S | re.M)
    if not m:
        return []
    block = re.sub(r'#.*', '', m.group(1))
    return sorted(set(re.findall(r'(\w+)\s*=', block)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="also run verify_*.py (4GB cap)")
    args = ap.parse_args()
    cat = json.load(open(CATALOG))
    A = cat["assumptions"]

    print("=" * 76)
    print(f"ASSUMPTION VALIDATOR — {len(A)} catalogued assumptions")
    print("=" * 76)
    print("\n(1) DASHBOARD")
    print("    status     :", dict(Counter(a["status"] for a in A)))
    print("    role       :", dict(Counter(a["role"] for a in A)))
    print("    controversy:", dict(Counter(a["controversy"] for a in A)))

    print("\n(2) DIG-HERE QUEUE  (load-bearing/structural AND not 'supported';  * = kills the result if wrong)")
    queue = [a for a in A if a["role"] in ("load-bearing", "structural") and a["status"] != "supported"]
    queue.sort(key=lambda a: (not a["kills_result_if_wrong"], a["status"]))
    for a in queue or [None]:
        if a is None:
            print("    (none — every load-bearing/structural assumption is supported)"); break
        star = "*" if a["kills_result_if_wrong"] else " "
        print(f"   {star}[{a['id']:>3}] {a['status']:>9}/{a['controversy']:<6} {a['statement'][:60]}")

    covered = set().union(*[set(a.get("params", [])) for a in A]) if A else set()
    print("\n(3) BLIND-SPOT SURFACER  (model parameters with NO catalogued assumption)")
    any_blind = False
    for fn in CORE_MODELS:
        ps = model_params(fn)
        if not ps:
            if os.path.exists(os.path.join(HERE, fn)):       # model exists but no P/PARAMS dict parsed -> FLAG, don't silently skip
                print(f"    {fn:18s}  WARNING: no P/PARAMS dict parsed -- NOT gap-checked (fix formatting)")
                any_blind = True
            continue
        blind = [p for p in ps if p not in covered]
        any_blind = any_blind or bool(blind)
        print(f"    {fn:18s} {len(ps)-len(blind):>2}/{len(ps):<2} covered  | uncovered: "
              f"{', '.join(blind) if blind else '(all covered)'}")
    if any_blind:
        print("    -> each uncovered parameter is a choice with no recorded justification: catalog it (even")
        print("       'standard kinetic constant, low controversy') or remove it. That is how a blind spot dies.")

    print("\n(4) HONEST UNKNOWNS / OPEN GAPS")
    for a in A:
        if a["status"] in ("shaky", "unchecked"):
            print(f"    [{a['id']:>3}] {a['statement'][:60]}  ({a['status']})")
    print("\n    CONCEPTUAL-FRAME LIMIT (the unknown-unknowns this tool CANNOT see):")
    print("   ", cat["_meta"]["honest_limit"])

    if args.run:
        print("\n(5) VERIFY RUN (4 GB cap)")
        for v in sorted(glob.glob(os.path.join(HERE, "verify_*.py"))):
            r = subprocess.run(["bash", "-c", f"ulimit -v 4194304; timeout 595 python3 {os.path.basename(v)}"],
                               capture_output=True, text=True, cwd=HERE)
            tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
            print(f"    {os.path.basename(v):26s} exit={r.returncode}  {tail[:46]}")


if __name__ == "__main__":
    main()
