# Sources

- `cities15000.csv`: GeoNames `cities15000.zip` (https://download.geonames.org/export/dump/), downloaded 2026-11-12 UTC, CC BY 4.0. Trimmed to id, name, country code, lat, lon, population and feature code. Capitals are rows with feature code `PPLC`. Rows with `PPLX` (sections of a larger city) are dropped in the analysis.
- `countries.csv`: GeoNames `countryInfo.txt`, same source and date. Used for country names and population (to flag states under 1 million people in the sensitivity check).
- Israel has no `PPLC` row in GeoNames; Jerusalem (the seat of government) is used. Western Sahara and Palestine have no single capital in the data and are left out of the "home" side.

Derived:
- `city_capital_distance.csv`: per city, great-circle km to its own capital and to the nearest foreign capital.
- `country_share.csv`: per state, city population and share closer to a foreign capital.
