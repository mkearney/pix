"""2026-11-26: BMI's link to death weakens with age.

Finding (moderator, association): in 3.95 million never-smokers without chronic
disease (Global BMI Mortality Collaboration, Lancet 2016, 189 studies), each 5
kg/m2 of BMI above 25 went with a hazard ratio for death of 1.52 when BMI was
measured at 35-49, against 1.21 at 70-89. The BMI with the lowest death rate
rose with age, from 22 to 24. A UK cohort of 3.6 million (Bhaskaran 2018) and an
older US cohort (Stevens 1998) show the same weakening with age.

Data: values transcribed from the paper's text (data/transcribed.csv), each
asserted against the saved abstract and full-text excerpt.
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
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-26"

# ---------------------------------------------------------------- data ------
t = pd.read_csv(HERE / "data/transcribed.csv")
txt = re.sub(r"\s+", " ", "".join((HERE / "data" / f).read_text() for f in
                                    ["pubmed_abstracts.txt", "gbmc_2016_results_excerpt.txt", "bhaskaran_2018_excerpt.txt"]))
for c in [
    "3 951 455 people in 189 studies were never-smokers without chronic diseases at recruitment who survived 5 years, "
    "of whom 385 879 died",
    "1·52 (1·47–1·56) for ages 35–49 years at baseline to 1·21 (1·17–1·25) for ages 70–89 years at baseline",
    "The HR was 1·51 (1·46–1·56) for men versus 1·30 (1·26–1·33) for women",
    "1·31 (95% CI 1·29–1·33) overall, 1·39 (1·34–1·44) in east Asia, 1·39 (1·34–1·43) in Europe, 1·29 (1·26–1·32) "
    "in North America, and 1·31 (1·27–1·35) in Australia and New Zealand",
    "BMI=22 kg/m 2 for baseline age 35–49 years, BMI=23 kg/m 2 for baseline age 50–69 years, and BMI=24 kg/m 2 for "
    "baseline age 70–89 years",
    "1·51, 1·43-1·59 for BMI 15·0-<18·5", "1·13, 1·09-1·17 for BMI 18·5-<20·0", "1·07, 1·07-1·08 for BMI 25·0-<27·5",
    "1·20, 1·18-1·22 for BMI 27·5-<30·0", "30·0-<35·0 kg/m(2)) was 1·45, 95% CI 1·41-1·48",
    "obesity grade 2 (35·0–<40·0 kg/m 2 ) was 1·94, 1·87–2·01", "grade 3 (40·0–<60·0 kg/m 2 ) was 2·76, 2·60–2·92",
    "Associations between BMI and mortality were stronger at younger ages than at older ages",
    "the relative risk associated with greater body-mass index declined with age",
    "1 969 648 people and 188 057 deaths",
    "In the older age group, mortality risk increased at BMIs lower than 22",
]:
    assert c in txt, c

per5 = t[t.panel == "per5"].set_index("group")
band = t[t.panel == "band"].copy()
band[["b0", "b1"]] = band.group.str.split("-", expand=True).astype(float)
band["mid"] = (band.b0 + band.b1.clip(upper=45)) / 2
nadir = t[t.panel == "nadir"].set_index("group").value
young, old = per5.loc["Age 35-49 at baseline"], per5.loc["Age 70-89 at baseline"]

print("GBMC 2016: 3,951,455 never-smokers without chronic disease, 189 studies, 385,879 deaths")
print("HR per 5 kg/m2 above BMI 25:")
for g, r in per5.iterrows():
    print(f"  {g}: {r.value:.2f} ({r.lo:.2f}-{r.hi:.2f}), {r.value - 1:.0%} higher")
print("HR by BMI band (ref 22.5-25):", "; ".join(f"{r.group} {r.value:.2f}" for _, r in band.iterrows()))
print("BMI with lowest mortality by baseline age:", ", ".join(f"{g} {v:.0f}" for g, v in nadir.items()))

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17.2)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Health · Weight and mortality",
    "BMI's link to death\n*weakens with age*",
    f"Among never-smokers without chronic disease, each 5 units of BMI above 25 went with a {young.value - 1:.0%} higher death\n"
    f"rate when BMI was measured at 35 to 49, but {old.value - 1:.0%} when it was measured at 70 to 89.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Individual-participant meta-\nanalysis of 189 cohort studies"),
    ("Sample", "3.95 million never-smokers,\n385,879 deaths, four continents"),
    ("Source", "Global BMI Mortality\nCollaboration, Lancet 2016"),
    ("Consistent with", "Bhaskaran et al. 2018 (2.0m UK\nnever-smokers) · Winter et al. 2017"),
], widths=[0.27, 0.27, 0.21, 0.25])

# --- 01: forest of HR per 5 units -----------------------------------------------
top1 = y - 0.07
h1 = 0.23
ax = fig.add_axes([px.LEFT + 0.25, top1 - h1, px.WIDTH - 0.25 - 0.2, h1])
groups = [("By age at BMI measurement", [("Age 35-49 at baseline", "Aged 35–49"), ("Age 70-89 at baseline", "Aged 70–89")], SIGNAL),
          ("By sex", [("Men", "Men"), ("Women", "Women")], INK_2),
          ("By region", [("Europe", "Europe"), ("East Asia", "East Asia"), ("Australia and New Zealand", "Australia, NZ"),
                         ("North America", "North America")], TAUPE),
          ("Overall", [("All", "All")], INK)]
yy, ys = 0.0, []
for head, rows, col in groups:
    ax.text(-0.03, yy + 0.05, head.upper(), transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=8.5,
            family=px.MONO, color=INK_3)
    yy -= 0.75
    for key, lab in rows:
        r = per5.loc[key]
        ax.plot([r.lo, r.hi], [yy, yy], color=col, lw=2, zorder=3, solid_capstyle="round")
        ax.scatter([r.value], [yy], s=60 if col != INK else 80, marker="s" if col != INK else "D", color=col,
                   edgecolor=PAPER, lw=0.8, zorder=4)
        ax.text(-0.03, yy, lab, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=11,
                color=SIGNAL if col == SIGNAL else INK)
        ax.text(1.03, yy, f"{r.value:.2f} ({r.lo:.2f}–{r.hi:.2f})", transform=ax.get_yaxis_transform(), fontsize=9.5,
                family=px.MONO, color=SIGNAL if col == SIGNAL else INK_2, va="center")
        ys.append(yy)
        yy -= 0.75
    yy -= 0.15
ax.axvline(1, color=INK, lw=0.8)
ax.set_xscale("log")
ax.set_xlim(0.95, 1.65)
ax.xaxis.set_major_locator(FixedLocator([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]))
ax.xaxis.set_minor_locator(NullLocator())
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_ylim(min(ys) - 0.6, 0.45)
ax.set_yticks([])
ax.grid(axis="x")
ax.set_xlabel("Hazard ratio for death per 5 kg/m² of BMI above 25 (95% CI, log scale)")
px.mono_ticks(ax)
hdr = fig.add_axes([px.LEFT, top1 - h1, 0.01, h1])
hdr.axis("off")
px.panel(hdr, 1, "How much higher the death rate is per 5 units of BMI above 25",
         "Hazard ratios adjusted for study, age and sex. Deaths in the first 5 years of follow-up excluded.", pad=0.55)

# --- 02: J-curve -------------------------------------------------------------------
top2 = top1 - h1 - 0.11
h2 = 0.17
ax2 = fig.add_axes([px.LEFT, top2 - h2, px.WIDTH - 0.12, h2])
ax2.axvspan(20, 25, color=PAPER_2, lw=0, zorder=0)
ax2.vlines(band.mid, band.lo, band.hi, color=INK, lw=1.1, zorder=3)
ax2.plot(band.mid, band.value, color=INK_3, lw=1, zorder=2)
ax2.scatter(band.mid, band.value, s=55, color=INK, edgecolor=PAPER, lw=0.8, zorder=4)
for _, r in band.iterrows():
    dy = 1.06 if r.value > 1.05 else 1.045
    ax2.text(r.mid, r.hi * dy, f"{r.value:.2f}", ha="center", va="bottom", fontsize=9, family=px.MONO, color=INK_2)
ax2.text(22.5, 0.86, "Lowest death rate:\nBMI 22 at 35–49, 23 at 50–69,\n24 at 70–89", ha="center", va="top",
         fontsize=9.5, color=SIGNAL)
for v in nadir.values:
    ax2.plot([v, v], [0.9, 0.94], color=SIGNAL, lw=2, zorder=3)
ax2.axhline(1, color=INK, lw=0.6)
ax2.set_yscale("log")
ax2.set_ylim(0.62, 3.6)
ax2.yaxis.set_major_locator(FixedLocator([0.8, 1, 1.5, 2, 3]))
ax2.yaxis.set_minor_locator(NullLocator())
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax2.set_xlim(14, 46)
ax2.set_xticks([15, 18.5, 20, 22.5, 25, 27.5, 30, 35, 40])
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax2.set_xlabel("BMI band (kg/m²); 40–60 drawn at 42.5")
ax2.set_ylabel("Hazard ratio vs BMI 22.5–25 (log)")
ax2.grid(axis="y")
px.mono_ticks(ax2)
px.panel(ax2, 2, "Death rate by BMI band, all ages pooled",
         "Hazard ratios with floating-variance 95% CIs. Shaded: BMI 20–25, where death rates were lowest.", pad=0.55)

px.footer(fig,
          "DATA  Global BMI Mortality Collaboration, Lancet 388:776 (2016), abstract and Results. Values transcribed from the text.\n"
          "NOTE  Observational. Relative risks are smaller at older ages, but absolute death rates are higher. The size of the\n"
          "      overweight (25–30) effect is debated; the post does not rest on it.",
          NO)
px.save(fig, HERE)
print("saved")
