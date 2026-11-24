"""2026-11-24: Youngest children in class get more ADHD diagnoses.

Finding (effect, natural experiment): within a school year, the youngest
children are diagnosed with and treated for ADHD more often than the oldest.
In US states with a September 1 kindergarten cutoff, August-born children had
85.1 ADHD diagnoses per 10,000 against 63.6 for September-born children
(Layton et al., NEJM 2018); states without that cutoff showed no clear gap.
National registries in Canada, Norway, Finland and Iceland show the same,
Denmark (where many young children start school a year late) barely does, and
a 2025 meta-analysis pools a relative risk of 1.28 for ADHD medication.

Data: values transcribed from the papers' text (data/transcribed.csv), each
asserted against the saved abstracts and full-text excerpt.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-24"

# ---------------------------------------------------------------- data ------
t = pd.read_csv(HERE / "data/transcribed.csv")
raw = pd.read_csv(HERE / "data/transcribed.csv", dtype=str)  # keep published precision for labels
txt = re.sub(r"\s+", " ", (HERE / "data/pubmed_abstracts.txt").read_text()
             + (HERE / "data/frisira_2025_results_excerpt.txt").read_text())

checks = [
    "85.1 per 10,000 children (309 cases among 36,319 children; 95% confidence interval [CI], 75.6 to 94.2)",
    "63.6 per 10,000 children (225 cases among 35,353 children; 95% CI, 55.4 to 71.9)",
    "an absolute difference of 21.5 per 10,000 children (95% CI, 8.8 to 34.0)",
    "states without the September 1 cutoff was 8.9 per 10,000 children (95% CI, -14.9 to 20.8)",
    "52.9 per 10,000 children (192 of 36,319 children; 95% CI, 45.4 to 60.3)",
    "40.4 per 10,000 children (143 of 35,353 children; 95% CI, 33.8 to 47.1)",
    "407,846 children",
    "(relative risk [RR] 1.30, 95% confidence interval [CI] 1.23-1.37)",
    "(RR 1.70, 95% CI 1.53-1.88)",
    "was 1.4 (95% confidence interval: 1.4-1.5) for boys and 1.8 (1.7-2.0) for girls",
    "for boys the incidence ratio was 1·26 (95% CI 1·18-1·35; p<0·0001) and for girls it was 1·31 (1·12-1·54",
    "50% more likely (1.5; 95% CI 1.3-1.8)",
    "The average PPR over the study period was 1.08 (95% CI, 1.04-1.12)",
    "40% of children born October-December had entered school a year after",
    "1.28 (95% CI 1.21, 1.36)",
    "Thirty-two studies were included",
    "A total of 17 of the 19 studies found that the youngest children",
]
for c in checks:
    assert c in txt, c

lay = t[t.study == "Layton 2018"].reset_index(drop=True)
dx_aug, dx_sep = lay.loc[0], lay.loc[1]
tx_aug, tx_sep = lay.loc[4], lay.loc[5]
ratio_dx = dx_aug.value / dx_sep.value
assert round(dx_aug.value - dx_sep.value, 1) == lay.loc[2, "value"] == 21.5

print(f"Layton 2018, 407,846 US children born 2007-09; states with a Sept 1 cutoff:")
print(f"  ADHD diagnosis per 10,000: August-born {dx_aug.value} ({dx_aug.lo}-{dx_aug.hi}), "
      f"September-born {dx_sep.value} ({dx_sep.lo}-{dx_sep.hi}); difference 21.5 (8.8-34.0); "
      f"ratio {ratio_dx:.2f} ({ratio_dx - 1:.0%} higher)")
print(f"  ADHD treatment per 10,000: August {tx_aug.value} ({tx_aug.lo}-{tx_aug.hi}), "
      f"September {tx_sep.value} ({tx_sep.lo}-{tx_sep.hi})")
print("  states without a Sept 1 cutoff: difference 8.9 (-14.9 to 20.8)")
fp = t[t.study != "Layton 2018"]
for _, r in fp.iterrows():
    print(f"{r.study}, {r.place}, {r.group}, {r.outcome} ({r.comparison}): {r.value} ({r.lo}-{r.hi})")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 18.0)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Children · School age and ADHD",
    "Youngest children in class\nget more *ADHD diagnoses*",
    f"In US states where children must turn 5 by September 1 to start school, August-born children, the youngest in\n"
    f"their year, were diagnosed with ADHD {ratio_dx - 1:.0%} more often than September-born children, the oldest.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Natural experiment: birthdays\neither side of a school cutoff"),
    ("Sample", "407,846 US children,\ninsurance claims 2007–15"),
    ("Source", "Layton et al.\nNEJM, 2018"),
    ("Consistent with", "Frisira et al. 2025 (review, 32 studies)\nWhitely et al. 2019 (19 studies)"),
], widths=[0.29, 0.25, 0.16, 0.30])

# --- 01: August vs September, US -----------------------------------------------
top1 = y - 0.07
h1 = 0.15
ax = fig.add_axes([px.LEFT + 0.2, top1 - h1, px.WIDTH - 0.2 - 0.16, h1])
rows = [("Diagnosed", dx_aug, dx_sep, 3.0), ("Treated", tx_aug, tx_sep, 1.0)]
for lab, a, s, yy in rows:
    for r, dy, col, name in ((a, 0.32, SIGNAL, "Born August (youngest)"), (s, -0.32, TAUPE, "Born September (oldest)")):
        ax.plot([r.lo, r.hi], [yy + dy] * 2, color=col, lw=2, zorder=3, solid_capstyle="round")
        ax.scatter([r.value], [yy + dy], s=80, color=col, edgecolor=PAPER, lw=1, zorder=4)
        ax.text(r.hi + 1.5, yy + dy, f"{r.value:.1f}  ({r.lo:.1f}–{r.hi:.1f})", fontsize=9.5, family=px.MONO,
                color=col if col == SIGNAL else INK_2, va="center")
        ax.text(-0.02, yy + dy, name, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=10,
                color=col if col == SIGNAL else INK_2)
    ax.text(-0.02, yy + 0.85, lab, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=11.5,
            color=INK, weight="semibold")
ax.set_xlim(0, 110)
ax.set_ylim(0.2, 4.0)
ax.set_yticks([])
ax.set_xticks([0, 25, 50, 75, 100])
ax.grid(axis="x")
ax.set_xlabel("Children with ADHD claims per 10,000 (95% CI)")
px.mono_ticks(ax)
hdr = fig.add_axes([px.LEFT, top1 - h1, 0.01, h1])
hdr.axis("off")
px.panel(hdr, 1, "US children born 2007–09, followed to 2015, in states with a September 1 cutoff",
         "Without that cutoff, the August-September gap in diagnosis was 8.9 per 10,000 (95% CI −14.9 to 20.8), not significant.",
         pad=0.55)

# --- 02: forest plot across countries ------------------------------------------
top2 = top1 - h1 - 0.10
h2 = 0.28
ax2 = fig.add_axes([px.LEFT + 0.33, top2 - h2, px.WIDTH - 0.33 - 0.2, h2])
labels = {
    "Morrow 2012": "Canada (BC) · diagnosis\nDec vs Jan born",
    "Karlstad 2017": "Norway · medication\nOct–Dec vs Jan–Mar",
    "Sayal 2017": "Finland · diagnosis\nSep–Dec vs Jan–Apr",
    "Zoega 2012": "Iceland · stimulants\nyoungest vs oldest third",
    "Pottegard 2014": "Denmark · medication\nOct–Dec vs Jan–Mar",
    "Frisira 2025": "Pooled · medication\nmeta-analysis, 2025",
}
order = ["Morrow 2012", "Karlstad 2017", "Sayal 2017", "Zoega 2012", "Pottegard 2014", "Frisira 2025"]
ypos, yy = [], 0.0
for st in order:
    sub = fp[fp.study == st]
    first = True
    for _, r in sub.iterrows():
        pooled = st == "Frisira 2025"
        col = INK if pooled else (TAUPE if st == "Pottegard 2014" else SIGNAL)
        ax2.plot([r.lo, r.hi], [yy, yy], color=col, lw=2, zorder=3, solid_capstyle="round")
        ax2.scatter([r.value], [yy], s=90 if pooled else 55, marker="D" if pooled else "s", color=col,
                    edgecolor=PAPER, lw=0.8, zorder=4)
        g = "" if r.group == "all" else f"{r.group}  "
        rr = raw.loc[r.name]
        ax2.text(2.35, yy, f"{g}{rr.value} ({rr.lo}–{rr.hi})", fontsize=9.5, family=px.MONO, va="center",
                 color=INK if pooled else INK_2)
        ypos.append(yy)
        if first:
            ax2.text(-0.03, yy - (0.25 if len(sub) > 1 else 0), labels[st], transform=ax2.get_yaxis_transform(),
                     ha="right", va="center", fontsize=10, color=INK, linespacing=1.35)
            first = False
        yy -= 0.45
    yy -= 0.4
ax2.axvline(1, color=INK, lw=0.8, zorder=1)
ax2.set_xscale("log")
ax2.set_xlim(0.9, 2.3)
ax2.xaxis.set_major_locator(FixedLocator([1, 1.25, 1.5, 2]))
ax2.xaxis.set_minor_locator(NullLocator())
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax2.set_ylim(min(ypos) - 0.5, 0.5)
ax2.set_yticks([])
ax2.grid(axis="x")
ax2.set_xlabel("Youngest vs oldest in the school year: ratio of ADHD diagnosis or medication (95% CI, log scale)")
dk = ypos[order.index("Pottegard 2014") + 3]
ax2.annotate("40% of the youngest Danish children\nstarted school a year late", xy=(1.12, dk), xytext=(1.3, dk + 0.05),
             fontsize=9, color=INK_2, va="center", arrowprops=dict(arrowstyle="-", color=INK_3, lw=0.7))
px.mono_ticks(ax2)
hdr2 = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr2.axis("off")
px.panel(hdr2, 2, "A similar gap in other countries' health records",
         "Each country uses its own school cutoff. Ratios of risk, hazard, incidence or prevalence.", pad=0.55)

px.footer(fig,
          "DATA  Layton et al., NEJM 379:2122 (2018); Morrow 2012; Karlstad 2017; Sayal 2017; Zoëga 2012; Pottegård 2014;\n"
          "      Frisira et al., Eur Child Adolesc Psychiatry 34:381 (2025). Values transcribed from the papers' text.\n"
          "NOTE  US diagnosis = ADHD billing code or stimulant prescription in insurance claims. Shows who gets diagnosed\n"
          "      and treated, not whether the diagnoses are right.",
          NO)
px.save(fig, HERE)
print("saved")
