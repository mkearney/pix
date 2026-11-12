# Sources

- `wpp2024_single_age_2026.csv`: UN World Population Prospects 2024, population by single year of age, medium variant, 2024 to 2100 (`WPP2024_PopulationBySingleAgeSex_Medium_2024-2100.csv.gz` from https://population.un.org/wpp/downloads), downloaded 2026-11-12. Trimmed to the year 2026 (population on 1 July 2026), countries/areas plus World, both sexes. `pop_thousands` is in thousands. Age 100 is an open 100+ group. CC BY 3.0 IGO.
- Event dates are standard historical dates: Moon landing 20 Jul 1969, Chernobyl 26 Apr 1986, fall of the Berlin Wall 9 Nov 1989, end of the Soviet Union 26 Dec 1991, 9/11 attacks 11 Sep 2001, WHO declares Covid-19 a pandemic 11 Mar 2020.

Derived (written by `analysis.py`):

- `country_share.csv`: population and share born after 9 Nov 1989, by country.
- `world_curve.csv`: share of the world population born after each date, 1925 to 2026.
