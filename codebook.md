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

## infra sub-classification (preservation vs creation)

Papers coded `infra` are sub-classified by *what the asset is for*:

- **preservation** — recording/preserving/organizing what the field has already made (museum/performance/film archives, collection data, acquisition policy).
- **creation** — lowering the threshold for the *next* work (externalized techniques/workflows, shared creator data, a field knowledge base).

In this corpus all 15 `infra` papers are **preservation**; `infra_type` is given in `data/corpus_110.tsv` / `corpus_110.json`.

## Reliability note

Both the author coding and the independent blind re-coding were performed by the author with large-language-model assistance. The reported Cohen's κ therefore reflects **codebook-application reproducibility**, not human multi-coder reliability. Independent human coders (especially from the arts/archival fields) remain future work. See the paper, §III.4 and §VI.
