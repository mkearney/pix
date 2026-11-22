# Evidence

Finding: Warming caused by CO2 is close to proportional to cumulative CO2 emissions, about 0.45°C per 1000 GtCO2 (likely 0.27 to 0.63°C).

Type: dose-response.

Source: IPCC, 2021: Summary for Policymakers. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge University Press, pp. 3–32. doi:10.1017/9781009157896.001. Full text: https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf. Paragraphs D.1.1 and D.1.2 saved in `data/ipcc_ar6_wg1_spm_D1.txt`.

Design: Consensus assessment (high confidence) combining observations, Earth system and emulator models and carbon-cycle theory; reaffirms the AR5 (2013) finding. The chart's observed series are public data: Global Carbon Budget cumulative CO2 including land-use change (via Our World in Data), 1850–2025, and HadCRUT.5.1.0.0 global annual temperature with 95% ranges, re-based to 1850–1900.

Key numbers:
- 0.45°C per 1000 GtCO2, likely range 0.27–0.63°C; "near-linear relationship". IPCC SPM D.1.1. `analysis.py` asserts the exact wording appears in the saved SPM text.
- 1850–2019 cumulative emissions 2390 ± 240 GtCO2. IPCC SPM D.1.2. The Global Carbon Budget series used here gives 2,528 GtCO2 for 1850–2019, inside that range (`analysis.py` asserts it); later Global Carbon Budget editions revised land-use emissions upward.
- 2,780 GtCO2 emitted 1850–2025. Computed from the Global Carbon Budget series.
- 1.28°C: mean HadCRUT5 anomaly 2016–2025 relative to 1850–1900. Computed here. Check: 2011–2020 gives 1.11°C against the IPCC's 1.09°C (SPM A.1.2).
- 43 GtCO2 emitted in 2025 (43.3 in the series; preliminary) and 47% of the all-time total emitted from 1990 on. Computed from the series; chart only.
- The observed ratio, 0.49°C per 1000 GtCO2 in 2016–2025, is printed by `analysis.py` but not claimed in the post, because observed warming includes non-CO2 effects.

Corroboration:
- Matthews HD, Gillett NP, Stott PA, Zickfeld K. The proportionality of global warming to cumulative carbon emissions. Nature 459, 829–832 (2009). doi:10.1038/nature08047. Shows warming is approximately proportional to cumulative carbon emissions, independent of the emission pathway, across models and observations.
- Allen MR, Frame DJ, Huntingford C, et al. Warming caused by cumulative carbon emissions towards the trillionth tonne. Nature 458, 1163–1166 (2009). doi:10.1038/nature08019. Peak warming is determined by cumulative CO2 emissions, largely independent of their timing.
- Earlier groundwork: Matthews HD, Caldeira K. Stabilizing climate requires near-zero emissions. Geophysical Research Letters 35, L04705 (2008), showed warming from emitted CO2 persists roughly constant after emissions stop; the post therefore says the relationship was formalised, not first shown, in 2009.
- Forster PM, Smith C, Walsh T, et al. Indicators of Global Climate Change 2024. Earth System Science Data 17, 2641–2680 (2025). doi:10.5194/essd-17-2641-2025. Annual update following IPCC methods: observed and human-induced warming and remaining carbon budgets derived from the cumulative-emissions relationship.

Wording check: "Rises in step" and "close to proportional" describe the assessed relationship. A causal reading is supported by the IPCC's attribution of warming to human emissions (high confidence) and by the physics of CO2 radiative forcing. The post attributes the 0.45°C figure to the IPCC and does not claim the observed points validate it, since observed warming also includes methane, other gases and aerosols (the chart note says so).

Limits: The IPCC relationship is for CO2-induced warming; total observed warming also reflects non-CO2 forcings, which on net add warming. The near-linearity is assessed as robust while emissions stay positive; it is less certain under large net-negative emissions, and some recent work argues the response can depend on the timing of emissions. HadCRUT5 has incomplete early coverage, shown by the wider 19th-century ranges.

Fact-check: An independent subagent checked the IPCC SPM text (D.1.1, D.1.2, A.1.2), recomputed every number from the saved data (2,528 GtCO2 to 2019, 2,780 to 2025, 1.28°C for 2016–2025, 1.11°C for 2011–2020, 43.3 Gt in 2025, 47% since 1990), confirmed the DOIs, and found no retraction or credible dispute of near-linear TCRE over the historical period. Verdict: pass with fixes. Changed as a result: the first sentence now says 'warming caused by carbon dioxide' rather than all warming; the alt text no longer says the observed points sit inside the IPCC band (early years and the 1960s–70s decade means sit at or below its lower edge, and observed warming includes non-CO2 effects); 'first shown by' Matthews and Allen became 'formalised in 2009', with Matthews and Caldeira 2008 noted; the best-estimate label was moved off a data point. The 'remaining budget' sentence rests on D.1.1, which is the paragraph cited.
