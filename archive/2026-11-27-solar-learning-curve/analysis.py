"""2026-11-27: Solar panel prices fell 24% per doubling of capacity.

Finding (dose-response): the price of solar photovoltaic modules has fallen by
a roughly constant share each time the world's cumulative installed capacity
doubled (a learning curve, or Wright's law). Fitting the 1975-2025 series gives
a learning rate of 24% per doubling, in line with the 23% average across 13
studies reviewed by Rubin et al. (Energy Policy 2015).

Data: Our World in Data series combining Nemet (2009), Farmer & Lafond (2016)
and IRENA module prices (constant 2025 US$ per watt) with Nemet and IRENA
cumulative capacity. The fit is checked against the published range.
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
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-27"

# ---------------------------------------------------------------- data ------
d = pd.read_csv(HERE / "data/solar-pv-prices-vs-cumulative-capacity.csv").dropna()
d = d[d.entity == "World"].sort_values("year").reset_index(drop=True)
d["gw"] = d.cumulative_capacity / 1000
rubin = re.sub(r"\s+", " ", (HERE / "data/rubin_2015_excerpt.txt").read_text())
assert "Solar PV 13 3 10 –47% 23%" in rubin
assert "average learning rates for one-factor models were 12% and 23%" in rubin
assert "from 32% to 14% over periods from 1976 to 2006" in rubin
RUBIN_LO, RUBIN_HI, RUBIN_MEAN = 0.10, 0.47, 0.23


def fit(a: int, b: int) -> dict:
    x = d[(d.year >= a) & (d.year <= b)]
    X, Y = np.log2(x.cumulative_capacity.values), np.log2(x.cost.values)
    (s, i), cov = np.polyfit(X, Y, 1, cov=True)
    se = np.sqrt(cov[0, 0])
    return dict(a=a, b=b, slope=s, icpt=i, lr=1 - 2 ** s, lo=1 - 2 ** (s + 1.96 * se), hi=1 - 2 ** (s - 1.96 * se),
                doublings=X[-1] - X[0], n=len(x))


full = fit(1975, 2025)
early = fit(1975, 2010)
late = fit(2010, 2025)
assert RUBIN_LO <= full["lr"] <= RUBIN_HI and abs(full["lr"] - RUBIN_MEAN) < 0.03   # consistent with the review

p0, p1 = d.iloc[0], d.iloc[-1]
drop = 1 - p1.cost / p0.cost
print(f"OWID series {int(p0.year)}-{int(p1.year)}: module price ${p0.cost:.2f}/W -> ${p1.cost:.2f}/W (2025 US$), "
      f"down {drop:.1%}; cumulative capacity {p0.cumulative_capacity:.2f} MW -> {p1.gw:,.0f} GW, "
      f"{full['doublings']:.1f} doublings")
for f, name in ((full, "all years"), (early, "to 2010"), (late, "from 2010")):
    print(f"learning rate {f['a']}-{f['b']} ({name}): {f['lr']:.1%} per doubling (95% CI {f['lo']:.1%}-{f['hi']:.1%}), "
          f"{f['doublings']:.1f} doublings, n={f['n']}")
print(f"Rubin et al. 2015 review of 13 solar PV studies: one-factor learning rates {RUBIN_LO:.0%}-{RUBIN_HI:.0%}, "
      f"mean {RUBIN_MEAN:.0%}")
for y in (1975, 1990, 2000, 2010, 2020, 2025):
    r = d[d.year == y].iloc[0]
    print(f"  {y}: ${r.cost:.2f}/W at {r.gw:,.3f} GW")

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 16.4)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Technology · Solar power",
    "Solar panel prices fell 24%\nper *doubling of capacity*",
    f"Each time the world's installed solar capacity doubled, module prices fell by about a quarter. Over {full['doublings']:.0f}\n"
    f"doublings since 1975, a watt of panel went from ${p0.cost:.0f} to {p1.cost * 100:.0f} cents, in 2025 dollars.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Learning curve fitted to\nmodule prices, 1975–2025"),
    ("Sample", "Global module prices and\ncumulative capacity, 50 years"),
    ("Source", "Our World in Data from Nemet,\nFarmer & Lafond, IRENA"),
    ("Consistent with", "Rubin et al. 2015 (13 studies, 23%)\nIPCC AR6 2022 · Kavlak et al. 2018"),
], widths=[0.24, 0.26, 0.24, 0.26])

# --- 01: log-log learning curve ----------------------------------------------------
top1 = y - 0.07
h1 = 0.29
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.12, h1])
xs = np.logspace(np.log10(d.cumulative_capacity.min()), np.log10(d.cumulative_capacity.max()), 50)
ax.plot(xs / 1000, 2 ** (full["icpt"] + full["slope"] * np.log2(xs)), color=INK_3, lw=1.2, ls=(0, (4, 3)), zorder=2)
ax.scatter(d.gw, d.cost, s=26, color=SIGNAL, edgecolor=PAPER, lw=0.6, zorder=3)
for yv, dx, dy, ha in [(1975, 6, 4, "left"), (1990, 6, 4, "left"), (2000, 6, 4, "left"), (2010, 6, 4, "left"),
                       (2020, -10, 8, "right"), (2025, -4, -14, "right")]:
    r = d[d.year == yv].iloc[0]
    ax.annotate(f"{yv}  ${r.cost:.2f}" if r.cost < 10 else f"{yv}  ${r.cost:.0f}", (r.gw, r.cost),
                xytext=(dx, dy), textcoords="offset points", fontsize=9.5, family=px.MONO, color=INK, ha=ha)
mid = 10 ** ((np.log10(d.cumulative_capacity.min()) + np.log10(d.cumulative_capacity.max())) / 2)
ax.text(mid / 1000 * 3, 2 ** (full["icpt"] + full["slope"] * np.log2(mid * 3)) * 4.5,
        f"Fitted line: about −{full['lr']:.0%} per doubling\n(naive regression CI {full['lo']:.0%}–{full['hi']:.0%})", fontsize=10.5,
        color=INK_2, ha="left")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(2e-4, 1e4)
ax.set_ylim(0.06, 300)
ax.xaxis.set_major_locator(FixedLocator([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, 1e4]))
ax.xaxis.set_minor_locator(NullLocator())
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.3f}".rstrip("0").rstrip(".") if v < 1 else f"{v:,.0f}"))
ax.yaxis.set_major_locator(FixedLocator([0.1, 1, 10, 100]))
ax.yaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:g}"))
ax.grid(axis="y")
ax.set_xlabel("Cumulative installed solar capacity, gigawatts (log scale)")
ax.set_ylabel("Module price per watt, 2025 US$ (log)")
px.mono_ticks(ax)
px.panel(ax, 1, "Module price against cumulative capacity, world, 1975–2025",
         "One dot per year. A straight line on these log axes would mean a constant percentage fall per doubling.", pad=0.55)

# --- 02: learning rate by period vs literature -------------------------------------
top2 = top1 - h1 - 0.12
h2 = 0.11
ax2 = fig.add_axes([px.LEFT + 0.22, top2 - h2, px.WIDTH - 0.22 - 0.2, h2])
ax2.axvspan(RUBIN_LO * 100, RUBIN_HI * 100, color=PAPER_2, lw=0, zorder=0)
ax2.axvline(RUBIN_MEAN * 100, color=INK_3, lw=1, ls=(0, (4, 3)), zorder=1)
ax2.text(RUBIN_MEAN * 100 + 0.6, 2.62, f"Review average {RUBIN_MEAN:.0%}", fontsize=9, color=INK_2, va="bottom")
ax2.text(RUBIN_LO * 100 + 0.6, 2.62, f"13 studies: {RUBIN_LO:.0%}–{RUBIN_HI:.0%}", fontsize=9, color=INK_3,
         va="bottom", ha="left")
rows = [(full, "1975–2025", SIGNAL), (early, "1975–2010", TAUPE), (late, "2010–2025", TAUPE)]
for i, (f, lab, col) in enumerate(rows):
    yy = 2 - i
    ax2.plot([f["lo"] * 100, f["hi"] * 100], [yy, yy], color=col if col == SIGNAL else INK_2, lw=2, zorder=3)
    ax2.scatter([f["lr"] * 100], [yy], s=70, marker="s", color=col, edgecolor=PAPER, lw=0.8, zorder=4)
    ax2.text(f["hi"] * 100 + 1, yy, f"{f['lr']:.0%}", fontsize=12, family=px.MONO, va="center",
             color=SIGNAL if col == SIGNAL else INK_2)
    ax2.text(-0.02, yy, lab, transform=ax2.get_yaxis_transform(), ha="right", va="center", fontsize=11, color=INK)
ax2.set_xlim(0, 50)
ax2.set_ylim(-0.7, 3.1)
ax2.set_yticks([])
ax2.set_xticks([0, 10, 20, 30, 40, 50])
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax2.grid(axis="x")
ax2.set_xlabel("Price fall per doubling of capacity (fit, naive 95% regression CI)")
px.mono_ticks(ax2)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "Learning rate by period, against published estimates",
         "Shaded: one-factor solar PV learning rates in 13 studies reviewed by Rubin et al. (2015), mostly of modules.", pad=0.55)

px.footer(fig,
          "DATA  Our World in Data, solar PV prices vs cumulative capacity (Nemet 2009; Farmer & Lafond 2016; IRENA 2025, 2026).\n"
          "      Fit: least squares of log price on log cumulative capacity. Rubin et al., Energy Policy 86:198 (2015), Table 1.\n"
          "NOTE  Module prices. From 2010, European benchmark prices (thin-film until 2013); 2023–25 include oversupply. Association, not cause.",
          NO)
px.save(fig, HERE)
print("saved")
