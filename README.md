# AI 기반 예술 창작 공유 지식 인프라 연구의 현황 분석과 개념틀 제안
### Research Landscape and a Conceptual Framework for AI-Based Shared Knowledge Infrastructure for Art Creation

위 논문의 **재현용 코퍼스·코드** 저장소입니다.
Reproducibility corpus and code for the paper:

> 배준형 (Joonhyung Bae), 한국과학기술원(KAIST) 문화기술연구소 연수연구원 (Postdoctoral Researcher, Culture Technology Research Institute, KAIST).
> 한국콘텐츠학회논문지, **게재 확정** (2026년 9월 7일 채택 / accepted 7 September 2026). 권·호·쪽수는 게재 후 갱신.

---

## 무엇이 들어 있나 / What's here

```
data/
  corpus_110.tsv          분석 코퍼스 110편: 번호·연도·저자·제목·학술지·분석단위(저자 코딩)·인프라유형·URL
  corpus_110.json         같은 코퍼스 원자료(서지·저자 키워드·저자 코딩 proposed_unit·코더ID pid)
  blind_recode_110.json   저널명·원 코드를 가린 독립 블라인드 재코딩 (P001–P110)
  emerging_ai_infra.tsv   본문 §IV.3이 적시한, 생성형 AI를 분야 인프라 구축에 쓴 신생 사례 5건
  infra_phase_15.tsv      인프라 15편의 이용 국면 하위코딩(보존·정리 / 열람·이용 / 창작 생산)
  perturbed_recode_110.json  교란 프로토콜(범주 역순·지시문 변경) 독립 재코딩
  thirdparty_recode_110.json 다른 계열 모델의 독립 재코딩
  thirdparty_recode_source.txt 위 재코딩에 쓴 모델명·버전·실행일
  recode_prompt.md        다른 계열 모델 재코딩용 지시문 + 코드북
  recode_items.tsv        블라인드 항목 110편(저널·저자·코드 제거)
  sample_43.json          인간 코더 검증용 층화표본 43편(seed 고정)
  coding_sheet_*.tsv      코더용 블라인드 코딩 시트(저널·저자·원 코드 비표시)
code/
  kappa.py                코더 간 일치도(Cohen's κ) 재현
  three_way.py            저자 확정 코딩 + 세 재코딩의 4자 일치도(Krippendorff's α)
  convergent.py           외부 준거(게재 학술지 분과)와의 수렴타당도
  ingest_thirdparty.py    외부 모델 재코딩 응답 검증·설치
  sensitivity.py          불일치 20건을 전부 뒤집는 민감도 분석
  sample_stratified.py    층화표본 추출 + 블라인드 코딩 시트 생성
  make_figures.py         논문 그림 1–3 재생성(matplotlib)
figures/
  fig1.png fig2.png fig3.png   300 dpi
codebook.md               분석 단위 6범주 정의·결정규칙·이용 국면 하위분류
LICENSE                   CC BY 4.0
```

## 코퍼스 / Corpus

- **110편 / 66개 KCI 등재 학술지** (2021–2025). 특정 저널을 앵커로 삼지 않고 네 주제군 검색식을 KCI·DBpia·KISTI ScienceON·KoreaScience 전반에 균일하게 적용한 **목적 표집**(전수 census 아님). 따라서 절대 빈도가 아니라 **수집된 코퍼스 내 분포**를 보고한다.
- 어느 저널도 지배적이지 않으며, 가장 큰 비중인 한국콘텐츠학회논문지도 9.1%(10편)다.
- 분석 단위 분포(저자 코딩): 작품·제작 29 · 제도·정책 23 · 교육·리터러시 20 · 개인 역량 15 · **공유 지식 인프라 15** · 관객·수용 8.
- 인프라 15편의 이용 국면: **보존·정리 7 · 열람·이용 8 · 창작 생산 0.** 보존과 창작은 배타적인 두 종류가 아니라 하나의 연속선 위의 두 국면이며, 축적된 자산을 새 작업의 제작 워크플로에 되먹이는 설계를 연구 대상으로 삼은 경우가 없다는 것이 본 연구가 말하는 공백이다(`data/infra_phase_15.tsv`).

## 재현 / Reproduce

```bash
python3 code/kappa.py             # -> N=110, observed 81.8% (90/110), Cohen's kappa = 0.77
python3 code/sensitivity.py       # -> 불일치 20건 전부 뒤집어도 infra 15->14, 신규 유입 0
python3 code/three_way.py         # -> 4자 Krippendorff alpha = 0.807, 만장일치 79/110
python3 code/sample_stratified.py # -> data/sample_43.json, coding_sheet_*.tsv
python3 code/make_figures.py      # -> figures/fig{1,2,3}.pdf  (한글 폰트 Noto Sans CJK KR 필요)
```

