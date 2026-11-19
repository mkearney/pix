"""2026-11-19: A pedestrian's risk of death climbs steeply with speed.

Finding (dose-response): the risk that a struck pedestrian dies rises along a
steep S-curve with the car's impact speed. Tefft (2013) gives the speeds at
which the average risk reaches 10%, 25%, 50%, 75% and 90% for US pedestrians;
studies from Germany and Britain find the same steepness.

No individual-level data were released, so the published values are
transcribed (see data/SOURCES.md). This script checks the transcription
against the saved PubMed abstract, fits a logistic curve through each set of
five published points for drawing, and prints every number the post uses.
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
DATE = "2026-11-19"
KMH = 1.609344

# ---------------------------------------------------------------- data ------
th = pd.read_csv(HERE / "data/tefft2013_thresholds.csv")
st = pd.read_csv(HERE / "data/tefft2011_table4_studies.csv")
abstract = (HERE / "data/pubmed_abstracts.txt").read_text()

# Transcription check: every threshold must appear in the Tefft 2013 abstract text.
tefft = abstract.split("\n\n\n")[0]
for _, r in th.iterrows():
    assert re.search(rf"{r.impact_speed_mph:.1f}\s*m", tefft.replace("\n", " ")), r.impact_speed_mph
AGE_SHIFT = 11.8
assert "11.8mph faster" in tefft.replace("\n", " ")


def logit(p):
    return np.log(p / (1 - p))


def fit(speeds, risks):
    """Least-squares logistic through the published points: logit(p) = a + b * mph."""
    b, a = np.polyfit(speeds, logit(np.asarray(risks)), 1)
    return a, b


death = th[th.outcome == "death"]
sev = th[th.outcome == "severe_injury"]
aD, bD = fit(death.impact_speed_mph, death.risk)
aS, bS = fit(sev.impact_speed_mph, sev.risk)
resid = death.risk - 1 / (1 + np.exp(-(aD + bD * death.impact_speed_mph)))
assert resid.abs().max() < 0.03, resid  # the S-curve passes within 3 points of every published value

v = np.linspace(0, 70, 141)
curves = pd.DataFrame({"mph": v, "death": 1 / (1 + np.exp(-(aD + bD * v))),
                       "severe_injury": 1 / (1 + np.exp(-(aS + bS * v)))})
curves.round(4).to_csv(HERE / "data/fitted_curves.csv", index=False)

d10, d50, d90 = (death.set_index("risk").impact_speed_mph[k] for k in (0.10, 0.50, 0.90))
s50 = sev.set_index("risk").impact_speed_mph[0.50]
or_lo, or_hi = st.or_per_5mph.min(), st.or_per_5mph.max()
fit_or5 = np.exp(5 * bD)

print("Tefft 2013, risk of death by impact speed:")
for _, r in death.iterrows():
    print(f"  {r.risk:.0%} at {r.impact_speed_mph:.1f} mph ({r.impact_speed_mph * KMH:.0f} km/h)")
print("Tefft 2013, risk of severe injury or death:")
for _, r in sev.iterrows():
    print(f"  {r.risk:.0%} at {r.impact_speed_mph:.1f} mph ({r.impact_speed_mph * KMH:.0f} km/h)")
print(f"10% to 90% risk of death spans {d90 - d10:.1f} mph ({(d90 - d10) * KMH:.0f} km/h)")
print(f"70-year-old's risk = 30-year-old's at {AGE_SHIFT} mph ({AGE_SHIFT * KMH:.0f} km/h) faster")
print(f"logistic fit through the death thresholds: max residual {resid.abs().max() * 100:.1f} points; "
      f"implied odds ratio per 5 mph {fit_or5:.2f}")
print("Odds ratio of death per 5 mph, four studies (Tefft 2011, Table 4):")
for _, r in st.iterrows():
    print(f"  {r.study:<20} {r.country:<15} {r.years:<24} {r.or_per_5mph:.2f} ({r.or_lo:.2f}-{r.or_hi:.2f})")
print(f"range {or_lo:.2f} to {or_hi:.2f}; heterogeneity test p = 0.29 (reported, Tefft 2011 p. 13)")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17.5)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Safety · Speed and pedestrians",
    "A pedestrian's risk of death\n*climbs steeply* with speed",
    f"For a pedestrian struck by a car or light truck in the US, the risk of death reaches 10% at {d10:.1f} mph\n"
    f"({d10 * KMH:.0f} km/h), 50% at {d50:.1f} mph ({d50 * KMH:.0f} km/h) and 90% at {d90:.1f} mph ({d90 * KMH:.0f} km/h).",
    size=46,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "In-depth crash investigations,\nweighted to national injury data"),
    ("Sample", "Pedestrians aged 15+ struck by\ncars and light trucks, US, 1994–98"),
    ("Source", "Tefft\nAccid Anal Prev, 2013"),
    ("Consistent with", "Rosén & Sander 2009 (Germany)\nRichards 2010, Davis 2001 (UK)"),
], widths=[0.27, 0.29, 0.16, 0.28])

# --- 01: the S-curves ---------------------------------------------------------
top1 = y - 0.075
h1 = 0.31
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.08, h1])
ax.axhspan(0.5, 0.5, color=INK_3)
ax.plot(curves.mph, curves.severe_injury, color=TAUPE, lw=2.0, zorder=3)
ax.plot(curves.mph, curves.death, color=SIGNAL, lw=2.6, zorder=4)
ax.scatter(sev.impact_speed_mph, sev.risk, s=30, color=TAUPE, edgecolor=PAPER, lw=0.8, zorder=5)
ax.scatter(death.impact_speed_mph, death.risk, s=46, color=SIGNAL, edgecolor=PAPER, lw=0.9, zorder=6)
for _, r in death.iterrows():
    ax.text(r.impact_speed_mph + 1.0, r.risk - 0.035, f"{r.impact_speed_mph:.1f} mph", fontsize=9.5,
            family=px.MONO, color=INK, va="top", ha="left")
ax.text(s50 - 1.5, 0.62, "Severe injury\nor death", color=INK_2, fontsize=10.5, ha="right", va="bottom")
ax.text(d50 + 3.5, 0.40, "Death", color=SIGNAL, fontsize=12, weight="semibold", ha="left", va="top")
ax.set_xlim(0, 70)
ax.set_ylim(0, 1.0)
ax.set_xticks(range(0, 71, 10))
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Impact speed (mph)")
ax.grid(axis="y")
for mph in range(0, 71, 10):
    ax.text(mph, 1.025, f"{mph * KMH:.0f}", ha="center", va="bottom", fontsize=8.5, family=px.MONO,
            color=INK_3, transform=ax.transData)
ax.text(71.5, 1.025, "km/h", ha="left", va="bottom", fontsize=8.5, family=px.MONO, color=INK_3)
px.mono_ticks(ax)
px.panel(ax, 1, "Average risk for a struck pedestrian, by the car's speed at impact",
         "Dots: the published speeds at 10%, 25%, 50%, 75% and 90% risk. Lines: approximate logistic fits through them.",
         pad=0.55)

# --- 02: same steepness in four studies ---------------------------------------
top2 = top1 - h1 - 0.12
h2 = 0.12
ax2 = fig.add_axes([px.LEFT + 0.30, top2 - h2, px.WIDTH - 0.30 - 0.10, h2])
rows = st.iloc[::-1].reset_index(drop=True)
for i, r in rows.iterrows():
    us = r.country == "United States"
    col = SIGNAL if us else INK_2
    ax2.plot([r.or_lo, r.or_hi], [i, i], color=col, lw=1.6, zorder=3, solid_capstyle="round")
    ax2.scatter([r.or_per_5mph], [i], s=60 if us else 44, marker="s", color=col, edgecolor=PAPER, lw=0.8, zorder=4)
    ax2.text(r.or_hi + 0.06, i, f"{r.or_per_5mph:.2f}  ({r.or_lo:.2f}–{r.or_hi:.2f})", fontsize=9.5,
             family=px.MONO, color=col, va="center")
    ax2.text(-0.03, i, f"{r.country}, {r.years.replace(' and ', ', ')}", transform=ax2.get_yaxis_transform(),
             ha="right", va="center", fontsize=10.5, color=INK, weight="semibold" if us else "normal")
    ax2.text(-0.03, i - 0.32, r.study, transform=ax2.get_yaxis_transform(), ha="right", va="center",
             fontsize=8.5, color=INK_3)
ax2.axvline(1, color=INK, lw=0.8, zorder=2)
ax2.set_xlim(0.8, 4.6)
ax2.set_ylim(-0.6, len(rows) - 0.4)
ax2.set_yticks([])
ax2.set_xticks([1, 2, 3, 4])
ax2.set_xticklabels(["1x", "2x", "3x", "4x"])
ax2.grid(axis="x")
ax2.set_xlabel("Odds of death for each extra 5 mph (95% CI)")
px.mono_ticks(ax2)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "The curve is about as steep in four studies' data",
         "Each extra 5 mph multiplies the odds of death by about 2 to 2.8. No evidence the studies differ (p = 0.29).", pad=0.55)

px.footer(fig,
          "DATA  Thresholds: Tefft, Accid Anal Prev 50:871 (2013), abstract. Odds ratios: Tefft, AAA Foundation report\n"
          "      (2011), Table 4, unadjusted models. All values transcribed from text and tables; no figure was read.\n"
          "NOTE  Impact speed, not travel speed. US vehicles of model years 1989-99. Source reports no interval for the thresholds.",
          NO)
px.save(fig, HERE)
print("saved")
