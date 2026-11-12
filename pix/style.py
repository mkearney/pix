"""Shared house style for pix graphics.

Every daily chart imports this so the archive reads as one coherent series:
same type, same ink, same surfaces, same accent logic.

    from pix.style import apply, PALETTE, INK, title_block, footer
"""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---- Surfaces & ink ---------------------------------------------------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"          # primary text
INK_2 = "#52514e"        # secondary text
INK_3 = "#8a8984"        # muted text / axis labels
GRID = "#e6e5e0"
NEUTRAL = "#c9c8c1"      # context marks (the "everything else")

# ---- Categorical (fixed order, never cycle; fold past 8 into "Other") -----
PALETTE = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#6250d6",  # 7 violet
    "#e34948",  # 8 red
]
ACCENT = PALETTE[1]       # the one thing the reader should look at
ACCENT_2 = PALETTE[0]     # its counterpoint, when there is one

# Sequential blue ramp (light -> dark) for magnitude encodings.
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def _pick_font() -> str:
    names = {f.name for f in font_manager.fontManager.ttflist}
    for cand in ("Inter", "Inter Display", "Helvetica Neue", "Arial", "DejaVu Sans"):
        if cand in names:
            return cand
    return "DejaVu Sans"


FONT = _pick_font()


def apply() -> None:
    """Install the house rcParams."""
    mpl.rcParams.update({
        "font.family": FONT,
        "font.size": 11,
        "text.color": INK,
        "axes.facecolor": SURFACE,
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK_2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": INK_3,
        "ytick.color": INK_3,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "ytick.left": False,
        "xtick.major.size": 0,
        "legend.frameon": False,
        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",
    })


def title_block(fig, title: str, subtitle: str, *, x: float = 0.06, top: float = 0.965,
                title_size: float = 26, sub_size: float = 13.5, kicker: str | None = None) -> None:
    """Left-aligned headline (the claim) + deck (how to read it)."""
    y = top
    if kicker:
        fig.text(x, y, kicker.upper(), fontsize=10.5, color=ACCENT, weight="bold",
                 va="top")
        y -= 0.022
    fig.text(x, y, title, fontsize=title_size, weight="bold", color=INK, va="top",
             linespacing=1.1)
    n_lines = title.count("\n") + 1
    fig.text(x, y - 0.036 * n_lines - 0.006, subtitle, fontsize=sub_size, color=INK_2,
             va="top", linespacing=1.45)


def footer(fig, source: str, *, x: float = 0.06, y: float = 0.022, tag: str = "pix") -> None:
    fig.text(x, y, source, fontsize=9, color=INK_3, va="bottom", linespacing=1.4)
    fig.text(1 - x, y, tag, fontsize=10, color=INK_2, weight="bold", ha="right", va="bottom")
