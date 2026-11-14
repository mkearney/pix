"""2026-11-14: Coffee doubled on the same land. Cocoa doubled its land.

Question: world coffee and cocoa output both roughly doubled between the late
1980s and the early 2020s. How much of each came from planting more land, and
how much from getting more out of each hectare?

Method: production = area x yield, so log(P1/P0) = log(A1/A0) + log(Y1/Y0).
The land share of growth is log(A1/A0) / log(P1/P0). Both ends are five-year
averages (1986-90 and 2020-24) so one good or bad harvest doesn't decide it.

Data: FAOSTAT, Crops and livestock products (QCL), area harvested and production.
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
from pix.style import INK, INK_2, INK_3, PAPER, PAPER_2, SIGNAL, TAUPE  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-14"
EARLY, LATE = (1986, 1990), (2020, 2024)

# ---------------------------------------------------------------- data ------
w = pd.read_csv(HERE / "data/faostat_world_area_production.csv")
w = w[w.element.isin(["Area harvested", "Production"])]
wp = w.pivot_table(index=["item", "year"], columns="element", values="value").reset_index()
wp = wp.dropna(subset=["Area harvested", "Production"])
wp = wp.rename(columns={"Area harvested": "area", "Production": "prod"})
wp["yield"] = wp["prod"] / wp["area"]


def window(g: pd.DataFrame, span) -> pd.Series:
    return g[(g.year >= span[0]) & (g.year <= span[1])][["area", "prod"]].mean()


rows = []
for item, g in wp.groupby("item"):
    e, l = window(g, EARLY), window(g, LATE)
    if e.isna().any() or l.isna().any():
        continue
    rows.append({"item": item, "area0": e.area, "area1": l.area, "prod0": e["prod"], "prod1": l["prod"]})
dec = pd.DataFrame(rows)
dec["prod_x"] = dec.prod1 / dec.prod0
dec["area_x"] = dec.area1 / dec.area0
dec["yield_x"] = dec.prod_x / dec.area_x
dec["land_share"] = np.log(dec.area_x) / np.log(dec.prod_x)
dec.round(4).to_csv(HERE / "data/decomposition_by_crop.csv", index=False)

cof = dec.set_index("item").loc["Coffee, green"]
coc = dec.set_index("item").loc["Cocoa beans"]

# single crops (no totals or "n.e.c." groups) on 10M+ ha whose output grew 30%+
AGG = ("Total", "Primary", "n.e.c", "Equivalent")
crops = dec[~dec.item.str.contains("|".join(AGG), case=False) & (dec.area1 >= 10e6) & (dec.prod_x >= 1.3)].copy()
crops = crops.sort_values("land_share")

# countries
c = pd.read_csv(HERE / "data/faostat_coffee_cocoa_by_country.csv")
c["area"] = c["area"].str.replace("CÃ´te d'Ivoire", "Côte d'Ivoire", regex=False)
cc = c.pivot_table(index=["area", "item", "year"], columns="element", values="value").reset_index()


def country_change(item: str) -> pd.DataFrame:
    x = cc[cc.item == item]
    e = x[x.year.between(*EARLY)].groupby("area")[["Area harvested", "Production"]].mean()
    l = x[x.year.between(*LATE)].groupby("area")[["Area harvested", "Production"]].mean()
    t = pd.concat({"e": e, "l": l}, axis=1).fillna(0)
    out = pd.DataFrame({
        "d_area": t[("l", "Area harvested")] - t[("e", "Area harvested")],
        "d_prod": t[("l", "Production")] - t[("e", "Production")],
        "yield0": t[("e", "Production")] / t[("e", "Area harvested")].replace(0, np.nan),
        "yield1": t[("l", "Production")] / t[("l", "Area harvested")].replace(0, np.nan),
    })
    return out.sort_values("d_prod", ascending=False)


cof_c, coc_c = country_change("Coffee, green"), country_change("Cocoa beans")
br, vn = cof_c.loc["Brazil"], cof_c.loc["Viet Nam"]
ci = coc_c.loc["Côte d'Ivoire"]

# sensitivity: 1991-95 start
alt = []
for item in ["Coffee, green", "Cocoa beans"]:
    g = wp[wp.item == item]
    e, l = window(g, (1991, 1995)), window(g, LATE)
    alt.append(np.log(l.area / e.area) / np.log(l["prod"] / e["prod"]))

print(f"windows: {EARLY} vs {LATE}")
for name, r in [("coffee", cof), ("cocoa", coc)]:
    print(f"{name:7} output x{r.prod_x:.2f} ({r.prod0 / 1e6:.2f} -> {r.prod1 / 1e6:.2f} Mt)  "
          f"area x{r.area_x:.2f} ({r.area0 / 1e6:.2f} -> {r.area1 / 1e6:.2f} Mha)  "
          f"yield x{r.yield_x:.2f}  land share {r.land_share:.0%}")
print(f"extra cocoa land: {(coc.area1 - coc.area0) / 1e6:.2f} Mha; extra coffee land: {(cof.area1 - cof.area0) / 1e6:.2f} Mha")
print(f"cocoa yield t/ha: {coc.prod0 / coc.area0:.3f} -> {coc.prod1 / coc.area1:.3f}; "
      f"coffee: {cof.prod0 / cof.area0:.3f} -> {cof.prod1 / cof.area1:.3f}")
print(f"if cocoa yields had grown like coffee's, today's crop would need {coc.prod1 / (coc.prod0 / coc.area0 * cof.yield_x) / 1e6:.2f} Mha")
print(f"Brazil coffee: area {br.d_area / 1e6:+.2f} Mha, output {br.d_prod / 1e6:+.2f} Mt, yield {br.yield0:.2f} -> {br.yield1:.2f}")
print(f"Vietnam coffee: area {vn.d_area / 1e6:+.2f} Mha, output {vn.d_prod / 1e6:+.2f} Mt, yield {vn.yield0:.2f} -> {vn.yield1:.2f}")
print(f"Cote d'Ivoire cocoa: area {ci.d_area / 1e6:+.2f} Mha, output {ci.d_prod / 1e6:+.2f} Mt, yield {ci.yield0:.2f} -> {ci.yield1:.2f}")
print(f"Cote d'Ivoire share of world extra cocoa land: {ci.d_area / coc_c.d_area.sum():.0%}")
print(f"sensitivity, 1991-95 start: coffee land share {alt[0]:.0%}, cocoa {alt[1]:.0%}")
print(f"{len(crops)} big crops; cocoa ranks #{int((crops.land_share > coc.land_share).sum()) + 1} by land share, "
      f"coffee #{int((crops.land_share > cof.land_share).sum()) + 1}")
print(crops[["item", "area1", "prod_x", "area_x", "yield_x", "land_share"]].round(2).to_string(index=False))

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 17)
px.masthead(fig, DATE, NO)
deck_bottom = px.headline(
    fig, "Food & land · Area vs yield",
    "Cocoa doubled its harvest\n*by doubling its land*",
    f"Since the late 1980s world coffee output grew {cof.prod_x:.1f}x on {cof.area_x - 1:.0%} more land. Cocoa grew "
    f"{coc.prod_x:.1f}x and needed\n{coc.area_x:.1f}x the land. {coc.land_share:.0%} of cocoa's extra output came from "
    f"new farms, against {cof.land_share:.0%} for coffee.",
)

# --- 01: twin small multiples ------------------------------------------------
top_A = deck_bottom - 0.065
hA = 0.27
gap = 0.11
wA = (px.WIDTH - gap - 0.07) / 2
for k, (item, label) in enumerate([("Coffee, green", "Coffee"), ("Cocoa beans", "Cocoa")]):
    ax = fig.add_axes([px.LEFT + k * (wA + gap), top_A - hA, wA, hA])
    g = wp[wp.item == item].set_index("year").sort_index()
    base = g.loc[EARLY[0]:EARLY[1], ["area", "prod", "yield"]].mean()
    idx = g[["area", "prod", "yield"]] / base * 100
    ax.axvspan(EARLY[0], EARLY[1], color=PAPER_2, lw=0, zorder=0)
    ax.axhline(100, color=INK_3, lw=0.6, zorder=1)
    ax.plot(idx.index, idx["prod"], color=INK, lw=1.6, zorder=3)
    ax.plot(idx.index, idx["area"], color=SIGNAL, lw=2.2, zorder=4)
    ax.plot(idx.index, idx["yield"], color=TAUPE, lw=1.6, zorder=2)
    ax.set_xlim(1961, 2027)
    ax.set_ylim(30, 260)
    ax.set_xticks([1970, 1990, 2010])
    ax.set_yticks([50, 100, 150, 200, 250])
    if k == 1:
        ax.set_yticklabels([])
    ax.grid(axis="y")
    last = idx.iloc[-1]
    yr = idx.index[-1]
    labels = {"prod": ("Output", INK), "area": ("Land", SIGNAL), "yield": ("Yield", INK_3)}
    order = sorted(labels, key=lambda s: last[s])
    ys = [last[s] for s in order]
    for i in range(1, len(ys)):          # keep end labels at least 16 points apart
        ys[i] = max(ys[i], ys[i - 1] + 16)
    for s, y in zip(order, ys):
        name, col = labels[s]
        ax.text(yr + 0.8, y, f"{name} {last[s]:.0f}", fontsize=9.5, color=col, va="center",
                weight="semibold" if s == "area" else "normal")
    ax.text(1963, 252, label, fontsize=15, family=px.SERIF, color=INK, va="top")
    px.mono_ticks(ax)
    if k == 0:
        px.panel(ax, 1, "World output, harvested land and yield, indexed to 1986-90 = 100",
                 "FAOSTAT, 1961 to 2024. The shaded band is the base period.")

# --- 02: land share across big crops -----------------------------------------
top_B = top_A - hA - 0.115
axB = fig.add_axes([px.LEFT + 0.2, 0.115, px.WIDTH - 0.33, top_B - 0.115])
y = np.arange(len(crops))
vals = crops.land_share.clip(-0.3, 1.05).to_numpy()
cols = [SIGNAL if it == "Cocoa beans" else INK if it == "Coffee, green" else TAUPE for it in crops.item]
axB.barh(y, vals, color=cols, height=0.62, zorder=3)
axB.axvline(0, color=INK, lw=0.8, zorder=4)
axB.axvline(0.5, color=INK_3, lw=0.6, ls=(0, (1, 2)), zorder=2)
axB.set_xlim(-0.3, 1.12)
axB.set_ylim(-0.6, len(crops) - 0.4)
axB.set_yticks([])
axB.set_xticks([-0.25, 0, 0.25, 0.5, 0.75, 1])
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axB.grid(axis="x")
NAME = {"Coffee, green": "Coffee", "Cocoa beans": "Cocoa", "Cassava, fresh": "Cassava", "Oil palm fruit": "Oil palm",
        "Natural rubber in primary forms": "Natural rubber", "Soya beans": "Soybeans", "Rape or colza seed": "Rapeseed",
        "Groundnuts, excluding shelled": "Groundnuts", "Maize (corn)": "Maize", "Beans, dry": "Beans",
        "Chick peas, dry": "Chickpeas", "Cow peas, dry": "Cowpeas", "Coconuts, in shell": "Coconuts",
        "Seed cotton, unginned": "Cotton", "Sugar cane": "Sugar cane", "Sunflower seed": "Sunflower",
        "Sesame seed": "Sesame", "Cashew nuts, in shell": "Cashews", "Yams": "Yams", "Olives": "Olives",
        "Rice": "Rice", "Wheat": "Wheat", "Potatoes": "Potatoes", "Lentils, dry": "Lentils"}
for yi, (_, r) in zip(y, crops.iterrows()):
    hi = r["item"] in ("Coffee, green", "Cocoa beans")
    axB.text(-0.32, yi, NAME.get(r["item"], r["item"]), ha="right", va="center", fontsize=10.5,
             color=INK, weight="semibold" if hi else "normal")
    v = r.land_share
    xt = max(min(v, 1.05), 0) + 0.015
    axB.text(xt, yi, f"{v:.0%}", ha="left", va="center", fontsize=9.5, family=px.MONO,
             color=SIGNAL if r["item"] == "Cocoa beans" else INK if hi else INK_3, zorder=5)
px.panel(axB, 2, "Share of extra output that came from new land, 1986-90 to 2020-24",
         f"The {len(crops)} biggest crops by area whose output grew 30% or more. Below zero, the crop now uses less land.")
px.mono_ticks(axB)

px.footer(fig,
          "DATA  FAOSTAT Crops and livestock products (QCL), world area harvested and production, 1961-2024.\n"
          "NOTE  Land share = log(area ratio) / log(output ratio), five-year averages at each end.\n"
          "      Harvested area, so young trees not yet bearing are not counted.",
          NO)

px.save(fig, HERE)
print("saved")
