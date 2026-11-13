# Sources

- `oecd_annual_hours_per_worker.csv`: OECD, average annual hours actually worked per worker, all workers (dataflow `OECD.ELS.SAE,DSD_HW@DF_AVG_ANN_HRS_WKD,1.0`, `WORKER_STATUS=_T`), 2019 to 2025, from the OECD Data Explorer SDMX API (https://sdmx.oecd.org/public/rest/data/), downloaded 2026-11-13. Total hours worked in a year divided by average employment.
- `oecd_employment_rate_15_64.csv`: OECD Infra-annual labour statistics, employment rate, ages 15 to 64, annual, seasonally adjusted, both sexes (dataflow `OECD.SDD.TPS,DSD_LFS@DF_IALFS_EMP_WAP_Q,1.0`, key `.EMP_WAP.._Z.Y._T.Y15T64..A`), 2022 to 2025, same API and date. Percent of people aged 15 to 64 who are employed.

Derived (written by `analysis.py`):

- `hours_per_adult_2024.csv`: hours per worker, employment rate, hours per person aged 15 to 64, and both ranks, for every OECD member with both series in 2024.
