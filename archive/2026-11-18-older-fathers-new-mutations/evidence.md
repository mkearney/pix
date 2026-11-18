# Evidence

Finding: The number of new (de novo) mutations in a child rises by about 1.51 per year of the father's age at conception and 0.37 per year of the mother's.

Type: moderator (the age effect depends on which parent).

Source: Jónsson H, Sulem P, Kehr B, et al. Parental influence on human germline de novo mutations in 1,548 trios from Iceland. Nature 549, 519–522 (2017). doi:10.1038/nature24018. Article: https://www.nature.com/articles/nature24018. Released data: Supplementary Data, `41586_2017_BFnature24018_MOESM2_ESM.zip`.

Design: Whole-genome sequencing at about 35x of 1,548 Icelandic parent-child trios (deCODE genetics). 108,778 high-quality de novo mutations. Parent of origin traced for 42,961 of them, by haplotype sharing in 225 three-generation families or by read-pair tracing.

Key numbers:
- 70.3 mutations per child. Paper, p. 519 ("an average of 70.3 DNMs per proband"). Reproduced: 70.3.
- Paternal slope 1.51 a year (95% CI 1.45–1.57), maternal 0.37 (0.32–0.43). Paper, p. 520, and Supplementary Table 6. Reproduced exactly from the released table using the paper's model on autosomes; `analysis.py` asserts the match.
- 80.4% of mutations of paternal origin in the three-generation families. Paper, p. 520. Reproduced: 80.4%.
- 225 three-generation families, 97.7% of their autosomal mutations traced. Computed here.
- Expected totals of 47, 66 and 85 for parents aged 20, 30 and 40, and a paternal share of 77% to 78% at those ages. Derived here from the refit lines; not in the paper.

Corroboration:
- Kong A, et al. Rate of de novo mutations and the importance of father's age to disease risk. Nature 488, 471–475 (2012). doi:10.1038/nature11396. 78 Icelandic trios; about two extra mutations per year of the father's age, which explains nearly all the remaining variation between children.
- Goldmann JM, et al. Parent-of-origin-specific signatures of de novo mutations. Nature Genetics 48, 935–939 (2016). doi:10.1038/ng.3597. 816 trios, no deCODE samples; mutations increase with paternal age and, less, with maternal age.
- Porubsky D, et al. Human de novo mutation rates from a four-generation pedigree reference. Nature 643, 427–436 (2025). doi:10.1038/s41586-025-08922-2. Near-complete genomes of a 28-member family; 75–81% of new mutations of every kind come from fathers.

Wording check: The data are observational, but "older fathers pass on more" and "each year adds" are causal phrasings. They are justified: parental age cannot plausibly be confounded with germline mutation counts, the gradient is replicated across cohorts and methods, and accumulation with age in the male germline is accepted biology. The mechanism sentence in the post is labelled "the usual explanation" because how much of the paternal excess comes from cell division rather than DNA damage is still debated (Gao et al., PNAS 2019).

Limits: One population (Iceland). Short-read sequencing misses repeats and structural changes, so true totals are higher: Porubsky et al. count 98–206 per generation with near-complete genomes. The expected totals extrapolate straight lines; 157 of the 1,548 mothers were 38 or older at conception.

Fact-check: Every number in post.md and on the chart traced to `analysis.py` output and, where the paper reports it, to the page above. Citations, DOIs and author lists checked against PubMed and doi.org. Plate's "consistent with" column checked against each abstract (Porubsky 2025 is cited for the paternal share, not for the age slope).
