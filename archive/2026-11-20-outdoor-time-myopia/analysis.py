"""2026-11-20: Getting children outdoors lowers their risk of myopia.

Finding (effect): randomised trials that add outdoor time to the school day
lower the share of children who become short-sighted. Cochrane (Kido et al.
2024) pools five trials; the largest single trials are He et al. 2015
(Guangzhou) and He et al. 2022 (Shanghai).

No microdata were released, so values are transcribed from the abstracts
(data/SOURCES.md). This script checks every transcribed value against the saved
abstract text, reproduces the Guangzhou percentages from the case counts, and
prints every number the post and chart use.
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
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-20"

# ---------------------------------------------------------------- data ------
co = pd.read_csv(HERE / "data/cochrane2024_incidence.csv")
tr = pd.read_csv(HERE / "data/trials.csv")
text = re.sub(r"\s+", " ", (HERE / "data/pubmed_abstracts.txt").read_text())

# Transcription checks against the saved abstracts.
for _, r in co.iterrows():
    for s in (f"{r.incidence_outdoor_pct}% with intervention versus {r.incidence_control_pct}% with control",
              f"(RR), {r.rr:.2f}" if r.years == 1 else f"RR {r.rr:.2f}",
              f"95% CI {r.rr_lo:.2f} to {r.rr_hi:.2f}", f"{int(r.studies)} stud", f"{int(r.participants)} participants",
              f"{r.certainty}-certainty"):
        assert s in text, s
assert "five RCTs" in text and "10,733" in text
for s in ("30.4% in the intervention group (259 incident cases among 853", "39.5% (287 incident cases among 726",
          "-9.1% [95% CI, -14.1% to -4.1%]", "24.9%, 20.6%, and 23.8% for control, test I, and II",
          "IRR], 0.84; 95% confidence interval [CI], 0.72-0.99", "IRR = 0.89; 95% CI, 0.79-0.99",
          "pooled risk ratio was 0.76 (95% CI 0.67-0.87)"):
    assert s in text, s

# Reproduce the Guangzhou percentages from the case counts.
g = tr.iloc[0]
p_out, p_ctl = g.cases_outdoor / g.n_outdoor * 100, g.cases_control / g.n_control * 100
assert round(p_out, 1) == g.incidence_outdoor_pct and round(p_ctl, 1) == g.incidence_control_pct
assert abs((p_out - p_ctl) - g.effect) < 0.1  # paper reports -9.1; raw counts give -9.17

y2 = co.set_index("years").loc[2]
print("Cochrane 2024 (5 RCTs, 10,733 children), incidence of myopia, outdoor vs control:")
for _, r in co.iterrows():
    print(f"  {int(r.years)} yr: {r.incidence_outdoor_pct}% vs {r.incidence_control_pct}%  "
          f"diff {r.incidence_outdoor_pct - r.incidence_control_pct:+.1f} pts  RR {r.rr:.2f} ({r.rr_lo:.2f}-{r.rr_hi:.2f})  "
          f"{int(r.studies)} studies, {int(r.participants)} participants, {r.certainty} certainty")
print(f"Guangzhou (He 2015): {g.cases_outdoor}/{g.n_outdoor} = {p_out:.1f}% vs {g.cases_control}/{g.n_control} = "
      f"{p_ctl:.1f}% over 3 years; difference {g.effect} points ({g.effect_lo} to {g.effect_hi}); reproduced")
for _, r in tr.iloc[1:].iterrows():
    print(f"Shanghai (He 2022) {r.arm}: {r.incidence_outdoor_pct}% vs {r.incidence_control_pct}% over 2 years; "
          f"adjusted IRR {r.effect:.2f} ({r.effect_lo:.2f}-{r.effect_hi:.2f})")
print("Cao 2020, 5 RCTs: pooled RR 0.76 (0.67-0.87)")
print(f"2-year relative reduction in Cochrane: {1 - y2.rr:.0%}")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 16.5)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Children's health · Myopia",
    "Getting children outdoors\nlowers their *risk of myopia*",
    f"In randomised trials that ran two years, {y2.incidence_outdoor_pct}% of children in programmes to get them outdoors became\n"
    f"short-sighted, against {y2.incidence_control_pct}% of those without (risk ratio {y2.rr:.2f}, 95% CI {y2.rr_lo:.2f}–{y2.rr_hi:.2f}).",
    size=48,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Cochrane review of\nfive randomised trials"),
    ("Sample", "10,733 schoolchildren,\nmostly aged 6 to 9, in Asia"),
    ("Source", "Kido et al.\nCochrane, 2024"),
    ("Consistent with", "Cao et al. 2020: RR 0.76 (0.67–0.87)\nIMI 2025 consensus"),
], widths=[0.23, 0.26, 0.17, 0.34])

# --- 01: pooled incidence by follow-up year -----------------------------------
top1 = y - 0.075
h1 = 0.21
ax = fig.add_axes([px.LEFT + 0.12, top1 - h1, px.WIDTH - 0.12 - 0.20, h1])
for i, r in co.iterrows():
    yy = len(co) - 1 - i
    ax.plot([r.incidence_outdoor_pct, r.incidence_control_pct], [yy, yy], color=TAUPE, lw=5, zorder=2,
            solid_capstyle="round")
    ax.scatter([r.incidence_control_pct], [yy], s=110, color=INK_2, edgecolor=PAPER, lw=1, zorder=3)
    ax.scatter([r.incidence_outdoor_pct], [yy], s=130, color=SIGNAL, edgecolor=PAPER, lw=1, zorder=4)
    ax.text(r.incidence_control_pct + 1.0, yy + 0.18, f"{r.incidence_control_pct}%", fontsize=10, family=px.MONO,
            color=INK_2, va="bottom", ha="left")
    ax.text(r.incidence_outdoor_pct - 1.0, yy + 0.18, f"{r.incidence_outdoor_pct}%", fontsize=10, family=px.MONO,
            color=SIGNAL, va="bottom", ha="right")
    ax.text(-0.02, yy, f"{int(r.years)} year{'s' if r.years > 1 else ''}", transform=ax.get_yaxis_transform(),
            ha="right", va="center", fontsize=12, color=INK)
    ax.text(1.03, yy + 0.12, f"RR {r.rr:.2f} ({r.rr_lo:.2f}–{r.rr_hi:.2f})", transform=ax.get_yaxis_transform(),
            fontsize=9.5, family=px.MONO, color=INK, va="bottom")
    ax.text(1.03, yy - 0.08, f"{int(r.studies)} trial{'s' if r.studies > 1 else ''} · {r.certainty} certainty",
            transform=ax.get_yaxis_transform(), fontsize=9, color=INK_3, va="top")
ax.text(co.incidence_outdoor_pct.iloc[-1], len(co) - 1 - 2 - 0.42, "Outdoor\nprogramme", color=SIGNAL,
        fontsize=10, ha="center", va="top", weight="semibold")
ax.text(co.incidence_control_pct.iloc[-1], len(co) - 1 - 2 - 0.42, "Without", color=INK_2, fontsize=10,
        ha="center", va="top", weight="semibold")
ax.set_xlim(0, 45)
ax.set_ylim(-0.95, len(co) - 0.5)
ax.set_yticks([])
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_xticklabels(["0%", "10%", "20%", "30%", "40%"])
ax.grid(axis="x")
ax.set_xlabel("Children who became short-sighted")
px.mono_ticks(ax)
px.panel(ax, 1, "Share of children who became short-sighted, pooled trials, by follow-up",
         "Cochrane review. Risk ratios with 95% CIs. The three-year row is the Guangzhou trial alone, cluster-adjusted.", pad=0.55)
ax.set_position([px.LEFT + 0.12, top1 - h1, px.WIDTH - 0.12 - 0.20, h1])

# --- 02: the two largest trials ----------------------------------------------
top2 = top1 - h1 - 0.12
h2 = 0.16
ax2 = fig.add_axes([px.LEFT + 0.30, top2 - h2, px.WIDTH - 0.30 - 0.20, h2])
rows = tr.reset_index(drop=True)
for i, r in rows.iterrows():
    yy = len(rows) - 1 - i
    ax2.plot([r.incidence_outdoor_pct, r.incidence_control_pct], [yy, yy], color=TAUPE, lw=4, zorder=2,
             solid_capstyle="round")
    ax2.scatter([r.incidence_control_pct], [yy], s=80, color=INK_2, edgecolor=PAPER, lw=1, zorder=3)
    ax2.scatter([r.incidence_outdoor_pct], [yy], s=95, color=SIGNAL, edgecolor=PAPER, lw=1, zorder=4)
    ax2.text(-0.03, yy + 0.12, f"{r.city}, {int(r.years)} years", transform=ax2.get_yaxis_transform(),
             ha="right", va="bottom", fontsize=11, color=INK)
    ax2.text(-0.03, yy - 0.06, f"{r.arm} · {r.trial}", transform=ax2.get_yaxis_transform(), ha="right", va="top",
             fontsize=9, color=INK_3)
    if r.effect_type.startswith("risk difference"):
        lab = f"{r.incidence_outdoor_pct}% vs {r.incidence_control_pct}%\ndiff {r.effect:+.1f} pts ({r.effect_lo:+.1f} to {r.effect_hi:+.1f})"
    else:
        lab = f"{r.incidence_outdoor_pct}% vs {r.incidence_control_pct}%\nadj. RR {r.effect:.2f} ({r.effect_lo:.2f}–{r.effect_hi:.2f})"
    ax2.text(1.03, yy, lab, transform=ax2.get_yaxis_transform(), fontsize=9, family=px.MONO, color=INK,
             va="center", linespacing=1.4)
ax2.set_xlim(0, 45)
ax2.set_ylim(-0.6, len(rows) - 0.4)
ax2.set_yticks([])
ax2.set_xticks([0, 10, 20, 30, 40])
ax2.set_xticklabels(["0%", "10%", "20%", "30%", "40%"])
ax2.grid(axis="x")
px.mono_ticks(ax2)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "The two largest trials, school by school randomisation",
         "Red: schools given extra outdoor time. Grey: control schools. Children without myopia at the start.",
         pad=0.55)

px.footer(fig,
          "DATA  Kido et al., Cochrane CD013549 (2024); He et al., JAMA 314:1142 (2015); He et al., Ophthalmology\n"
          "      129:1245 (2022). Values transcribed from the abstracts; Guangzhou percentages reproduced from case counts.\n"
          "NOTE  Myopia: spherical equivalent of -0.5 D or worse. Effects on myopia that has already begun are less certain.",
          NO)
px.save(fig, HERE)
print("saved")
