# -*- coding: utf-8 -*-
"""논문 그림을 벡터 PDF로 생성(matplotlib, 단색/흑백, 한글 Noto Sans CJK KR).
재현: python3 figures/make_figures.py  ->  figures/fig{1,2,3}.pdf
데이터: ../ref/jkca/analysis/corpus110.json (n=110, 중복 4쌍 제거)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch

from matplotlib import font_manager as fm
for _fp in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/baekmuk/dotum.ttf"]:
    if os.path.exists(_fp):
        fm.fontManager.addfont(_fp)
        rcParams["font.family"] = fm.FontProperties(fname=_fp).get_name()
        break
rcParams["axes.unicode_minus"] = False
rcParams["pdf.fonttype"] = 42

# 절제된 학술용 팔레트 (색맹에서도 명도차로 구분됨)
C_MAIN = "#5B7DB1"   # 파랑: 창작연구 분포
C_PRES = "#D9913B"   # 황색: 보존 인프라(존재)
C_GAP  = "#B5402F"   # 빨강: 창작 인프라 공백
C_EDGE = "#2c2c2c"

OUT = os.path.dirname(os.path.abspath(__file__))
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig); print("wrote", name)

# ============ 그림 1: 연도별 편수(급증) ============
years = ["2021","2022","2023","2024","2025"]
cnt   = [3, 8, 18, 49, 32]
fig, ax = plt.subplots(figsize=(3.3, 2.0))
ax.bar(years, cnt, width=0.62, color=C_MAIN, edgecolor=C_EDGE, linewidth=0.4)
for x,c in zip(years,cnt):
    ax.text(x, c+0.8, str(c), ha="center", va="bottom", fontsize=7.5)
ax.set_ylabel("편수", fontsize=8); ax.tick_params(labelsize=7.5)
ax.set_ylim(0, 56)
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig, "fig1.pdf")

# ============ 그림 2: 분석 단위 분포 (보존 인프라 강조) ============
labels = ["관객·수용","공유 인프라(보존)","개인 역량","교육","제도·정책","작품·제작"]
vals   = [8, 15, 15, 20, 23, 29]
fig, ax = plt.subplots(figsize=(3.4, 2.3))
ypos = list(range(1, len(labels)+1))
bars = ax.barh(ypos, vals, color=C_MAIN, edgecolor=C_EDGE, linewidth=0.4, height=0.6)
bars[1].set_color(C_PRES)     # 공유 인프라(보존) 강조
for y,v in zip(ypos, vals):
    ax.text(v+0.4, y, str(v), va="center", fontsize=7.3)
ax.set_yticks(ypos)
ax.set_yticklabels(labels, fontsize=7.3)
ax.set_xlabel("편수", fontsize=8); ax.tick_params(axis="x", labelsize=7)
ax.set_xlim(0, 34); ax.set_ylim(0.3, len(labels)+0.7)
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig, "fig2.pdf")

# ============ 그림 3: 4층 개념틀 = 형식지/암묵지 x 객체/주체 2x2 ============
# (순차 파이프라인이 아니라 2x2 구획에서 네 층이 도출됨 — 본문 5.2절과 정합)
fig, ax = plt.subplots(figsize=(3.6, 2.45))
ax.set_xlim(0.6, 9.4); ax.set_ylim(0.7, 9.3); ax.axis("off")

C_OBJ = "#E8EEF6"   # 객체 행
C_SUBJ = "#EAF1E9"  # 주체 행
def cell(x,y,w,h,name,fn):
    fc = C_OBJ if y > 4.6 else C_SUBJ
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.10",
                 linewidth=0.9,edgecolor=C_MAIN,facecolor=fc))
    ax.text(x+w/2, y+h*0.60, name, ha="center", va="center", fontsize=8.8, fontweight="bold")
    ax.text(x+w/2, y+h*0.24, fn, ha="center", va="center", fontsize=7.0, style="italic", color="0.45")

# 셀 좌표 (좌열=형식지, 우열=암묵지 / 상행=객체, 하행=주체)
CW, CH = 3.05, 2.55
LX, RX = 2.35, 5.55
TY, BY = 4.45, 1.55
# 표제: 네 층이 함께 구성하는 대상
ax.text((LX+RX+CW)/2, 8.95, "창작을 위한 공유 지식 인프라", ha="center", va="center",
        fontsize=8.8, fontweight="bold", color=C_EDGE)
# 열 라벨 (지식의 형태)
ax.text(LX+CW/2, 7.75, "형식지", ha="center", va="center", fontsize=7.9, color="0.4")
ax.text(RX+CW/2, 7.75, "암묵지", ha="center", va="center", fontsize=7.9, color="0.4")
cell(LX, TY, CW, CH, "L1  기록", "축적")      # 객체 x 형식지
cell(RX, TY, CW, CH, "L2  플러그인", "운용")   # 객체 x 암묵지
cell(LX, BY, CW, CH, "L4  필드자원", "자기표상")# 주체 x 형식지
cell(RX, BY, CW, CH, "L3  커뮤니티", "순환")   # 주체 x 암묵지
# 행 라벨 (지식의 대상) — 가로 표기
ax.text(1.55, TY+CH/2, "객체", ha="center", va="center", fontsize=7.9, color="0.4")
ax.text(1.55, BY+CH/2, "주체", ha="center", va="center", fontsize=7.9, color="0.4")
save(fig, "fig3.pdf")
print("done")
