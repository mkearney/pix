# Sources

- `submarinecablemap_cables_2026-11-15.json`: every cable on TeleGeography's Submarine Cable Map (https://www.submarinecablemap.com), fetched 2026-11-15 from its public API: the list at `/api/v3/cable/all.json` (714 cables) and each cable's record at `/api/v3/cable/<id>.json` (name, length, owners, ready-for-service year, planned flag, landing points). The map covers cables in service or planned; retired cables are not listed. Data © TeleGeography, used under the map's CC BY-NC-SA 3.0 licence.

Derived (written by `analysis.py`):

- `cables.csv`: one row per cable with length in km, ready-for-service year, planned flag, number of owners, and which of Google, Meta, Amazon and Microsoft are among the owners.
- `cohorts.csv`: for each five-year ready-for-service cohort, cables and km in total and with a big-tech owner, and both shares.
