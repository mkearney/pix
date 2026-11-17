# Sources

All three files were downloaded on 2026-11-17 from Our World in Data grapher CSVs (`?v=1&csvType=full&useColumnShortNames=true`).

- `owid_migrant_stock_share.csv`: https://ourworldindata.org/grapher/migrant-stock-share. International migrants (people living in a country other than the one they were born in, or of foreign citizenship where birthplace isn't recorded) as a percent of the population, 1990-2024 in five-year steps. Underlying source: UN DESA Population Division, International Migrant Stock 2024. CC BY 4.0 via OWID.
- `owid_migrant_stock_total.csv`: https://ourworldindata.org/grapher/migrant-stock-total. The same series as a count of people.
- `owid_world_bank_income_groups.csv`: https://ourworldindata.org/grapher/world-bank-income-groups. World Bank income classification by year; the latest year (2025) is used to pick high-income countries.

Derived (written by `analysis.py`):

- `high_income_1990_2024.csv`: for each high-income country with 1 million people or more, the foreign-born share and count in 1990 and 2024, the implied total population (count / share), and the native-born population.
