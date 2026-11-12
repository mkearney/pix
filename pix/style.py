"""pix house style: "Plate".

Every chart is a printed plate: warm paper, black ink, one vermilion signal,
an indigo counterpoint, a serif headline, mono numbers, and crop marks.
See STYLE.md for the rules.

    from pix import style as px
    fig = px.plate()
    px.masthead(fig, date="2026-11-12", no=px.issue_number(__file__))
    y = px.headline(fig, "Time", "The world's clocks *run fast*", "Deck text...")
    ax = fig.add_axes([px.LEFT, 0.42, px.WIDTH, 0.36]); px.panel(ax, 1, "Title", "Subtitle")
    px.footer(fig, "Source: ...", no=...)
"""
from __future__ import annotations

import re
from datetime import date as _date
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap

# ---- Fonts (bundled in pix/fonts, OFL) ----------------------------------------
_FONT_DIR = Path(__file__).resolve().parent / "fonts"
for _f in sorted(_FONT_DIR.glob("*.[ot]tf")):
    font_manager.fontManager.addfont(str(_f))

SERIF = "Instrument Serif"     # headlines, big numbers
SANS = "Inter"                 # decks, labels, notes
MONO = "IBM Plex Mono"         # ticks, kickers, masthead, sources

# ---- Colour -------------------------------------------------------------------
PAPER = "#f3eee4"      # warm bone paper
PAPER_2 = "#e9e2d4"    # a shade darker: bands, highlights, empty states
INK = "#17171a"        # primary ink
INK_2 = "#4a4741"      # secondary text
INK_3 = "#8c877d"      # muted text, ticks
RULE = "#d6cebf"       # hairlines, grid

SIGNAL = "#e4572e"     # vermilion: the one thing to look at
INDIGO = "#2b4592"     # counterpoint: the contrast, the "other side"
TAUPE = "#bdb4a4"      # context marks, everything else
OCHRE = "#d19a2a"      # rare third accent
SAGE = "#5f8a6e"       # rare fourth accent

# Use in this order when identity needs more than signal/indigo. Keep to <= 5.
PALETTE = [SIGNAL, INDIGO, OCHRE, SAGE, TAUPE]

# Ramps: sequential (paper -> indigo / paper -> vermilion), diverging via taupe.
SEQ_INDIGO = LinearSegmentedColormap.from_list("pix_indigo", ["#ece6d9", "#a9b3cf", "#5b6fae", INDIGO, "#17255a"])
SEQ_SIGNAL = LinearSegmentedColormap.from_list("pix_signal", ["#f1e3d3", "#efb393", "#ea8160", SIGNAL, "#9c3015"])
DIVERGING = LinearSegmentedColormap.from_list("pix_div", ["#17255a", INDIGO, "#9aa5c6", "#ddd6c8", "#eba98f", SIGNAL, "#9c3015"])

# ---- Geometry -----------------------------------------------------------------
LEFT = 0.085        # left edge for axes and text
RIGHT = 0.935
WIDTH = RIGHT - LEFT
TEXT_X = 0.065      # headline/masthead x (slightly outside the axes)


def apply() -> None:
    mpl.rcParams.update({
        "font.family": SANS,
        "font.size": 11,
        "text.color": INK,
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "axes.edgecolor": INK,
        "axes.linewidth": 0.9,
        "axes.labelcolor": INK_3,
        "axes.labelsize": 9.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": RULE,
        "grid.linewidth": 0.8,
        "grid.linestyle": (0, (1, 2.5)),
        "xtick.color": INK_3,
        "ytick.color": INK_3,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "xtick.major.size": 3,
        "xtick.major.width": 0.8,
        "xtick.major.pad": 6,
        "ytick.major.size": 0,
        "ytick.major.pad": 6,
        "legend.frameon": False,
        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",
        "svg.fonttype": "none",
    })


def mono_ticks(ax) -> None:
    """Numbers are set in mono. Call after ticks/formatters are final."""
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontfamily(MONO)


def issue_number(path) -> int:
    """1-based position of this entry's folder among archive/ entries."""
    entry = Path(path).resolve()
    entry = entry if entry.is_dir() else entry.parent
    dirs = sorted(p.name for p in entry.parent.iterdir() if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}-", p.name))
    return dirs.index(entry.name) + 1 if entry.name in dirs else len(dirs) + 1


def plate(width: float = 12, height: float = 15) -> plt.Figure:
    """New figure on paper with crop marks in the corners."""
    apply()
    fig = plt.figure(figsize=(width, height), dpi=100)
    m, L = 0.022, 0.018                       # margin, mark length (fig fraction of width)
    ly = L * width / height
    my = m * width / height
    kw = dict(color=INK_3, lw=0.6, transform=fig.transFigure, zorder=0)
    for x0, sx in ((m, 1), (1 - m, -1)):
        for y0, sy in ((my, 1), (1 - my, -1)):
            fig.add_artist(plt.Line2D([x0 - sx * L * 0.25, x0 + sx * L], [y0, y0], **kw))
            fig.add_artist(plt.Line2D([x0, x0], [y0 - sy * ly * 0.25, y0 + sy * ly], **kw))
    return fig


