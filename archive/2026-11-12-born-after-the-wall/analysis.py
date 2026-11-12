"""2026-11-12: Most people alive were born after the Berlin Wall fell.

Question: what share of people alive today were born after 9 Nov 1989? And how
does that differ by country?

Method: UN WPP 2024 population by single year of age on 1 July 2026. Everyone
aged a on that date was born in the year ending 1 July (2026 - a). Births are
spread evenly over that year, so the share of an age group born after date t is
clip((2026.5 - a) - t, 0, 1). Sum over ages, weighted by population.
Deaths between birth and now are already in the data: these are people alive.

Data: UN World Population Prospects 2024 (CC BY 3.0 IGO).
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-12"
REF = 2026.5  # WPP populations are for 1 July


def frac_year(d: date) -> float:
    start = date(d.year, 1, 1)
    return d.year + (d - start).days / (date(d.year + 1, 1, 1) - start).days


WALL = frac_year(date(1989, 11, 9))
EVENTS = [
    ("Moon landing", date(1969, 7, 20)),
    ("Chernobyl", date(1986, 4, 26)),
    ("Berlin Wall falls", date(1989, 11, 9)),
    ("Soviet Union ends", date(1991, 12, 26)),
    ("9/11", date(2001, 9, 11)),
    ("Covid pandemic", date(2020, 3, 11)),
]

# ---------------------------------------------------------------- data ------
d = pd.read_csv(HERE / "data/wpp2024_single_age_2026.csv", keep_default_na=False)


def share_after(g: pd.DataFrame, t: float) -> float:
    frac = np.clip((REF - g.age.to_numpy()) - t, 0, 1)
    return float((g.pop_thousands.to_numpy() * frac).sum() / g.pop_thousands.sum())


world = d[d.iso3 == "WLD"]
W = world.pop_thousands.sum() * 1e3
w_share = share_after(world, WALL)

rows = []
for (iso, name), g in d[d.iso3 != "WLD"].groupby(["iso3", "location"]):
    rows.append({"iso3": iso, "country": name, "pop": g.pop_thousands.sum() * 1e3,
                 "share_after_wall": share_after(g, WALL)})
c = pd.DataFrame(rows).sort_values("share_after_wall")
c.round({"pop": 0, "share_after_wall": 4}).to_csv(HERE / "data/country_share.csv", index=False)

years = np.arange(1925, 2026.6, 0.25)
curve = pd.DataFrame({"year": years, "share_born_after": [share_after(world, t) for t in years]})
curve.round(4).to_csv(HERE / "data/world_curve.csv", index=False)

ev = [(n, frac_year(dt), share_after(world, frac_year(dt))) for n, dt in EVENTS]

# half of everyone alive was born after this date
lo, hi = 1950.0, 2026.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if share_after(world, mid) > 0.5 else (lo, mid)
half_year = lo
half_date = date(int(half_year), 1, 1) + pd.Timedelta(days=(half_year % 1) * 365.25)

minority = c[c.share_after_wall < 0.5]
n_min = len(minority)
min_pop = minority["pop"].sum()
born_after_n = w_share * W

big = c[c["pop"] >= 50e6].sort_values("share_after_wall")
big_min = big[big.share_after_wall < 0.5]
big_min_pop = big_min["pop"].sum()
dev = c.set_index("iso3")

print(f"world population mid-2026: {W / 1e9:.2f}bn")
print(f"born after the Wall fell: {w_share:.1%} = {born_after_n / 1e9:.2f}bn")
print(f"half of everyone alive was born after: {half_date:%d %b %Y} ({half_year:.2f})")
for n, t, s in ev:
    print(f"  born after {n:<20} {s:6.1%}")
print(f"countries where most were born before the Wall fell: {n_min} of {len(c)}, "
      f"holding {min_pop / 1e9:.2f}bn = {min_pop / W:.1%} of people")
print(f"of countries 50M+: {len(big_min)} of {len(big)} have a minority born after, "
      f"{big_min_pop / 1e9:.2f}bn people")
for iso in ["DEU", "JPN", "ITA", "KOR", "CHN", "USA", "RUS", "GBR", "FRA", "IND", "NGA", "PAK", "NER", "HKG"]:
    r = dev.loc[iso]
    print(f"  {r.country:<28} {r.share_after_wall:6.1%}")
print("lowest (1M+):")
print(c[c["pop"] >= 1e6].head(6)[["country", "share_after_wall"]].round(3).to_string(index=False))
print("highest (1M+):")
print(c[c["pop"] >= 1e6].tail(4)[["country", "share_after_wall"]].round(3).to_string(index=False))

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 18)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Demography · Born after",
    "Most people alive were born\n*after the Berlin Wall fell*",
    f"The Wall came down 37 years ago this week. {w_share:.0%} of the {W / 1e9:.1f} billion people alive today were born\n"
    f"after that. In Germany it's {dev.loc['DEU'].share_after_wall:.0%}.",
)

# --- 01: the world curve -----------------------------------------------------
top_A = deck_bottom - 0.06
hA = 0.20
axA = fig.add_axes([px.LEFT, top_A - hA, px.WIDTH, hA])
axA.fill_between(curve.year, curve.share_born_after, color=PAPER_2, lw=0, zorder=1)
axA.plot(curve.year, curve.share_born_after, color=INK, lw=1.4, zorder=3)
axA.set_xlim(1925, 2027)
axA.set_ylim(0, 1.02)
axA.set_yticks([0, 0.25, 0.5, 0.75, 1])
axA.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axA.set_xticks(range(1930, 2030, 10))
axA.axhline(0.5, color=INK_3, lw=0.6, ls=(0, (1, 2)), zorder=2)
axA.grid(axis="y")
OFF = {
    "Moon landing": (-12, -14, "right"),
    "Chernobyl": (-16, -4, "right"),
    "Berlin Wall falls": (0, 0, "left"),
    "Soviet Union ends": (16, 14, "left"),
    "9/11": (12, 10, "left"),
    "Covid pandemic": (-12, -12, "right"),
}
for n, t, s in ev:
    if n == "Berlin Wall falls":
        axA.scatter([t], [s], s=70, color=SIGNAL, edgecolor=PAPER, lw=1, zorder=5)
        continue
    axA.scatter([t], [s], s=26, color=TAUPE, edgecolor=PAPER, lw=0.8, zorder=4)
    dx, dy, ha = OFF[n]
    px.note(axA, (t, s), (dx, dy), f"{n} {s:.0%}", ha=ha, size=9.5)
axA.plot([WALL, WALL], [0, w_share], color=SIGNAL, lw=1, ls=(0, (2, 2)), zorder=4)
px.big_number(axA, 0.70, 0.98, f"{w_share:.0%}",
              f"of people alive were born after\n9 Nov 1989, about {born_after_n / 1e9:.1f} billion people")
axA.text(1926, 0.515, f"Half of everyone alive was born after {half_date:%B %Y}", fontsize=9, color=INK_3,
         va="bottom", ha="left")
px.panel(axA, 1, "Share of everyone alive who was born after each date",
         "Read along the line: pick a year, see how many people alive today came later")
px.mono_ticks(axA)

# --- 02: countries -----------------------------------------------------------
NAME = {"United States of America": "United States", "Russian Federation": "Russia",
        "Iran (Islamic Republic of)": "Iran", "Democratic Republic of the Congo": "DR Congo",
        "United Republic of Tanzania": "Tanzania", "Viet Nam": "Vietnam", "Republic of Korea": "South Korea",
        "Türkiye": "Turkey"}
top_B = top_A - hA - 0.11
axB = fig.add_axes([px.LEFT + 0.16, 0.115, px.WIDTH - 0.32, top_B - 0.115])
y = np.arange(len(big))
vals = big.share_after_wall.to_numpy()
col = np.where(vals < 0.5, SIGNAL, TAUPE)
axB.axvspan(0.25, 0.5, color=PAPER_2, lw=0, zorder=0)
for yi, v in zip(y, vals):
    axB.plot([0.5, v], [yi, yi], color=INK_3 if v >= 0.5 else SIGNAL, lw=0.8, alpha=0.6, zorder=2)
axB.scatter(vals, y, s=60, c=col, edgecolor=PAPER, lw=0.8, zorder=4)
axB.axvline(0.5, color=INK, lw=0.8, zorder=3)
axB.axvline(w_share, color=INK_3, lw=0.7, ls=(0, (1, 2)), zorder=3)
axB.text(w_share + 0.006, 1.0, f"World {w_share:.0%}", fontsize=9, color=INK_2, ha="left", va="center",
         family=px.MONO)
axB.set_xlim(0.25, 0.9)
axB.set_ylim(-0.7, len(big) + 0.6)
axB.set_yticks([])
axB.set_xticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axB.grid(axis="x")
axB.grid(axis="y", visible=False)
for yi, (_, r) in zip(y, big.iterrows()):
    is_de = r.iso3 == "DEU"
    axB.text(0.245, yi, NAME.get(r.country, r.country), ha="right", va="center",
             fontsize=10.5, color=INK, weight="semibold" if is_de else "normal")
    axB.text(0.905, yi, f"{r.share_after_wall:.0%}", ha="left", va="center", fontsize=9.5,
             family=px.MONO, color=SIGNAL if r.share_after_wall < 0.5 else INK_3)
axB.text(0.49, len(big) - 0.1, "Most born before", ha="right", va="bottom", fontsize=9.5, color=SIGNAL)
axB.text(0.51, len(big) - 0.1, "Most born after", ha="left", va="bottom", fontsize=9.5, color=INK_3)
px.panel(axB, 2, f"The {len(big)} countries with 50 million people or more",
         f"Share born after the Wall fell. In {n_min} countries, holding {min_pop / W:.0%} of humanity, "
         "it's under half.")
px.mono_ticks(axB)

px.footer(fig,
          "DATA  UN World Population Prospects 2024, population by single year of age, 1 July 2026 (CC BY 3.0 IGO).\n"
          "NOTE  Births spread evenly within each year of age. Shares are of people alive now, so they\n"
          "      already reflect who has died. Later 2026 births and deaths are ignored.",
          NO)

px.save(fig, HERE)
print("saved")
