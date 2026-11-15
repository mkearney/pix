"""2026-11-15: By length, most new undersea cable has a Big Tech owner.

Question: how much of the undersea cable entering service now has Google, Meta,
Amazon or Microsoft among its owners? Published answers disagree because they
count cables. Here I count kilometres too.

A cable counts as big-tech if any of the four is listed as an owner (sole owner
or consortium member). Cables are grouped by ready-for-service (RFS) year into
five-year cohorts. 2027-29 cables are planned, not built.

Data: TeleGeography Submarine Cable Map, public API, fetched 2026-11-15.
"""
from __future__ import annotations

import json
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
DATE = "2026-11-15"
BIG = {"Google": "Google", "Meta": "Meta", "Facebook": "Meta", "Amazon": "Amazon", "Microsoft": "Microsoft"}

# ---------------------------------------------------------------- data ------
raw = json.loads((HERE / "data/submarinecablemap_cables_2026-11-15.json").read_text())
rows = []
for c in raw:
    length = c.get("length") or ""
    km = float(re.sub(r"[^0-9.]", "", length)) if re.search(r"\d", length) else np.nan
    owners = [o.strip() for o in (c.get("owners") or "").split(",") if o.strip()]
    bt = sorted({BIG[k] for k in BIG if any(re.search(rf"\b{k}\b", o) for o in owners)})
    bt_owners = [o for o in owners if any(re.search(rf"\b{k}\b", o) for k in BIG)]
    rows.append({"id": c["id"], "name": c["name"], "km": km, "rfs": c.get("rfs_year"),
                 "planned": bool(c.get("is_planned")), "n_owners": len(owners),
                 "big_tech": ";".join(bt), "is_bt": bool(bt), "bt_only": bool(bt) and len(bt_owners) == len(owners)})
t = pd.DataFrame(rows)
t.to_csv(HERE / "data/cables.csv", index=False)

n_all, n_nokm = len(t), int(t.km.isna().sum())
k = t.dropna(subset=["km", "rfs"]).copy()
k["rfs"] = k.rfs.astype(int)
k["cohort"] = k.rfs // 5 * 5
co = k[(k.cohort >= 2000) & (k.cohort <= 2025)].groupby("cohort").apply(lambda x: pd.Series({
    "cables": len(x), "cables_bt": int(x.is_bt.sum()), "km": x.km.sum(), "km_bt": x[x.is_bt].km.sum(),
    "km_bt_only": x[x.bt_only].km.sum()}))
co["share_count"] = co.cables_bt / co.cables
co["share_km"] = co.km_bt / co.km
co.round(4).to_csv(HERE / "data/cohorts.csv")

new = k[k.rfs.between(2025, 2029)]
built = k[k.rfs.between(2020, 2024)]
med_bt = new[new.is_bt].km.median()
med_other = new[~new.is_bt].km.median()
per_co = {c: new[new.big_tech.str.contains(c)].km.sum() for c in ["Google", "Meta", "Microsoft", "Amazon"]}
solo = new[new.bt_only]
long10 = new.nlargest(10, "km")

print(f"cables on the map: {n_all}; without a length: {n_nokm}; used: {len(k)}")
print(co.assign(share_count=lambda x: (x.share_count * 100).round(1), share_km=lambda x: (x.share_km * 100).round(1),
                km=lambda x: (x.km / 1e3).round(0), km_bt=lambda x: (x.km_bt / 1e3).round(0))
      [["cables", "cables_bt", "share_count", "km", "km_bt", "share_km"]].to_string())
print(f"2025-29: {len(new)} cables, {new.km.sum() / 1e3:,.0f}k km; big tech in {new.is_bt.sum()} "
      f"({new.is_bt.mean():.0%}) holding {new[new.is_bt].km.sum() / new.km.sum():.0%} of km")
print(f"2025-29 planned share of km: {new[new.planned].km.sum() / new.km.sum():.0%}")
print(f"2020-24: big tech {built.is_bt.mean():.0%} of cables, {built[built.is_bt].km.sum() / built.km.sum():.0%} of km")
print(f"median length 2025-29: big tech {med_bt:,.0f} km, others {med_other:,.0f} km ({med_bt / med_other:.1f}x)")
print(f"2025-29 cables owned by big tech alone: {len(solo)}, {solo.km.sum() / new.km.sum():.0%} of km")
print("2025-29 km with each company as an owner:", {c: f"{v / 1e3:,.0f}k" for c, v in per_co.items()})
print(f"of the 10 longest 2025-29 cables, {long10.is_bt.sum()} have a big-tech owner")
print(long10[["name", "km", "rfs", "big_tech"]].to_string(index=False))

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 16.5)
px.masthead(fig, DATE, NO)
sh_n = new.is_bt.mean()
sh_km = new[new.is_bt].km.sum() / new.km.sum()
deck_bottom = px.headline(
    fig, "Infrastructure · Undersea cables",
    "By length, most new undersea\ncable *has a Big Tech owner*",
    f"Google, Meta, Amazon or Microsoft co-own {sh_n:.0%} of the cables due in service from 2025 to 2029.\n"
    f"Those cables are long, so they make up {sh_km:.0%} of the kilometres.",
)

