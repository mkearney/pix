"""2026-11-09: Last year the world added a South Korea of solar power.

Question: each year, how much new solar generation came online worldwide, and
which country's entire electricity generation is that the same size as?

New solar in year Y = world solar generation in Y minus Y-1 (TWh). It's matched
to the country whose total generation is closest, using each country's figure
for year Y (or its latest year before Y when Y isn't reported yet).

Data: Our World in Data energy dataset (Ember + Energy Institute).
"""
from __future__ import annotations

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
DATE = "2026-11-09"
Y0, Y1 = 2010, 2025

# ---------------------------------------------------------------- data ------
e = pd.read_csv(HERE / "data/owid-energy-data.csv", low_memory=False)
world = e[e.country == "World"].set_index("year")
solar = world.solar_electricity
gen = world.electricity_generation
add = solar.diff()

cty = e[e.iso_code.notna() & ~e.iso_code.astype(str).str.startswith("OWID")]
cty = cty[["country", "year", "electricity_generation"]].dropna()

rows = []
for y in range(Y0, Y1 + 1):
    latest = cty[cty.year <= y].sort_values("year").groupby("country").tail(1)
    i = (latest.electricity_generation - add[y]).abs().idxmin()
    m = latest.loc[i]
    rows.append({"year": y, "new_solar_twh": add[y], "match": m.country,
                 "match_twh": m.electricity_generation, "match_year": int(m.year),
                 "solar_share": solar[y] / gen[y]})
lad = pd.DataFrame(rows)
lad.round(3).to_csv(HERE / "data/solar_ladder.csv", index=False)

last = lad.iloc[-1]
first = lad.iloc[0]
add_2015 = add[2015]
print(lad.round(1).to_string(index=False))
print(f"\n{Y1} new solar: {last.new_solar_twh:.0f} TWh, ~ {last.match} ({last.match_twh:.0f} TWh, {last.match_year})")
print(f"{Y1} vs 2015 new solar: {last.new_solar_twh / add_2015:.0f}x")
print(f"solar share of world electricity: {Y0} {solar[Y0] / gen[Y0]:.1%}  {Y1} {solar[Y1] / gen[Y1]:.1%}")
print(f"world solar {Y1}: {solar[Y1]:,.0f} TWh   world generation growth {Y1}: {gen[Y1] - gen[Y1 - 1]:.0f} TWh")
print(f"new solar as share of new demand {Y1}: {add[Y1] / (gen[Y1] - gen[Y1 - 1]):.0%}")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 14.2)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Energy · Solar",
    "Last year the world added\n*a South Korea* of solar power",
    f"Each row is one year's new solar generation, next to the country whose entire electricity output is the\n"
    f"same size. In {Y0} the new solar matched {first.match}. In {Y1} it matched {last.match}.",
)

# --- 01: ladder ----------------------------------------------------------------
top_A = deck_bottom - 0.07
axA = fig.add_axes([px.LEFT + 0.03, 0.33, px.WIDTH - 0.03, top_A - 0.33])
yy = np.arange(len(lad))[::-1]
v = lad.new_solar_twh.to_numpy()
axA.hlines(yy, 0, v, color=TAUPE, lw=1.2, zorder=2)
hi = lad.year.isin([Y0, 2017, 2022, 2024, Y1]).to_numpy()
axA.scatter(v[~hi], yy[~hi], s=34, color=TAUPE, zorder=3, edgecolors=PAPER, linewidths=0.6)
axA.scatter(v[hi], yy[hi], s=70, color=SIGNAL, zorder=4, edgecolors=PAPER, linewidths=0.8)
axA.hlines(yy[hi], 0, v[hi], color=SIGNAL, lw=2, zorder=3)
for yi, r, h in zip(yy, lad.itertuples(), hi):
    lbl = f"{r.match}   {r.new_solar_twh:.0f} TWh" if h else r.match
    axA.text(r.new_solar_twh + 10, yi, lbl, va="center", ha="left",
             fontsize=10.5 if h else 9.5, color=INK if h else INK_2, weight="bold" if h else "normal")
    axA.text(-12, yi, f"{r.year}", va="center", ha="right", fontsize=9.5, family=px.MONO, color=INK_3)
axA.set_ylim(-0.7, len(lad) - 0.3)
axA.set_xlim(0, 830)
axA.set_yticks([])
axA.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
axA.set_xticks(range(0, 701, 100))
axA.grid(axis="y", visible=False)
axA.set_xlabel("New solar generation that year, terawatt-hours")
px.panel(axA, 1, "One year of new solar, as a whole country",
         "Matched to the country whose total electricity generation is closest in size")
px.mono_ticks(axA)

# --- 02: share line --------------------------------------------------------------
axB = fig.add_axes([px.LEFT + 0.03, 0.115, px.WIDTH - 0.03, 0.12])
yrs = np.arange(Y0, Y1 + 1)
sh = (solar / gen).loc[yrs].to_numpy()
axB.plot(yrs, sh, color=SIGNAL, lw=2, zorder=3)
axB.scatter([yrs[-1]], [sh[-1]], s=40, color=SIGNAL, zorder=4, edgecolors=PAPER)
axB.set_ylim(0, 0.1)
axB.set_xlim(Y0 - 0.3, Y1 + 0.3)
axB.set_yticks([0, 0.05, 0.1])
axB.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0%}"))
axB.set_xticks([2010, 2015, 2020, 2025])
axB.text(yrs[-1] - 0.3, sh[-1], f"{sh[-1]:.1%}", ha="right", va="center", fontsize=10, family=px.MONO, color=INK)
axB.text(yrs[0] + 0.2, sh[0] + 0.006, f"{sh[0]:.1%}", ha="left", va="bottom", fontsize=10, family=px.MONO, color=INK)
px.panel(axB, 2, "Solar's share of the world's electricity", None)
px.mono_ticks(axB)

px.footer(fig,
          "DATA  Our World in Data energy dataset (Ember, Energy Institute). World solar generation, change from the year before.\n"
          "NOTE  Country totals use the same year where reported, otherwise the latest year before it. Generation, not capacity.",
          NO)
px.save(fig, HERE)
print("saved")