`kappa.py`는 저자 코딩(`data/corpus_110.json`의 `proposed_unit`)과 독립 블라인드 재코딩(`data/blind_recode_110.json`)의 일치도를 산출한다. 공유 지식 인프라 셀은 저자 15편 중 14편을 블라인드 재코딩도 동일하게 분류했다(나머지 1건은 미술 아카이브 저작권 논문으로 제도 경계, 보존/창작 구분에는 무영향).

## 신뢰도 주의 / Reliability note

코딩과 블라인드 재코딩 모두 저자가 대규모 언어 모델의 보조로 수행했다. 따라서 κ는 인간 복수 코더 간 신뢰도가 아니라 **코드북 적용의 재현성**을 가리킨다. 재코딩이 저자의 코드북을 입력으로 받았으므로 코드북 자체의 개념 경계 오류는 이 절차로 탐지되지 않는다. 독립된 인간 코더(특히 예술·기록 분야)를 통한 검증은 한계로 남는다.

이 한계가 어디까지 미치는지는 두 가지로 한정된다.

- `code/sensitivity.py` — 불일치 20건을 **전부 재코딩 값으로 뒤집는** 최악의 경우를 계산한다. 공유 지식 인프라 셀은 15편에서 14편으로 줄 뿐이고 이 범주로 새로 들어오는 논문은 없으며, 전부 보존 자산을 대상으로 한다는 결과는 유지된다. 갈린 지점은 개인 역량·작품·제도의 인접 경계에 몰려 있다.
- `code/three_way.py` — **저자 확정 코딩 + 두 차례 독립 재코딩**의 일치도. 재코딩 하나는 원 프로토콜, 다른 하나는 **범주 제시 순서를 뒤집고 지시문 표현을 바꾼 교란 프로토콜**로, 앞의 코딩에 접근할 수 없는 별도 세션에서 수행했다. 여기에 **다른 계열 모델**의 재코딩까지 더한 네 코딩의 결과는 **Krippendorff's α = 0.807**, 만장일치 79/110(71.8%), 쌍별 κ = 0.693~0.885다.

인프라 셀은 네 코딩에서 **15 / 14 / 15 / 6편**으로 갈린다. 갈림의 축은 하나다. 특정 기관에 묶인 아카이브(서울시립 미술아카이브, 남산예술센터, 국립현대미술관 등)를 분야가 공유하는 자산으로 볼 것인가이며, 가장 엄격한 코딩은 이들을 `institution`으로 보내고 분야 단위로 열린 자산 6편만 남긴다. **이 불일치는 논문 §III.4에 그대로 보고되어 있다.** 다만 두 가지는 코딩 선택과 무관하게 유지된다. 어느 코딩도 저자 코딩에 없던 논문을 이 범주로 새로 끌어오지 않았고(합집합 15편), 어느 코딩에서도 `produce`(창작 생산) 국면에 도달한 논문은 없다.
- `data/recode_prompt.md`(+`recode_prompt_filled.md`, `recode_items.tsv`) — 다른 계열 모델 재코딩에 쓴 지시문과 블라인드 항목(저널·저자·기존 코드 제거). `code/ingest_thirdparty.py`가 모델 답변을 검증해 설치한다.
- `code/convergent.py` — **코딩에 쓰지 않은 외부 변수와의 수렴타당도.** 코더에게 게재 학술지는 제시되지 않았는데, 기록·문헌정보 계열 학술지 8편을 저자 확정 코딩은 전부 `infra`로 분류한다(재현율 100%, φ=0.71). 인프라를 6편으로 좁힌 코딩은 3편만 포함한다(재현율 37.5%, φ=0.40). 정밀도가 1에 못 미치는 것은 아카이브 연구가 무용·공연·음악 등 예술 분과지에도 실리기 때문이며, 이는 논문의 논지 자체다.
- `code/sample_stratified.py` — 후속 인간 코더 검증의 표본을 seed 고정으로 추출한다. 6범주 비례 층화 33편(30%)에 핵심 범주인 인프라 15편 전수를 더한 **43편(코퍼스의 39%)**이며, 코더에게 줄 블라인드 코딩 시트도 함께 생성한다. 헤드라인 κ는 비례 표본 33편에서 산출하고(95% 신뢰구간 반폭 약 0.16), 인프라 셀은 전수 포함으로 마진이 달라지므로 일치율로만 보고한다.

## 인용 / Citation

이 코퍼스·코드를 사용할 때는 해당 논문을 인용하십시오. 권·호·쪽수·DOI는 게재 후 갱신합니다.

```
배준형, "AI 기반 예술 창작 공유 지식 인프라 연구의 현황 분석과 개념틀 제안,"
한국콘텐츠학회논문지, 2026. (2026년 9월 7일 채택, 게재 예정)
```

```
J. Bae, "Research Landscape and a Conceptual Framework for AI-Based Shared Knowledge
Infrastructure for Art Creation," Journal of the Korea Contents Association, 2026.
(accepted 7 September 2026, in press)
```

코퍼스·코드 자체를 인용할 때: https://github.com/joonhyungbae/artkc

## 라이선스 / License

CC BY 4.0. See [LICENSE](LICENSE).
