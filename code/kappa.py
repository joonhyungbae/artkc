# -*- coding: utf-8 -*-
"""Reproduce inter-coder agreement (Cohen's kappa) for the 110-paper corpus.

  author coding   = data/corpus_110.json        (field: proposed_unit)
  blind re-coding = data/blind_recode_110.json   (codebook only, blind to author labels)

Run:  python3 code/kappa.py
Expected: N=110, observed 81.8% (90/110), kappa=0.77.
"""
import json, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")
corpus = json.load(open(os.path.join(DATA, "corpus_110.json"), encoding="utf-8"))
recode = json.load(open(os.path.join(DATA, "blind_recode_110.json"), encoding="utf-8"))

CATS = ["agency", "work", "edu", "audience", "institution", "infra"]
orig = {p["pid"]: p["proposed_unit"] for p in corpus}
ids = list(orig); N = len(ids)

agree = sum(1 for i in ids if orig[i] == recode[i]); po = agree / N
co = Counter(orig.values()); cr = Counter(recode.values())
pe = sum((co[c] / N) * (cr[c] / N) for c in CATS)
kappa = (po - pe) / (1 - pe)

print(f"N = {N}")
print(f"observed agreement = {agree}/{N} = {100*po:.1f}%")
print(f"Cohen's kappa = {kappa:.4f}")
oi = sum(1 for i in ids if orig[i] == "infra")
both = sum(1 for i in ids if orig[i] == "infra" and recode[i] == "infra")
print(f"shared-knowledge-infrastructure cell: author={oi}, agreed by blind recode={both}")
print("author unit distribution:", dict(co.most_common()))
dis = [(i, orig[i], recode[i]) for i in ids if orig[i] != recode[i]]
print(f"\ndisagreements ({len(dis)}):")
for i, a, b in dis:
    print(f"  {i}: author={a:12s} blind={b}")
