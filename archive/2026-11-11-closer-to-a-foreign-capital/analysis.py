"""2026-11-11: A lot of people live closer to a foreign capital than their own.

Question: for every city on Earth with 15,000+ people, which is closer: the
capital of its own country, or the nearest capital of some other country?
Weight by population.

Distances are great-circle (haversine, R = 6,371 km). Capitals are GeoNames
PPLC features. Dependent territories are folded into their parent state, so
Hong Kong counts as China and Reunion as France, and their capitals are not
treated as foreign capitals.

Data: GeoNames cities15000 + countryInfo (CC BY 4.0).
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
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, PAPER_2, RULE, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-11"

# ---------------------------------------------------------------- data ------
c = pd.read_csv(HERE / "data/cities15000.csv", keep_default_na=False)
# PPLX rows are sections of a bigger city (e.g. Puxi inside Shanghai). Drop them so people aren't counted twice.
n_pplx = int((c.fcode == "PPLX").sum())
c = c[c.fcode != "PPLX"].copy()
countries = pd.read_csv(HERE / "data/countries.csv", keep_default_na=False).set_index("cc")

# Dependent territories -> sovereign parent (GeoNames gives them their own code).
PARENT = {
    "HK": "CN", "MO": "CN",
    "PR": "US", "GU": "US", "VI": "US", "AS": "US", "MP": "US", "UM": "US",
    "GL": "DK", "FO": "DK",
    "RE": "FR", "GP": "FR", "MQ": "FR", "GF": "FR", "YT": "FR", "NC": "FR", "PF": "FR",
    "PM": "FR", "BL": "FR", "MF": "FR", "WF": "FR",
    "AW": "NL", "CW": "NL", "SX": "NL", "BQ": "NL",
    "GI": "GB", "BM": "GB", "KY": "GB", "VG": "GB", "TC": "GB", "AI": "GB", "MS": "GB",
    "FK": "GB", "IM": "GB", "JE": "GB", "GG": "GB", "SH": "GB",
    "CX": "AU", "CC": "AU", "NF": "AU",
    "CK": "NZ", "NU": "NZ", "TK": "NZ",
    "SJ": "NO", "AX": "FI",
}
c["state"] = c.cc.replace(PARENT)

caps = c[(c.fcode == "PPLC") & (c.cc == c.state)][["state", "name", "lat", "lon"]].copy()
# GeoNames has no PPLC for Israel; use Jerusalem, the seat of government.
jer = c[(c.name == "Jerusalem") & (c.cc == "IL")].iloc[0]
caps = pd.concat([caps, pd.DataFrame([{"state": "IL", "name": "Jerusalem", "lat": jer.lat, "lon": jer.lon}])])
caps = caps.drop_duplicates("state").set_index("state")

# Places with no single recognised capital in the data are left out of the "home" side.
home = c[c.state.isin(caps.index)].copy()
dropped = c[~c.state.isin(caps.index)]

R = 6371.0


def hav(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(lon2 - lon1)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


D = hav(home.lat.to_numpy()[:, None], home.lon.to_numpy()[:, None],
        caps.lat.to_numpy()[None, :], caps.lon.to_numpy()[None, :])
own_idx = caps.index.get_indexer(home.state)
home["d_own"] = D[np.arange(len(home)), own_idx]
Df = D.copy()
Df[np.arange(len(home)), own_idx] = np.inf
j = Df.argmin(axis=1)
home["d_foreign"] = Df[np.arange(len(home)), j]
home["foreign_cap"] = caps.name.to_numpy()[j]
home["foreign_state"] = caps.index.to_numpy()[j]
home["closer_foreign"] = home.d_foreign < home.d_own

w = home["pop"]
W = w.sum()
P = w[home.closer_foreign].sum()
share = P / W

# by country
g = home.assign(pf=w * home.closer_foreign).groupby("state").agg(pop=("pop", "sum"), pf=("pf", "sum"))
g["share"] = g.pf / g["pop"]
g["country"] = countries.reindex(g.index).country
g = g.sort_values("pf", ascending=False)

# which foreign capitals "pull" the most people
pull = (home[home.closer_foreign].groupby(["foreign_cap", "foreign_state"])["pop"].sum()
        .sort_values(ascending=False))

# Sensitivity: don't count Taipei as a foreign capital at all.
Dn = Df.copy()
Dn[:, caps.index.get_loc("TW")] = np.inf
share_no_tw = w[Dn.min(axis=1) < home.d_own.to_numpy()].sum() / W
cn = home.state == "CN"
cn_no_tw = w[cn & (Dn.min(axis=1) < home.d_own.to_numpy())].sum() / w[cn].sum()

# Sensitivity: ignore capitals of states with under 1 million people (San Marino, Vaduz, Luxembourg...).
small = countries.reindex(caps.index)["pop"].astype(float).to_numpy() < 1e6
Ds = Df.copy()
Ds[:, small] = np.inf
share_no_small = w[Ds.min(axis=1) < home.d_own.to_numpy()].sum() / W
Dboth = Ds.copy()
Dboth[:, caps.index.get_loc("TW")] = np.inf
share_strict = w[Dboth.min(axis=1) < home.d_own.to_numpy()].sum() / W
n_small = int(small.sum())

n_states = len(g)
n_any = int((g.pf > 0).sum())
n_major = int((g.share > 0.5).sum())

home[["name", "cc", "state", "lat", "lon", "pop", "d_own", "d_foreign", "foreign_cap", "closer_foreign"]] \
    .round(1).to_csv(HERE / "data/city_capital_distance.csv", index=False)
g.round(4).to_csv(HERE / "data/country_share.csv")

print(f"cities: {len(home):,}  people: {W / 1e9:.2f}bn  states: {n_states}  dropped cities: {len(dropped)} "
      f"({', '.join(sorted(dropped.cc.unique()))})")
print(f"closer to a foreign capital: {P / 1e6:.0f}M people = {share:.1%} (1 in {1 / share:.1f})")
print(f"PPLX rows dropped: {n_pplx}")
print(f"without Taipei: {share_no_tw:.1%}  China without Taipei: {cn_no_tw:.1%}")
print(f"without capitals of {n_small} states under 1M: {share_no_small:.1%}  and without Taipei too: {share_strict:.1%}")
print(f"world excl China: {w[~cn & home.closer_foreign].sum() / w[~cn].sum():.1%}")
print(f"cities: {home.closer_foreign.sum():,} of {len(home):,} = {home.closer_foreign.mean():.1%}")
print(f"states with anyone affected: {n_any}  states where most are: {n_major}")
print("\ntop by people:")
print(g.head(20).assign(pf=lambda x: (x.pf / 1e6).round(1), pop=lambda x: (x["pop"] / 1e6).round(1),
                        share=lambda x: (x.share * 100).round(1)).to_string())
big = g[g["pop"] >= 5e6].sort_values("share", ascending=False)
print("\ntop by share (5M+ city pop):")
print(big.head(20).assign(pf=lambda x: (x.pf / 1e6).round(1), pop=lambda x: (x["pop"] / 1e6).round(1),
                          share=lambda x: (x.share * 100).round(1)).to_string())
print("\nforeign capitals pulling most people (M):")
print((pull.head(15) / 1e6).round(1).to_string())
print("\nbiggest affected cities:")
print(home[home.closer_foreign].nlargest(25, "pop")[["name", "cc", "pop", "d_own", "foreign_cap", "d_foreign"]]
      .round(0).to_string())

# examples for the map
EX = [("Shanghai", "CN"), ("Lagos", "NG"), ("Bengaluru", "IN"), ("Los Angeles", "US"), ("Munich", "DE"),
      ("Ho Chi Minh City", "VN")]
ex = pd.concat([home[(home.name == n) & (home.cc == cc)].nlargest(1, "pop") for n, cc in EX])
print("\nexamples:")
print(ex[["name", "state", "d_own", "foreign_cap", "d_foreign"]].round(0).to_string())

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 15.4)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Borders · Distance to power",
    "Two in five city dwellers live\ncloser to *a foreign capital*",
    f"For {len(home):,} cities ({W / 1e9:.1f} billion people) I compared the distance to their own capital with the\n"
    f"distance to the nearest foreign one. For {share:.0%} of people, the foreign capital is closer.",
)

# --- 01: map -----------------------------------------------------------------
top_A = deck_bottom - 0.045
hA = 0.30
axA = fig.add_axes([px.LEFT, top_A - hA, px.WIDTH, hA])
s = np.clip(home["pop"].to_numpy() / 4e4, 0.6, 300)
col = np.where(home.closer_foreign, SIGNAL, TAUPE)
order = np.argsort(-home["pop"].to_numpy())
axA.scatter(home.lon.to_numpy()[order], home.lat.to_numpy()[order], s=s[order], c=col[order],
            alpha=0.75, edgecolors="none", zorder=3)
axA.scatter(caps.lon, caps.lat, s=9, facecolors=PAPER, edgecolors=INK, linewidths=0.6, zorder=4)
axA.set_xlim(-168, 158)
axA.set_ylim(-42, 62)
axA.set_aspect("equal")
axA.axis("off")
px.panel(axA, 1, "Every city, coloured by which capital is closer",
         "Red: a foreign capital is closer than its own. Rings are capitals. Dot size is population.")

for _, r in ex.iterrows():
    own = caps.loc[r.state]
    fc = caps.loc[r.foreign_state]
    axA.plot([r.lon, own.lon], [r.lat, own.lat], color=INK_3, lw=0.7, ls=(0, (2, 2)), zorder=5)
    axA.plot([r.lon, fc.lon], [r.lat, fc.lat], color=SIGNAL, lw=1.4, zorder=5)

LBL = {
    "Los Angeles": (-40, -26, "right", "Los Angeles\nMexico City {f:,.0f} km\nWashington {o:,.0f} km"),
    "Munich": (-70, 6, "right", "Munich\nVaduz {f:,.0f} km\nBerlin {o:,.0f} km"),
    "Lagos": (-30, -34, "right", "Lagos\nPorto-Novo {f:,.0f} km\nAbuja {o:,.0f} km"),
    "Bengaluru": (-30, -40, "right", "Bengaluru\nColombo {f:,.0f} km\nDelhi {o:,.0f} km"),
    "Ho Chi Minh City": (24, -52, "left", "Ho Chi Minh City\nPhnom Penh {f:,.0f} km\nHanoi {o:,.0f} km"),
    "Shanghai": (8, 54, "left", "Shanghai\nTaipei {f:,.0f} km\nBeijing {o:,.0f} km"),
}
for _, r in ex.iterrows():
    dx, dy, ha, t = LBL[r["name"]]
    px.note(axA, (r.lon, r.lat), (dx, dy), t.format(f=r.d_foreign, o=r.d_own), ha=ha, size=8.5,
            bbox=dict(boxstyle="square,pad=0.25", fc=PAPER, ec="none", alpha=0.92))

# --- 02: biggest countries ----------------------------------------------------
axB = fig.add_axes([px.LEFT + 0.17, 0.10, px.WIDTH - 0.37, top_A - hA - 0.13])
top = g.head(15).sort_values("share")
y = np.arange(len(top))
axB.barh(y, np.ones(len(top)), color=PAPER_2, height=0.66, zorder=2)
axB.barh(y, top.share, color=SIGNAL, height=0.66, zorder=3)
axB.set_xlim(0, 1)
axB.set_ylim(-0.6, len(top) - 0.4)
axB.set_yticks([])
axB.set_xticks([0, 0.25, 0.5, 0.75, 1])
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axB.axvline(0.5, color=INK, lw=0.6, ls=(0, (1, 2)), zorder=4)
axB.grid(False)
NAME = {"US": "United States", "CD": "DR Congo", "GB": "United Kingdom"}
main_pull = (home[home.closer_foreign].groupby(["state", "foreign_cap"])["pop"].sum()
             .reset_index().sort_values("pop", ascending=False).drop_duplicates("state")
             .set_index("state").foreign_cap)
for yi, (st, r) in zip(y, top.iterrows()):
    axB.text(-0.015, yi, NAME.get(st, r.country), ha="right", va="center", fontsize=10.5, color=INK)
    axB.text(r.share + 0.012, yi, f"{r.share:.0%}", ha="left", va="center", fontsize=10,
             family=px.MONO, color=INK, zorder=5)
    axB.text(1.015, yi, f"{r.pf / 1e6:,.0f}M · mostly {main_pull.get(st, '')}", ha="left", va="center",
             fontsize=9, color=INK_3)
px.panel(axB, 2, "The 15 countries with the most city dwellers",
         "Share of people closer to a foreign capital, how many that is, and which capital pulls most")
px.mono_ticks(axB)

px.footer(fig,
          "DATA  GeoNames cities of 15,000+ people and capitals (CC BY 4.0). Great-circle distances.\n"
          f"NOTE  Territories counted with their parent state. Without Taipei: {share_no_tw:.0%}. "
          f"Without capitals of states under 1M people: {share_no_small:.0%}.\n"
          "      City populations only, about half of humanity.",
          NO)

px.save(fig, HERE)
print("saved")