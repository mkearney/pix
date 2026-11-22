"""2026-11-22: Global warming rises in step with total CO2 emitted.

Finding (dose-response): warming is close to proportional to the total amount
of CO2 humans have emitted. The IPCC (AR6 WG1 SPM, D.1.1) assesses 0.45°C per
1000 GtCO2, likely 0.27 to 0.63°C, and calls the relationship near-linear.

Data: cumulative CO2 including land use (Global Carbon Budget via OWID) and
HadCRUT5 global temperature, re-based to 1850-1900. The IPCC numbers are
checked against the saved SPM text, and the Global Carbon Budget total for
1850-2019 is checked against the IPCC's 2390 +/- 240 GtCO2.
"""
from __future__ import annotations

import re
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
DATE = "2026-11-22"
TCRE, TCRE_LO, TCRE_HI = 0.45, 0.27, 0.63   # °C per 1000 GtCO2, IPCC AR6 SPM D.1.1

# ---------------------------------------------------------------- data ------
spm = re.sub(r"\s+", " ", (HERE / "data/ipcc_ar6_wg1_spm_D1.txt").read_text())
assert "near-linear relationship between cumulative anthropogenic CO2 emissions and the global warming they cause" in spm
assert "Each 1000 GtCO2 of cumulative CO2 emissions is assessed to likely cause a 0.27°C to 0.63°C increase" in spm
assert "best estimate of 0.45°C" in spm
assert "2390 ± 240 (likely range) GtCO2" in spm

c = pd.read_csv(HERE / "data/gcb_cumulative_co2_world.csv").set_index("year")
cum = c.iloc[:, -1] / 1e9                                   # GtCO2, cumulative since 1850
h = pd.read_csv(HERE / "data/hadcrut5_global_annual.csv").set_index("Time")
h.columns = ["anom", "lo", "hi"]
base = h.anom.loc[1850:1900].mean()
t = (h[["anom", "lo", "hi"]] - base).loc[:2025]             # 2026 is incomplete
d = pd.DataFrame({"cum": cum, "T": t.anom, "lo": t.lo, "hi": t.hi}).dropna()

cum_2019 = cum.loc[2019]
assert 2390 - 240 <= cum_2019 <= 2390 + 240, cum_2019      # inside the IPCC's likely range for 1850-2019
emit = cum.diff()
emit.iloc[0] = cum.iloc[0]

recent = d.loc[2016:2025]
t_recent, cum_recent = recent["T"].mean(), recent.cum.mean()
ratio = t_recent / cum_recent * 1000
assert TCRE_LO <= ratio <= TCRE_HI
slope, icpt = np.polyfit(d.cum, d["T"], 1)
dec = d.assign(decade=d.index // 10 * 10).groupby("decade").mean()
d.round(4).to_csv(HERE / "data/derived_annual.csv")

print(f"IPCC AR6: {TCRE}°C per 1000 GtCO2 (likely {TCRE_LO}-{TCRE_HI}); text verified")
print(f"cumulative CO2 1850-2019: {cum_2019:,.0f} GtCO2 (IPCC: 2390 ± 240); 1850-2025: {cum.loc[2025]:,.0f} GtCO2")
print(f"emissions 2025: {emit.loc[2025]:.1f} GtCO2; share of all-time total emitted since 1990: "
      f"{(cum.loc[2025] - cum.loc[1989]) / cum.loc[2025]:.0%}")
print(f"warming 2016-2025 vs 1850-1900: {t_recent:.2f}°C; mean cumulative then {cum_recent:,.0f} GtCO2; "
      f"ratio {ratio:.2f}°C per 1000 GtCO2 (inside the IPCC likely range)")
print(f"least-squares slope, annual 1850-2025: {slope * 1000:.2f}°C per 1000 GtCO2")
print(f"2011-2020 warming: {d['T'].loc[2011:2020].mean():.2f}°C (IPCC SPM A.1.2: 1.09)")
print("decadal means:")
print(dec[["cum", "T"]].round(2).loc[1950:].to_string())

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17.5)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Climate · Carbon and warming",
    "Global warming rises in step\nwith *total CO2 emitted*",
    f"The IPCC finds a near-linear link: about {TCRE}°C of warming for every 1,000 billion tonnes of CO2 emitted,\n"
    f"likely {TCRE_LO} to {TCRE_HI}°C. By 2025 the total since 1850 was {cum.loc[2025]:,.0f} billion tonnes; warming was "
    f"{t_recent:.2f}°C in 2016–25.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "IPCC assessment of observations,\nmodels and carbon-cycle theory"),
    ("Sample", "Global record, 1850–2025:\nemissions and temperature"),
    ("Source", "IPCC AR6 WG1\nSPM, 2021"),
    ("Consistent with", "Matthews et al. 2009 · Allen et al. 2009\nForster et al. 2025 (indicators)"),
], widths=[0.28, 0.26, 0.15, 0.31])

