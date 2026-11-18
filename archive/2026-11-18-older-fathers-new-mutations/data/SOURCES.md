# Sources

- `jonsson2017_decode_dnms.tsv.gz`: the paper's released table of 108,778 de novo mutations, one row each, with the proband, both parents' ages at conception, read counts and parent of origin where traced. It is `decode_DNMs/decode_DNMs.tsv` from the Supplementary Data of Jónsson et al., Nature 549, 519–522 (2017), doi:10.1038/nature24018, downloaded on 2026-11-18 from https://static-content.springer.com/esm/art%3A10.1038%2Fnature24018/MediaObjects/41586_2017_BFnature24018_MOESM2_ESM.zip (inside `Aging_Oocytes_Supplementary_Table_DNMs.tar.gz`). Gzipped here; otherwise unchanged.

Derived (written by `analysis.py`):

- `per_proband_autosomes.csv`: one row per child: parents' ages, autosomal mutation count, and how many were traced to the father, to the mother, or not traced.
- `model_fit.csv`: the refit Poisson model (intercepts and per-year slopes for each parent, with standard errors and 95% intervals).
- `expected_by_parent_age.csv`: expected mutations from each parent, and in total, when both parents are 20, 30 or 40.
