# Sources

- `usgs_m6_2000_2026.csv`: USGS ComCat FDSN event service, downloaded 2026-11-12 UTC.
  Query: `https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2000-01-01&endtime=2026-11-01&minmagnitude=6&orderby=time-asc`.
  Public domain (US government). Only rows with `type == earthquake` are used.
- Energy uses the Gutenberg-Richter energy relation, log10(E) = 1.5M + 4.8 (E in joules), applied to the catalogue magnitude.

Derived:
- `quakes_ranked.csv`: every quake ranked by energy, with cumulative share.
- `biggest_quakes.csv`: the quakes needed to reach half the total.