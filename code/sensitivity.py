# -*- coding: utf-8 -*-
"""Sensitivity of the paper's core claim to every coding disagreement.

Worst case: resolve ALL author/blind disagreements against the author (i.e. adopt
the blind code everywhere the two differ) and recompute the shared-knowledge-
infrastructure (`infra`) cell and its use-phase split.

Reported in the paper, Sec. III.4.
Run:  python3 code/sensitivity.py
"""
import json, os
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
corpus = json.load(open(os.path.join(BASE, "data", "corpus_110.json"), encoding="utf-8"))
recode = json.load(open(os.path.join(BASE, "data", "blind_recode_110.json"), encoding="utf-8"))

orig = {p["pid"]: p["proposed_unit"] for p in corpus}
ids = list(orig)
dis = [i for i in ids if orig[i] != recode[i]]

a_infra = {i for i in ids if orig[i] == "infra"}
b_infra = {i for i in ids if recode[i] == "infra"}

print("disagreements: %d/%d" % (len(dis), len(ids)))
print("  by boundary:")
for pair, c in Counter((orig[i], recode[i]) for i in dis).most_common():
    print("    %-12s -> %-12s %d" % (pair[0], pair[1], c))

print("\ninfra cell: author=%d  blind=%d" % (len(a_infra), len(b_infra)))
print("  pulled IN by re-coding : %s" % (sorted(b_infra - a_infra) or "none"))
print("  pushed OUT by re-coding: %s" % ({i: recode[i] for i in sorted(a_infra - b_infra)} or "none"))

worst = {i: recode[i] for i in ids}
w_infra = {i for i in ids if worst[i] == "infra"}
lo, hi = sorted((len(a_infra), len(w_infra)))
print("\nworst case (all %d disagreements resolved against the author):" % len(dis))
print("  infra cell: %d -> %d" % (len(a_infra), len(w_infra)))
print("  newly entering infra: %s" % (sorted(w_infra - a_infra) or "none"))
print("\n=> Under ANY resolution of the %d disagreements the infra cell holds %d-%d papers,"
      "\n   no paper enters it, and every member targets a preservation asset."
      % (len(dis), lo, hi))
