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

Import the house style: `from pix.style import apply, title_block, footer, ACCENT, ...`
(see `pix/style.py`). Its rules:

- Warm off-white surface, near-black ink, Inter typeface, recessive grid, no top/right spines.
- **One accent colour carries the story** (`ACCENT`, orange); everything else is ink or
  `NEUTRAL` gray. Add `ACCENT_2` (blue) only for a genuine contrast. Use the full `PALETTE`
  only when identity really needs it, in fixed order, max ~6 series.
- Headline (the claim) + a 2–3 line deck explaining how to read it, left-aligned at the top.
  A source and method line in the footer.
- Annotate directly on the chart. Avoid legends where labels can sit next to the marks.
- Never use dual y-axes, pie charts with more than 3 slices, rainbow colour scales, or 3D.
- Render `chart.png` at dpi 150 (around 1800 px wide) plus `chart.svg`. Then **open the PNG and
  look at it.** Fix overlapping labels, clipped text and empty space before publishing.
- Formats can vary: static chart (default), small multiples, an annotated map, a slope or dot
  plot, a single "hero number" infographic. If a richer interactive piece is warranted, add
  `index.html` alongside it (self-contained, no external data calls). The README still shows the
  PNG.

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
     H1 headline · the image · **The point** (2–3 sentences) · *What the chart shows* ·
     *What stands out* (3–5 numbered findings with numbers) · *Why it matters now* ·
     *Method & caveats* · links to files. Every number in the post must come from `analysis.py`
     output.
4. Run `python scripts/publish.py`. It regenerates `README.md` (today's post) and
   `archive/README.md` (index).
5. Commit as `pix YYYY-MM-DD: <title>` and push to `main`.

## Repo layout

```
README.md               today's post (generated, don't edit by hand)
CLAUDE.md               this brief
pix/style.py            house visual style
scripts/publish.py      rebuilds README.md + archive/README.md
archive/README.md       index of every entry (generated)
archive/YYYY-MM-DD-slug/{post.md, chart.png, chart.svg, analysis.py, data/}
```