# --- 01: every cable ---------------------------------------------------------
top_A = deck_bottom - 0.07
hA = 0.36
axA = fig.add_axes([px.LEFT, top_A - hA, px.WIDTH, hA])
rng = np.random.default_rng(7)
d = k[k.rfs >= 1995].copy()
d["x"] = d.rfs + rng.uniform(-0.32, 0.32, len(d))
other, bt = d[~d.is_bt], d[d.is_bt]
axA.axvspan(2026.5, 2029.6, color=PAPER_2, lw=0, zorder=0)
axA.text(2028.05, 60000, "PLANNED", fontsize=8.5, family=px.MONO, color=INK_3, ha="center", va="top")
axA.scatter(other.x, other.km, s=np.clip(other.km / 900, 6, 70), color=TAUPE, alpha=0.75, edgecolor=PAPER, lw=0.4, zorder=2)
axA.scatter(bt.x, bt.km, s=np.clip(bt.km / 900, 6, 70), color=SIGNAL, alpha=0.9, edgecolor=PAPER, lw=0.5, zorder=3)
axA.set_yscale("log")
axA.set_ylim(5, 70000)
axA.set_xlim(1994.3, 2029.7)
axA.set_yticks([10, 100, 1000, 10000])
axA.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f} km"))
axA.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
axA.grid(axis="y")
NOTE = {"2africa": (-14, 8, "right"), "bulikula": (-40, 4, "right"), "echo": (10, -14, "left"),
        "equiano": (-14, 6, "right"), "jupiter": (-14, 4, "right")}
for cid, (dx, dy, ha) in NOTE.items():
    r = d[d.id == cid].iloc[0]
    px.note(axA, (r.x, r.km), (dx, dy), r["name"].split(" (")[0], ha=ha, size=8.5)
axA.text(1995.2, 40, "Taupe: no big-tech owner\nRed: Google, Meta, Amazon\nor Microsoft among the owners",
         fontsize=9, color=INK_2, va="top", linespacing=1.4)
px.panel(axA, 1, "Every cable on the map, by year in service and length",
         "1995 onward. Log scale. Dot size also shows length.")
px.mono_ticks(axA)

# --- 02: share by count vs by km --------------------------------------------
top_B = top_A - hA - 0.12
axB = fig.add_axes([px.LEFT, 0.12, px.WIDTH * 0.62, top_B - 0.12])
x = co.index.to_numpy()
axB.plot(x, co.share_km, color=SIGNAL, lw=2.2, marker="o", ms=6, mec=PAPER, zorder=4)
axB.plot(x, co.share_count, color=INK_3, lw=1.6, marker="o", ms=5, mec=PAPER, zorder=3)
axB.axhline(0.5, color=INK_3, lw=0.6, ls=(0, (1, 2)), zorder=1)
axB.set_ylim(0, 0.62)
axB.set_xlim(1999, 2030.5)
axB.set_xticks(x)
axB.set_xticklabels([f"{c}-{str(c + 4)[2:]}" for c in x])
axB.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
axB.set_yticks([0, 0.25, 0.5])
axB.grid(axis="y")
last = co.iloc[-1]
axB.text(x[-1] + 0.5, last.share_km, f"By length\n{last.share_km:.0%}", color=SIGNAL, fontsize=10, va="center",
         weight="semibold")
axB.text(x[-1] + 0.5, last.share_count, f"By count\n{last.share_count:.0%}", color=INK_2, fontsize=10, va="center")
px.panel(axB, 2, "Share of each cohort with a big-tech owner",
         "Cables grouped by year in service. 2025-29 includes planned cables.")
px.mono_ticks(axB)

# hero number
px.big_number(fig, px.LEFT + px.WIDTH * 0.72, top_B + 0.005, f"{med_bt / med_other:.1f}x",
              f"how much longer the median\nbig-tech cable is, 2025-29\n({med_bt:,.0f} km against {med_other:,.0f} km)")

px.footer(fig,
          "DATA  TeleGeography Submarine Cable Map (CC BY-NC-SA 3.0), public API, fetched 15 Nov 2026.\n"
          f"NOTE  Co-owned means named among the owners, alone or in a consortium. {n_nokm} of {n_all} cables list no\n"
          "      length and are left out. Retired cables are not on the map.",
          NO)

px.save(fig, HERE)
print("saved")
