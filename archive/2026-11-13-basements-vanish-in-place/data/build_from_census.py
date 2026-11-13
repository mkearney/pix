"""Rebuild the two CSVs in this folder from Census downloads.

1. census_foundation_by_region.csv  <- foundation_cust.xls (kept here), sheet SFTotalFoundation.
   Houses completed by year, region and foundation type, 1971-2025 (thousands).
2. soc_completions_by_division.csv  <- Survey of Construction microdata, socYY.zip / socYY.xlsx
   for 1999-2025 (about 530 MB unzipped, so not kept here). Download them from
   https://www.census.gov/construction/chars/microdata.html into a folder and pass its path:

    python archive/2026-11-13-basements-vanish-in-place/data/build_from_census.py /path/to/soc

Needs xlrd and openpyxl on top of requirements.txt. analysis.py only reads the CSVs.
"""
import glob
import sys
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
REGIONS = ("United States", "Northeast", "Midwest", "South", "West")

v = pd.read_excel(HERE / "foundation_cust.xls", sheet_name="SFTotalFoundation", header=None)
rows, reg = [], None
for _, r in v.iterrows():
    if isinstance(r[1], str) and r[1].strip() in REGIONS:
        reg = r[1].strip()
        continue
    s = str(r[0]).strip()
    if reg and s.isdigit() and 1971 <= int(s) <= 2025:
        rows.append(dict(region=reg, year=int(s), total=r[1], basement=r[2], slab_other=r[3], crawl=r[4]))
pd.DataFrame(rows).to_csv(HERE / "census_foundation_by_region.csv", index=False)

if len(sys.argv) > 1:
    src = Path(sys.argv[1])
    out = []
    for year in range(1999, 2026):
        yy = f"{year % 100:02d}"
        f = [p for p in glob.glob(str(src / f"soc{yy}*")) + glob.glob(str(src / f"soc{yy}" / "*"))
             if p.lower().endswith((".xls", ".xlsx"))][0]
        x = pd.read_excel(f, usecols=lambda c: c.upper() in ("COMP", "DIV", "BASE", "WEIGHT", "DET"))
        x.columns = [c.upper() for c in x.columns]
        c = x[x.COMP // 100 == year]                       # houses completed in that year
        g = (c.assign(basement=(c.BASE == 1) * c.WEIGHT, not_reported=(c.BASE == 0) * c.WEIGHT)
              .groupby(["DIV", "DET"])
              .agg(units=("WEIGHT", "sum"), basement=("basement", "sum"),
                   not_reported=("not_reported", "sum"), sample=("WEIGHT", "size"))
              .reset_index())
        g.insert(0, "year", year)
        out.append(g)
    pd.concat(out).rename(columns=str.lower).to_csv(HERE / "soc_completions_by_division.csv", index=False)
