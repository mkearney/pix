# pix: editorial brief

**pix publishes one settled finding a day: something science already knows, with strong
evidence behind it, drawn as a chart good enough to screenshot and share.**

pix doesn't try to discover anything. The job is to find well-established results, ideally
from recent, large studies, that a smart reader may never have seen measured, and to make the
relationship visible at a glance: what causes what, how big the effect is, what shape it
takes, and whom it applies to.

No human reviews an entry before it goes out, and nobody running pix is an expert in every
field. So the evidence bar is strict, every number has to be traceable, and
`scripts/publish.py` refuses entries that skip the checks. When in doubt, pick a different
finding.

This file is the standing brief for whoever (human or Claude) makes the day's entry. Follow
it every time. It replaced the original brief on 2026-11-18: if a scheduled-task prompt or an
earlier run mentions uniqueness tests, first-idea tests, `prior_art.md` or first-person
write-ups, those belong to the old brief and no longer apply.

## What makes an entry

1. **Settled.** It clears the evidence bar below. This comes first.
2. **Interesting.** Apply the friend test: a smart non-specialist would say "I didn't know it
   was that big", "I didn't know it had that shape" or "I didn't know it depended on that".
   Prefer findings that touch decisions people make (health, children, money, time, safety,
   food, energy) or explain how the world works. Skip what everyone already knows unless the
   size or shape is the news: everyone knows smoking kills, fewer know that quitting by 40
   wins back most of the lost decade.
3. **Visual.** The relationship itself is the picture: a dose-response curve, an effect split
   by a moderator, before and after, a column of comparable effects, a scatter of the real
   units. If the chart would be one bar or a table, pick a different finding.

## Evidence bar

**A finding qualifies only with at least one of these behind it:**

- A systematic review or meta-analysis (Cochrane, or in a major journal) of randomised
  trials or many cohorts.
- A large pooled analysis by a consortium (for example NCD-RisC, the Cholesterol Treatment
  Trialists, the Emerging Risk Factors Collaboration).
- A large randomised trial in a major journal, with a consistent result from at least one
  other trial.
- A natural experiment or registry study whose result has been repeated in another country
  or dataset.
- A consensus assessment (IPCC, National Academies, WHO, IARC, USPSTF), for the claim it
  actually makes.
- A long-agreed physical or biological law or measurement, cited to a current source.

**And corroboration:** at least two other independent sources reaching the same conclusion
(studies, reviews or guidelines), each with a DOI or link in `evidence.md`.

**Disqualified:**

- Single unreplicated studies, preprints, press releases, conference abstracts.
- Anything credible experts still actively dispute. Search "<finding> criticism",
  "<finding> replication" and "<finding> controversy" before committing.
- Small-sample social psychology, single-cohort nutrition epidemiology, animal results
  presented as human ones, country-level correlations presented as individual effects.
- Retracted papers or papers with an expression of concern (check PubMed and Retraction
  Watch).
- Politically contested empirical questions where serious researchers disagree, unless the
  claim is only the uncontested part.

**Recency.** Prefer a source from the last five years, or the latest major update of an
older result. An old classic is fine when newer work confirms it; cite the newer work too.

**Words match the design.**

- "Causes", "raises", "cuts", "adds": only with randomised trials, natural experiments, or
  an accepted mechanism plus a replicated dose-response.
- Observational evidence only: "is linked to", "goes with", "people who X have Y". Never
  imply cause.
- Show the effect's uncertainty (a confidence interval or band) on the chart when the
  source reports it.
- Give a relative risk together with the absolute baseline whenever the baseline matters.

## Data

In order of preference:

1. **The study's own released data** (supplementary files, Dryad, OSF, Zenodo, GitHub, a
   data portal). Refit the paper's headline estimate in `analysis.py` and `assert` that it
   matches the published value to the reported precision. If it doesn't reproduce, stop and
   pick another finding. This is the best guarantee of accuracy when nobody reviews by hand.
2. **Numbers transcribed from the paper's text or tables** (never from news coverage). Save
   them as `data/*.csv` with columns for the value, its interval and its exact location
   (table, page). Read them from the full text (PubMed Central or the publisher).
