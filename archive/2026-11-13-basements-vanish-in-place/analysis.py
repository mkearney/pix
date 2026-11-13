"""2026-11-13: The move South explains only a third of lost basements.

Question: the share of new US houses with a basement has fallen by more than half
since 2000. The easy explanation is geography: houses are increasingly built in the
South, where almost nobody digs one. How much of the fall is that, and how much is
builders dropping basements in places that used to have them?

Method: a shift-share decomposition of the national basement rate between 2000 and
2025 across the nine census divisions, using Survey of Construction microdata
(houses completed each year, weighted). The change in the national rate splits
exactly into a mix term (shift in where houses are built, valued at the average of
the two years' basement rates) and a within term (change in each division's rate,
weighted by its average share of houses).

Data: Census Bureau, Characteristics of New Housing (1971-2025 regional table) and
Survey of Construction microdata (1999-2025). See data/SOURCES.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-13"
A, B = 2000, 2025

DIVS = {
    1: ("New England", "ME to CT"),
    2: ("Middle Atlantic", "NY, NJ, PA"),
    3: ("East North Central", "OH, IN, IL, MI, WI"),
    4: ("West North Central", "MN, IA, MO, KS and others"),
    5: ("South Atlantic", "DE and MD to FL"),
    6: ("East South Central", "KY, TN, AL, MS"),
    7: ("West South Central", "TX, OK, AR, LA"),
    8: ("Mountain", "AZ, CO, UT, NV and others"),
    9: ("Pacific", "CA, WA, OR, AK, HI"),
}
NORTH = [1, 2, 3, 4]

# ---------------------------------------------------------------- data ------
reg = pd.read_csv(HERE / "data/census_foundation_by_region.csv")
us = reg[reg.region == "United States"].set_index("year")
us_rate = us.basement / us.total

soc = pd.read_csv(HERE / "data/soc_completions_by_division.csv")


def decompose(keys: list[str], a: int, b: int) -> dict:
    g = soc.groupby(["year"] + keys)[["units", "basement"]].sum()
    ga, gb = g.loc[a], g.loc[b]
    idx = ga.index.union(gb.index)
    ga, gb = ga.reindex(idx, fill_value=0), gb.reindex(idx, fill_value=0)
    wa, wb = ga.units / ga.units.sum(), gb.units / gb.units.sum()
    sa, sb = (ga.basement / ga.units).fillna(0), (gb.basement / gb.units).fillna(0)
    total = (wb * sb).sum() - (wa * sa).sum()
    mix = ((wb - wa) * (sa + sb) / 2).sum()
    within_parts = (sb - sa) * (wa + wb) / 2
    return dict(a=(wa * sa).sum(), b=(wb * sb).sum(), total=total, mix=mix,
                within=within_parts.sum(), parts=within_parts, wa=wa, wb=wb, sa=sa, sb=sb)


main = decompose(["div"], A, B)
by_type = decompose(["div", "det"], A, B)
base99 = decompose(["div"], 1999, B)

# Counterfactual series: each division keeps its 2000 basement rate; only the mix moves.
g = soc.groupby(["year", "div"])[["units", "basement"]].sum()
share = g.units.unstack()
share = share.div(share.sum(axis=1), axis=0)
rate = (g.basement / g.units).unstack()
mix_only = (share * rate.loc[A]).sum(axis=1)
actual_micro = (g.basement.unstack().sum(axis=1) / g.units.unstack().sum(axis=1))

# Long-run check on the published four-region table, 1975 (the 1970s peak) to 2025.
r4 = reg[reg.region != "United States"]
p4 = r4.pivot(index="year", columns="region", values="total")
s4 = r4.pivot(index="year", columns="region", values="basement") / p4
w4 = p4.div(p4.sum(axis=1), axis=0)
mix4 = ((w4.loc[B] - w4.loc[1975]) * (s4.loc[1975] + s4.loc[B]) / 2).sum()
tot4 = us_rate[B] - us_rate[1975]

parts = main["parts"] / main["total"]
north_within = parts.loc[NORTH].sum()
mix_share = main["mix"] / main["total"]
south_w = lambda w: w.loc[[5, 6, 7]].sum()  # noqa: E731
not_rep = soc.groupby("year").not_reported.sum() / soc.groupby("year").units.sum()

out = pd.DataFrame({
    "division": [DIVS[d][0] for d in main["sa"].index],
    f"basement_rate_{A}": main["sa"].values, f"basement_rate_{B}": main["sb"].values,
    f"share_of_houses_{A}": main["wa"].values, f"share_of_houses_{B}": main["wb"].values,
    "within_contribution_pts": main["parts"].values * 100,
    "share_of_decline": parts.values,
}, index=main["sa"].index)
out.round(4).to_csv(HERE / "data/decomposition_2000_2025.csv", index_label="div")
pd.DataFrame({"actual": actual_micro, "mix_only": mix_only}).round(4).to_csv(
    HERE / "data/counterfactual_series.csv", index_label="year")

print(f"Published table, US basement share: 1975 {us_rate[1975]:.1%}  {A} {us_rate[A]:.1%}  {B} {us_rate[B]:.1%}")
print(f"Microdata, US basement share: {A} {main['a']:.1%}  {B} {main['b']:.1%}  change {main['total'] * 100:+.1f} pts")
print(f"  mix (where houses are built): {main['mix'] * 100:+.1f} pts = {mix_share:.0%} of the fall")
print(f"  within divisions:             {main['within'] * 100:+.1f} pts = {main['within'] / main['total']:.0%}")
print(f"  of which the four northern divisions: {north_within:.0%}; South {parts.loc[[5, 6, 7]].sum():.0%}; "
      f"West {parts.loc[[8, 9]].sum():.0%}")
print(f"Counterfactual {B}, every division at its {A} rate: {mix_only[B]:.1%}")
print(f"South's share of new houses: {south_w(main['wa']):.1%} -> {south_w(main['wb']):.1%}")
print(f"Northern divisions' share of new houses: {main['wa'].loc[NORTH].sum():.1%} -> {main['wb'].loc[NORTH].sum():.1%}")
print(f"Sensitivity: division x detached/attached, mix share {by_type['mix'] / by_type['total']:.0%}; "
      f"1999 base, mix share {base99['mix'] / base99['total']:.0%}; "
      f"four regions 1975-{B} (published table), mix share {mix4 / tot4:.0%}")
print(f"Foundation not reported, max share of houses in any year: {not_rep.max():.1%}")
print(f"Sample: {int(soc[soc.year == A]['sample'].sum()):,} houses in {A}, {int(soc[soc.year == B]['sample'].sum()):,} in {B}")
print(out.assign(**{c: out[c].round(3) for c in out.columns if c != "division"}).to_string())

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Housing · Foundations",
    "The move South explains\n*only a third* of lost basements",
    f"In {A}, {main['a']:.0%} of new American houses had a basement. In {B}, {main['b']:.0%}. If each part of the country had\n"
    f"kept its {A} habits, the shift of building to the South would have cut that only to {mix_only[B]:.0%}. "
    "The rest is builders\ndropping basements where they used to be standard.",
)

# --- 01: national line + counterfactual ------------------------------------
B_BOT, B_H = 0.105, 0.30
top_A = deck_bottom - 0.075
hA = top_A - (B_BOT + B_H + 0.095)
axA = fig.add_axes([px.LEFT + 0.03, top_A - hA, px.WIDTH - 0.13, hA])
yrs = mix_only.index[mix_only.index >= A]
axA.fill_between(yrs, actual_micro.loc[yrs], mix_only.loc[yrs], color=PAPER_2, lw=0, zorder=1)
axA.plot(us_rate.index, us_rate.values, color=INK, lw=2.0, zorder=4, solid_capstyle="round")
axA.plot(yrs, mix_only.loc[yrs].values, color=TAUPE, lw=2.0, ls=(0, (4, 2)), zorder=3)
axA.scatter([A, B], [us_rate[A], us_rate[B]], s=36, color=INK, edgecolor=PAPER, lw=0.8, zorder=5)
axA.scatter([B], [mix_only[B]], s=36, color=TAUPE, edgecolor=PAPER, lw=0.8, zorder=5)
axA.text(B + 0.8, us_rate[B], f"{us_rate[B]:.0%}  actual", va="center", fontsize=10.5, color=INK,
         weight="semibold")
axA.text(B + 0.8, mix_only[B], f"{mix_only[B]:.0%}  geography only", va="center",
         fontsize=10, color=INK_2, linespacing=1.25)
axA.text(A, us_rate[A] + 0.022, f"{us_rate[A]:.0%}", ha="center", fontsize=10.5, color=INK, family=px.MONO)
axA.annotate(f"Builders dropping basements\nwithin each division: {main['within'] / main['total']:.0%} of the fall",
             xy=(2019.5, 0.25), xytext=(2005.5, 0.13), fontsize=10.5, color=SIGNAL, ha="left", va="center",
             linespacing=1.3, arrowprops=dict(arrowstyle="-", color=SIGNAL, lw=0.8, shrinkB=2))
axA.annotate(f"Building moves South:\n{mix_share:.0%} of the fall", xy=(2023, mix_only[2023] + 0.004),
             xytext=(2009.5, 0.36), fontsize=10.5, color=INK_2, ha="left", va="center", linespacing=1.3,
             arrowprops=dict(arrowstyle="-", color=INK_3, lw=0.7, shrinkB=2))
axA.set_xlim(1970, B)
axA.set_ylim(0, 0.5)
axA.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axA.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
axA.set_xticks([1971, 1980, 1990, 2000, 2010, 2025])
axA.grid(axis="y")
for s in ("top", "right", "left"):
    axA.spines[s].set_visible(False)
axA.tick_params(axis="y", length=0)
px.panel(axA, 1, "Share of new single-family houses with a full or partial basement",
         f"Solid: actual. Dashed: every division keeps its {A} basement rate and only the location of building changes.")
px.mono_ticks(axA)

# --- 02: dumbbell by division ----------------------------------------------
axB = fig.add_axes([px.LEFT + 0.25, B_BOT, px.WIDTH - 0.47, B_H])
col = mpl.transforms.blended_transform_factory(fig.transFigure, axB.transData)
order = main["sa"].sort_values(ascending=True).index
for i, d in enumerate(order):
    a, b = main["sa"][d], main["sb"][d]
    hi = d in NORTH or d == 5
    c = SIGNAL if hi else TAUPE
    axB.plot([b, a], [i, i], color=c, lw=2.0 if hi else 1.2, zorder=2, solid_capstyle="round")
    axB.scatter([a], [i], s=34, color=PAPER, edgecolor=INK_3, lw=1.0, zorder=3)
    axB.scatter([b], [i], s=44, color=c, edgecolor=PAPER, lw=0.8, zorder=4)
    name, states = DIVS[d]
    axB.text(-0.03, i + 0.13, name, ha="right", va="center", fontsize=10.5,
             color=INK if hi else INK_2, weight="semibold" if hi else "normal",
             transform=axB.get_yaxis_transform())
    axB.text(-0.03, i - 0.25, states, ha="right", va="center", fontsize=8.5, color=INK_3,
             transform=axB.get_yaxis_transform())
    axB.text(0.80, i, f"{main['wa'][d]:.0%} → {main['wb'][d]:.0%}", ha="center", va="center", fontsize=9.5,
             family=px.MONO, color=INK_2, transform=col)
    axB.text(px.RIGHT, i, f"{parts[d]:.0%}", ha="right", va="center", fontsize=9.5, family=px.MONO,
             color=INK if hi else INK_3, weight="medium" if hi else "normal", transform=col)
top = len(order) - 0.35
axB.text(0.80, top, "SHARE OF HOUSES", ha="center", va="bottom", fontsize=8, family=px.MONO, color=INK_2,
         transform=col)
axB.text(px.RIGHT, top, "OF THE FALL", ha="right", va="bottom", fontsize=8, family=px.MONO, color=INK_2,
         transform=col)
i_ne = list(order).index(1)
axB.text(main["sa"][1], i_ne + 0.42, str(A), ha="center", va="bottom", fontsize=8.5, color=INK_3, family=px.MONO)
axB.text(main["sb"][1], i_ne + 0.42, str(B), ha="center", va="bottom", fontsize=8.5, color=SIGNAL, family=px.MONO)
axB.set_xlim(0, 1)
axB.set_ylim(-0.7, len(order) - 0.3)
axB.set_yticks([])
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axB.grid(axis="x")
for s in ("top", "right", "left"):
    axB.spines[s].set_visible(False)
px.panel(axB, 2, "Basement rate by census division, 2000 and 2025",
         "Right: each division's share of new houses, and how much of the national fall its own drop explains.",
         pad=0.42)
for t, x in zip(fig.texts[-3:], (px.LEFT + 0.03, px.LEFT + 0.062, px.LEFT + 0.062)):
    t.set_x(x)                       # align the heading with panel 01, not the indented axes
px.mono_ticks(axB)

px.footer(fig,
          "DATA  US Census Bureau, Survey of Construction microdata 1999-2025 (houses completed, weighted);\n"
          "      Characteristics of New Housing, 1971-2025. Single-family houses, detached and attached.\n"
          f"NOTE  Shift-share across nine divisions. Splitting detached and attached gives {by_type['mix'] / by_type['total']:.0%} for the mix.",
          NO)

px.save(fig, HERE)
print("saved")
