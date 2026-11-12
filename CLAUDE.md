# pix: editorial brief

**pix publishes one visual analysis of the world every day.** Each entry makes one clear,
non-obvious point about something that matters, and backs it with real data and a graphic
good enough to screenshot and share.

This file is the standing brief for whoever (human or Claude) makes the day's entry.
Follow it every time.

## The bar

**The test: the reader shouldn't be able to easily find another take like it.** Occasionally
someone will have done something similar. Usually nobody should have. Uniqueness matters more
than scale: a modest, specific question answered freshly beats a grand theme everyone has
already charted.

1. **One claim.** The headline is a sentence with a verb that states the finding
   ("Humanity's clocks run fast"), not a topic label ("Time zones of the world").
   If you can't write that sentence, you don't have a post yet.
2. **An original angle.** Get there by one of these routes:
   - *A question nobody asks.* Pick something ordinary that's rarely measured (when the sun
     peaks on the clock, how far apart a country's capitals have moved, what share of a
     river's length is dammed).
   - *Your own computation.* Combine or derive data rather than replotting a chart that already
     exists. If an Our World in Data, Statista or FT chart already shows your exact point, stop.
   - *A re-weighting.* Count people, not countries; hours, not dollars; per km², not per nation.
   - *An unexpected join.* Two datasets that are rarely put together.
3. **Doesn't have to be grand.** Small and specific is fine, even good. It does have to be
   *true, interesting and about the real world*. No trivia for its own sake, no novelty
   rankings.
4. **The first-idea test.** Before committing, ask: "Is this the first topic a newsroom or an AI
   would pick?" If yes, discard it or push the angle two steps further. Big, well-worn themes
   (fertility decline and ageing, warming curves, the rise of China, AI growth, inequality
   headline stats, GDP rankings, election maps, streaming or tech-company data) are allowed
   only with an angle you've verified isn't already out there.
5. **Readable in 10 seconds, rewarding in 2 minutes.** A headline reader gets the point at a
   glance; a curious reader finds texture (annotations, outliers, a second panel).
6. **Decisive.** Take a position on what the data says. Where data runs out, speculate openly
   and label it as speculation ("our estimate", "if the trend holds"). Never invent data and
   present it as measured.

## Topic selection

- Read `archive/README.md` first. **Don't repeat a topic family two days running**, and don't
  repeat a specific subject within 60 days. Rotate widely across: energy & climate ·
  demography & health · economics & work · cities, housing & transport · geopolitics, borders
  & migration · science & technology · food, water & land · culture, language & time ·
  oceans, space & the natural world · institutions & law · infrastructure & logistics ·
  sport & play (only with a real-world point).
- Timeliness is a bonus, not a requirement. Use the date when it helps (season, anniversary,
  an event this week), but never at the expense of originality.
- Vary the form. Rotate chart types (dot plot, small multiples, map, slope, sawtooth, hero
  number, timeline, flow) so the archive doesn't settle into one look.
- Write five candidate headlines, apply the first-idea test, pick the most original one that
  the available data can support, and move on.

## Voice

Write the way the maintainer talks: clear, direct, simple, short, natural. It should read like
a person wrote it, not an AI.

- First person is fine ("I took every city..."). Talk to the reader like a smart friend.
- Short sentences. Plain words. Say the number, then move on.
- **No em dashes** (—) anywhere: not in posts, chart text or commit messages. Use a period,
  comma, colon or parentheses.
- Not formal. No section headers like "Why it matters" or "Key takeaways". No bolded lead-ins on
  every bullet.
- Don't hype. Avoid: striking, stark, notably, crucially, underscores, highlights, delve,
  landscape, tapestry, "it's not X, it's Y", "the story here is", "in a world where",
  rhetorical questions as openers, triplets for rhythm, and ending on a big moral.
- Headlines are short and plain ("The world's clocks run fast"), not two-clause slogans.
- Chart text follows the same rules: a short title, a one or two line deck, and plain labels.
- Before publishing, reread the post and cut anything that sounds like a press release.

## Data

- Prefer primary or well-curated open sources: Our World in Data grapher CSVs
  (`https://ourworldindata.org/grapher/<slug>.csv?v=1&csvType=full&useColumnShortNames=true`,
  metadata at `.metadata.json`), World Bank API, UN, IEA/Ember, FRED, Eurostat, NOAA/NASA,
  USGS, Wikipedia tables (cross-checked), and official statistics offices.
  A `FRED_API_KEY` environment variable is available in the cloud environment.
- Save every input used under `data/` in the entry folder so the analysis reruns offline.
  Save derived tables too (e.g. `data/<name>.csv`).
- If live data is unavailable, a carefully sourced hand-built dataset is acceptable. Cite every
  number's origin in a `data/SOURCES.md`.

## Design system

Every graphic uses the **Plate** house style. Read `STYLE.md` before drawing anything and use
`pix/style.py` (`from pix import style as px`). In short:

- `px.plate()` → `px.masthead()` → `px.headline()` → numbered `px.panel()`s → `px.footer()` →
  `px.save()`. Look at the latest entry's `analysis.py` for a working example.
- Warm paper, black ink, serif headline with one optional `*vermilion italic*` phrase, mono
  numbers, crop marks.
- Vermilion (`SIGNAL`) carries the point and taupe carries the context. Add indigo only for a
  real contrast. Most plates use one or two colours.
- Annotate directly. No legends where labels fit. No dual axes, 3D, rainbow scales or pie charts
  with more than 3 slices.
- The chart *form* should change from day to day. The plate stays the same.
- Render, then **open chart.png and look at it**. Fix overlaps, clipping and dead space before
  publishing.
- For an interactive piece, add a self-contained `index.html` in the same style. The README
  still shows the PNG.

## Daily procedure

A Claude Code scheduled task runs this every day at 8:05am US Eastern.

0. Setup: `pip install -r requirements.txt` (Inter font optional; style falls back gracefully).
1. `TZ=America/Detroit date +%F` gives the entry date. Read `archive/README.md` to see what's been covered.
2. Choose the topic (see above). Decide the one claim.
3. Create `archive/YYYY-MM-DD-<short-slug>/` containing:
   - `data/`: raw inputs + derived tables
   - `analysis.py`: loads `data/`, computes every number quoted, prints the key stats, and
     renders `chart.png` + `chart.svg`. It must run from the repo root with
     `python archive/<dir>/analysis.py`.
   - `post.md`: front matter (`date`, `title`, `slug`, `topic`, `chart`, `summary`), then:
     H1 headline · the image · one or two short paragraphs saying what I looked at and what I
     found · 3–6 plain bullets with the key numbers · one or two sentences on what it means ·
     a short **How I did it.** paragraph (sources, method, main caveat) · links to code, data
     and SVG. Aim for 200–350 words. Every number must come from `analysis.py` output.
4. Run `python scripts/publish.py`. It regenerates `README.md` (today's post) and
   `archive/README.md` (index).
5. Commit as `pix YYYY-MM-DD: <title>` and push to `main`.

## Repo layout

```
README.md               today's post (generated, don't edit by hand)
CLAUDE.md               this brief
pix/style.py            house visual style (see STYLE.md)
pix/fonts/              bundled fonts (OFL)
STYLE.md                the Plate style guide
scripts/publish.py      rebuilds README.md + archive/README.md
archive/README.md       index of every entry (generated)
archive/YYYY-MM-DD-slug/{post.md, chart.png, chart.svg, analysis.py, data/}
```
