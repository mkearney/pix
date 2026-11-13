"""2026-11-13: Italy drops 19 places when every adult counts.

Question: the usual "who works the longest hours" ranking divides hours by
workers. What happens if you divide by everyone of working age instead?

Hours per person aged 15-64 = hours per worker x employment rate (15-64).
This is an approximation: the hours figure covers workers of all ages, the
employment rate only 15-64. It is exact if workers over 64 work the same hours
as everyone else, and close enough for ranking.

Data: OECD annual hours actually worked per worker; OECD employment rate 15-64.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-13"
YEAR = 2024

NAME = {
    "AUS": "Australia", "AUT": "Austria", "BEL": "Belgium", "BGR": "Bulgaria", "CAN": "Canada",
    "CHE": "Switzerland", "CHL": "Chile", "COL": "Colombia", "CRI": "Costa Rica", "CZE": "Czechia",
    "DEU": "Germany", "DNK": "Denmark", "ESP": "Spain", "EST": "Estonia", "FIN": "Finland",
    "FRA": "France", "GBR": "UK", "GRC": "Greece", "HRV": "Croatia", "HUN": "Hungary",
    "IRL": "Ireland", "ISL": "Iceland", "ISR": "Israel", "ITA": "Italy", "JPN": "Japan",
    "KOR": "South Korea", "LTU": "Lithuania", "LUX": "Luxembourg", "LVA": "Latvia", "MEX": "Mexico",
    "NLD": "Netherlands", "NOR": "Norway", "NZL": "New Zealand", "POL": "Poland", "PRT": "Portugal",
    "ROU": "Romania", "SVK": "Slovakia", "SVN": "Slovenia", "SWE": "Sweden", "TUR": "Turkey",
    "USA": "United States",
}

# ---------------------------------------------------------------- data ------
h = pd.read_csv(HERE / "data/oecd_annual_hours_per_worker.csv")
e = pd.read_csv(HERE / "data/oecd_employment_rate_15_64.csv")
h = h[h.year == YEAR].set_index("iso3").hours_per_worker
e = e[e.year == YEAR].set_index("iso3").emp_rate_15_64
d = pd.concat([h, e], axis=1).dropna()
oecd_avg = d.loc["OECD"] if "OECD" in d.index else None
d = d[d.index.isin(NAME)].copy()           # members only, no aggregates
d["country"] = d.index.map(NAME)
d["hours_per_adult"] = d.hours_per_worker * d.emp_rate_15_64 / 100
d["rank_worker"] = d.hours_per_worker.rank(ascending=False, method="first").astype(int)
d["rank_adult"] = d.hours_per_adult.rank(ascending=False, method="first").astype(int)
d["places"] = d.rank_adult - d.rank_worker   # positive = falls
d.round(1).sort_values("rank_worker").to_csv(HERE / "data/hours_per_adult_2024.csv")

n = len(d)
rho = d[["hours_per_worker", "hours_per_adult"]].corr(method="spearman").iloc[0, 1]
moved10 = int((d.places.abs() >= 10).sum())
it, nl, isl, jp, gr = (d.loc[c] for c in ["ITA", "NLD", "ISL", "JPN", "GRC"])

# Sensitivity: 2023 instead of 2024
h23 = pd.read_csv(HERE / "data/oecd_annual_hours_per_worker.csv").query("year == 2023").set_index("iso3").hours_per_worker
e23 = pd.read_csv(HERE / "data/oecd_employment_rate_15_64.csv").query("year == 2023").set_index("iso3").emp_rate_15_64
d23 = pd.concat([h23, e23], axis=1).dropna()
d23 = d23[d23.index.isin(NAME)]
d23["pa"] = d23.hours_per_worker * d23.emp_rate_15_64 / 100
r23 = d23.hours_per_worker.rank(ascending=False, method="first")
a23 = d23.pa.rank(ascending=False, method="first")

print(f"{YEAR}: {n} OECD members with both series")
print(f"Spearman rank correlation, per worker vs per adult: {rho:.2f}")
print(f"countries moving 10+ places: {moved10}")
for c in ["ITA", "GRC", "ROU", "ESP", "CHL", "ISL", "JPN", "NZL", "NLD", "CHE", "DEU", "USA", "MEX", "KOR"]:
    r = d.loc[c]
    print(f"  {r.country:<14} worker {r.hours_per_worker:6.0f} (#{r.rank_worker:>2})  emp {r.emp_rate_15_64:4.1f}%  "
          f"adult {r.hours_per_adult:6.0f} (#{r.rank_adult:>2})  moves {-r.places:+d}")
print(f"Italy vs Netherlands per worker: {it.hours_per_worker - nl.hours_per_worker:+.0f} h; "
      f"per adult: {it.hours_per_adult - nl.hours_per_adult:+.0f} h")
print(f"Italy per adult per week (52 wks): {it.hours_per_adult / 52:.1f}  Netherlands: {nl.hours_per_adult / 52:.1f}")
print(f"2023 check, Italy rank worker #{int(r23['ITA'])} -> adult #{int(a23['ITA'])} of {len(d23)}; "
      f"Iceland #{int(r23['ISL'])} -> #{int(a23['ISL'])}")
print("biggest fallers:")
print(d.nlargest(6, "places")[["country", "rank_worker", "rank_adult", "places"]].to_string())
print("biggest risers:")
print(d.nsmallest(6, "places")[["country", "rank_worker", "rank_adult", "places"]].to_string())

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 21)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Work · Hours per adult",
    "Italy drops 19 places\nwhen *every adult counts*",
    f"Per worker, Italy works the {it.rank_worker}th longest hours of {n} OECD countries. Divide the same hours by\n"
    f"everyone aged 15 to 64 and it falls to {it.rank_adult}th, below the Netherlands. Iceland goes the other way.",
)

FALL = ["ITA", "ROU", "GRC", "ESP", "CHL"]
RISE = ["ISL", "JPN", "NZL", "NLD", "CHE"]

# --- 01: slope of ranks ------------------------------------------------------
top_A = deck_bottom - 0.065
B_BOT, B_H = 0.11, 0.20
hA = top_A - (B_BOT + B_H + 0.085)
axA = fig.add_axes([px.LEFT + 0.17, top_A - hA, px.WIDTH - 0.34, hA])
for iso, r in d.iterrows():
    if iso in FALL:
        c, lw, z = SIGNAL, 2.0, 4
    elif iso in RISE:
        c, lw, z = INDIGO, 2.0, 4
    else:
        c, lw, z = TAUPE, 1.0, 2
    axA.plot([0, 1], [r.rank_worker, r.rank_adult], color=c, lw=lw, zorder=z, solid_capstyle="round")
    axA.scatter([0, 1], [r.rank_worker, r.rank_adult], s=16 if z == 2 else 28, color=c, edgecolor=PAPER,
                lw=0.6, zorder=z + 1)
    hi = z == 4
    kw = dict(fontsize=9.5, va="center", color=INK if hi else INK_3, weight="semibold" if hi else "normal")
    axA.text(-0.03, r.rank_worker, f"{r.country}  {r.hours_per_worker:,.0f}", ha="right", **kw)
    tail = f"  {-r.places:+d}" if hi else ""
    axA.text(1.03, r.rank_adult, f"{r.hours_per_adult:,.0f}  {r.country}{tail}", ha="left", **kw)
axA.set_ylim(n + 0.8, 0.2)
axA.set_xlim(0, 1)
axA.axis("off")
axA.text(-0.03, -0.6, "HOURS PER WORKER", ha="right", va="bottom", fontsize=9, family=px.MONO, color=INK_2)
axA.text(1.03, -0.6, "HOURS PER PERSON 15-64", ha="left", va="bottom", fontsize=9, family=px.MONO, color=INK_2)
px.panel(axA, 1, f"Rank of {n} OECD countries by annual hours worked, {YEAR}",
         "Left: the usual ranking. Right: the same hours spread over everyone of working age. "
         "Red fell 10+ places, blue rose 10+.", pad=0.55)

# --- 02: the mechanism -------------------------------------------------------
axB = fig.add_axes([px.LEFT + 0.03, B_BOT, px.WIDTH - 0.03, B_H])
xs = np.linspace(55, 90, 200)
for lvl in [1000, 1100, 1200, 1300, 1400]:
    ys = lvl / (xs / 100)
    axB.plot(xs, ys, color=INK_3, lw=0.6, ls=(0, (1, 2)), zorder=1)
    axB.text(90.3, lvl / 0.90, f"{lvl:,}", fontsize=8.5, color=INK_3, ha="left", va="center",
             family=px.MONO)
cols = [SIGNAL if i in FALL else INDIGO if i in RISE else TAUPE for i in d.index]
sizes = [46 if i in FALL + RISE else 22 for i in d.index]
axB.scatter(d.emp_rate_15_64, d.hours_per_worker, s=sizes, c=cols, edgecolor=PAPER, lw=0.7, zorder=4)
LBL = {"ITA": (-10, -12, "right"), "NLD": (8, -10, "left"), "ISL": (6, 14, "left"), "GRC": (-10, 6, "right"),
       "JPN": (8, 10, "left"), "ROU": (-10, -4, "right"), "MEX": (8, 6, "left"), "DEU": (-8, -10, "right"),
       "CHE": (8, 8, "left"), "ESP": (-10, -6, "right"), "CHL": (8, 6, "left"), "NZL": (-8, 10, "right")}
for iso, (dx, dy, ha) in LBL.items():
    r = d.loc[iso]
    px.note(axB, (r.emp_rate_15_64, r.hours_per_worker), (dx, dy), r.country, ha=ha, size=9)
axB.set_xlim(55, 90)
axB.set_ylim(1000, 2300)
axB.text(90.3, 1400 / 0.90 + 75, "per adult", fontsize=8.5, color=INK_3, ha="left", va="bottom", family=px.MONO)
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
axB.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
axB.grid(axis="y")
axB.set_xlabel("Share of people aged 15 to 64 in work", fontsize=10, color=INK_2)
axB.set_ylabel("Hours per worker", fontsize=10, color=INK_2)
px.panel(axB, 2, "Why: long hours, but fewer people working",
         "Each country by employment rate and hours per worker. Dotted curves join equal hours per adult.")
px.mono_ticks(axB)

px.footer(fig,
          f"DATA  OECD annual hours actually worked per worker; OECD employment rate, ages 15-64. {YEAR}.\n"
          "NOTE  Hours per adult = hours per worker x employment rate. Hours cover workers of all ages.\n"
          f"      Spearman correlation between the two rankings: {rho:.2f}.",
          NO)

px.save(fig, HERE)
print("saved")