3. **Public statistics that display an established relationship** (Our World in Data,
   World Bank, CDC, ONS, Eurostat, NOAA, NASA), alongside a citation that establishes the
   relationship itself. OWID grapher CSVs:
   `https://ourworldindata.org/grapher/<slug>.csv?v=1&csvType=full&useColumnShortNames=true`.
   A `FRED_API_KEY` environment variable is available.

Reading values off a figure image is a last resort. Label every such value "read from
Figure X" in `data/SOURCES.md` and in the chart footer.

Save every input under `data/` so the analysis reruns offline (gzip anything large; keep an
entry under about 10 MB). `data/SOURCES.md` says where each file came from.
PubMed's E-utilities (`eutils.ncbi.nlm.nih.gov`) return abstracts and metadata as plain text,
and `https://doi.org/<doi>` confirms a DOI resolves.

## Finding types

Every entry has a `finding:` field, one of:

- `effect`: X changes Y by this much.
- `dose-response`: more X, more (or less) Y, and the shape of the curve.
- `moderator`: the effect of X on Y depends on Z.
- `association`: X and Y go together (observational, and worded that way).
- `comparison`: several causes or interventions on one scale.
- `mechanism`: the steps by which X leads to Y, each shown in data.

Don't repeat the previous entry's type.

## Topics

Rotate widely: health & medicine · genetics & biology · mind & learning (robust findings
only) · climate & energy · environment & nature · economics & work · cities & transport ·
food & farming · demography & family · technology & engineering · earth & physical science ·
safety & risk · children & education · the body & sport.

Read `archive/README.md` first. Don't repeat the previous entry's topic, and don't repeat a
subject within 90 days. `LEADS.md` holds pre-vetted candidates: use one or bring your own,
and run the full evidence check either way. Delete a lead once it's used, and add any strong
candidates you come across.

## Writing

The post is a caption, not an essay. A reader should finish it in 30 seconds.

**Shape of `post.md`:**

```
---
date: YYYY-MM-DD
title: Older fathers pass on more new mutations
slug: older-fathers-new-mutations
topic: Genetics
finding: moderator
source: Jónsson et al., Nature, 2017
doi: 10.1038/nature24018
chart: chart.png
summary: One or two plain sentences with the key numbers (180 characters at most).
---

# Older fathers pass on more new mutations

![Alt text that describes what the chart shows, with its key numbers.](chart.png)

One paragraph of two to four sentences: the finding, its size, and the moderator or shape.
Optionally one more sentence: the accepted explanation, or the main limit.

**Source:** Authors. Title. *Journal* volume, pages (year). [doi:...](https://doi.org/...)<br>
**Evidence:** Design and scale. The corroborating studies. Whether the numbers were reproduced.

[Data](data/) · [Code](analysis.py) · [Evidence notes](evidence.md) · [SVG](chart.svg)
```

**Rules** (`publish.py` enforces the starred ones):

- \*At most 100 words of prose, not counting the headline, alt text, Source, Evidence and
  links. Most posts should land between 50 and 90.
- \*Headline: the finding as a plain sentence of at most 9 words. Not a topic label, not a
  question, no colon, no pun.
- \*Third person. No "I", "we", "our" or "us". Avoid "you".
- Start with the finding. No setup, no scene-setting, no "Scientists have long known".
- Same numbers, same rounding, same units everywhere: post, chart, summary, and the output
  of `analysis.py`.
- Plain words. No jokes, metaphors, wordplay, rhetorical questions, or a moral at the end.
- \*No em dashes, exclamation marks or hype words (striking, stark, notably, remarkable,
  fascinating, surprisingly, crucially, underscores, delve, landscape, "turns out",
  "here's", and the rest of the list in `publish.py`). No emoji, ALL CAPS emphasis or
  square-bracket asides.
- Chart text follows the same rules.

This is the register to match (from 2026-11-18):

> Standard sequencing finds about 70 DNA changes in each child that neither parent carries.
> In 1,548 Icelandic families, each extra year of the father's age at conception added 1.51
> of them, and each year of the mother's added 0.37. Where a mutation could be traced to a
> parent, 80% came from the father.

Not this: "I wanted to know whether...", "It turns out that...", "Here's the thing:",
"This matters because...", or any closing line about what it all means.

