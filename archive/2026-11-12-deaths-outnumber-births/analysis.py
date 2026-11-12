"""2026-11-12 — The tipping point, country by country.

Question: what share of humanity lives in a country where more people die
each year than are born — and when does that become most of us?

Data: UN World Population Prospects 2024 (estimates 1950–2023, medium-variant
projections 2024–2100), via Our World in Data grapher CSVs in ./data.
Natural decrease = deaths > births in a calendar year (migration ignored).
"Tipping year" = first year of the final, unbroken run of natural decrease
that lasts through 2100 (so brief COVID-era dips don't count).
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
from pix.style import (ACCENT, ACCENT_2, GRID, INK, INK_2, INK_3, NEUTRAL, SURFACE,  # noqa: E402
                       apply, footer, title_block)

TODAY = 2026

# ---------------------------------------------------------------- data ------
b = pd.read_csv(HERE / "data/births-and-deaths-projected-to-2100.csv")
p = pd.read_csv(HERE / "data/pop.csv")
b.columns = ["entity", "code", "year", "d_e", "d_p", "b_e", "b_p"]
p.columns = ["entity", "code", "year", "p_e", "p_p"]
df = b.merge(p, on=["entity", "code", "year"])
df["deaths"] = df.d_e.fillna(df.d_p)
df["births"] = df.b_e.fillna(df.b_p)
df["pop"] = df.p_e.fillna(df.p_p)

world = df[df.entity == "World"].set_index("year")
c = df[df.code.fillna("").str.fullmatch(r"[A-Z]{3}")].copy()   # countries only
c["decline"] = c.deaths > c.births

share = (c.assign(pd_=c["pop"] * c.decline).groupby("year")
         .agg(pop_decl=("pd_", "sum"), pop=("pop", "sum"), n=("decline", "sum")))
share["share"] = share.pop_decl / share["pop"]

rows = []
for name, g in c.sort_values("year").groupby("entity"):
    dec, yrs = g.decline.to_numpy(), g.year.to_numpy()
    tip = None
    if dec[-1]:
        i = len(dec) - 1
        while i > 0 and dec[i - 1]:
            i -= 1
        tip = int(yrs[i])
    rows.append({"country": name, "code": g.code.iloc[0], "tip_year": tip,
                 "pop_2026": float(g.loc[g.year == TODAY, "pop"].iloc[0])})
tips = pd.DataFrame(rows)

world_tip = int(world.index[(world.deaths > world.births)].min())
s_now = share.loc[TODAY]
s_2050, s_2070 = share.loc[2050, "share"], share.loc[2070, "share"]
first_majority = int(share.index[share.share > 0.5].min())
india_tip = int(tips.set_index("country").loc["India", "tip_year"])

# Persist tidy outputs for anyone who wants to check the work.
share[["n", "share"]].round(4).to_csv(HERE / "data/share_by_year.csv")
tips.sort_values(["tip_year", "pop_2026"]).to_csv(HERE / "data/tipping_years.csv", index=False)

print(f"{TODAY}: {int(s_now.n)} countries, {s_now.share:.1%} of people in natural decrease")
print(f"2050: {s_2050:.1%}  2070: {s_2070:.1%}  first majority year: {first_majority}")
print(f"India tips {india_tip}; world tips {world_tip}; "
      f"never by 2100: {tips.tip_year.isna().sum()} countries, "
      f"{tips.loc[tips.tip_year.isna(), 'pop_2026'].sum() / 1e9:.2f}bn people today")

# ---------------------------------------------------------------- figure ----
apply()
fig = plt.figure(figsize=(12, 15.6), dpi=100)
X0, X1 = 1950, 2100

title_block(
    fig,
    "Deaths now outnumber births for more than one\n"
    "in four people on Earth. India decides when it's most.",
    f"Share of the world's population living in a country where more people die each year than are born.\n"
    f"{int(s_now.n)} countries are there in {TODAY}, led by China. The share creeps up for 35 years — then "
    f"India tips (~{india_tip})\nand natural decline becomes the majority human experience. "
    f"Migration aside, the world as a whole follows in {world_tip}.",
    kicker="Population · The tipping point",
)

# --- Panel A: share of humanity in natural decrease --------------------------
axA = fig.add_axes([0.075, 0.535, 0.86, 0.228])
hist = share.loc[:TODAY]
proj = share.loc[TODAY:]
axA.fill_between(hist.index, hist.share, step="mid", color=ACCENT, alpha=0.9, lw=0)
axA.fill_between(proj.index, proj.share, step="mid", color=ACCENT, alpha=0.32, lw=0)
axA.step(proj.index, proj.share, where="mid", color=ACCENT, lw=1.6)
axA.axvline(TODAY, color=INK, lw=1, zorder=5)
axA.text(TODAY + 1.2, 0.99, f"{TODAY}", color=INK, fontsize=10.5, weight="bold", va="top")
axA.text(TODAY + 1.2, 0.935, "UN projection →", color=INK_2, fontsize=10, va="top")
axA.axhline(0.5, color=INK_3, lw=0.9, ls=(0, (2, 3)))
axA.text(X0 + 1, 0.515, "half of humanity", color=INK_3, fontsize=9.5, va="bottom")
axA.set_xlim(X0, X1)
axA.set_ylim(0, 1)
axA.set_yticks([0, .25, .5, .75, 1])
axA.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axA.set_xticks(range(1950, 2101, 25))
axA.tick_params(axis="x", pad=6)


def note(ax, x, y, tx, ty, text, ha="left"):
    ax.annotate(text, (x, y), (tx, ty), fontsize=10, color=INK_2, ha=ha, va="center",
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-", color=INK_3, lw=0.8, shrinkA=2, shrinkB=1))


note(axA, 1960, share.loc[1960, "share"] + 0.01, 1964, 0.36,
     "China's Great Leap\nForward famine, 1959–61")
note(axA, 1997, share.loc[1997, "share"] + 0.01, 1980, 0.17,
     "Post-Soviet Russia,\nUkraine, Eastern Europe")
note(axA, 2021.5, share.loc[2022, "share"] + 0.01, 2000, 0.45,
     "China tips, 2021", ha="left")
axA.text(2000, 0.40, f"{s_now.share:.0%} of people, {int(s_now.n)} countries",
         fontsize=10, color=INK, weight="bold", va="center")
note(axA, india_tip, share.loc[india_tip, "share"] + 0.01, 2048, 0.80,
     f"India tips, ~{india_tip}", ha="right")
note(axA, world_tip, share.loc[world_tip, "share"] + 0.01, 2082, 0.84,
     f"Whole world\ntips, {world_tip}", ha="center")

axA.text(0, 1.06, "Share of world population living in a country with natural decrease",
         transform=axA.transAxes, fontsize=12, weight="bold", color=INK)

# --- Panel B: every country's tipping year -----------------------------------
axB = fig.add_axes([0.075, 0.08, 0.86, 0.37])
NEVER_X = 2112
t = tips.copy()
t["x"] = t.tip_year.fillna(NEVER_X).astype(float)
rng = np.random.default_rng(7)
t.loc[t.tip_year.isna(), "x"] += rng.uniform(-5, 5, t.tip_year.isna().sum())
t["s"] = np.clip(np.sqrt(t.pop_2026 / 1e6) * 9, 6, 1400)

past = t.tip_year.notna() & (t.tip_year <= TODAY)
future = t.tip_year.notna() & (t.tip_year > TODAY)
never = t.tip_year.isna()
kw = dict(edgecolors=SURFACE, linewidths=1.0, zorder=3)
axB.scatter(t.loc[past, "x"], t.loc[past, "pop_2026"], s=t.loc[past, "s"], c=ACCENT, alpha=.92, **kw)
axB.scatter(t.loc[future, "x"], t.loc[future, "pop_2026"], s=t.loc[future, "s"],
            facecolor="none", edgecolors=ACCENT, linewidths=1.6, zorder=3)
axB.scatter(t.loc[never, "x"], t.loc[never, "pop_2026"], s=t.loc[never, "s"], c=NEUTRAL, alpha=.95, **kw)

axB.set_yscale("log")
axB.set_ylim(8e3, 4e9)
axB.set_yticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
axB.set_yticklabels(["10k", "100k", "1M", "10M", "100M", "1B"])
axB.grid(axis="y", color=GRID)
axB.set_xlim(X0, 2122)
axB.set_xticks(list(range(1950, 2101, 25)) + [NEVER_X])
axB.set_xticklabels([str(v) for v in range(1950, 2101, 25)] + ["Not by\n2100"])
axB.axvline(TODAY, color=INK, lw=1, zorder=1)
axB.axvspan(2103.5, 2122, color="#f1f0ec", zorder=0, lw=0)
axB.set_ylabel("Population, 2026 (log scale)", color=INK_3, fontsize=10)

labels = {
    "China": (0, 15, "center"), "India": (0, 15, "center"), "United States": (0, 13, "center"),
    "Japan": (0, 11, "center"), "Germany": (0, 11, "center"), "Russia": (0, 11, "center"),
    "Italy": (0, -12, "center"), "South Korea": (0, -11, "center"), "Thailand": (-8, 0, "right"),
    "Brazil": (9, 0, "left"), "Indonesia": (0, 14, "center"), "Bangladesh": (0, 13, "center"),
    "Mexico": (9, -2, "left"), "Hungary": (0, -10, "center"), "Bulgaria": (0, -10, "center"),
    "Pakistan": (-16, 0, "right"),
}
ti = t.set_index("country")
for name, (dx, dy, ha) in labels.items():
    r = ti.loc[name]
    label = "Pakistan & Nigeria" if name == "Pakistan" else name
    axB.annotate(label, (r.x, r.pop_2026), xytext=(dx, dy), textcoords="offset points",
                 fontsize=9.5, color=INK_2 if not np.isnan(r.tip_year if r.tip_year is not None else np.nan) else INK_3,
                 ha=ha, va="center", zorder=4)

axB.text(0, 1.075, "The year each country tips into permanent natural decrease",
         transform=axB.transAxes, fontsize=12, weight="bold", color=INK)
axB.text(0, 1.035, "Circle area = population. Filled = already tipped · outlined = projected · "
         "gray = still growing naturally in 2100", transform=axB.transAxes, fontsize=10, color=INK_2)

n_never = int(never.sum())
pop_never = t.loc[never, "pop_2026"].sum() / 1e9
axB.text(2112.75, 1.0e4, f"{n_never} countries\n{pop_never:.1f}bn people\nmostly in\nsub-Saharan\nAfrica",
         fontsize=9, color=INK_2, ha="center", va="bottom", linespacing=1.3)

footer(fig,
       "Source: UN World Population Prospects 2024 (estimates to 2023, medium variant thereafter), via Our World in Data.\n"
       "Natural decrease = annual deaths exceed births; migration excluded. Tipping year = start of the last unbroken run "
       "of natural decrease through 2100.")

fig.savefig(HERE / "chart.png", dpi=150)
fig.savefig(HERE / "chart.svg")
print("saved")
