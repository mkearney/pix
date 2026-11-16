# Sources

- `gcat_payloads.csv`: Jonathan McDowell's General Catalog of Artificial Space Objects (GCAT), main satellite catalog `satcat.tsv` from https://planet4589.org/space/gcat/ (file header: updated 2026 Nov 15), downloaded 2026-11-16. Trimmed to payloads (object type starting with P) and the columns JCAT id, US catalog number, type, name, launch date, owner, state, mass (kg), mass flag and operational orbit. GCAT is released under CC BY 4.0.

Derived (written by `analysis.py`):

- `median_mass_by_year.csv`: payloads launched per year, how many have a mass, median mass with and without Starlink, and the share at 10 kg or less.
