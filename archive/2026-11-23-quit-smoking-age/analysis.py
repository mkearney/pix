"""2026-11-23: The earlier smokers quit, the more years they gain.

Finding (moderator): the benefit of stopping smoking depends on the age at
stopping. British doctors (Doll et al., BMJ 2004) and US adults (Jha et al.,
NEJM 2013) who quit around 30 gained about 10 years of life expectancy over
continuing smokers; quitting at 60 gained about 3. In one million UK women
(Pirie et al., Lancet 2013), stopping at 25-34 avoided about 97% of the excess
mortality of continuing smokers, and stopping at 35-44 about 90%.

Data: values transcribed from the papers' text (data/transcribed.csv), each
checked against the saved abstracts and full-text excerpt.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-23"

# ---------------------------------------------------------------- data ------
t = pd.read_csv(HERE / "data/transcribed.csv", dtype={"age_at_quitting": str})
txt = re.sub(r"\s+", " ", (HERE / "data/pubmed_abstracts.txt").read_text()
             + (HERE / "data/pirie_2013_results_excerpt.txt").read_text())

# Every transcribed value appears in the saved source text.
assert "Cessation at age 60, 50, 40, or 30 years gained, respectively, about 3, 6, 9, or 10 years of life expectancy" in txt
assert "died on average about 10 years younger than lifelong non-smokers" in txt
assert "quit smoking at 25 to 34, 35 to 44, or 45 to 54 years of age gained about 10, 9, and 6 years of life" in txt
assert "34 439 male British doctors" in txt
assert "rate ratio 2·97, 2·88-3·07" in txt
assert "1·05 (95% CI 1·00-1·11) and 1·20 (1·14-1·26) for all-cause mortality" in txt
assert "relative risk 1·56 (95% CI 1·49–1·64) for overall mortality" in txt
assert "it is only 3% and 10% of the excess mortality among continuing smokers" in txt

doll = t[t.study == "Doll 2004"].assign(age=lambda d: d.age_at_quitting.astype(int))
jha = t[t.study == "Jha 2013"].assign(age=lambda d: d.age_at_quitting.str[:2].astype(int) + 5)  # band midpoints
pir = t[t.study == "Pirie 2013"].set_index("age_at_quitting")
rr_cont = pir.loc["still smoking", "value"]

# Share of continuing smokers' excess risk avoided by stopping: 1 - (RR_ex - 1) / (RR_cont - 1).
avoided = {g: 1 - (pir.loc[g, "value"] - 1) / (rr_cont - 1) for g in ("25-34", "35-44", "45-54")}
assert round(1 - avoided["25-34"], 2) == 0.03 and round(1 - avoided["35-44"], 2) == 0.10  # paper: 3% and 10%

print("Doll 2004, UK male doctors (n=34,439, 1951-2001): years gained by age at quitting:",
      ", ".join(f"{a}: {v:.0f}" for a, v in zip(doll.age, doll.value)), "| continuing smokers died about 10 years younger")
print("Jha 2013, US adults: years gained:", ", ".join(f"{g}: {v:.0f}" for g, v in zip(jha.age_at_quitting, jha.value)))
print(f"Pirie 2013, UK women: RR still smoking {rr_cont:.2f} ({pir.loc['still smoking', 'lo']:.2f}-{pir.loc['still smoking', 'hi']:.2f})")
for g, a in avoided.items():
    r = pir.loc[g]
    print(f"  stopped at {g}: RR {r.value:.2f} ({r.lo:.2f}-{r.hi:.2f}); excess risk avoided {a:.0%}")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17.5)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Health · Smoking and lifespan",
    "The earlier smokers quit,\nthe more *years they gain*",
    "British doctors who kept smoking cigarettes died about 10 years younger than non-smokers. Quitting at 30 gained\n"
    "about 10 years over continuing smokers, and quitting at 60 about 3. US adults showed a similar pattern.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Prospective cohorts linked\nto death records"),
    ("Sample", "34,439 UK doctors, 50 years;\n1.2 million UK women; US survey"),
    ("Source", "Doll et al. BMJ 2004\nPirie et al. Lancet 2013"),
    ("Consistent with", "Jha et al. NEJM 2013 · Cho et al. 2024\nUS Surgeon General 2020"),
], widths=[0.22, 0.29, 0.20, 0.29])

# --- 01: years gained by age at quitting --------------------------------------
top1 = y - 0.07
h1 = 0.25
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.14, h1])
ax.plot([36, 66], [10, 10], color=INK_3, lw=0.8, ls=(0, (4, 3)), zorder=1)
ax.text(64.5, 10.25, "Continuing cigarette smokers lost about 10 years vs non-smokers (UK doctors)", ha="right", va="bottom", fontsize=9.5,
        color=INK_2)
ax.plot(doll.age, doll.value, color=SIGNAL, lw=2, zorder=3)
ax.scatter(doll.age, doll.value, s=70, color=SIGNAL, edgecolor=PAPER, lw=1, zorder=4)
for g, v in zip(jha.age_at_quitting, jha.value):
    a0, a1 = (int(x) for x in g.split("-"))
    ax.plot([a0, a1 + 1], [v, v], color=INDIGO, lw=11, solid_capstyle="butt", zorder=2, alpha=0.3)
    ax.text(a0 + 0.4, v, f"{v:.0f}", color=INDIGO, fontsize=11, family=px.MONO, va="center", ha="left", zorder=4)
for a, v in zip(doll.age, doll.value):
    ax.text(a + 0.9, v + 0.35, f"{v:.0f}", fontsize=12, color=SIGNAL, weight="semibold", family=px.MONO)
ax.text(60, 2.4, "UK male doctors\nDoll et al. 2004 (line)", color=SIGNAL, fontsize=10, va="top", ha="center", weight="semibold")
ax.text(26, 7.6, "US adults, Jha et al. 2013 (bars):\nquit at 25–34, 35–44, 45–54", color=INDIGO, fontsize=9.5,
        va="top", ha="left")
ax.set_xlim(24, 66)
ax.set_ylim(0, 12)
ax.set_xticks([30, 40, 50, 60])
ax.set_xticklabels(["30", "40", "50", "60"])
ax.set_yticks([0, 3, 6, 9, 12])
ax.set_xlabel("Age at quitting")
ax.set_ylabel("Years of life gained")
ax.grid(axis="y")
px.mono_ticks(ax)
px.panel(ax, 1, "Years of life gained over continuing smokers, by age at quitting",
         "Line: UK doctors by exact age. Bars: US adults by age band. Both papers give approximate figures, no intervals.", pad=0.55)

# --- 02: Million Women Study, risk of death against never-smokers --------------
top2 = top1 - h1 - 0.12
h2 = 0.16
ax2 = fig.add_axes([px.LEFT + 0.2, top2 - h2, px.WIDTH - 0.2 - 0.2, h2])
rows = [("Never smoked", 1.0, 1.0, 1.0, None, INK_3),
        ("Stopped at 25–34", *pir.loc["25-34", ["value", "lo", "hi"]], avoided["25-34"], SIGNAL),
        ("Stopped at 35–44", *pir.loc["35-44", ["value", "lo", "hi"]], avoided["35-44"], SIGNAL),
        ("Stopped at 45–54", *pir.loc["45-54", ["value", "lo", "hi"]], avoided["45-54"], SIGNAL),
        ("Still smoking", rr_cont, *pir.loc["still smoking", ["lo", "hi"]], None, INK)]
n = len(rows)
for i, (lab, v, lo, hi, av, col) in enumerate(rows):
    yy = n - 1 - i
    if lo != hi:
        ax2.plot([lo, hi], [yy, yy], color=col, lw=2, zorder=3, solid_capstyle="round")
    ax2.scatter([v], [yy], s=70, marker="s", color=col, edgecolor=PAPER, lw=0.8, zorder=4)
    ax2.text(-0.03, yy, lab, transform=ax2.get_yaxis_transform(), ha="right", va="center", fontsize=11, color=INK)
    val = "1 (reference)" if lo == hi else f"{v:.2f} ({lo:.2f}–{hi:.2f})"
    ax2.text(max(hi, v) + 0.07, yy, val, fontsize=9.5, family=px.MONO, color=col, va="center")
    if av is not None:
        ax2.text(1.03, yy, f"{av:.0%}" + ("*" if lab.endswith("45–54") else ""), transform=ax2.get_yaxis_transform(), fontsize=12, color=SIGNAL,
                 weight="semibold", family=px.MONO, va="center")
ax2.text(1.03, n - 0.35, "Excess risk\navoided", transform=ax2.get_yaxis_transform(), fontsize=9, color=INK_2,
         va="bottom")
ax2.axvline(1, color=INK_3, lw=0.7, zorder=1)
ax2.set_xlim(0.8, 3.6)
ax2.set_ylim(-0.6, n - 0.4)
ax2.set_yticks([])
ax2.set_xticks([1, 1.5, 2, 2.5, 3, 3.5])
ax2.grid(axis="x")
ax2.set_xlabel("Risk of death relative to never-smokers (95% CI)")
px.mono_ticks(ax2)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "UK women: risk of death in later middle age, by age at stopping",
         "Million Women Study, 1.2 million women followed about 12 years. Share avoided computed from the relative risks.",
         pad=0.55)

px.footer(fig,
          "DATA  Doll et al., BMJ 328:1519 (2004); Jha et al., NEJM 368:341 (2013); Pirie et al., Lancet 381:133 (2013).\n"
          "      Values transcribed from the papers' text. Excess risk avoided = 1 - (RR ex-smoker - 1) / (RR still smoking - 1).\n"
          "      *Derived here; the paper says at least two-thirds.\n"
          "NOTE  Cohort comparisons adjusted for age and other factors, not trials. People who quit can differ from those who don't.",
          NO)
px.save(fig, HERE)
print("saved")
