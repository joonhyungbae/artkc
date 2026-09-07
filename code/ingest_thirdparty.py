# -*- coding: utf-8 -*-
"""Validate and install a third-party model's re-coding of the 110-paper corpus.

Paste the model's reply into a text file (markdown fences and surrounding prose are
tolerated; several partial replies can simply be concatenated) and run:

    python3 code/ingest_thirdparty.py <replyfile> [--model "gpt-x, 2026-08-24"]

On success it writes data/thirdparty_recode_110.json and prints the agreement.
Nothing is written unless all 110 pids are present with valid codes.
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
CATS = {"agency", "work", "edu", "audience", "institution", "infra"}

if len(sys.argv) < 2:
    sys.exit(__doc__)
raw = open(sys.argv[1], encoding="utf-8").read()
model = ""
if "--model" in sys.argv:
    model = sys.argv[sys.argv.index("--model") + 1]

# Collect every "Pnnn": "code" pair anywhere in the reply.
pairs = re.findall(r'"(P\d{3})"\s*:\s*"([a-z]+)"', raw)
coding, dup = {}, []
for pid, code in pairs:
    if pid in coding and coding[pid] != code:
        dup.append((pid, coding[pid], code))
    coding[pid] = code

expected = {p["pid"] for p in json.load(open(os.path.join(DATA, "corpus_110.json"), encoding="utf-8"))}
missing = sorted(expected - set(coding))
extra = sorted(set(coding) - expected)
bad = sorted((p, c) for p, c in coding.items() if c not in CATS)

print("parsed pairs      : %d" % len(pairs))
print("unique pids       : %d / %d" % (len(coding), len(expected)))
if dup:
    print("!! conflicting duplicates: %s" % dup[:5])
if missing:
    print("!! missing pids (%d): %s" % (len(missing), missing[:15]))
if extra:
    print("!! unknown pids: %s" % extra[:10])
if bad:
    print("!! invalid codes: %s" % bad[:10])
if missing or extra or bad or dup:
    sys.exit("\n검증 실패 — 파일을 저장하지 않았다. 누락된 pid를 모델에 다시 물어 보완할 것.")

out = os.path.join(DATA, "thirdparty_recode_110.json")
json.dump(coding, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
print("\n검증 통과 → %s" % out)
if model:
    note = os.path.join(DATA, "thirdparty_recode_source.txt")
    open(note, "w", encoding="utf-8").write(model + "\n")
    print("출처 기록 → %s (%s)" % (note, model))
else:
    print("(--model 로 모델명·버전·실행일을 함께 기록할 것. 논문 각주에 밝힌다.)")

print("\n--- 일치도 ---")
import subprocess
subprocess.run([sys.executable, os.path.join(BASE, "code", "three_way.py")], check=False)
