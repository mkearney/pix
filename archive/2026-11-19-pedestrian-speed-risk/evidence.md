# Evidence

Finding: The risk that a struck pedestrian dies rises along a steep S-curve with the vehicle's impact speed, from 10% at about 24 mph to 90% at about 55 mph in US data, with each extra 5 mph roughly doubling the odds of death in several countries' data.

Type: dose-response.

Source: Tefft BC. Impact speed and a pedestrian's risk of severe injury or death. Accident Analysis & Prevention 50, 871–878 (2013). doi:10.1016/j.aap.2012.07.022. PubMed: https://pubmed.ncbi.nlm.nih.gov/22935347/. Report version with full tables: Tefft BC, Impact Speed and a Pedestrian's Risk of Severe Injury or Death, AAA Foundation for Traffic Safety (2011), https://aaafoundation.org/impact-speed-pedestrians-risk-severe-injury-death/ (copy used: https://rules.cityofnewyork.us/wp-content/uploads/2025/06/2011PedestrianRiskVsSpeedReport.pdf). No individual-level data released.

Design: NHTSA Pedestrian Crash Data Study, US crashes 1994–1998, pedestrians aged 15 and over struck by a single forward-moving car, light truck, van or SUV (422 pedestrians in the report version). The sample over-represents severe cases, so it was post-stratified and weighted to national injury statistics. Logistic regression adjusted for age, height, weight, BMI and vehicle type, with risks standardised to US pedestrians struck in 2007–2009. Missing speeds imputed.

Key numbers:
- Risk of death 10%, 25%, 50%, 75%, 90% at 24.1, 32.5, 40.6, 48.0, 54.6 mph. Tefft 2013, abstract. Transcribed; `analysis.py` asserts each value appears in the saved abstract text.
- Risk of severe injury (AIS 4+, including death) at the same levels: 17.1, 24.9, 33.0, 40.8, 48.1 mph. Tefft 2013, abstract. Transcribed and checked the same way. Shown on the chart only.
- km/h conversions (39, 65, 88 km/h): derived here, 1 mph = 1.609344 km/h.
- 70-year-old's risk equals a 30-year-old's at 11.8 mph faster. Tefft 2013, abstract.
- Odds ratio of death per 5 mph, unadjusted: Davis 2001 2.78 (2.09–3.69), Rosén & Sander 2009 2.06 (1.60–2.66), Richards 2010 2.41 (1.79–3.24), Tefft (US, cars only) 1.99 (1.60–2.49). Tefft 2011 report, Table 4, p. 13. Transcribed. The range 1.99 to 2.78 in the post is the minimum and maximum of these four; the post says they are unadjusted. Tefft's adjusted US odds ratio is 2.18 (1.78–2.67), same table. Tefft notes the rise looked somewhat steeper in Davis and Richards, but not beyond chance (p = 0.29).
- Test of homogeneity across the four unadjusted odds ratios, p = 0.29. Tefft 2011 report, p. 13. Transcribed.
- Curves on the chart: logistic fits through the five published points per outcome, derived here for drawing. Largest gap between the fitted death curve and a published point: 2.3 percentage points. Implied odds ratio per 5 mph from the fit: 2.05.

Corroboration:
- Rosén E, Sander U. Pedestrian fatality risk as a function of car impact speed. Accident Analysis & Prevention 41, 536–542 (2009). doi:10.1016/j.aap.2009.02.002. German in-depth crash data (GIDAS) weighted for sampling bias; risk at 50 km/h more than twice that at 40 km/h and more than five times that at 30 km/h.
- Rosén E, Stigson H, Sander U. Literature review of pedestrian fatality risk as a function of car impact speed. Accident Analysis & Prevention 43, 25–33 (2011). doi:10.1016/j.aap.2010.04.003. Every study reviewed found fatality risk rising monotonically with impact speed; pre-2000 studies overestimated absolute risk because of sampling bias.
- Davis GA. Relating severity of pedestrian injury to impact speed in vehicle-pedestrian crashes: simple threshold model. Transportation Research Record 1773, 108–113 (2001). doi:10.3141/1773-13. British data weighted to national statistics; steep rise in risk with speed (odds ratio per 5 mph 2.78 as tabulated by Tefft).
- Richards DC. Relationship between speed and risk of fatal injury: pedestrians and car occupants. UK Department for Transport (2010), https://www.gov.uk/government/organisations/department-for-transport (DfT road safety research series). British data 2000–2009; odds ratio per 5 mph 2.41 as tabulated by Tefft.

Wording check: The data are observational crash records, but the post's verbs ("climbs", "reaches", "multiplies the odds") describe the measured dose-response rather than claiming an intervention effect. A causal reading is also supported: impact energy rises with the square of speed, and the gradient is replicated across countries, decades and methods.

Limits: Impact speed, not travel speed; braking before impact lowers it. The US vehicles are model years 1989–1999, before today's taller SUVs and pickups, which later work finds more dangerous at a given speed. Absolute risk levels differ between studies (the US reaches each level a few mph lower than Germany); the steepness agrees. The report and journal versions of Tefft's analysis give slightly different US thresholds; the post uses the peer-reviewed journal values.

Fact-check: An independent subagent checked every number against the Tefft 2013 abstract, the report's Table 4 and the script output, confirmed the DOIs via Crossref, found no retraction, erratum or dispute of the gradient, and passed the entry with fixes. Changed as a result: panel 2 title said four countries (it is three; now four studies); 'the same steepness' softened to 'a similar steepness' with the p = 0.29 test; the post now says the odds ratios come from unadjusted models; 'Britain' made 'UK' throughout; summary gives the odds range as about 2 to 2.8; curves labelled approximate fits; Richards 2010's series number dropped as unconfirmed.
