"""2026-11-16: Satellites stopped shrinking in 2017.

Question: what does the typical satellite weigh, and how has that changed? The
median, not the mean: a few 20-tonne station modules would swamp a mean.

For each launch year I take every payload in GCAT with a known mass and report
the median, with and without Starlink. 2026 runs to the catalog's 15 November
update.

Data: Jonathan McDowell, GCAT (General Catalog of Artificial Space Objects).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-16"
Y0, Y1 = 1990, 2026

# ---------------------------------------------------------------- data ------
p = pd.read_csv(HERE / "data/gcat_payloads.csv", dtype=str)
p["year"] = pd.to_numeric(p.LDate.str[:4], errors="coerce")
p["mass"] = pd.to_numeric(p.Mass, errors="coerce")
p["starlink"] = p.Name.str.startswith("Starlink", na=False)
p = p[p.year.between(Y0, Y1)]
n_launched = len(p)
m = p[p.mass > 0].copy()
n_mass = len(m)

by = m.groupby("year").agg(n=("mass", "size"), median=("mass", "median"),
                           cube=("mass", lambda x: (x <= 10).mean()))
by["median_ex_starlink"] = m[~m.starlink].groupby("year").mass.median()
by["starlink_share"] = m.groupby("year").starlink.mean()
by.round(3).to_csv(HERE / "data/median_mass_by_year.csv")

low_year = int(by["median"].idxmin())
low = by.loc[low_year, "median"]
pre = by.loc[2005:2011, "median"].median()
now = by.loc[2024:2026, "median"]
low_ex = by.loc[low_year, "median_ex_starlink"]
now_ex = by.loc[Y1, "median_ex_starlink"]
cube_peak_year = int(by.cube.idxmax())

print(f"payloads launched {Y0}-{Y1}: {n_launched:,}; with a mass: {n_mass:,}")
print(by.loc[2008:].round(2).to_string())
print(f"median mass, 2005-11 typical year: {pre:,.0f} kg")
print(f"lowest median: {low:,.0f} kg in {low_year}")
print(f"median 2024 / 2025 / 2026: {now.loc[2024]:,.0f} / {now.loc[2025]:,.0f} / {now.loc[2026]:,.0f} kg")
print(f"2026 vs {low_year}: {now.loc[2026] / low:,.0f}x")
print(f"without Starlink: {low_ex:,.0f} kg in {low_year} -> {now_ex:,.0f} kg in {Y1} ({now_ex / low_ex:,.0f}x)")
print(f"share at 10 kg or less: peak {by.cube.max():.0%} in {cube_peak_year}; {Y1}: {by.loc[Y1, 'cube']:.0%}")
print(f"Starlink share of payloads, {Y1}: {by.loc[Y1, 'starlink_share']:.0%}")
plateau = m[m.year.between(2008, 2011) & (m.mass == 1450)]
print(f"2008-11 payloads at exactly 1,450 kg: {len(plateau)} of {int(m.year.between(2008, 2011).sum())}; "
      f"named Kosmos (GLONASS-M): {plateau.Name.str.startswith('Kosmos').sum()}")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 15.5)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Space · Satellite mass",
    "Satellites *stopped shrinking* in 2017",
    f"The median satellite fell from about {pre:,.0f} kg to {low:,.0f} kg as cheap CubeSats took over. Since {low_year} it has\n"
    f"climbed back to {now.loc[2026]:,.0f} kg. Leave out Starlink and the rise is still {low_ex:,.0f} kg to {now_ex:,.0f} kg.",
)

# --- 01: density of every payload by year and mass ---------------------------
top_A = deck_bottom - 0.07
hA = 0.34
axA = fig.add_axes([px.LEFT, top_A - hA, px.WIDTH, hA])
ybins = np.logspace(-1, 5, 49)
xbins = np.arange(Y0 - 0.5, Y1 + 1.5, 1)
H, _, _ = np.histogram2d(m.year, m.mass, bins=[xbins, ybins])
share = H / H.sum(axis=1, keepdims=True)           # each year's column sums to 1
cmap = LinearSegmentedColormap.from_list("paper_ink", [PAPER, PAPER_2, TAUPE, INK_2])
axA.pcolormesh(xbins, ybins, np.where(share > 0, share, np.nan).T, cmap=cmap, vmin=0, vmax=0.35,
               shading="flat", zorder=1)
axA.plot(by.index, by["median"], color=SIGNAL, lw=2.4, zorder=4, solid_capstyle="round")
axA.scatter([low_year], [low], s=60, color=SIGNAL, edgecolor=PAPER, lw=1, zorder=5)
px.note(axA, (low_year, low), (-40, -6), f"{low_year}: median {low:,.0f} kg", ha="right", size=9.5, color=INK)
px.note(axA, (Y1, now.loc[Y1]), (-10, 26), f"{Y1}: {now.loc[Y1]:,.0f} kg", ha="right", size=9.5, color=INK)
px.note(axA, (2008, by.loc[2008, "median"]), (0, 24), f"2008: {by.loc[2008, 'median']:,.0f} kg", ha="center",
        size=9.5, color=INK)
axA.text(2020.0, 1300, "Starlink", fontsize=9, color=INK_2, ha="left", va="bottom")
axA.text(2014.0, 2.2, "CubeSats", fontsize=9, color=INK_2, ha="left", va="top")
axA.set_yscale("log")
axA.set_ylim(0.1, 1e5)
axA.set_xlim(Y0 - 0.5, Y1 + 0.5)
axA.set_yticks([1, 10, 100, 1000, 10000])
axA.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f} kg"))
axA.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
axA.grid(False)
px.panel(axA, 1, "Every payload launched since 1990, by year and mass",
         "Shading shows where each year's satellites sit (darker = more of them). Red line: the median.")
px.mono_ticks(axA)

# --- 02: median with and without Starlink ------------------------------------
top_B = top_A - hA - 0.12
axB = fig.add_axes([px.LEFT, 0.115, px.WIDTH * 0.64, top_B - 0.115])
yrs = by.loc[2005:].index
axB.plot(yrs, by.loc[yrs, "median"], color=SIGNAL, lw=2.2, zorder=4)
axB.plot(yrs, by.loc[yrs, "median_ex_starlink"], color=INK_2, lw=1.6, ls=(0, (4, 2)), zorder=3)
axB.set_yscale("log")
axB.set_ylim(2, 4000)
axB.set_xlim(2004.5, 2029.5)
axB.set_yticks([10, 100, 1000])
axB.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f} kg"))
axB.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
axB.grid(axis="y")
axB.text(Y1 + 0.5, by.loc[Y1, "median"] * 1.5, f"All\n{by.loc[Y1, 'median']:,.0f} kg", color=SIGNAL, fontsize=9.5,
         va="center", weight="semibold")
axB.text(Y1 + 0.5, by.loc[Y1, "median_ex_starlink"] / 1.6, f"Without\nStarlink\n{now_ex:,.0f} kg", color=INK_2,
         fontsize=9.5, va="center")
px.panel(axB, 2, "Median payload mass, 2005 onward",
         "The rise isn't only Starlink: without it the median still climbs.")
px.mono_ticks(axB)

px.big_number(fig, px.LEFT + px.WIDTH * 0.73, top_B + 0.005, f"{by.cube.max():.0%}",
              f"of payloads launched in {cube_peak_year} weighed\n10 kg or less. In {Y1}: {by.loc[Y1, 'cube']:.0%}")

px.footer(fig,
          "DATA  Jonathan McDowell, GCAT (CC BY 4.0), catalog updated 15 Nov 2026. Payloads with a known mass.\n"
          f"NOTE  Mass at launch. {Y1} runs to 15 November. Starlink = payloads named Starlink.",
          NO)

px.save(fig, HERE)
print("saved")
