"""2026-11-18: Older fathers pass on more new mutations.

Finding: the number of new (de novo) mutations a child carries rises with the
father's age at conception about four times faster than with the mother's.

Source: Jónsson H, et al. Parental influence on human germline de novo mutations
in 1,548 trios from Iceland. Nature 549, 519-522 (2017). doi:10.1038/nature24018

This script refits the paper's model from its released mutation table and checks
the result against the published estimates (paternal 1.51/yr, 95% CI 1.45-1.57;
maternal 0.37/yr, 0.32-0.43). Model, as in the paper's Methods: each parent's
count is Poisson with mean alpha + beta * age, and the parent of origin of
untraced mutations is summed out of the likelihood. Autosomes only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize
from scipy.special import gammaln, logsumexp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pix import style as px  # noqa: E402
from pix.style import INDIGO, INK, INK_2, INK_3, PAPER, SIGNAL  # noqa: E402

NO = px.issue_number(HERE)
DATE = "2026-11-18"
PUBLISHED = {"beta_P": (1.51, 1.45, 1.57), "beta_M": (0.37, 0.32, 0.43)}

# ---------------------------------------------------------------- data ------
raw = pd.read_csv(HERE / "data/jonsson2017_decode_dnms.tsv.gz", sep="\t")
THREE_GEN = ["three_generation", "both_approaches"]


def per_proband(d: pd.DataFrame) -> pd.DataFrame:
    g = d.groupby("Proband_nr").agg(
        father_age=("Fathers_age_at_conception", "first"),
        mother_age=("Mothers_age_at_conception", "first"),
        dnms=("Chr", "size"),
        paternal=("Phase_combined", lambda s: int((s == "father").sum())),
        maternal=("Phase_combined", lambda s: int((s == "mother").sum())),
        three_gen=("Phase_source", lambda s: bool(s.isin(THREE_GEN).any())),
    )
    g["unphased"] = g.dnms - g.paternal - g.maternal
    return g


all_chr = per_proband(raw)
auto = per_proband(raw[raw.Chr != "chrX"])
auto.to_csv(HERE / "data/per_proband_autosomes.csv")

# ---------------------------------------------------------------- model -----
U = auto.unphased.to_numpy()
K = np.arange(U.max() + 1)                                    # extra paternal among unphased
yP = auto.paternal.to_numpy()[:, None] + K[None, :]           # latent paternal count
yM = auto.dnms.to_numpy()[:, None] - yP                       # latent maternal count
ok = K[None, :] <= U[:, None]
AP = auto.father_age.to_numpy()[:, None]
AM = auto.mother_age.to_numpy()[:, None]
const = -gammaln(yP + 1) - gammaln(np.where(ok, yM, 0) + 1)


def nll(theta: np.ndarray) -> float:
    aP, bP, aM, bM = theta
    lP, lM = aP + bP * AP, aM + bM * AM
    if (lP <= 0).any() or (lM <= 0).any():
        return 1e12
    ll = yP * np.log(lP) - lP + np.where(ok, yM, 0) * np.log(lM) - lM + const
    return -logsumexp(np.where(ok, ll, -np.inf), axis=1).sum()


fit = optimize.minimize(nll, x0=[6, 1.5, 4, 0.4], method="Nelder-Mead",
                        options=dict(maxiter=20000, xatol=1e-7, fatol=1e-7))
theta = fit.x
eps = 1e-3 * np.maximum(1, np.abs(theta))
H = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        ei, ej = np.eye(4)[i] * eps[i], np.eye(4)[j] * eps[j]
        H[i, j] = (nll(theta + ei + ej) - nll(theta + ei - ej) - nll(theta - ei + ej) + nll(theta - ei - ej)) / (
            4 * eps[i] * eps[j])
se = np.sqrt(np.diag(np.linalg.inv(H)))
names = ["alpha_P", "beta_P", "alpha_M", "beta_M"]
est = pd.DataFrame({"estimate": theta, "se": se, "lo95": theta - 1.96 * se, "hi95": theta + 1.96 * se}, index=names)
est.round(4).to_csv(HERE / "data/model_fit.csv")
aP, bP, aM, bM = theta

for k, (p, lo, hi) in PUBLISHED.items():
    r = est.loc[k]
    match = abs(round(r.estimate, 2) - p) < 0.005 and abs(round(r.lo95, 2) - lo) < 0.015 and abs(round(r.hi95, 2) - hi) < 0.015
    print(f"{k}: refit {r.estimate:.2f} ({r.lo95:.2f}-{r.hi95:.2f}) vs published {p} ({lo}-{hi}) -> "
          f"{'MATCH' if match else 'MISMATCH'}")
    assert match, f"{k} does not reproduce the paper"

# ---------------------------------------------------------------- stats -----
tg = auto[auto.three_gen]
traced = (tg.paternal + tg.maternal).sum() / tg.dnms.sum()
pat_share = tg.paternal.sum() / (tg.paternal + tg.maternal).sum()
pred = pd.DataFrame({"age": [20, 30, 40]})
pred["paternal"] = aP + bP * pred.age
pred["maternal"] = aM + bM * pred.age
pred["total"] = pred.paternal + pred.maternal
pred["paternal_share"] = pred.paternal / pred.total
pred.round(2).to_csv(HERE / "data/expected_by_parent_age.csv", index=False)

print(f"trios: {len(all_chr):,}; mutations: {all_chr.dnms.sum():,}; mean per child {all_chr.dnms.mean():.1f} "
      f"(autosomes {auto.dnms.mean():.1f})")
print(f"father age {auto.father_age.min()}-{auto.father_age.max()} (mean {auto.father_age.mean():.1f}); "
      f"mother age {auto.mother_age.min()}-{auto.mother_age.max()} (mean {auto.mother_age.mean():.1f}); "
      f"mothers aged 38+: {(auto.mother_age >= 38).sum()}")
print(f"three-generation families: {len(tg)}; traced to a parent: {traced:.1%}; from the father: {pat_share:.1%}")
print(f"slope ratio father/mother: {bP / bM:.1f}")
print(f"ten years of father's age: +{10 * bP:.1f}; of mother's: +{10 * bM:.1f}")
print(pred.round(3).to_string(index=False))

# ---------------------------------------------------------------- figure ----
fig = px.plate(12, 16.5)
px.masthead(fig, DATE, NO)
y = px.headline(
    fig, "Genetics · Parental age",
    "Older fathers pass on more *new mutations*",
    f"Standard sequencing finds about {all_chr.dnms.mean():.0f} DNA changes in a child that neither parent carries.\n"
    f"Each extra year of the father's age at conception adds {bP:.2f}. Each year of the mother's adds {bM:.2f}.",
    size=50,
)
y = px.evidence(fig, y - 0.022, [
    ("Study", "Whole-genome sequencing\nof parents and child"),
    ("Sample", f"{len(all_chr):,} Icelandic families,\n{all_chr.dnms.sum():,} new mutations"),
    ("Source", "Jónsson et al.\nNature, 2017"),
    ("Consistent with", "Kong et al. 2012 · Goldmann et al. 2016\nPorubsky et al. 2025: 75–81% from fathers"),
], widths=[0.22, 0.25, 0.17, 0.36])

# --- 01: scatter, one dot per parent, three-generation families ---------------
top1 = y - 0.068
h1 = 0.34
ax = fig.add_axes([px.LEFT, top1 - h1, px.WIDTH - 0.13, h1])
ax.scatter(tg.mother_age, tg.maternal, s=26, color=INDIGO, alpha=0.55, edgecolor=PAPER, lw=0.5, zorder=3)
ax.scatter(tg.father_age, tg.paternal, s=26, color=SIGNAL, alpha=0.6, edgecolor=PAPER, lw=0.5, zorder=3)
for a0, a1, a, b, col in [(tg.father_age.min(), tg.father_age.max(), aP, bP, SIGNAL),
                          (tg.mother_age.min(), tg.mother_age.max(), aM, bM, INDIGO)]:
    xs = np.array([a0, a1])
    ax.plot(xs, a + b * xs, color=PAPER, lw=5.5, zorder=4, solid_capstyle="round")
    ax.plot(xs, a + b * xs, color=col, lw=2.4, zorder=5, solid_capstyle="round")
x_end_P, x_end_M = tg.father_age.max(), tg.mother_age.max()
ax.text(x_end_P + 1.2, aP + bP * x_end_P + 3, "Fathers", color=SIGNAL, fontsize=13, weight="semibold", va="bottom")
ax.text(x_end_P + 1.2, aP + bP * x_end_P + 2, f"+{bP:.2f} a year", color=SIGNAL, fontsize=11, va="top",
        family=px.MONO)
ax.text(x_end_P + 1.2, aP + bP * x_end_P - 4.5, f"95% CI {est.loc['beta_P', 'lo95']:.2f}–{est.loc['beta_P', 'hi95']:.2f}",
        color=INK_3, fontsize=9, va="top", family=px.MONO)
ax.text(x_end_M + 1.2, aM + bM * x_end_M + 3, "Mothers", color=INDIGO, fontsize=13, weight="semibold", va="bottom")
ax.text(x_end_M + 1.2, aM + bM * x_end_M + 2, f"+{bM:.2f} a year", color=INDIGO, fontsize=11, va="top",
        family=px.MONO)
ax.text(x_end_M + 1.2, aM + bM * x_end_M - 4.5, f"95% CI {est.loc['beta_M', 'lo95']:.2f}–{est.loc['beta_M', 'hi95']:.2f}",
        color=INK_3, fontsize=9, va="top", family=px.MONO)
ax.set_xlim(14, 58)
ax.set_ylim(0, 120)
ax.set_xticks(range(15, 60, 5))
ax.set_yticks(range(0, 121, 20))
ax.set_xlabel("Parent's age at conception")
ax.set_ylabel("New mutations from that parent")
ax.yaxis.set_label_coords(-0.055, 0.5)
px.mono_ticks(ax)
px.panel(ax, 1, "New mutations a child inherits from each parent",
         f"One dot per parent in the {len(tg)} three-generation families, where {traced:.0%} of mutations could be "
         f"traced. Lines fit all {len(auto):,} families.")

# --- 02: expected total by parents' age --------------------------------------
top2 = top1 - h1 - 0.125
h2 = 0.105
ax2 = fig.add_axes([px.LEFT + 0.14, top2 - h2, px.WIDTH - 0.14 - 0.09, h2])
rows = pred.iloc[::-1].reset_index(drop=True)
for i, r in rows.iterrows():
    ax2.barh(i, r.paternal, color=SIGNAL, height=0.62, zorder=3)
    ax2.barh(i, r.maternal, left=r.paternal, color=INDIGO, height=0.62, zorder=3)
    ax2.text(r.paternal / 2, i, f"{r.paternal:.0f}", color=PAPER, ha="center", va="center", fontsize=11,
             family=px.MONO, weight="medium", zorder=4)
    ax2.text(r.paternal + r.maternal / 2, i, f"{r.maternal:.0f}", color=PAPER, ha="center", va="center",
             fontsize=11, family=px.MONO, weight="medium", zorder=4)
    ax2.text(r.total + 1.2, i, f"{r.total:.0f}", color=INK, ha="left", va="center", fontsize=15,
             family=px.SERIF, zorder=4)
    ax2.text(-0.025, i, f"Both parents {r.age:.0f}", transform=ax2.get_yaxis_transform(), fontsize=11.5,
             color=INK, ha="right", va="center")
top_row = rows.iloc[-1]
ax2.text(top_row.paternal / 2, len(rows) - 0.62, "From the father", color=SIGNAL, ha="center", va="bottom",
         fontsize=10, weight="semibold")
ax2.text(top_row.paternal + top_row.maternal / 2, len(rows) - 0.62, "From the mother", color=INDIGO,
         ha="center", va="bottom", fontsize=10, weight="semibold")
ax2.set_xlim(0, 92)
ax2.set_ylim(-0.45, len(rows) - 0.3)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.grid(False)
ax2.spines["bottom"].set_visible(False)
hdr = fig.add_axes([px.LEFT, top2 - h2, 0.01, h2])
hdr.axis("off")
px.panel(hdr, 2, "Expected new mutations in a child, by the parents' age",
         f"From the fitted lines. The father's share is {pred.paternal_share.min():.0%} to "
         f"{pred.paternal_share.max():.0%} at each age.", pad=0.55)

px.footer(fig,
          "DATA  Jónsson et al., Nature 549:519 (2017), supplementary table of de novo mutations (deCODE genetics).\n"
          "NOTE  Autosomes, as in the paper. Poisson model with untraced mutations' parent summed out, refit here;\n"
          "      it reproduces the published slopes. Counts cover the ~2.7 billion bases short reads can reach.",
          NO)
px.save(fig, HERE)
print("saved")
