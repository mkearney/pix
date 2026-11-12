"""2026-11-11: The world's clocks run fast.

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
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

YEAR = 2026
LATE, EARLY = SIGNAL, INDIGO
NO = px.issue_number(HERE)

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
fig = px.plate(12, 15.6)
px.masthead(fig, "2026-11-11", NO)
deck_bottom = px.headline(
    fig, "Time · Sun vs. clock",
    "The world's clocks *run fast*",
    f"When is the sun highest? The clock time of solar noon in {len(c):,} cities ({W / 1e9:.1f} billion people),\n"
    f"averaged over {YEAR}. {late30:.0%} of people see it at 12:30 or later. Only {early30:.0%} see it at 11:30 or earlier.",
)


def hhmm(v, _=None):
    v = int(round(v))
    return f"{12 + v // 60}:{v % 60:02d}"


# --- 01: every city, longitude vs clock time of solar noon --------------------
top_A = deck_bottom - 0.07
axA = fig.add_axes([px.LEFT, 0.40, px.WIDTH, top_A - 0.40])
s = np.clip(np.sqrt(c["pop"] / 1e3) * 1.1, 1.5, 450)
col = np.where(c.noon_min >= 30, LATE, np.where(c.noon_min <= -30, EARLY, TAUPE))
order = np.argsort(-c["pop"].to_numpy())          # big cities underneath
axA.scatter(c.lon.to_numpy()[order], c.noon_min.to_numpy()[order], s=s.to_numpy()[order],
            c=col[order], alpha=0.8, edgecolors=PAPER, linewidths=0.4, zorder=3)
axA.axhspan(-30, 30, color=PAPER_2, zorder=0, lw=0)
axA.axhline(0, color=INK, lw=0.9, zorder=2)
axA.set_xlim(-170, 180)
axA.set_ylim(-80, 195)
axA.set_yticks(range(-60, 181, 30))
axA.yaxis.set_major_formatter(FuncFormatter(hhmm))
axA.set_xticks(range(-150, 181, 30))
axA.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{abs(int(v))}°{'W' if v < 0 else 'E' if v > 0 else ''}"))
axA.spines["bottom"].set_visible(False)
axA.tick_params(axis="x", length=0)
axA.text(-168, 3, "12:00 on the clock", fontsize=9.5, color=INK, va="bottom")
axA.text(-168, -27, "within 30 min of true noon", fontsize=9, color=INK_3, va="bottom")
px.panel(axA, 1, "Where the sun peaks, on the clock",
         "Each dot is a city. The sawtooth comes from time zones. Long slopes are countries using one clock.")
px.mono_ticks(axA)

ci = c.sort_values("pop", ascending=False).drop_duplicates("name").set_index("name")


def lab(name, dx, dy, text=None, ha="left"):
    r = ci.loc[name]
    m = int(round(r.noon_min))
    off = ("+" if m >= 0 else "−") + (f"{abs(m) // 60}h{abs(m) % 60:02d}" if abs(m) >= 60 else f"{abs(m)}m")
    px.note(axA, (r.lon, r.noon_min), (dx, dy), (text or "{name} {off}").format(name=name, off=off), ha=ha)


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

# --- 02: population-weighted distribution --------------------------------------
axB = fig.add_axes([px.LEFT, 0.115, px.WIDTH, 0.19])
bins = np.arange(-60, 181, 10)
hist, edges = np.histogram(c.noon_min.clip(-59.9, 179.9), bins=bins, weights=w / 1e6)
mid = (edges[:-1] + edges[1:]) / 2
bcol = [LATE if m >= 30 else EARLY if m <= -30 else TAUPE for m in mid]
axB.bar(mid, hist, width=8.4, color=bcol, zorder=3)
axB.set_xlim(-62, 182)
axB.set_xticks(range(-60, 181, 30))
axB.xaxis.set_major_formatter(FuncFormatter(hhmm))
axB.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.1f}bn" if v >= 1000 else f"{v:.0f}M"))
axB.axvline(0, color=INK, lw=0.9, zorder=4)
px.panel(axB, 2, "How many people live at each offset", "People in cities, by when the sun peaks (10-minute bins)")
px.big_number(axB, 0.015, 0.98, f"{early30:.1%}", "sun 30+ min early", color=EARLY)
px.big_number(axB, 0.985, 0.98, f"{late30:.0%}", f"sun 30+ min late\n({late60:.0%} by an hour or more)",
              color=LATE, ha="right")
axB.set_xlabel("Clock time when the sun is highest (annual average)")
px.mono_ticks(axB)

px.footer(fig,
          f"DATA  GeoNames cities of 15,000+ people (CC BY 4.0). IANA time-zone database, {YEAR} rules, DST averaged over the year.\n"
          "NOTE  Solar noon from longitude; the equation of time averages out over a year. China set to Beijing time.\n"
          "      City populations only, about half of humanity.",
          NO)

px.save(fig, HERE)
print("saved")
