"""2026-11-25: The IQ gap is steepest at low lead levels.

Finding (dose-response): in a pooled analysis of 1,333 children from seven
cohorts (Lanphear et al., EHP 2005, corrected 2019), IQ fell with concurrent
blood lead along a log-linear curve: 6.7 points (95% CI 4.1-9.3) from 2.4 to
30 ug/dL, of which 3.8 came in the first step from 2.4 to 10 ug/dL, 1.8 from
10 to 20 and 1.1 from 20 to 30.

Data: the corrected estimates, transcribed from the 2019 erratum
(data/transcribed.csv). A single log-linear coefficient is recovered from the
headline estimate and must reproduce all three step estimates to one decimal.
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
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-25"

# ---------------------------------------------------------------- data ------
t = pd.read_csv(HERE / "data/transcribed.csv")
err = re.sub(r"\s+", " ", (HERE / "data/lanphear_2019_erratum_excerpt.txt").read_text())
abst = re.sub(r"\s+", " ", (HERE / "data/pubmed_abstracts.txt").read_text())
for c in [
    "we found a 6.7 IQ point decrement [95% confidence interval (CI), 4.1–9.3] associated with an increase in concurrent "
    "blood lead levels from 2.4 to 30 μ g / dL",
    "were 3.8 (95% CI, 2.3–5.3), 1.8 (95% CI, 1.1–2.6), and 1.1 (95% CI, 0.7–1.5), respectively",
    "We examined data collected from 1,333 children who participated in seven international population-based "
    "longitudinal cohort studies",
    "the data errors had only minor effects on the estimates",
]:
    assert c in err, c
assert "our reanalysis tended to support their conclusions" in abst
assert "the exposure-response is non-linear over the full range of BPb evaluated" in abst

head = t.iloc[0]
beta = head.iq_decrement / np.log(head.to_ugdl / head.from_ugdl)          # IQ points per natural-log unit
beta_lo = head.lo / np.log(head.to_ugdl / head.from_ugdl)
beta_hi = head.hi / np.log(head.to_ugdl / head.from_ugdl)
steps = t.iloc[1:].copy()
steps["model"] = beta * np.log(steps.to_ugdl / steps.from_ugdl)
assert (steps.model.round(1) == steps.iq_decrement).all(), steps          # reproduces the paper's step estimates
w = steps.to_ugdl - steps.from_ugdl
steps["per_ug"], steps["per_lo"], steps["per_hi"] = steps.iq_decrement / w, steps.lo / w, steps.hi / w
steps["per_model"] = steps.model / w

print(f"Lanphear 2005 (corrected 2019), 1,333 children, 7 cohorts: 2.4 -> 30 ug/dL, {head.iq_decrement} IQ points "
      f"({head.lo}-{head.hi}); log-linear coefficient {beta:.2f} per ln unit ({beta_lo:.2f}-{beta_hi:.2f})")
for _, r in steps.iterrows():
    print(f"  {r.from_ugdl:g} -> {r.to_ugdl:g} ug/dL: {r.iq_decrement} ({r.lo}-{r.hi}); model {r.model:.2f}; "
          f"{r.per_ug:.2f} ({r.per_lo:.2f}-{r.per_hi:.2f}) IQ points per ug/dL")
print(f"share of the 2.4-30 loss in the first step (2.4-10): {steps.iloc[0].iq_decrement / head.iq_decrement:.0%}")
ratio = steps.iloc[0].per_ug / steps.iloc[2].per_ug
ratio_model = steps.iloc[0].per_model / steps.iloc[2].per_model
assert ratio > 4 and ratio_model > 4
print(f"per-ug difference, first step vs last step: {ratio:.1f}x from rounded estimates, {ratio_model:.1f}x in the model (more than four times)")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 16.0)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Environment · Lead and children",
    "The IQ gap is steepest\nat *low lead levels*",
    f"Across seven cohorts, IQ was {head.iq_decrement} points lower at a blood lead of 30 than at 2.4 micrograms per decilitre.\n"
    f"More than half of that gap, {steps.iloc[0].iq_decrement} points, came between 2.4 and 10.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Pooled analysis of seven\ncohorts, IQ at about 5–10"),
    ("Sample", "1,333 children in the US, Mexico,\nAustralia and Yugoslavia"),
    ("Source", "Lanphear et al. EHP 2005\n(corrected 2019)"),
    ("Consistent with", "US EPA lead assessment 2024\nNTP 2012 · Crump 2013 (same data)"),
], widths=[0.25, 0.27, 0.22, 0.26])

# --- 01: the curve -------------------------------------------------------------
top1 = y - 0.07
h1 = 0.27
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.12, h1])
x = np.linspace(2.4, 30, 300)
ax.fill_between(x, -beta_lo * np.log(x / 2.4), -beta_hi * np.log(x / 2.4), color=PAPER_2, lw=0, zorder=1)
ax.plot(x, -beta * np.log(x / 2.4), color=SIGNAL, lw=2.2, zorder=3)
for b0, b1 in [(2.4, 10), (10, 20), (20, 30)]:
    ax.axvline(b1, color=INK_3, lw=0.6, ls=(0, (1, 2)), zorder=1)
for _, r in steps.iterrows():
    y0, y1 = -beta * np.log(r.from_ugdl / 2.4), -beta * np.log(r.to_ugdl / 2.4)
    ax.annotate("", xy=(r.to_ugdl, y1), xytext=(r.to_ugdl, y0),
                arrowprops=dict(arrowstyle="-", color=INK, lw=1.2))
    ax.plot([r.from_ugdl, r.to_ugdl], [y0, y0], color=INK, lw=0.7, ls=(0, (2, 2)))
    ax.text(r.to_ugdl + 0.4, (y0 + y1) / 2, f"−{r.iq_decrement}", fontsize=13, color=INK, va="center",
            weight="semibold")
ax.scatter([30], [-head.iq_decrement], s=50, color=SIGNAL, edgecolor=PAPER, zorder=4)
ax.text(29.6, -head.iq_decrement - 0.55, f"−{head.iq_decrement} IQ points at 30\n(95% CI {head.lo}–{head.hi})",
        ha="right", va="top", fontsize=10, color=SIGNAL)
ax.set_xlim(0, 32)
ax.set_ylim(-10.5, 0.8)
ax.set_xticks([2.4, 10, 20, 30])
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_yticks([0, -2, -4, -6, -8, -10])
ax.axhline(0, color=INK, lw=0.6)
ax.grid(axis="y")
ax.set_xlabel("Concurrent blood lead (micrograms per decilitre)")
ax.set_ylabel("IQ points, relative to 2.4")
px.mono_ticks(ax)
px.panel(ax, 1, "Change in full-scale IQ with blood lead, log-linear model",
         "2.4 is the 5th percentile of blood lead. Band: 95% CI, from the paper's interval for 2.4 to 30. Step figures: the paper's estimates.", pad=0.55)

# --- 02: per microgram ----------------------------------------------------------
top2 = top1 - h1 - 0.12
h2 = 0.12
ax2 = fig.add_axes([px.LEFT + 0.22, top2 - h2, px.WIDTH - 0.22 - 0.2, h2])
for i, (_, r) in enumerate(steps.iterrows()):
    yy = len(steps) - 1 - i
    ax2.barh(yy, r.per_ug, height=0.55, color=SIGNAL if i == 0 else TAUPE, zorder=2)
    ax2.plot([r.per_lo, r.per_hi], [yy, yy], color=INK, lw=1.1, zorder=3)
    for xv in (r.per_lo, r.per_hi):
        ax2.plot([xv, xv], [yy - 0.08, yy + 0.08], color=INK, lw=1.1, zorder=3)
    ax2.text(r.per_hi + 0.012, yy, f"{r.per_ug:.2f}  ({r.per_lo:.2f}–{r.per_hi:.2f})", fontsize=11, family=px.MONO, va="center",
             color=SIGNAL if i == 0 else INK_2)
    ax2.text(-0.02, yy, f"{r.from_ugdl:g} to {r.to_ugdl:g}", transform=ax2.get_yaxis_transform(), ha="right",
             va="center", fontsize=11, color=INK)
ax2.set_xlim(0, 0.9)
ax2.set_ylim(-0.55, len(steps) - 0.45)
ax2.set_yticks([])
ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
ax2.grid(axis="x")
ax2.set_xlabel("IQ points lower per microgram per decilitre, 95% CI (derived: step estimate ÷ width)")
px.mono_ticks(ax2)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "IQ difference per microgram, by blood lead range",
         "In the paper's log-linear model, the gap per microgram is more than four times larger at 2.4 to 10 than at 20 to 30.",
         pad=0.55)

px.footer(fig,
          "DATA  Lanphear et al., Environ Health Perspect 113:894 (2005), corrected abstract in the 2019 erratum (127:099001).\n"
          "      Step estimates checked against one log-linear slope (no raw data reanalysed). Per-microgram values derived here.\n"
          "NOTE  Observational cohorts adjusted for confounders. Few children had blood lead below 7.5, so the low end is least certain.",
          NO)
px.save(fig, HERE)
print("saved")
