"""2026-11-12: The world's clocks run fast.

Question: when the clock says 12:00, where is the sun? For every city on Earth
with 15,000+ people, compute the clock time of solar noon (the moment the sun is
highest), averaged over 2026 so daylight-saving time counts for the months it
applies. Then weight by population.

Solar noon (UTC hours) = 12 − longitude/15 − EoT/60. Averaged over a full year
the equation of time (EoT) nets to ~0, so the annual-mean clock time of solar
noon = 12 − lon/15 + mean UTC offset. The offset comes from the IANA time-zone
database for each day of 2026.

Data: GeoNames cities15000 (CC BY 4.0), IANA tz database via Python zoneinfo.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix.style import (ACCENT, ACCENT_2, GRID, INK, INK_2, INK_3, NEUTRAL, SURFACE,  # noqa: E402
                       apply, footer, title_block)

YEAR = 2026
LATE, EARLY = ACCENT, ACCENT_2

# ---------------------------------------------------------------- data ------
c = pd.read_csv(HERE / "data/cities15000.csv", keep_default_na=False)
# China officially runs on Beijing time everywhere. The tz database gives
# Xinjiang its informal UTC+6, so override it to the legal time.
c.loc[c.tz == "Asia/Urumqi", "tz"] = "Asia/Shanghai"

days = [datetime(YEAR, 1, 1) + timedelta(d) for d in range(365)]


def offsets(tz: str) -> np.ndarray:
    z = ZoneInfo(tz)
    return np.array([datetime(d.year, d.month, d.day, 12, tzinfo=z).utcoffset().total_seconds() / 3600
                     for d in days])


tz_tab = pd.DataFrame({tz: offsets(tz) for tz in sorted(c.tz.unique())})
mean_off = tz_tab.mean()
std_off = tz_tab.min()                    # standard time = smallest offset in the year
c["noon_min"] = (-c.lon / 15 + c.tz.map(mean_off)) * 60      # minutes after 12:00, DST-averaged
c["noon_std_min"] = (-c.lon / 15 + c.tz.map(std_off)) * 60   # standard time only
w = c["pop"]
W = w.sum()


def share(mask) -> float:
    return w[mask].sum() / W


late30, early30 = share(c.noon_min >= 30), share(c.noon_min <= -30)
late60 = share(c.noon_min >= 60)
mean_min = np.average(c.noon_min, weights=w)
mean_std = np.average(c.noon_std_min, weights=w)
late_any = share(c.noon_min > 0)
late30_std = share(c.noon_std_min >= 30)

by_cc = (c.assign(wn=c.noon_min * w).groupby("cc")
         .agg(pop=("pop", "sum"), wn=("wn", "sum")))
by_cc["noon_min"] = by_cc.wn / by_cc["pop"]
by_cc = by_cc.drop(columns="wn").sort_values("pop", ascending=False)

c[["name", "cc", "lat", "lon", "pop", "tz", "noon_min", "noon_std_min"]].round(1) \
    .to_csv(HERE / "data/city_solar_noon.csv", index=False)
by_cc.round(1).to_csv(HERE / "data/country_solar_noon.csv")

print(f"cities: {len(c):,}  people: {W / 1e9:.2f}bn")
print(f"mean solar noon: {mean_min:+.1f} min (standard time only: {mean_std:+.1f})")
print(f"sun after clock noon: {late_any:.1%}")
print(f">=30 min late: {late30:.1%}  >=60 late: {late60:.1%}  >=30 early: {early30:.2%}  "
      f"ratio {late30 / early30:.0f}:1")
print(f">=30 late on standard time only: {late30_std:.1%}")
print(by_cc.head(20).round(1).to_string())

# ---------------------------------------------------------------- figure ----
apply()
fig = plt.figure(figsize=(12, 15.0), dpi=100)

title_block(
    fig,
    "The world's clocks run fast",
    f"When is the sun highest? The clock time of solar noon in {len(c):,} cities ({W / 1e9:.1f} billion people), averaged over {YEAR}.\n"
    f"{late30:.0%} of people see it at 12:30 or later. Only {early30:.0%} see it at 11:30 or earlier.",
    kicker="Time",
)

# --- Panel A: every city, longitude vs clock time of solar noon --------------
axA = fig.add_axes([0.085, 0.405, 0.85, 0.38])
s = np.clip(np.sqrt(c["pop"] / 1e3) * 1.1, 1.5, 450)
col = np.where(c.noon_min >= 30, LATE, np.where(c.noon_min <= -30, EARLY, NEUTRAL))
order = np.argsort(-c["pop"].to_numpy())          # big cities underneath
axA.scatter(c.lon.to_numpy()[order], c.noon_min.to_numpy()[order], s=s.to_numpy()[order],
            c=col[order], alpha=0.75, edgecolors=SURFACE, linewidths=0.4, zorder=3)
axA.axhspan(-30, 30, color="#f1f0ec", zorder=0, lw=0)
axA.axhline(0, color=INK, lw=1, zorder=2)
axA.set_xlim(-170, 180)
axA.set_ylim(-80, 195)
axA.set_yticks(range(-60, 181, 30))
axA.yaxis.set_major_formatter(FuncFormatter(
    lambda v, _: f"{12 + int(v) // 60}:{int(v) % 60:02d}" if v >= 0 else f"11:{60 + int(v):02d}" if v > -60 else "11:00"))
axA.set_xticks(range(-150, 181, 30))
axA.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{abs(int(v))}°{'W' if v < 0 else 'E' if v > 0 else ''}"))
axA.set_ylabel("Clock time when the sun is highest", color=INK_3, fontsize=10)
axA.text(-168, 3, "12:00 on the clock", fontsize=9.5, color=INK, va="bottom")
axA.text(-168, -27, "within ±30 min of true noon", fontsize=9, color=INK_3, va="bottom")
axA.text(0, 1.035, "Each dot is a city. The sawtooth comes from time zones. Long slopes are countries using one clock.",
         transform=axA.transAxes, fontsize=10, color=INK_2)
axA.text(0, 1.075, "Where the sun peaks, on the clock", transform=axA.transAxes,
         fontsize=12, weight="bold", color=INK)

ci = c.sort_values("pop", ascending=False).drop_duplicates("name").set_index("name")


def lab(name, dx, dy, text=None, ha="left"):
    r = ci.loc[name]
    m = int(round(r.noon_min))
    off = ("+" if m >= 0 else "−") + (f"{abs(m) // 60}h{abs(m) % 60:02d}" if abs(m) >= 60 else f"{abs(m)}m")
    text = (text or "{name} {off}").format(name=name, off=off)
    axA.annotate(text, (r.lon, r.noon_min), xytext=(dx, dy), textcoords="offset points",
                 fontsize=9.5, color=INK_2, ha=ha, va="center", zorder=5, linespacing=1.3,
                 arrowprops=dict(arrowstyle="-", color=INK_3, lw=0.7, shrinkA=0, shrinkB=2))


lab("Madrid", -16, 12, "Spain is on Berlin time\nMadrid {off}", ha="right")
lab("Paris", 18, 22, "Paris {off}")
lab("Kashgar", 12, 6, "Kashgar, on Beijing time {off}")
lab("Lhasa", 10, 18, "Lhasa {off}")
lab("Chengdu", 12, 24, "Chengdu {off}")
lab("Shanghai", 10, -28, "Shanghai {off}")
lab("Hegang", 10, -18, "NE China, sun early\nHegang {off}")
lab("Recife", 8, -20, "Recife {off}")
lab("Indianapolis", -8, 20, "Indianapolis {off}", ha="right")
lab("Novosibirsk", 4, 34, "Novosibirsk {off}")
lab("Mumbai", -10, 26, "India: one zone\nMumbai {off}", ha="right")
lab("Salta", 6, 26, "Argentina\nSalta {off}")
lab("Lagos", 16, -24, "Lagos {off}")

# --- Panel B: population-weighted distribution --------------------------------
axB = fig.add_axes([0.085, 0.105, 0.85, 0.19])
bins = np.arange(-60, 181, 10)
hist, edges = np.histogram(c.noon_min.clip(-59.9, 179.9), bins=bins, weights=w / 1e6)
mid = (edges[:-1] + edges[1:]) / 2
bcol = [LATE if m >= 30 else EARLY if m <= -30 else NEUTRAL for m in mid]
axB.bar(mid, hist, width=8.6, color=bcol, zorder=3)
axB.set_xlim(-62, 182)
axB.set_xticks(range(-60, 181, 30))
axB.xaxis.set_major_formatter(axA.yaxis.get_major_formatter())
axB.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.1f}bn" if v >= 1000 else f"{v:.0f}M"))
axB.axvline(0, color=INK, lw=1, zorder=4)
axB.text(0, 1.16, "How many people live at each offset", transform=axB.transAxes,
         fontsize=12, weight="bold", color=INK)
axB.text(0, 1.06, "People in cities, by when the sun peaks (10-minute bins)",
         transform=axB.transAxes, fontsize=10, color=INK_2)
ymax = hist.max()
axB.text(-58, ymax * 0.92, f"{early30:.1%}", fontsize=22, weight="bold", color=EARLY, va="top")
axB.text(-58, ymax * 0.74, "sun ≥30 min early", fontsize=10, color=INK_2, va="top")
axB.text(178, ymax * 0.92, f"{late30:.0%}", fontsize=22, weight="bold", color=LATE, va="top", ha="right")
axB.text(178, ymax * 0.74, f"sun ≥30 min late\n({late60:.0%} by an hour or more)", fontsize=10,
         color=INK_2, va="top", ha="right", linespacing=1.35)
axB.set_xlabel("Clock time when the sun is highest (annual average)", color=INK_3, fontsize=10)

footer(fig,
       f"Data: GeoNames cities ≥15,000 people (CC BY 4.0); IANA time-zone database ({YEAR} rules, DST averaged over the year). "
       "China set to its legal Beijing time.\nSolar noon from longitude; the equation of time averages out over a year. "
       "City populations only, about half of humanity.")

fig.savefig(HERE / "chart.png", dpi=150)
fig.savefig(HERE / "chart.svg")
print("saved")
