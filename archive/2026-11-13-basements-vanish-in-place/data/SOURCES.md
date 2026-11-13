# Sources

- `foundation_cust.xls`: US Census Bureau, Characteristics of New Housing, "Type of Foundation in New Single-Family Houses Completed", 1971-2025, by region. https://www.census.gov/construction/chars/xls/foundation_cust.xls (downloaded 2026-11-13). Sheet `SFTotalFoundation` is parsed to `census_foundation_by_region.csv` (thousands of houses).
- Survey of Construction public-use microdata, 1999-2025, https://www.census.gov/construction/chars/microdata.html (files `soc99.zip` to `soc19.zip`, `soc20.xlsx` to `soc25.xlsx`, downloaded 2026-11-13). Variables: `COMP` (completion month), `DIV` (census division), `DET` (detached/attached), `BASE` (1 = full or partial basement), `WEIGHT`. The raw files are about 530 MB, so only the aggregate is kept: `soc_completions_by_division.csv` = weighted houses completed in each calendar year by division and design, with weighted basement and not-reported counts and the sample size. Rebuild with `build_from_census.py`.
- Check: the microdata gives 37.3% (2000) and 15.8% (2025) with basements; the published table gives 37.4% and 15.9%.

Derived by `analysis.py`:
- `decomposition_2000_2025.csv`: basement rate and share of houses by division in 2000 and 2025, and each division's within-division contribution to the national change.
- `counterfactual_series.csv`: actual national basement share from the microdata, and the share if every division had kept its 2000 rate.
