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
- Write five candidate headlines, apply the first-idea test and the originality checks below,
  pick the most original one that the available data can support, and move on.

## Originality checks

Asking for originality isn't enough; these checks make it a step you can't skip. Every
entry records them in `prior_art.md`, and `scripts/publish.py` refuses entries without it.

1. **Search before you build.** For the chosen candidate, run at least five web searches
   before writing any analysis code: the claim in plain words, the key number, the dataset
   name plus "chart" or "map", and checks of the usual suspects (Our World in Data, FT, The
   Economist, Visual Capitalist, Reddit r/dataisbeautiful and r/MapPorn, Wikipedia). Log the
   queries.
2. **Name the closest take.** Link the one or two existing pieces nearest to yours and say in
   one sentence what yours adds. If one of them makes the same point with the same kind of
   data, the candidate is dead. Pick another or push the angle further. "Nobody has done
   this" is only allowed after the searches came back empty, and it should be rare.
3. **Write the naive prediction first.** Before looking at results, write one sentence on what
   a smart reader would guess. If the data just confirms that guess, it isn't a post unless
   the size of the effect is the surprise, and then the headline has to lead with the size.
4. **Your own number has to carry it.** The headline figure must come from your own
   computation (a join, a re-weighting, a derived measure), not be read off a single
   published table. If the key number already appears in a source's summary, you're
   re-reporting, not analysing.
5. **Rotate the kind of claim, not just the chart.** Give every entry a `claim:` field in its
   front matter, one of:
   - `share`: what fraction of some population is in a group ("57% were born after...")
   - `concentration`: a few cases account for most of the total
   - `equivalence`: one quantity restated as a familiar one ("a South Korea of solar")
   - `gap`: two things that should match don't (clock noon vs solar noon)
   - `reversal`: a ranking or trend flips under a different measure or weighting
   - `turning-point`: when something changed direction, and by how much
   - `mechanism`: the data shows why something happens, not just that it does
   - `outlier`: one case breaks a pattern everything else follows
   - `crossover`: when two lines met or will meet (forecasts labelled as estimates)

   Don't use the same claim type as either of the previous two entries, and don't use any
   type more than twice in the last seven. Headlines shaped "X% of people..." are the house
   habit to watch.
6. **Avoid known viral formats** unless the angle is clearly new: "share of people born after
   [event]", "more people live inside this circle than outside it", solar time vs clock time
   maps, true-size or Mercator overlays, "if the world were 100 people", population by
   latitude, and "[country] compared with every other country" equivalences. Don't reuse a
   format the archive itself used in the last 30 days.
7. **Distrust the calendar.** Anniversaries and this week's news are where every other outlet
   is looking. A date-hooked topic needs a closest-take search aimed at that date (e.g. the
   event name plus "chart" plus this year) and must still pass check 2.

`prior_art.md` is short and plain, in this shape:

```
# Prior art
Claim type: gap
Naive prediction: one sentence.
Candidates considered: the five headlines, one line each on why the losers lost.
Searches: the queries run.
Closest takes: link, one line each.
What this adds: one or two sentences.
```

## Voice

Write like the maintainer: a senior, Python-first data scientist who has been sharing analyses in
public for a long time. Clear, direct, confident, a little dry. It should read like a person
wrote it, and like that person reviewed it before posting.

**Tone (keep):**
- First person, talking to a smart reader as a peer. Say what you looked at, what you found, and
  move on.
- The point first, in plain words. Then the numbers that back it up.
- Dry wit is welcome, at most one light line per post, and never at the expense of the finding.
  Understatement over exclamation.
- Generous: credit the dataset, the method or the person whose work made it possible.
- Practical: the code and data are always there, and the post makes it easy to check the work.

**Maturity and depth:**
- Write for people who already know what a median, a log scale or a regression is. Don't explain
  basics. Do explain the one methodological choice that matters (weighting, a threshold, a
  definition) and why it was made.
- Show rigour without showing off: a sensitivity check, an honest caveat, the size of the
  uncertainty when it matters. One sentence each, not a methods section.
- The toolkit is Python (pandas, numpy, matplotlib, statsmodels, scikit-learn and friends). If a
  tool is worth naming, name the Python one.
- Be decisive. Take a position the data supports and label speculation as speculation.

**Polish (required):**
- Every post gets an edit pass before publishing. Cut filler, hedges and repeated ideas until
  every sentence earns its place.
- Check each number against `analysis.py` output: same rounding, units and spelling everywhere
  (post, chart, summary).
- No typos, no slang ("nah", "obvi", "y'all"), no emoji, no exclamation marks, no
  ALL CAPS for emphasis, no square-bracket asides.
- **No em dashes** (—) anywhere: not in posts, chart text or commit messages. Use a period,
  comma, colon or parentheses.
- Not formal either. No section headers like "Why it matters" or "Key takeaways", and no bolded
  lead-ins on every bullet.
- Don't hype. Avoid: striking, stark, notably, crucially, underscores, highlights, delve,
  landscape, tapestry, game-changer, "it's not X, it's Y", "the story here is", "in a world
  where", rhetorical questions as openers, triplets for rhythm, and ending on a big moral.
- Headlines are short and plain ("The world's clocks run fast"), not two-clause slogans.
- Chart text follows the same rules: a short title, a one or two line deck, and plain labels.
- Last step: read the post once as a skeptical expert and once as a busy reader. Fix whatever
  either one would trip on.

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
2. Choose the topic (see above). Decide the one claim. Run the originality checks before
   writing analysis code.
3. Create `archive/YYYY-MM-DD-<short-slug>/` containing:
   - `prior_art.md`: the originality log (see Originality checks)
   - `data/`: raw inputs + derived tables
   - `analysis.py`: loads `data/`, computes every number quoted, prints the key stats, and
     renders `chart.png` + `chart.svg`. It must run from the repo root with
     `python archive/<dir>/analysis.py`.
   - `post.md`: front matter (`date`, `title`, `slug`, `topic`, `claim`, `chart`, `summary`), then:
     H1 headline · the image · one or two short paragraphs saying what I looked at and what I
     found · 3–6 plain bullets with the key numbers · one or two sentences on what it means ·
     a short **How I did it.** paragraph (sources, method, main caveat) · links to code, data
     and SVG. Aim for 200–350 words. Every number must come from `analysis.py` output.
4. Run `python scripts/publish.py`. It regenerates `README.md` (today's post) and
   `archive/README.md` (index).
5. Commit as `pix YYYY-MM-DD: <title>` and push to `main`.

**Never rename, re-date, move or edit a published entry** unless the maintainer asks. If an
entry already exists for today's date, stop and report it.

## Repo layout

```
README.md               today's post (generated, don't edit by hand)
CLAUDE.md               this brief
pix/style.py            house visual style (see STYLE.md)
pix/fonts/              bundled fonts (OFL)
STYLE.md                the Plate style guide
scripts/publish.py      rebuilds README.md + archive/README.md
archive/README.md       index of every entry (generated)
archive/YYYY-MM-DD-slug/{post.md, prior_art.md, chart.png, chart.svg, analysis.py, data/}
```