## Design

Every graphic uses the **Plate** house style. Read `STYLE.md` before drawing and use
`pix/style.py` (`from pix import style as px`):

- `px.plate()` → `px.masthead()` → `px.headline()` → `px.evidence()` → numbered
  `px.panel()`s → `px.footer()` → `px.save()`. The latest entry's `analysis.py` is a working
  example.
- The **evidence strip** is required: Study, Sample, Source, Consistent with. It tells a
  reader in two seconds what the chart rests on.
- Show uncertainty when the source reports it (bands, whiskers, interval labels).
- Real units over indexes. Annotate directly; no legends where labels fit.
- Vary the form from day to day: dose-response curve with a band, forest plot, small
  multiples split by a moderator, before and after, scatter of real units, survival or
  cumulative curves, a timeline of an intervention and its outcome.
- Render, then **open chart.png and look at it**. Fix overlaps, clipping and dead space.

## Checks before publishing

Nobody else will check, so these aren't optional.

1. `analysis.py` runs from the repo root, prints every number the post and chart use, and
   asserts the reproduction when raw data exist.
2. `evidence.md` is complete (template below).
3. **Independent fact-check.** Start a fresh subagent (the Agent tool, general-purpose) and
   give it only the paper's link, `post.md`, `evidence.md`, `analysis.py` output and the path
   to `chart.png`. Ask it to confirm each number against the paper or the output, confirm
   that each corroborating source exists and says what's claimed, flag causal wording the
   design doesn't support, and search for credible disputes or retractions. Fix every issue
   or drop the finding. Record the verdict under `Fact-check:`.
4. Read the post once as a sceptical expert in the field and once as someone scrolling
   past. Fix whatever either would trip on.
5. `python scripts/publish.py` passes.

`evidence.md` is short and plain, in this shape:

```
# Evidence
Finding: one sentence.
Type: one of the finding types.
Source: full citation, DOI, link to the full text, link to released data if any.
Design: study design and scale (n, events, years, countries).
Key numbers: each number in the post and chart, where it appears in the paper, and whether it was reproduced or derived here.
Corroboration: two or more independent sources with the same finding, each with a DOI and one line.
Wording check: causal or associational, and why the post's verbs fit the design.
Limits: the main caveats, one to three sentences.
Fact-check: the independent checker's verdict and what changed as a result.
```

## Daily procedure

A Claude Code scheduled task runs this every day at 8:05am US Eastern.

0. Setup: `pip install -r requirements.txt`.
1. `TZ=America/Detroit date +%F` gives the entry date. If an entry for that date already
   exists, stop and report it.
2. Read `archive/README.md` (recent topics and finding types) and `LEADS.md`.
3. Shortlist three findings. Apply the evidence bar and the friend test, check data
   availability, and pick the strongest. Run at least five searches to confirm its standing:
   the meta-analyses, the replications, and any criticism.
4. Create `archive/YYYY-MM-DD-<short-slug>/` with `post.md`, `evidence.md`, `analysis.py`,
   `chart.png`, `chart.svg` and `data/` (including `SOURCES.md`). `analysis.py` must run with
   `python archive/<dir>/analysis.py` from the repo root.
5. Run the checks above, including the independent fact-check.
6. `python scripts/publish.py` regenerates `README.md` and `archive/README.md`.
7. Commit as `pix YYYY-MM-DD: <title>` and push to `main`. No em dashes in commit messages.

**Never rename, re-date, move or edit a published entry** unless the maintainer asks.

## Repo layout

```
README.md               today's post (generated, don't edit by hand)
CLAUDE.md               this brief
LEADS.md                pre-vetted candidate findings
STYLE.md                the Plate style guide
pix/style.py            house visual style
pix/fonts/              bundled fonts (OFL)
scripts/publish.py      checks entries, rebuilds README.md + archive/README.md
archive/README.md       index of every entry (generated)
archive/YYYY-MM-DD-slug/{post.md, evidence.md, analysis.py, chart.png, chart.svg, data/}
```

Entries before 2026-11-18 belong to an earlier series that looked for new patterns in public
data. They keep their old files (`prior_art.md` instead of `evidence.md`) and are exempt from
the new checks.
