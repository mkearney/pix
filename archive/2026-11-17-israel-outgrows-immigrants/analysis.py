"""2026-11-17: Israel is outgrowing its immigrants.

Question: in which rich countries did the foreign-born share of the population
fall between 1990 and 2024, and why?

Rich = World Bank high-income in its latest (2025) classification, 1 million
people or more in 2024. Total population is the UN migrant count divided by
the UN migrant share, so both come from the same UN release; native-born is
total minus migrants.

Data: UN DESA International Migrant Stock 2024, via Our World in Data.
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
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-17"

# ---------------------------------------------------------------- data ------
sh = pd.read_csv(HERE / "data/owid_migrant_stock_share.csv")
ct = pd.read_csv(HERE / "data/owid_migrant_stock_total.csv")
inc = pd.read_csv(HERE / "data/owid_world_bank_income_groups.csv")
share = sh.pivot_table(index="entity", columns="year", values="immigrant_share_of_dest_population_all")
count = ct.pivot_table(index="entity", columns="year", values="immigrants_all")
pop = count / (share / 100)
native = pop - count

latest = inc[inc.year == inc.year.max()].set_index("entity").classification
rich = latest[latest == "High-income countries"].index
rich = [c for c in rich if c in share.index and pop.loc[c, 2024] >= 1e6]

t = pd.DataFrame({
    "share_1990": share.loc[rich, 1990], "share_2024": share.loc[rich, 2024],
    "migrants_1990": count.loc[rich, 1990], "migrants_2024": count.loc[rich, 2024],
    "pop_1990": pop.loc[rich, 1990], "pop_2024": pop.loc[rich, 2024],
    "native_1990": native.loc[rich, 1990], "native_2024": native.loc[rich, 2024],
}).dropna()
t["change"] = t.share_2024 - t.share_1990
t["migrants_x"] = t.migrants_2024 / t.migrants_1990
t["native_x"] = t.native_2024 / t.native_1990
t = t.sort_values("change")
t.round(3).to_csv(HERE / "data/high_income_1990_2024.csv")

n, fell = len(t), int((t.change < 0).sum())
isr = t.loc["Israel"]
BALT = ["Latvia", "Estonia", "Lithuania"]
fell_and_more = t[(t.change < 0) & (t.migrants_x > 1)]

print(f"high-income countries, 1M+ people: {n}; foreign-born share fell in {fell}, rose in {n - fell}")
print(t[["share_1990", "share_2024", "change", "migrants_x", "native_x"]].head(10).round(2).to_string())
print(f"Israel: share {isr.share_1990:.1f}% -> {isr.share_2024:.1f}%; migrants {isr.migrants_1990 / 1e6:.2f}M -> "
      f"{isr.migrants_2024 / 1e6:.2f}M ({isr.migrants_x - 1:+.0%}); native-born {isr.native_1990 / 1e6:.2f}M -> "
      f"{isr.native_2024 / 1e6:.2f}M ({isr.native_x:.1f}x)")
for b in BALT:
    r = t.loc[b]
    print(f"{b}: share {r.share_1990:.1f}% -> {r.share_2024:.1f}%; migrants {r.migrants_x - 1:+.0%}; native {r.native_x - 1:+.0%}")
print("share fell while migrant numbers rose:", ", ".join(f"{c} ({r.change:+.1f} pts)" for c, r in fell_and_more.iterrows()))
print(f"median change, all {n}: {t.change.median():+.1f} pts; biggest rise: {t.change.idxmax()} {t.change.max():+.1f}")
isr_path = share.loc["Israel"]
print("Israel share path:", isr_path.round(1).to_dict())

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Migration · Foreign-born share",
    "Israel is *outgrowing* its immigrants",
    f"The foreign-born share rose in {n - fell} of {n} rich countries since 1990. Israel's fell the most, from "
    f"{isr.share_1990:.0f}% to {isr.share_2024:.0f}%,\neven though {isr.migrants_x - 1:.0%} more immigrants live there now. "
    f"The Baltic states fell too, for the opposite reason.",
)

# --- 01: slope ---------------------------------------------------------------
top_A = deck_bottom - 0.075
hA = 0.37
axA = fig.add_axes([px.LEFT + 0.16, top_A - hA, px.WIDTH - 0.32, hA])
for c, r in t.iterrows():
    if c == "Israel":
        col, lw, z = SIGNAL, 2.4, 5
    elif c in BALT:
        col, lw, z = INDIGO, 1.8, 4
    elif r.change < 0:
        col, lw, z = INK_3, 1.2, 3
    else:
        col, lw, z = TAUPE, 0.9, 2
    axA.plot([0, 1], [r.share_1990, r.share_2024], color=col, lw=lw, zorder=z, solid_capstyle="round")
    axA.scatter([0, 1], [r.share_1990, r.share_2024], s=22 if z > 2 else 10, color=col, edgecolor=PAPER, lw=0.5,
                zorder=z + 1)
axA.set_xlim(-0.02, 1.02)
axA.set_ylim(0, 80)
axA.axis("off")
for x, lab in [(0, "1990"), (1, "2024")]:
    axA.text(x, 82, lab, ha="center", va="bottom", fontsize=10, family=px.MONO, color=INK_2)
L = {"Israel": (SIGNAL, 0, 0), "Latvia": (INDIGO, 0, -1.6), "Estonia": (INDIGO, 0, 1.2), "Lithuania": (INDIGO, 0, 0)}
for c, (col, d0, d1) in L.items():
    r = t.loc[c]
    axA.text(-0.03, r.share_1990 + d0 + (1.4 if c == "Latvia" else -1.4 if c == "Estonia" else 0),
             f"{c} {r.share_1990:.0f}%", ha="right", va="center", fontsize=10, color=col, weight="semibold")
    axA.text(1.03, r.share_2024 + d1, f"{r.share_2024:.0f}% {c}", ha="left", va="center", fontsize=10, color=col,
             weight="semibold")
for c in ["Qatar", "United Arab Emirates", "Singapore", "Switzerland", "Germany", "Japan"]:
    r = t.loc[c]
    name = {"United Arab Emirates": "UAE", "United States": "US"}.get(c, c)
    axA.text(1.03, r.share_2024, f"{r.share_2024:.0f}% {name}", ha="left", va="center", fontsize=9, color=INK_3)
px.panel(axA, 1, f"Foreign-born share of the population, {n} high-income countries",
         "Red: Israel. Blue: the Baltic states. Grey: other countries where the share fell.", pad=0.55)

# --- 02: Israel vs Latvia, people in millions --------------------------------
top_B = top_A - hA - 0.1
yrs = np.array(sorted(share.columns))
wB = (px.WIDTH - 0.08) / 2
for k, (c, col) in enumerate([("Israel", SIGNAL), ("Latvia", INDIGO)]):
    ax = fig.add_axes([px.LEFT + k * (wB + 0.08), 0.115, wB, top_B - 0.115])
    nat = native.loc[c, yrs] / 1e6
    mig = count.loc[c, yrs] / 1e6
    ax.fill_between(yrs, 0, mig, color=col, lw=0, alpha=0.9, zorder=3)
    ax.fill_between(yrs, mig, mig + nat, color=PAPER_2, lw=0, zorder=2)
    ax.plot(yrs, mig + nat, color=INK_3, lw=0.8, zorder=4)
    ax.set_xlim(1990, 2024)
    ax.set_xticks([1990, 2000, 2010, 2020])
    ax.grid(axis="y")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}M"))
    top = float((mig + nat).max())
    ax.set_ylim(0, top * 1.12)
    thin = float(mig.iloc[-1]) < 0.25 * top
    ax.text(2023.5, float(mig.iloc[-1]) * (1.15 if thin else 0.5), f"Foreign-born\n{mig.iloc[-1]:.2f}M", ha="right",
            va="bottom" if thin else "center", fontsize=9, color=col if thin else PAPER, weight="semibold")
    ax.text(2023.5, float(mig.iloc[-1] + nat.iloc[-1] * (0.7 if thin else 0.5)), f"Native-born\n{nat.iloc[-1]:.2f}M", ha="right",
            va="center", fontsize=9, color=INK_2)
    ax.text(1991, top * 1.08, c, fontsize=15, family=px.SERIF, color=INK, va="top")
    px.mono_ticks(ax)
    if k == 0:
        px.panel(ax, 2, "Two ways to fall: more natives, or fewer immigrants",
                 "People living in each country, millions. Israel's immigrants rose; Latvia's fell by two-thirds.")

px.footer(fig,
          "DATA  UN DESA International Migrant Stock 2024, via Our World in Data. World Bank income groups, 2025.\n"
          "NOTE  Foreign-born includes people of foreign citizenship where birthplace isn't recorded. Population\n"
          "      is the UN migrant count divided by the UN migrant share. Countries with 1 million people or more.",
          NO)

px.save(fig, HERE)
print("saved")
