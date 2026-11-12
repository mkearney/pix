"""Render pix/specimen.png: the house style on one plate (palette, type, marks)."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pix import style as px  # noqa: E402

fig = px.plate(12, 11)
px.masthead(fig, "2026-11-12", 0)
bottom = px.headline(fig, "House style · Plate", "Printed plates, *read on screens*",
                     "Warm paper, black ink, one vermilion signal and an indigo counterpoint.\n"
                     "Serif for the headline, sans for words, mono for numbers.")

# palette swatches
names = [("PAPER", px.PAPER), ("PAPER_2", px.PAPER_2), ("INK", px.INK), ("TAUPE", px.TAUPE),
         ("SIGNAL", px.SIGNAL), ("INDIGO", px.INDIGO), ("OCHRE", px.OCHRE), ("SAGE", px.SAGE)]
y0 = bottom - 0.05
for i, (n, c) in enumerate(names):
    x = px.LEFT + i * (px.WIDTH / 8)
    ax = fig.add_axes([x, y0 - 0.075, px.WIDTH / 8 - 0.012, 0.07])
    ax.set_facecolor(c); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(px.RULE); sp.set_linewidth(0.6)
    fig.text(x, y0 - 0.09, n, fontfamily=px.MONO, fontsize=8.5, color=px.INK, va="top")
    fig.text(x, y0 - 0.108, c, fontfamily=px.MONO, fontsize=8.5, color=px.INK_3, va="top")

# ramps
for j, (n, cm) in enumerate([("SEQ_INDIGO", px.SEQ_INDIGO), ("SEQ_SIGNAL", px.SEQ_SIGNAL), ("DIVERGING", px.DIVERGING)]):
    ax = fig.add_axes([px.LEFT + j * px.WIDTH / 3, y0 - 0.175, px.WIDTH / 3 - 0.02, 0.025])
    ax.imshow(np.linspace(0, 1, 256)[None, :], cmap=cm, aspect="auto")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.text(px.LEFT + j * px.WIDTH / 3, y0 - 0.188, n, fontfamily=px.MONO, fontsize=8.5, color=px.INK, va="top")

# sample chart
rng = np.random.default_rng(3)
ax = fig.add_axes([px.LEFT, 0.13, px.WIDTH * 0.58, 0.27])
x = np.arange(1990, 2027)
for k in range(6):
    ax.plot(x, np.cumsum(rng.normal(0.2, 1, len(x))), color=px.TAUPE, lw=1.2)
yy = np.cumsum(rng.normal(0.6, 1, len(x)))
ax.plot(x, yy, color=px.SIGNAL, lw=2.2)
ax.scatter([x[-1]], [yy[-1]], s=40, color=px.SIGNAL, zorder=5, edgecolors=px.PAPER, linewidths=1.5)
px.note(ax, (x[-1], yy[-1]), (-10, 16), "The one series\nthat matters", ha="right")
ax.set_xlim(1990, 2028)
px.panel(ax, 1, "One signal, everything else in taupe", "Lines 2px, context 1.2px, dotted hairline grid")
px.mono_ticks(ax)
px.big_number(fig, px.LEFT + px.WIDTH * 0.66, 0.40, "35:1", "serif hero number\nfor the headline stat")
px.big_number(fig, px.LEFT + px.WIDTH * 0.66, 0.26, "1.1%", "indigo for the\nother side", color=px.INDIGO)

px.footer(fig, "TYPE  Instrument Serif (headlines) · Inter (text) · IBM Plex Mono (numbers, notes)\n"
               "MARKS crop marks, masthead rule, numbered panels, mono footer", 0)
fig.savefig(ROOT / "pix" / "specimen.png", dpi=110)
print("saved")
