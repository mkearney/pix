# Sources

- `faostat_world_area_production.csv`: FAOSTAT, Crops and livestock products (QCL), bulk download `Production_Crops_Livestock_E_All_Data_(Normalized).zip` from https://bulks-faostat.fao.org/production/ (file dated 2025-12-23), downloaded 2026-11-14. Trimmed to World (area code 5000) and the elements area harvested (ha), yield and production (t), every item, 1961 to 2024. CC BY 4.0 (FAO).
- `faostat_coffee_cocoa_by_country.csv`: same file, trimmed to coffee, green (item 656) and cocoa beans (item 661), area harvested and production, every country (area codes below 5000). Côte d'Ivoire's name is double-encoded in this file and fixed in `analysis.py`.

Derived (written by `analysis.py`):

- `decomposition_by_crop.csv`: for every item with data in both windows, area and production in 1986-90 and 2020-24 (five-year means), the output, area and yield ratios, and the land share of output growth.
