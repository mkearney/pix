"""2026-11-09: Four earthquakes released half this century's quake energy.

Question: of all the energy released by big earthquakes (magnitude 6+) since
2000, how much came from the very biggest few?

Radiated seismic energy follows log10(E) = 1.5 M + 4.8 (E in joules,
Gutenberg-Richter). Each whole step in magnitude is ~32x more energy.

Data: USGS ComCat, all events M6+ from 2000-01-01 to 2026-11-01.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INK, INK_3, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-09"

# ---------------------------------------------------------------- data ------
q = pd.read_csv(HERE / "data/usgs_m6_2000_2026.csv")
q = q[q.type == "earthquake"].copy()
q["time"] = pd.to_datetime(q.time, utc=True).dt.tz_localize(None)
q["E"] = 10 ** (1.5 * q.mag + 4.8)          # joules
TOT = q.E.sum()

r = q.sort_values("E", ascending=False).reset_index(drop=True)
r["cum"] = r.E.cumsum() / TOT
n_half = int((r.cum < 0.5).sum()) + 1
n_90 = int((r.cum < 0.9).sum()) + 1
top4 = r.head(4)
share4 = top4.E.sum() / TOT
share_m8 = q.E[q.mag >= 8].sum() / TOT
n_m8 = int((q.mag >= 8).sum())
bottom_half_n = len(q) // 2
share_bottom_half = r.tail(bottom_half_n).E.sum() / TOT
ratio_counts = ((q.mag >= 6) & (q.mag < 7)).sum() / ((q.mag >= 7) & (q.mag < 8)).sum()

t = q.sort_values("time").reset_index(drop=True)
t["cum"] = t.E.cumsum() / TOT

days = r.head(n_half)[["time", "mag", "place"]].copy()
days["share"] = r.head(n_half).E / TOT
days.to_csv(HERE / "data/biggest_quakes.csv", index=False)
r[["time", "mag", "place", "E", "cum"]].to_csv(HERE / "data/quakes_ranked.csv", index=False)

print(f"quakes M6+: {len(q):,}  ({q.time.min():%Y-%m-%d} to {q.time.max():%Y-%m-%d})")
print(f"top 4 share: {share4:.1%}  quakes for 50%: {n_half}  for 90%: {n_90} ({n_90 / len(q):.1%} of quakes)")
print(f"M8+: {n_m8} quakes = {share_m8:.1%}")
print(f"bottom half of quakes ({bottom_half_n:,}): {share_bottom_half:.2%}")
print(f"M6-7 vs M7-8 count ratio: {ratio_counts:.1f}x")
print(f"one M9.1 = {10 ** (1.5 * 3.1):,.0f} M6.0s")
print(days.assign(share=lambda d: (d.share * 100).round(1)).to_string())

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 14.6)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Natural world · Earthquakes",
    "Four earthquakes released *half*\nthis century’s quake energy",
    f"USGS logged {len(q):,} earthquakes of magnitude 6 or more since 2000. Ranked by the energy they released,\n"
    f"the top four account for {share4:.0%} of it. The other {len(q) - 4:,} share the rest.",
)

# --- 01: cumulative staircase over time --------------------------------------
top_A = deck_bottom - 0.065
axA = fig.add_axes([px.LEFT, 0.43, px.WIDTH, top_A - 0.43])
axA.step(t.time, t.cum, where="post", color=SIGNAL, lw=2, zorder=3)
axA.fill_between(t.time, t.cum, step="post", color=PAPER_2, zorder=1, lw=0)
axA.set_ylim(0, 1.04)
axA.set_xlim(pd.Timestamp("2000-01-01"), pd.Timestamp("2026-12-31"))
axA.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axA.set_yticks([0, 0.25, 0.5, 0.75, 1])
axA.xaxis.set_major_locator(mdates.YearLocator(5))
axA.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
px.panel(axA, 1, "Running total of energy released, 2000 to 2026",
         "Share of all the energy from magnitude 6+ quakes. Each jump is one quake.")
px.mono_ticks(axA)

LBL = {"Tohoku": ("Japan (Tohoku)", (-14, 40), "right"), "Sumatra": ("Sumatra", (-14, 30), "right"),
       "Maule": ("Chile (Maule)", (26, -46), "left"), "Kamchatka": ("Kamchatka, Russia", (-14, 30), "right")}
for i, row in top4.iterrows():
    key = next(k for k in LBL if k in row.place)
    name, off, ha = LBL[key]
    k = t.index[t.time == row.time][0]
    y_after = t.cum.iloc[k]
    y_before = t.cum.iloc[k - 1] if k > 0 else 0
    axA.vlines(row.time, y_before, y_after, color=SIGNAL, lw=3.2, zorder=4)
    px.note(axA, (row.time, (y_before + y_after) / 2), off,
            f"{row.time:%b %Y}  M{row.mag:.1f}  {name}\n+{row.E / TOT:.0%} of the total", ha=ha)

# --- 02: rank curve ------------------------------------------------------------
axB = fig.add_axes([px.LEFT, 0.115, px.WIDTH, 0.21])
x = np.arange(1, len(r) + 1)
axB.plot(x, r.cum, color=INK, lw=1.2, zorder=3)
axB.scatter(x[:4], r.cum[:4], s=40, color=SIGNAL, zorder=4, edgecolors="white", linewidths=0.6)
axB.set_xscale("log")
axB.set_xlim(0.8, len(r) * 1.3)
axB.set_ylim(0, 1.04)
axB.set_yticks([0, 0.5, 1])
axB.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
axB.axhline(0.5, color=INK_3, lw=0.6, ls=(0, (1, 2)))
axB.axhline(0.9, color=INK_3, lw=0.6, ls=(0, (1, 2)))
px.note(axB, (4, r.cum[3]), (26, -16), f"top 4: {share4:.0%}")
px.note(axB, (n_90, 0.9), (22, -22), f"{n_90} quakes reach 90%")
axB.text(len(r) * 1.2, 0.95, f"all {len(q):,}", ha="right", va="top", fontsize=9.5, color=INK_3)
axB.set_xlabel("Quakes, ranked from biggest (log scale)")
px.panel(axB, 2, "How few quakes it takes",
         "Cumulative share of energy, adding quakes from the biggest down")
px.mono_ticks(axB)
px.big_number(axB, 0.985, 0.62, f"{share_bottom_half:.1%}",
              f"the smaller half of all\n{len(q):,} quakes, combined", color=TAUPE, ha="right")

px.footer(fig,
          "DATA  USGS ComCat earthquake catalogue, magnitude 6.0+, 1 Jan 2000 to 1 Nov 2026.\n"
          "NOTE  Energy from log10(E) = 1.5M + 4.8. Quakes under M6 are left out; each step down in magnitude\n"
          "      is about 32x less energy but only about 10x as common, so they add little.",
          NO)
px.save(fig, HERE)
print("saved")
