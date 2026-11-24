# Evidence

Finding: Within a school year, the youngest children are diagnosed with and treated for ADHD more often than the oldest; in US states with a September 1 kindergarten cutoff, August-born children had a 34% higher diagnosis rate than September-born children.

Type: effect.

Source: Layton TJ, Barnett ML, Hicks TR, Jena AB. Attention deficit-hyperactivity disorder and month of school enrollment. N Engl J Med 379(22), 2122–2130 (2018). doi:10.1056/NEJMoa1806828. PubMed 30485780. Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6322209/. No released data (commercial claims database).

Design: Natural experiment using birth month around an arbitrary school-entry cutoff. 407,846 US children born 2007–2009 in a large commercial insurance database, followed through 2015 (so up to about age 7; the paper describes them as 4 to 7 years old). Diagnosis is claims-based: an ICD-9 ADHD code (314.00/314.01) or a filled stimulant prescription. Compares August-born with September-born children in states with a September 1 cutoff, with states without that cutoff as a control; placebo comparisons of other adjacent months, and of asthma, diabetes and obesity, showed no difference.

Key numbers:
- Diagnosis per 10,000: August-born 85.1 (95% CI 75.6–94.2; 309 of 36,319), September-born 63.6 (55.4–71.9; 225 of 35,353); difference 21.5 (8.8–34.0). Abstract, Results. Transcribed and asserted against the saved abstract.
- 34% more: 85.1 / 63.6 = 1.34, derived here.
- States without a September 1 cutoff: difference 8.9 (−14.9 to 20.8). Abstract. The authors say the gap was not present; there was no formal test of whether the two gaps differ. The post says "smaller and not significant".
- Treatment per 10,000: 52.9 (45.4–60.3) vs 40.4 (33.8–47.1). Abstract. Chart only.
- Canada (BC): December vs January born, diagnosis RR boys 1.30 (1.23–1.37), girls 1.70 (1.53–1.88). Morrow 2012 abstract.
- Norway: October–December vs January–March, ADHD medication HR boys 1.4 (1.4–1.5), girls 1.8 (1.7–2.0). Karlstad 2017 abstract.
- Finland: September–December vs January–April, diagnosis incidence ratio boys 1.26 (1.18–1.35), girls 1.31 (1.12–1.54). Sayal 2017 abstract.
- Iceland: youngest vs oldest third, stimulant prescription RR 1.5 (1.3–1.8). Zoëga 2012 abstract.
- Denmark: October–December vs January–March, medication PPR 1.08 (1.04–1.12); 40% of October–December born children entered school a year late. Pottegård 2014 abstract.
- Pooled medication RR 1.28 (1.21–1.36) from the meta-analysis (the review covered 32 studies; fewer were pooled for medication, with I² = 94%). Frisira 2025 abstract and Results. The paper's pooled diagnosis RR is printed as 1.38 (95% CI 1.36–1.52), an interval that sits oddly around its estimate, so it is not used.
- "17 of 19 studies", "13 countries": Whitely 2019 abstract.
All asserted against the saved texts in `analysis.py`.

Corroboration:
- Frisira E, Holland J, Sayal K. Systematic review and meta-analysis: relative age in attention-deficit/hyperactivity disorder and autism spectrum disorder. Eur Child Adolesc Psychiatry 34, 381–401 (2025). doi:10.1007/s00787-024-02459-x. 32 studies; younger relative age associated with ADHD diagnosis and medication (medication RR 1.28).
- Whitely M, Raven M, Timimi S, et al. Annual Research Review: Attention deficit hyperactivity disorder late birthdate effect common in both high and low prescribing international jurisdictions: a systematic review. J Child Psychol Psychiatry 60, 380–391 (2019). doi:10.1111/jcpp.12991. 19 studies in 13 countries, 15.4 million children; 17 found the youngest considerably more likely to be diagnosed or medicated; two Danish studies found a weak or no effect.
- Morrow RL, Garland EJ, Wright JM, et al. Influence of relative age on diagnosis and treatment of attention-deficit/hyperactivity disorder in children. CMAJ 184, 755–762 (2012). doi:10.1503/cmaj.111619. 937,943 children in British Columbia.
- Sayal K, Chudal R, Hinkka-Yli-Salomäki S, et al. Relative age within the school year and diagnosis of attention-deficit hyperactivity disorder: a nationwide population-based study. Lancet Psychiatry 4, 868–875 (2017). doi:10.1016/S2215-0366(17)30394-2.
- Also: Karlstad 2017 (doi:10.1177/1403494817708080), Zoëga 2012 (doi:10.1542/peds.2012-0689), Pottegård 2014 (doi:10.1111/jcpp.12243); regression-discontinuity studies such as Evans, Morrill and Parente, J Health Econ 2010.

Independence: Sayal is an author of both Frisira 2025 and the Finland study; the other corroborating studies come from separate groups and countries.

Wording check: Birth month relative to an arbitrary cutoff is close to random, so the design supports a causal reading for the effect of relative age on being diagnosed and treated. The post uses descriptive verbs ("are diagnosed", "had", "show") and does not claim that the extra diagnoses are wrong, since whether they reflect misdiagnosis of immaturity or real difficulty is still debated (the chart note says so).

Limits: Claims and registry data record diagnoses and prescriptions, not symptoms; the reasons for the gap (teacher comparisons with older classmates, real stress at school entry) are not settled. Comparisons differ between countries (single months, quarters, thirds of a year), so the ratios are not directly comparable. The US data come from one commercial insurer and exclude Medicaid; rates are early-school-age rates and lower than national childhood ADHD prevalence. The meta-analysis estimates are highly heterogeneous (I² = 94% for medication).

Fact-check: An independent subagent checked every number against the Layton full text (PMC6322209) and the other abstracts, confirmed all eight DOIs on Crossref with no update or retraction relations, found no retraction, erratum or expression of concern in PubMed, and found the effect itself undisputed (the NEJM 2019 letters and the wider debate concern why it happens). Verdict: pass with fixes. Changed as a result: the meta-analysis is no longer described as pooling 32 studies (32 is the whole review); the US rates now say 'by about age 7', since children were followed only to 2015; the claims-based definition of diagnosis is stated in the chart footer and Design; 'no clear gap' became 'smaller and not significant'; 'the same pattern' became 'a similar gap' and the panel title no longer calls British Columbia and the meta-analysis national registries; the Denmark sentence states the 40% fact rather than implying a cause; the panel subtitle names prevalence ratios; the axis notes the log scale; the treatment ratio printout was dropped; Limits now note Medicaid exclusion, heterogeneity and shared authorship.
