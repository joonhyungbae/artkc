# -*- coding: utf-8 -*-
"""Three-way agreement: author-confirmed coding vs. two independent machine re-codings.

  coder 1 = author-confirmed coding      data/corpus_110.json  (proposed_unit)
  coder 2 = blind re-coding                data/blind_recode_110.json
  coder 3 = blind re-coding, perturbed     data/perturbed_recode_110.json
  coder 4 = blind re-coding, other family  data/thirdparty_recode_110.json  <- optional

Coder 3 applies the same codebook under a *perturbed protocol* (categories presented
in reverse order, re-worded instructions, separate session with no access to the other
codings), testing whether the agreement is an artefact of one prompt.
Coder 4, when present, is produced by running data/recode_prompt.md against a model
from a different family, testing whether it is an artefact of one model.

Reports pairwise Cohen's kappa and, when three codings are present,
Krippendorff's alpha (nominal).

Run:  python3 code/three_way.py
"""
import json, os, itertools
from collections import Counter

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CATS = ["agency", "work", "edu", "audience", "institution", "infra"]


def load():
    corpus = json.load(open(os.path.join(BASE, "corpus_110.json"), encoding="utf-8"))
    coders = {"author": {p["pid"]: p["proposed_unit"] for p in corpus},
              "modelA": json.load(open(os.path.join(BASE, "blind_recode_110.json"), encoding="utf-8"))}
    pert = os.path.join(BASE, "perturbed_recode_110.json")
    if os.path.exists(pert):
        coders["perturbed"] = json.load(open(pert, encoding="utf-8"))
    third = os.path.join(BASE, "thirdparty_recode_110.json")
    if os.path.exists(third):
        coders["otherfamily"] = json.load(open(third, encoding="utf-8"))
    return coders


def cohen_kappa(x, y):
    ids = [i for i in x if i in y]
    n = len(ids)
    po = sum(1 for i in ids if x[i] == y[i]) / n
    cx, cy = Counter(x[i] for i in ids), Counter(y[i] for i in ids)
    pe = sum((cx[c] / n) * (cy[c] / n) for c in CATS)
    return n, po, (po - pe) / (1 - pe)


def krippendorff_alpha(codings):
    """Nominal alpha for m coders over the units they all coded."""
    ids = sorted(set.intersection(*[set(c) for c in codings]))
    m = len(codings)
    # observed disagreement
    Do = 0.0
    for i in ids:
        vals = [c[i] for c in codings]
        Do += sum(1 for a, b in itertools.permutations(vals, 2) if a != b)
    Do /= len(ids) * m * (m - 1)
    # expected disagreement
    allvals = [c[i] for i in ids for c in codings]
    n = len(allvals)
    cnt = Counter(allvals)
    De = sum(cnt[a] * cnt[b] for a, b in itertools.permutations(CATS, 2) if a != b) / (n * (n - 1))
    return len(ids), 1 - Do / De


coders = load()
print("coders present: %s" % ", ".join(coders))
print("\npairwise Cohen's kappa")
for a, b in itertools.combinations(coders, 2):
    n, po, k = cohen_kappa(coders[a], coders[b])
    print("  %-8s x %-8s  n=%d  observed=%.1f%%  kappa=%.3f" % (a, b, n, 100 * po, k))

if len(coders) >= 3:
    n, alpha = krippendorff_alpha(list(coders.values()))
    print("\nKrippendorff's alpha (nominal, %d coders, n=%d) = %.3f" % (len(coders), n, alpha))
    ids = sorted(set.intersection(*[set(c) for c in coders.values()]))
    unan = sum(1 for i in ids if len({c[i] for c in coders.values()}) == 1)
    print("  unanimous across all coders: %d/%d (%.1f%%)" % (unan, len(ids), 100 * unan / len(ids)))
    inf = {name: {i for i in ids if c[i] == "infra"} for name, c in coders.items()}
    core = set.intersection(*inf.values())
    print("\ninfra cell per coder: %s" % {k: len(v) for k, v in inf.items()})
    print("  agreed by every coder: %d" % len(core))
    print("  union (any coder): %d" % len(set.union(*inf.values())))
else:
    print("\n(data/thirdparty_recode_110.json 없음 — 3자 일치도는 산출하지 않음)")
    print("  생성법: data/recode_prompt.md 를 다른 계열 모델에 적용")
