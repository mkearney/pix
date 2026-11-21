# Evidence

Finding: In the US, life expectancy at 40 is higher at every part of the household income distribution, with a gap of 14.6 years for men and 10.1 years for women between the top and bottom 1%.

Type: association.

Source: Chetty R, Stepner M, Abraham S, Lin S, Scuderi B, Turner N, Bergeron A, Cutler D. The association between income and life expectancy in the United States, 2001–2014. JAMA 315(16), 1750–1766 (2016). doi:10.1001/jama.2016.4226. PubMed 27063997. Released data: Health Inequality Project, Online Data Table 1, https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_1.csv (readme saved alongside). Erratum: JAMA 317(1):90 (2017), doi:10.1001/jama.2016.18691, "Missing Negative Symbol" (corrects a missing minus sign; the current abstract, full text and released table all give the headline numbers used here).

Design: Population-wide administrative data: 1,408,287,218 person-year observations of individuals aged 40 to 76 from deidentified federal tax records 1999–2014, linked to Social Security Administration death records (4.1 million deaths among men, 2.7 million among women). Life expectancy at 40 estimated by household income percentile and sex, race- and ethnicity-adjusted, pooling 2001–2014.

Key numbers:
- Gap top 1% minus bottom 1%: men 14.6 years (95% CI 14.4–14.8), women 10.1 (9.9–10.3). Abstract, Results. Reproduced from Online Data Table 1 (`le_raceadj`, normal-approximation CI from the reported standard errors); `analysis.py` asserts the match to one decimal place.
- Life expectancy at 40, bottom 1% and top 1%: men 72.7 and 87.3; women 78.8 and 88.9; median percentile men 81.7, women 85.0. Read from the released table in `analysis.py`.
- Life expectancy rises in 84 of 99 adjacent-percentile steps for men and 76 of 99 for women. Computed here; the dips are percentile-to-percentile noise, so the post says "across the whole income range" rather than "at every step".
- Mean household income in the men's table: p1 $356, p50 $62,567, p100 $1,982,300. Released table (`hh_inc`). Chart only.
- Norway: gap 13.8 years (12.3–15.2) for men and 8.4 (7.2–9.6) for women. Kinge et al. 2019, abstract. Transcribed; `analysis.py` asserts the strings appear in the saved abstract.

Corroboration:
- Kinge JM, Modalsli JH, Øverland S, et al. Association of household income with life expectancy and cause-specific mortality in Norway, 2005–2015. JAMA 321(19), 1916–1925 (2019). doi:10.1001/jama.2019.4329. Whole-population Norwegian registry data; life expectancy rises with income across the distribution; gaps of 13.8 (men) and 8.4 (women) years between the top and bottom 1%.
- National Academies of Sciences, Engineering, and Medicine. The Growing Gap in Life Expectancy by Income: Implications for Federal Programs and Policy Responses. National Academies Press (2015). doi:10.17226/19015. https://nap.edu/catalog/19015. Finds a large and widening gap in life expectancy between high and low earners in the US.

Wording check: Observational, so association wording throughout: "had a life expectancy ... longer", "rose across the income range", "the pattern is an association". The post states the main reason it cannot be read as causal (poor health lowers income).

Limits: The paper's own main caveat is confounding: income is correlated with other traits that affect health, so causal effects are likely smaller than the associations. Income is measured from tax records two years before the mortality year to limit reverse causation, but people whose health limited their earnings for longer can still sit in low percentiles, which can widen the gap at the bottom. Estimates are race-adjusted, and mortality beyond the ages observed is extrapolated in the paper. Covers 2001–2014; later years (including COVID) are not included. The Norway comparison is not like-for-like: Kinge et al. use household income adjusted for household size over 2005–2015, while Chetty et al. use pretax household earnings.

Fact-check: An independent subagent checked every number against the released CSV, the Chetty and Kinge abstracts and the PMC full text, confirmed the sample description and that the y-axis is expected age at death, confirmed 'no plateau' against the paper ('no dividing line above or below which higher income was not associated with higher life expectancy'), and found no retraction or credible dispute of the gradient (Deaton's editorial concerns measurement, not the gradient). Verdict: pass with fixes. Changed as a result: the caveat now names confounding as well as reverse causation (post and chart); the chart's mean-income labels say they are the men's rows; the erratum is described as a missing minus sign rather than 'typographic'; Limits now note the two-year income lag and the different income definition in Norway; the summary and chart deck now use the past tense.