# --- 01: temperature against cumulative CO2 -----------------------------------
top1 = y - 0.07
h1 = 0.33
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.13, h1])
xs = np.array([0, 3200])
ax.fill_between(xs, xs * TCRE_LO / 1000, xs * TCRE_HI / 1000, color=PAPER_2, lw=0, zorder=1)
ax.plot(xs, xs * TCRE / 1000, color=INK_3, lw=1.2, ls=(0, (4, 3)), zorder=2)
ax.vlines(d.cum, d.lo, d.hi, color=TAUPE, lw=0.6, alpha=0.6, zorder=2)
ax.scatter(d.cum, d["T"], s=10, color=TAUPE, zorder=3)
dd = dec.loc[1880:]
ax.scatter(dd.cum, dd["T"], s=44, color=SIGNAL, edgecolor=PAPER, lw=0.8, zorder=5)
for dk, r in dd.iterrows():
    if dk in (1880, 1980, 2000, 2020):
        lab = f"{dk}s" if dk < 2020 else "2020–25"
        ax.annotate(lab, (r.cum, r["T"]), xytext=(-8, 9), textcoords="offset points", ha="right", fontsize=9,
                    color=INK, family=px.MONO)
ax.text(3150, 3150 * TCRE_HI / 1000 - 0.05, f"{TCRE_HI}°C per 1,000 Gt", ha="right", va="top", fontsize=9,
        color=INK_3, rotation=0)
ax.annotate(f"IPCC best estimate {TCRE}°C", xy=(1400, 1400 * TCRE / 1000), xytext=(250, 1.15), ha="left", va="bottom",
            fontsize=9.5, color=INK_2, weight="semibold",
            arrowprops=dict(arrowstyle="-", color=INK_3, lw=0.7, shrinkA=2, shrinkB=2))
ax.text(3150, 3150 * TCRE_LO / 1000 - 0.04, f"{TCRE_LO}°C", ha="right", va="top", fontsize=9, color=INK_3)
ax.set_xlim(0, 3200)
ax.set_ylim(-0.6, 2.1)
ax.set_xticks(range(0, 3201, 500))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.set_yticks([-0.5, 0, 0.5, 1.0, 1.5, 2.0])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.1f}°C" if v else "0°C"))
ax.axhline(0, color=INK, lw=0.6, zorder=1)
ax.set_xlabel("Cumulative CO2 emitted since 1850 (billion tonnes)")
ax.grid(axis="y")
px.mono_ticks(ax)
px.panel(ax, 1, "Global temperature against total CO2 emitted, 1850–2025",
         "Small dots: each year, with 95% range. Red: decade averages. Band: the IPCC's likely range, starting at zero.",
         pad=0.55)

# --- 02: where the total came from --------------------------------------------
top2 = top1 - h1 - 0.11
h2 = 0.11
ax2 = fig.add_axes([px.LEFT, top2 - h2, px.WIDTH - 0.13, h2])
ax2.fill_between(emit.index, 0, emit.values, color=SIGNAL, alpha=0.85, lw=0, zorder=2, step="mid")
ax2.set_xlim(1850, 2026)
ax2.set_ylim(0, 48)
ax2.set_yticks([0, 20, 40])
ax2.grid(axis="y")
ax2.set_ylabel("Gt a year")
ax2.text(2024, emit.loc[2025] + 2, f"{emit.loc[2025]:.0f} Gt in 2025", ha="right", va="bottom", fontsize=9.5,
         color=INK, family=px.MONO)
share90 = (cum.loc[2025] - cum.loc[1989]) / cum.loc[2025]
ax2.axvline(1990, color=INK_3, lw=0.7, ls=(0, (1, 2)))
ax2.text(1988, 44, f"{share90:.0%} of the all-time total\nwas emitted from 1990 on", fontsize=9, color=INK_2, va="top", ha="right")
px.mono_ticks(ax2)
px.panel(ax2, 2, "CO2 emitted each year, fossil fuels, industry and land use", None, pad=0.35)

px.footer(fig,
          "DATA  Global Carbon Budget via Our World in Data (cumulative CO2 incl. land use); HadCRUT.5.1.0.0, re-based to\n"
          "      1850-1900. IPCC AR6 WG1 SPM D.1.1 and D.1.2. 1850-2019 total checked against the IPCC's 2390 ± 240 GtCO2.\n"
          "NOTE  The IPCC range is for warming caused by CO2. The observed record also includes other gases and aerosols.",
          NO)
px.save(fig, HERE)
print("saved")
