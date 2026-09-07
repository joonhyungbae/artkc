# -*- coding: utf-8 -*-
"""Draw the human-coder reliability sample and emit blinded coding sheets.

Design (Sec. III.4):
  * proportional stratified random sample of 30% (n=33) across the six units,
    largest-remainder allocation; the tie at 4.50 between `agency` and `infra`
    is resolved in favour of `infra` (the cell the study's claim rests on).
  * the `infra` cell is then taken as a census (all 15), so 43 papers are coded.
  * the headline kappa is computed on the proportional 33 only. Over-sampling
    `infra` changes the marginals, so the 43-paper set is not an unbiased
    estimate of the corpus-level kappa; the infra cell is reported as raw
    agreement instead.
  * a 10-paper training pilot is drawn from OUTSIDE the reliability sample.

Seed is fixed so the draw is reproducible by a third party.
Run:  python3 code/sample_stratified.py
"""
import json, os, csv, random
from collections import defaultdict

SEED = 20260824
PROPORTION = 0.30
CENSUS_CELL = "infra"
PILOT_N = 10
ALLOC = {"work": 9, "institution": 7, "edu": 6, "infra": 5, "agency": 4, "audience": 2}

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
corpus = json.load(open(os.path.join(BASE, "corpus_110.json"), encoding="utf-8"))
by_unit = defaultdict(list)
for p in corpus:
    by_unit[p["proposed_unit"]].append(p["pid"])

rng = random.Random(SEED)
proportional, remainder = [], []
for unit in sorted(by_unit):
    pids = sorted(by_unit[unit])
    rng.shuffle(pids)
    k = ALLOC[unit]
    proportional += pids[:k]
    remainder += pids[k:]

census = sorted(pid for pid in by_unit[CENSUS_CELL])
reliability = sorted(set(proportional) | set(census))
pilot_pool = sorted(set(pid for p in corpus for pid in [p["pid"]]) - set(reliability))
rng.shuffle(pilot_pool)
pilot = sorted(pilot_pool[:PILOT_N])

print(f"seed={SEED}")
print(f"proportional sample n={len(proportional)} ({PROPORTION:.0%} of {len(corpus)})")
for unit in sorted(ALLOC):
    got = sum(1 for pid in proportional if pid in by_unit[unit])
    print(f"  {unit:12s} {got:2d} / {len(by_unit[unit]):2d}")
print(f"{CENSUS_CELL} census n={len(census)}")
print(f"reliability set n={len(reliability)}  ({len(reliability)/len(corpus):.0%} of corpus)")
print(f"training pilot n={len(pilot)} (disjoint from the reliability set)")

# Blinded coding sheets. Journal, author and the author's own code are withheld,
# matching the blind re-coding protocol so the two stages stay comparable.
idx = {p["pid"]: p for p in corpus}
for name, pids in (("coding_sheet_reliability", reliability), ("coding_sheet_pilot", pilot)):
    path = os.path.join(BASE, f"{name}.tsv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["item", "pid", "year", "title", "author_keywords", "code", "note"])
        order = list(pids)
        rng.shuffle(order)                       # present in random order, not by unit
        for n, pid in enumerate(order, 1):
            p = idx[pid]
            w.writerow([n, pid, p["year"], p["title"],
                        ", ".join(p.get("ko_keywords") or []), "", ""])
    print(f"wrote {path}")

json.dump({"seed": SEED, "allocation": ALLOC, "proportional": proportional,
           "census_cell": CENSUS_CELL, "census": census,
           "reliability": reliability, "pilot": pilot},
          open(os.path.join(BASE, "sample_43.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote sample_43.json")
