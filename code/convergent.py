# -*- coding: utf-8 -*-
"""Convergent validity of the `infra` code against an external variable.

The coders saw only title and author keywords. The journal a paper appeared in was
never shown to them and was never used in coding. If the `infra` code tracks something
real rather than the author's private reading, it should line up with the archival /
library-and-information-science journals without having been told about them.

Reports recall, precision and the phi coefficient for each available coding.
Precision below 1.0 is expected and is itself part of the paper's argument: archive
research also appears in arts journals (dance, performance, music).

Run:  python3 code/convergent.py
"""
import json, csv, math, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
ARCHIVAL = re.compile(r"기록|문헌정보|도서관|구술|아카이|박물관")

corpus = json.load(open(os.path.join(DATA, "corpus_110.json"), encoding="utf-8"))
rows = {"P%03d" % int(r["no"]): r for r in
        csv.DictReader(open(os.path.join(DATA, "corpus_110.tsv"), encoding="utf-8"), delimiter="\t")}

codings = {"author": {p["pid"]: p["proposed_unit"] for p in corpus}}
for name, fn in (("recode-1", "blind_recode_110.json"),
                 ("recode-2 (perturbed)", "perturbed_recode_110.json"),
                 ("recode-3 (other family)", "thirdparty_recode_110.json")):
    path = os.path.join(DATA, fn)
    if os.path.exists(path):
        codings[name] = json.load(open(path, encoding="utf-8"))

ids = sorted(rows)
archival = {p for p in ids if ARCHIVAL.search(rows[p]["journal"])}
print("기록·문헌정보 계열 학술지 게재 논문: %d편" % len(archival))
print("  %s\n" % ", ".join(sorted({rows[p]["journal"] for p in archival})))
print("%-24s %6s %8s %10s %8s" % ("coding", "infra", "recall", "precision", "phi"))
for name, code in codings.items():
    inf = {p for p in ids if code.get(p) == "infra"}
    a = len(inf & archival)
    b, c = len(inf) - a, len(archival) - a
    dd = len(ids) - a - b - c
    denom = math.sqrt((a + b) * (c + dd) * (a + c) * (b + dd))
    phi = (a * dd - b * c) / denom if denom else float("nan")
    print("%-24s %6d %8.1f%% %9.1f%% %8.3f"
          % (name, len(inf), 100 * a / len(archival), 100 * a / len(inf) if inf else 0, phi))

print("\n저널명은 코더에게 제시되지 않았고 코딩에도 쓰이지 않았다.")
print("재현율이 높다는 것은 코드가 분과 경계와 독립적으로 수렴함을 뜻한다.")
