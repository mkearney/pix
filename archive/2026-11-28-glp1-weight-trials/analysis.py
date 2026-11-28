"""2026-11-28: Obesity drug users lost 15% to 21% in trials.

Finding (effect): in large placebo-controlled trials in adults with obesity
and without diabetes, weekly semaglutide 2.4 mg cut body weight by 14.9% over
68 weeks against 2.4% with placebo (STEP 1), and weekly tirzepatide by 15.0% to
20.9% over 72 weeks, depending on dose, against 3.1% (SURMOUNT-1). In a
withdrawal trial (STEP 4), people switched to placebo regained weight.

Data: values transcribed from the trial abstracts (data/transcribed.csv), each
asserted against the saved abstract text.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-28"

# ---------------------------------------------------------------- data ------
t = pd.read_csv(HERE / "data/transcribed.csv")
txt = re.sub(r"\s+", " ", (HERE / "data/pubmed_abstracts.txt").read_text())
for c in [
    "-14.9% in the semaglutide group as compared with -2.4% with placebo, for an estimated treatment difference of "
    "-12.4 percentage points (95% confidence interval [CI], -13.4 to -11.5",
    "we enrolled 1961 adults",
    "-15.0% (95% confidence interval [CI], -15.9 to -14.2) with 5-mg weekly doses of tirzepatide, -19.5% (95% CI, -20.4 "
    "to -18.5) with 10-mg doses, and -20.9% (95% CI, -21.8 to -19.9) with 15-mg doses and -3.1% (95% CI, -4.3 to -1.9) "
    "with placebo",
    "we assigned 2539 adults",
    "-16.0% for semaglutide vs -5.7% for placebo (difference, -10.3 percentage points [95% CI, -12.0 to -8.6]",
    "mean body weight change from week 20 to week 68 was -7.9% vs +6.9% with the switch to placebo (difference, -14.8 "
    "[95% CI, -16.0 to -13.5] percentage points",
    "more than 10% for semaglutide and tirzepatide",
    "WMD -12.1%, 95% CI -13.5 to -10.7",
]:
    assert c in txt, c


def g(trial, arm, drug=None):
    x = t[(t.trial == trial) & (t.arm == arm)]
    if drug:
        x = x[x.drug == drug]
    assert len(x) == 1, (trial, arm, drug)
    return x.iloc[0]


s1d, s1p, s1x = g("STEP 1", "drug"), g("STEP 1", "placebo"), g("STEP 1", "difference")
s3d, s3p, s3x = g("STEP 3", "drug"), g("STEP 3", "placebo"), g("STEP 3", "difference")
sm = {mg: g("SURMOUNT-1", "drug", f"tirzepatide {mg} mg") for mg in (5, 10, 15)}
smp = g("SURMOUNT-1", "placebo")
s4c, s4p, s4x = g("STEP 4", "continued"), g("STEP 4", "switched to placebo"), g("STEP 4", "difference")
assert round(s1d.value - s1p.value, 1) in (-12.5, -12.4)    # reported difference is model-estimated

print(f"STEP 1 (1,961 adults, 68 wk): semaglutide {s1d.value}% vs placebo {s1p.value}%; difference {s1x.value} "
      f"({s1x.lo} to {s1x.hi}) points")
print(f"STEP 3 (611 adults, 68 wk, with intensive behavioural therapy): {s3d.value}% vs {s3p.value}%; difference "
      f"{s3x.value} ({s3x.lo} to {s3x.hi})")
print("SURMOUNT-1 (2,539 adults, 72 wk): " + "; ".join(f"tirzepatide {mg} mg {r.value}% ({r.lo} to {r.hi})"
                                                       for mg, r in sm.items())
      + f"; placebo {smp.value}% ({smp.lo} to {smp.hi}); differences "
      + ", ".join(f"{r.value - smp.value:.1f}" for r in sm.values()))
print(f"STEP 4 (803 after 20-wk run-in, weeks 20-68): continued {s4c.value}% vs switched to placebo +{s4p.value}%; "
      f"difference {s4x.value} ({s4x.lo} to {s4x.hi})")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 16.2)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Health · Obesity drugs",
    "Obesity drug users lost\n*15% to 21%* in trials",
    f"Over 68 to 72 weeks, people on weekly semaglutide lost {abs(s1d.value)}% of their weight, against {abs(s1p.value)}% on placebo.\n"
    f"On tirzepatide they lost {abs(sm[5].value)}% to {abs(sm[15].value)}%, depending on dose, against {abs(smp.value)}%.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Double-blind randomised\nplacebo-controlled trials"),
    ("Sample", "Adults with obesity or overweight\nplus a related condition, no diabetes"),
    ("Source", "STEP 1, 3 and 4 (2021)\nSURMOUNT-1 (2022)"),
    ("Consistent with", "Meta-analyses: Nat Med 2025\n(56 trials), Am J Cardiol 2024"),
], widths=[0.25, 0.28, 0.21, 0.26])

# --- 01: drug vs placebo dumbbells -------------------------------------------------
top1 = y - 0.07
h1 = 0.24
ax = fig.add_axes([px.LEFT + 0.25, top1 - h1, px.WIDTH - 0.25 - 0.27, h1])
rows = [
    ("STEP 1", "semaglutide, 68 weeks", s1d, s1p, None),
    ("STEP 3", "semaglutide + intensive\nlifestyle support, 68 weeks", s3d, s3p, None),
    ("SURMOUNT-1", "tirzepatide 5 mg, 72 weeks", sm[5], smp, (sm[5].lo, sm[5].hi)),
    ("SURMOUNT-1", "tirzepatide 10 mg, 72 weeks", sm[10], smp, (sm[10].lo, sm[10].hi)),
    ("SURMOUNT-1", "tirzepatide 15 mg, 72 weeks", sm[15], smp, (sm[15].lo, sm[15].hi)),
]
for i, (trial, lab, dr, pl, ci) in enumerate(rows):
    yy = len(rows) - 1 - i
    ax.plot([pl.value, dr.value], [yy, yy], color=TAUPE, lw=2.5, zorder=2, solid_capstyle="butt")
    if not pd.isna(pl.lo):
        ax.plot([pl.lo, pl.hi], [yy - 0.14, yy - 0.14], color=INK_2, lw=1.4, zorder=3)
    ax.scatter([pl.value], [yy], s=60, color=PAPER, edgecolor=INK_2, lw=1.2, zorder=4)
    if ci:
        ax.plot(ci, [yy - 0.14, yy - 0.14], color=SIGNAL, lw=1.8, zorder=3)
    ax.scatter([dr.value], [yy], s=70, color=SIGNAL, edgecolor=PAPER, lw=0.8, zorder=4)
    if trial == "STEP 1":
        dtxt = f"{s1x.value} ({s1x.lo} to {s1x.hi})"
    elif trial == "STEP 3":
        dtxt = f"{s3x.value} ({s3x.lo} to {s3x.hi})"
    else:
        dtxt = f"{dr.value - pl.value:.1f} (derived)"
    ax.text(1.03, yy, dtxt, transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=9.5,
            family=px.MONO, color=INK)
    lx = min(dr.value, ci[0] if ci else dr.value) - 0.5
    ax.text(lx, yy, f"{dr.value:.1f}%", ha="right", va="center", fontsize=11, family=px.MONO, color=SIGNAL)
    ax.text(pl.value, yy + 0.2, f"{pl.value:.1f}%", ha="center", va="bottom", fontsize=9, family=px.MONO, color=INK_2)
    ax.text(-0.03, yy + 0.12, trial, transform=ax.get_yaxis_transform(), ha="right", va="bottom", fontsize=11, color=INK)
    ax.text(-0.03, yy + 0.02, lab, transform=ax.get_yaxis_transform(), ha="right", va="top", fontsize=8.5,
            color=INK_3, linespacing=1.2)
ax.text(s1d.value, len(rows) - 0.3, "Drug", ha="center", va="bottom", fontsize=9.5, color=SIGNAL, weight="semibold")
ax.text(s1p.value, len(rows) - 0.3, "Placebo", ha="center", va="bottom", fontsize=9.5, color=INK_2)
ax.text(1.03, len(rows) - 0.3, "Difference, points", transform=ax.get_yaxis_transform(), ha="left", va="bottom",
        fontsize=9.5, color=INK)
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlim(-27, 2)
ax.set_ylim(-0.6, len(rows) + 0.05)
ax.set_yticks([])
ax.set_xticks([-25, -20, -15, -10, -5, 0])
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.grid(axis="x")
ax.set_xlabel("Mean change in body weight from the start of the trial")
px.mono_ticks(ax)
hdr = fig.add_axes([px.LEFT, top1 - h1, 0.01, h1])
hdr.axis("off")
px.panel(hdr, 1, "Weight change by the end of each trial, drug against placebo",
         "Separate trials, not head-to-head. All arms had lifestyle advice. Whiskers: 95% CIs reported for the arm.",
         pad=0.55)

# --- 02: STEP 4 withdrawal ---------------------------------------------------------
top2 = top1 - h1 - 0.12
h2 = 0.12
ax2 = fig.add_axes([px.LEFT + 0.25, top2 - h2, px.WIDTH - 0.25 - 0.17, h2])
for yy, r, lab, col in ((1, s4c, "Stayed on semaglutide", SIGNAL), (0, s4p, "Switched to placebo", INDIGO)):
    ax2.barh(yy, r.value, height=0.55, color=col, zorder=2)
    ax2.text(r.value + (0.4 if r.value > 0 else -0.4), yy, f"{r.value:+.1f}%", ha="left" if r.value > 0 else "right",
             va="center", fontsize=12, family=px.MONO, color=col)
    ax2.text(-0.03, yy, lab, transform=ax2.get_yaxis_transform(), ha="right", va="center", fontsize=11, color=INK)
ax2.axvline(0, color=INK, lw=0.8)
ax2.set_xlim(-12, 12)
ax2.set_ylim(-0.6, 1.6)
ax2.set_yticks([])
ax2.set_xticks([-10, -5, 0, 5, 10])
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}%" if v else "0%"))
ax2.grid(axis="x")
ax2.set_xlabel(f"Change in body weight from week 20 to week 68 (difference {s4x.value}, 95% CI {s4x.lo} to {s4x.hi})")
px.mono_ticks(ax2)
hdr2 = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr2.axis("off")
px.panel(hdr2, 2, "After 20 weeks on semaglutide, a third were switched to placebo (STEP 4)",
         "803 adults who had lost 10.6% on average in the first 20 weeks; randomised 2:1. Changes are % of week-20 weight.", pad=0.55)

px.footer(fig,
          "DATA  Wilding et al., NEJM 384:989 (2021); Wadden et al., JAMA 325:1403 (2021); Jastreboff et al., NEJM 387:205 (2022);\n"
          "      Rubino et al., JAMA 325:1414 (2021). Values transcribed from the abstracts. Trials funded by the manufacturers.\n"
          "NOTE  Trials excluded people with diabetes. Gastrointestinal side effects were common, mostly mild to moderate.",
          NO)
px.save(fig, HERE)
print("saved")
