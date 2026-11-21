"""2026-11-21: Life expectancy rises across the whole US income range.

Finding (association): life expectancy at 40 rises with household income at
every percentile of the US income distribution. Chetty et al. (JAMA 2016),
1.4 billion tax records 1999-2014 linked to Social Security death records.

Data: the study's released Online Data Table 1 (national life expectancy at 40
by sex and income percentile, pooling 2001-14). This script reproduces the
paper's headline gaps between the top and bottom 1% and asserts the match.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-21"

# ---------------------------------------------------------------- data ------
t = pd.read_csv(HERE / "data/health_ineq_online_table_1.csv")
text = re.sub(r"\s+", " ", (HERE / "data/pubmed_abstracts.txt").read_text())

res = {}
for g in ("M", "F"):
    x = t[t.gnd == g].set_index("pctile")
    gap = x.le_raceadj[100] - x.le_raceadj[1]
    se = np.hypot(x.sd_le_raceadj[100], x.sd_le_raceadj[1])
    res[g] = dict(x=x, gap=gap, lo=gap - 1.96 * se, hi=gap + 1.96 * se)

# Reproduce the published gaps (JAMA 2016 abstract): 14.6 (14.4-14.8) men, 10.1 (9.9-10.3) women.
assert (round(res["M"]["gap"], 1), round(res["M"]["lo"], 1), round(res["M"]["hi"], 1)) == (14.6, 14.4, 14.8)
assert (round(res["F"]["gap"], 1), round(res["F"]["lo"], 1), round(res["F"]["hi"], 1)) == (10.1, 9.9, 10.3)
assert "14.6 years (95% CI, 14.4 to 14.8 years) for men and 10.1 years (95% CI, 9.9 to 10.3 years) for women" in text

# Monotone rise: share of one-percentile steps where life expectancy goes up.
for g in ("M", "F"):
    d = np.diff(res[g]["x"].le_raceadj.values)
    res[g]["up"] = int((d > 0).sum())

# Norway comparison (Kinge et al., JAMA 2019, abstract).
NOR = {"M": (13.8, 12.3, 15.2), "F": (8.4, 7.2, 9.6)}
assert "13.8 years (95% CI, 12.3-15.2)" in text and "8.4 years (95% CI, 7.2-9.6)" in text

for g, name in (("M", "Men"), ("F", "Women")):
    x = res[g]["x"]
    print(f"{name}: life expectancy at 40, bottom 1% {x.le_raceadj[1]:.1f}, median (p50) {x.le_raceadj[50]:.1f}, "
          f"top 1% {x.le_raceadj[100]:.1f}; gap {res[g]['gap']:.1f} ({res[g]['lo']:.1f}-{res[g]['hi']:.1f}) reproduced; "
          f"rises in {res[g]['up']} of 99 percentile steps")
    print(f"  bottom-half gain p1->p50 {x.le_raceadj[50] - x.le_raceadj[1]:.1f} yrs; top-half gain p50->p100 "
          f"{x.le_raceadj[100] - x.le_raceadj[50]:.1f} yrs")
inc = res["M"]["x"].hh_inc
print(f"mean household income (men's table): p1 ${inc[1]:,.0f}, p50 ${inc[50]:,.0f}, p100 ${inc[100]:,.0f}")
print(f"Norway (Kinge 2019): men {NOR['M'][0]} ({NOR['M'][1]}-{NOR['M'][2]}), women {NOR['F'][0]} ({NOR['F'][1]}-{NOR['F'][2]})")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17.5)
px.masthead(fig, DATE, NO)
mx, fx = res["M"]["x"], res["F"]["x"]
y = px.headline(
    fig, "Economics · Income and lifespan",
    "Life expectancy rises across\nthe whole US *income range*",
    f"At 40, the richest 1% of US men had a life expectancy {res['M']['gap']:.1f} years longer than the poorest 1%; for women\n"
    f"the gap was {res['F']['gap']:.1f} years. Life expectancy rose across the whole income range, with no plateau at the top.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Tax records linked to\nSocial Security deaths"),
    ("Sample", "1.4 billion person-years,\nUS adults aged 40–76, 2001–14"),
    ("Source", "Chetty et al.\nJAMA, 2016"),
    ("Consistent with", "Kinge et al. 2019 (Norway)\nNational Academies 2015"),
], widths=[0.24, 0.30, 0.17, 0.29])

# --- 01: life expectancy by income percentile ---------------------------------
top1 = y - 0.07
h1 = 0.30
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.12, h1])
for g, col, name in (("F", INDIGO, "Women"), ("M", SIGNAL, "Men")):
    x = res[g]["x"]
    ax.fill_between(x.index, x.le_raceadj - 1.96 * x.sd_le_raceadj, x.le_raceadj + 1.96 * x.sd_le_raceadj,
                    color=col, alpha=0.18, lw=0, zorder=2)
    ax.scatter(x.index, x.le_raceadj, s=14, color=col, edgecolor="none", zorder=3)
    ax.text(101.5, x.le_raceadj[100], f"{name}\n{x.le_raceadj[100]:.1f}", color=col, fontsize=10.5,
            weight="semibold", va="center")
    ax.text(-1.5, x.le_raceadj[1], f"{x.le_raceadj[1]:.1f}", color=col, fontsize=10, family=px.MONO,
            va="center", ha="right")
ax.annotate("", xy=(100, mx.le_raceadj[100]), xytext=(100, mx.le_raceadj[1]),
            arrowprops=dict(arrowstyle="<->", color=INK_3, lw=0.8))
ax.text(98, (mx.le_raceadj[100] + mx.le_raceadj[1]) / 2 - 0.6, f"Men: {res['M']['gap']:.1f}-year gap\nbetween bottom\nand top 1%",
        ha="right", va="center", fontsize=9.5, color=INK_2)
ax.set_xlim(-6, 100.5)
ax.set_ylim(70, 90)
ax.set_yticks([70, 75, 80, 85, 90])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
ax.set_xticks([1, 25, 50, 75, 100])
ax.set_xlabel("Household income percentile")
ax.set_ylabel("Expected age at death, at age 40")
ax.yaxis.set_label_coords(-0.07, 0.5)
ax.grid(axis="y")
for p, ha in ((1, "left"), (50, "center"), (100, "right")):
    ax.text(p, 70.35, f"men's mean ${inc[p]:,.0f}", ha=ha, va="bottom", fontsize=8.5, family=px.MONO, color=INK_3)
px.mono_ticks(ax)
px.panel(ax, 1, "Life expectancy at 40, by household income percentile, US 2001–14",
         "One dot per percentile, race-adjusted. Bands: 95% confidence intervals.", pad=0.55)

# --- 02: the gap in the US and Norway -----------------------------------------
top2 = top1 - h1 - 0.12
h2 = 0.13
ax2 = fig.add_axes([px.LEFT + 0.26, top2 - h2, px.WIDTH - 0.26 - 0.22, h2])
rows = [("US men", res["M"]["gap"], res["M"]["lo"], res["M"]["hi"], SIGNAL, "Chetty et al. 2016"),
        ("Norway men", *NOR["M"], SIGNAL, "Kinge et al. 2019"),
        ("US women", res["F"]["gap"], res["F"]["lo"], res["F"]["hi"], INDIGO, "Chetty et al. 2016"),
        ("Norway women", *NOR["F"], INDIGO, "Kinge et al. 2019")]
for i, (lab, v, lo, hi, col, src) in enumerate(rows[::-1]):
    ax2.plot([lo, hi], [i, i], color=col, lw=1.8, zorder=3, solid_capstyle="round")
    ax2.scatter([v], [i], s=60, marker="s", color=col, edgecolor=PAPER, lw=0.8, zorder=4)
    ax2.text(hi + 0.25, i, f"{v:.1f}  ({lo:.1f}–{hi:.1f})", fontsize=9.5, family=px.MONO, color=col, va="center")
    ax2.text(-0.03, i + 0.08, lab, transform=ax2.get_yaxis_transform(), ha="right", va="bottom", fontsize=11, color=INK)
    ax2.text(-0.03, i - 0.06, src, transform=ax2.get_yaxis_transform(), ha="right", va="top", fontsize=8.5,
             color=INK_3)
ax2.set_xlim(0, 17)
ax2.set_ylim(-0.6, len(rows) - 0.4)
ax2.set_yticks([])
ax2.set_xticks([0, 5, 10, 15])
ax2.grid(axis="x")
ax2.set_xlabel("Years of life expectancy at 40, top 1% minus bottom 1% (95% CI)")
px.mono_ticks(ax2)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "The gap between the richest and poorest 1%, US and Norway",
         "Norway's registry data, 2005–15, show a similar gap for men and a smaller one for women.", pad=0.55)

px.footer(fig,
          "DATA  Chetty et al., JAMA 315:1750 (2016), Online Data Table 1 (Health Inequality Project). Kinge et al., JAMA\n"
          "      321:1916 (2019), abstract. US gaps reproduced from the released table and match the paper.\n"
          "NOTE  Association, not cause: income tracks other traits that affect health, and poor health can lower income.",
          NO)
px.save(fig, HERE)
print("saved")
