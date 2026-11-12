<sub>**pix** · one visual analysis of the world, every day · No. 1 · 2026-11-12 · Time · [archive →](archive/)</sub>

# Humanity's clocks run fast. Almost nobody lives with the sun ahead of the clock.

![Clock time of solar noon for 34,212 cities by longitude, and the population-weighted distribution](archive/2026-11-12-clocks-run-fast/chart.png)

**The point:** In theory, time zones are centred on the sun, so cities should sit evenly on both sides of "true noon". In practice, governments almost always push the clock forward and almost never pull it back. **38% of the world's city-dwellers see the sun peak at 12:30 or later. Only 1.1% see it at 11:30 or earlier.** That's a 35-to-1 skew, and the typical urban human's sun peaks 24 minutes after the clock says noon.

### What the chart shows

- **Top:** every city with 15,000+ people, plotted by longitude against the clock time when the sun is highest, averaged over 2026 (so daylight saving counts for the months it's in force). Within a time zone the sun reaches cities later as you go west, which produces the sawtooth. A long, unbroken diagonal means a country has chosen one clock for a lot of longitude.
- **Bottom:** the same cities weighted by population. Orange means the sun is at least 30 minutes late, blue at least 30 minutes early.

### What stands out

1. **The skew is the story.** 78% of city-dwellers have solar noon after 12:00. Push the threshold to 30 minutes and it's 38% late against 1.1% early. At an hour, it's 12% against effectively zero.
2. **Daylight saving explains only part of it.** On standard time alone, 27.5% of people still have the sun 30+ minutes late, and the mean offset is 17 minutes. Clocks are set ahead even before summer time adds its extra hour.
3. **Spain is the world's most "jet-lagged" country.** The population-weighted solar noon is 1h43m after 12:00. Spain lies mostly west of London but has kept Central European Time since 1940, and Seville's sun peaks at almost 2pm. France (+1h23), Argentina (+1h05) and Malaysia (+1h07) follow.
4. **China's single clock creates both extremes.** Beijing time covers more than 60° of longitude. Kashgar's sun peaks near 3pm and Lhasa's near 2pm, while Hegang in the far northeast sees solar noon at 11:19, one of the few large blue clusters on Earth. Officially, every one of them is "noon at 12".
5. **The early-sun club is small and specific:** Brazil's Atlantic coast (Recife −40m), the eastern edges of Indonesia's zones and of India's single zone, northeast China and Mozambique. Japan (−9m) is one of the only big countries that sits slightly early.

### Why it matters

Clock time sets when school starts, when shifts begin and when people wake. Solar time sets when it gets light and when the body clock expects to be up. Societies that keep their clocks well ahead of the sun get darker mornings, later dinners and, according to a growing body of sleep research, shorter sleep. Spain has debated returning to "its" time zone for a decade, and the EU's plan to abolish clock changes stalled in 2019. The chart shows how unusual the alternative would be: almost no country chooses to have the sun early.

### Method & caveats

- **Cities:** GeoNames `cities15000` (34,212 places, 4.08bn people). That is urban population only, roughly half of humanity, with city boundaries that vary by country.
- **Solar noon** = 12:00 − longitude/15 h + UTC offset. Offsets come from the IANA time-zone database for every day of 2026 and are averaged, so DST is weighted by how long it lasts. Averaged over a year, the equation of time nets to about zero, so it's omitted. On any given day the sun can be up to about 16 minutes either side of these values.
- **China** is set to its legal Beijing time everywhere. Many people in Xinjiang informally use UTC+6, which would halve Kashgar's offset.
- "Late" and "early" are relative to astronomical noon, not to a judgement about the right time.

**Files:** [`analysis.py`](archive/2026-11-12-clocks-run-fast/analysis.py) · [`data/`](archive/2026-11-12-clocks-run-fast/data/) · [`chart.svg`](archive/2026-11-12-clocks-run-fast/chart.svg)

---

<sub>Previously: this is the first one. · [full archive](archive/) · [how this works](CLAUDE.md)</sub>
