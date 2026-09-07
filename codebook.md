# Codebook — analysis-unit coding

Each paper receives **one primary code**: *what the paper takes as its object of study*.

## Analysis unit (6 categories)

| code | 한글 | definition (unit of analysis) |
|---|---|---|
| `agency` | 개인 역량·주체성 | the individual creator's competence, identity, role-change, career |
| `work` | 작품·제작 | the artwork / creative output / the making process itself (methods, pipelines) |
| `edu` | 교육·리터러시 | an education program, teaching method, learning effect, or literacy cultivation |
| `audience` | 관객·수용 | perception / reception / acceptance / UX of audiences, users, consumers |
| `institution` | 제도·정책·산업 | institutions, policy, industry, law, copyright, welfare, discourse, research-trend |
| `infra` | 공유 지식 인프라 | construction/operation of a **field-level shared knowledge asset** (shared archives, datasets, knowledge bases, platforms, metadata standards, classification systems) |

## Decision rules (boundaries)

- Education program / effect → `edu` (even if individuals change inside it).
- UX / reception / perception → `audience`.
- Policy / institution / industry / copyright / research-trend → `institution`.
- Analysis of the artwork or the making process → `work`.
- Individual's competence / identity / role → `agency`.
- A field-wide shared asset's construction/operation → `infra`.
- **`infra` is restricted** to building/operating an asset the whole field shares. A single artwork's archiving or one institution's one-off system → `institution`. A machine-learning detection dataset, or merely *using* existing infrastructure as data → coded by the analysis target, not `infra`.

## infra sub-classification (use phase)

Papers coded `infra` are sub-classified by the **use phase** the asset is designed for.
The phases sit on one continuum, and a later phase subsumes the earlier ones, so each
paper is coded at the furthest phase it reaches.

- **preserve** (보존·정리) — collecting, describing and keeping what the field has already
  made (acquisition policy, classification/description schemes, building an archive).
- **access** (열람·이용) — opening the accumulated asset so researchers, audiences or
  citizens can find and use it (search/sharing improvements, open-data programmes,
  user studies).
- **produce** (창작 생산) — designing the asset so it feeds back into the production
  workflow of new work (externalized techniques/workflows, shared creator data, a field
  knowledge base wired into creation tools).

Preservation and creation are therefore **not two exclusive kinds** of infrastructure but
two phases of one continuum. An archive is a precondition for the next work, and what
separates the phases is whether description, access conditions and licensing were designed
for reuse in production.

In this corpus all 15 `infra` papers target **preservation assets**: 7 stop at `preserve`
and 8 reach `access`. **None reaches `produce`.** The closest boundary case is no.104
(an online film sound-effect library). Per-paper assignments and the signal used for each
are in `data/infra_phase_15.tsv`; the legacy two-way `infra_type` column in
`data/corpus_110.tsv` / `corpus_110.json` is retained for backward compatibility.

## Reliability note

Both the author coding and the independent blind re-coding were performed by the author with large-language-model assistance. The reported Cohen's κ therefore reflects **codebook-application reproducibility**, not human multi-coder reliability. Independent human coders (especially from the arts/archival fields) remain future work.

Two things bound how far this limitation reaches. `code/sensitivity.py` resolves **all 20
disagreements against the author** and shows the `infra` cell moves only 15 -> 14, with no
paper entering it, so the paper's core result is unchanged. `code/sample_stratified.py`
draws the planned human-coder validation sample (proportional stratified 33 = 30%, plus the
15-paper `infra` census, 43 papers = 39% of the corpus) with a fixed seed and emits blinded
coding sheets. See the paper, §III.4 and §VI.