def masthead(fig, date: str, no: int, *, top: float = 0.962) -> None:
    """Thin top band: wordmark + issue number left, date right, rule under it."""
    d = _date.fromisoformat(date)
    fig.text(TEXT_X, top, "PIX", fontfamily=MONO, fontsize=10, weight="medium", color=INK, va="baseline")
    fig.text(TEXT_X + 0.04, top, f"No. {no:03d}", fontfamily=MONO, fontsize=10, color=INK_3, va="baseline")
    fig.text(1 - TEXT_X, top, d.strftime("%a %d %b %Y").upper(), fontfamily=MONO, fontsize=10,
             color=INK_3, va="baseline", ha="right")
    fig.add_artist(plt.Line2D([TEXT_X, 1 - TEXT_X], [top - 0.009] * 2, color=INK, lw=0.9,
                              transform=fig.transFigure))


def _rich(fig, x, y, text, *, size, color, accent, family, va="top"):
    """Draw one line where *starred* phrases are italic and in the accent colour."""
    r = fig.canvas.get_renderer()
    for i, part in enumerate(re.split(r"\*([^*]+)\*", text)):
        if not part:
            continue
        italic = i % 2 == 1
        t = fig.text(x, y, part, fontfamily=family, fontsize=size, va=va,
                     color=accent if italic else color, style="italic" if italic else "normal")
        x = fig.transFigure.inverted().transform(t.get_window_extent(r))[1][0]
    return x


def headline(fig, kicker: str, title: str, deck: str, *, top: float = 0.925,
             size: float = 54, deck_size: float = 13.5) -> float:
    """Kicker (mono, vermilion) + serif headline + sans deck. Returns the y just below the deck.

    Mark a phrase in the title with *asterisks* to set it in vermilion italic. Use \\n for a
    second title line.
    """
    fig_h = fig.get_figheight()
    fig.text(TEXT_X, top, kicker.upper(), fontfamily=MONO, fontsize=10.5, color=SIGNAL,
             weight="medium", va="top")
    y = top - 0.24 / fig_h
    line_h = size * 1.02 / 72 / fig_h
    for line in title.split("\n"):
        _rich(fig, TEXT_X - 0.003, y, line, size=size, color=INK, accent=SIGNAL, family=SERIF)
        y -= line_h
    y -= 0.16 / fig_h
    t = fig.text(TEXT_X, y, deck, fontsize=deck_size, color=INK_2, va="top", linespacing=1.5)
    n = deck.count("\n") + 1
    return y - n * deck_size * 1.5 / 72 / fig_h


def panel(ax, index: int, title: str, subtitle: str | None = None, *, pad: float = 0.30) -> None:
    """Panel heading above an axes: vermilion mono index, sans title, muted subtitle."""
    fig = ax.figure
    fig_h = fig.get_figheight()
    bb = ax.get_position()
    y = bb.y1 + (pad + (0.22 if subtitle else 0)) / fig_h
    fig.text(bb.x0, y, f"{index:02d}", fontfamily=MONO, fontsize=10.5, color=SIGNAL, weight="medium",
             va="baseline")
    fig.text(bb.x0 + 0.032, y, title, fontsize=13, weight="semibold", color=INK, va="baseline")
    if subtitle:
        fig.text(bb.x0 + 0.032, y - 0.22 / fig_h, subtitle, fontsize=10.5, color=INK_2, va="baseline")


def note(ax, xy, xytext, text, *, ha="left", color=INK_2, size=9.5, **kw):
    """Direct annotation with a hairline leader."""
    return ax.annotate(text, xy, xytext, textcoords="offset points", fontsize=size, color=color,
                       ha=ha, va="center", linespacing=1.3, zorder=6,
                       arrowprops=dict(arrowstyle="-", color=INK_3, lw=0.7, shrinkA=1, shrinkB=2), **kw)


def big_number(target, x, y, value: str, label: str, *, color=SIGNAL, ha="left", size=44) -> None:
    """Serif hero number with a small sans label under it. target = axes or figure."""
    fig = target.figure if hasattr(target, "transAxes") else target
    tr = target.transAxes if hasattr(target, "transAxes") else target.transFigure
    target.text(x, y, value, fontfamily=SERIF, fontsize=size, color=color, ha=ha, va="top", transform=tr)
    under = mpl.transforms.offset_copy(tr, fig=fig, y=-size * 1.08, units="points")
    target.text(x, y, label, fontsize=10, color=INK_2, ha=ha, va="top", transform=under, linespacing=1.35)


def footer(fig, source: str, no: int, *, y: float = 0.03) -> None:
    """Rule, then mono source notes left and the plate number right."""
    fig.add_artist(plt.Line2D([TEXT_X, 1 - TEXT_X], [y + 0.034] * 2, color=INK, lw=0.6,
                              transform=fig.transFigure))
    fig.text(TEXT_X, y + 0.026, source, fontfamily=MONO, fontsize=8, color=INK_3, va="top",
             linespacing=1.6)
    fig.text(1 - TEXT_X, y + 0.026, f"PIX · {no:03d}", fontfamily=MONO, fontsize=9, color=INK,
             weight="medium", ha="right", va="top")


def save(fig, here) -> None:
    here = Path(here).resolve()
    here = here if here.is_dir() else here.parent
    fig.savefig(here / "chart.png", dpi=150)
    fig.savefig(here / "chart.svg")
