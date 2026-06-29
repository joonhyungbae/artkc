# AI 기반 예술 창작 공유 지식 인프라 연구의 현황 분석과 개념틀 제안
### Research Landscape and a Conceptual Framework for AI-Based Shared Knowledge Infrastructure for Art Creation

위 논문의 **재현용 코퍼스·코드** 저장소입니다. 한국콘텐츠학회논문지 투고(심사 중), 2026.
*심사용 익명 저장소 — 저자 정보는 표기하지 않습니다.*

---

## 무엇이 들어 있나 / What's here

```
data/
  corpus_110.tsv          분석 코퍼스 110편: 번호·연도·저자·제목·학술지·분석단위(저자 코딩)·인프라유형·URL
  corpus_110.json         같은 코퍼스 원자료(서지·저자 키워드·저자 코딩 proposed_unit·코더ID pid)
  blind_recode_110.json   저널명·원 코드를 가린 독립 블라인드 재코딩 (P001–P110)
  emerging_ai_infra.tsv   본문 §IV.3이 적시한, 생성형 AI를 분야 인프라 구축에 쓴 신생 사례 5건
code/
  kappa.py                코더 간 일치도(Cohen's κ) 재현
  make_figures.py         논문 그림 1–3 재생성(matplotlib)
figures/
  fig1.png fig2.png fig3.png   300 dpi
codebook.md               분석 단위 6범주 정의·결정규칙·보존/창작 하위분류
LICENSE                   CC BY 4.0
```

## 코퍼스 / Corpus

- **110편 / 66개 KCI 등재 학술지** (2021–2025). 특정 저널을 앵커로 삼지 않고 네 주제군 검색식을 KCI·DBpia·KISTI ScienceON·KoreaScience 전반에 균일하게 적용한 **목적 표집**(전수 census 아님). 따라서 절대 빈도가 아니라 **수집된 코퍼스 내 분포**를 보고한다.
- 어느 저널도 지배적이지 않으며, 가장 큰 비중인 한국콘텐츠학회논문지도 9.1%(10편)다.
- 분석 단위 분포(저자 코딩): 작품·제작 29 · 제도·정책 23 · 교육·리터러시 20 · 개인 역량 15 · **공유 지식 인프라 15(전부 보존)** · 관객·수용 8.

## 재현 / Reproduce

```bash
python3 code/kappa.py        # -> N=110, observed 81.8% (90/110), Cohen's kappa = 0.77
python3 code/make_figures.py # -> figures/fig{1,2,3}.pdf  (한글 폰트 Noto Sans CJK KR 필요)
```

`kappa.py`는 저자 코딩(`data/corpus_110.json`의 `proposed_unit`)과 독립 블라인드 재코딩(`data/blind_recode_110.json`)의 일치도를 산출한다. 공유 지식 인프라 셀은 저자 15편 중 14편을 블라인드 재코딩도 동일하게 분류했다(나머지 1건은 미술 아카이브 저작권 논문으로 제도 경계, 보존/창작 구분에는 무영향).

## 신뢰도 주의 / Reliability note

코딩과 블라인드 재코딩 모두 저자가 대규모 언어 모델의 보조로 수행했다. 따라서 κ는 인간 복수 코더 간 신뢰도가 아니라 **코드북 적용의 재현성**을 가리킨다. 독립된 인간 코더(특히 예술·기록 분야)를 통한 검증은 한계로 남는다.

## 인용 / Citation

이 코퍼스·코드를 사용할 때는 해당 논문을 인용하십시오. 심사용 익명화로 저자·서지 정보는 생략합니다(채택 후 갱신).

## 라이선스 / License

CC BY 4.0. See [LICENSE](LICENSE).
