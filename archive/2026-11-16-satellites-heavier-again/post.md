---
date: 2026-11-16
title: Satellites stopped shrinking in 2017
slug: satellites-heavier-again
topic: Space
claim: turning-point
chart: chart.png
summary: The median satellite fell from about 1,450 kg to 5 kg by 2017 as CubeSats took over. It has since climbed back to 575 kg, and to 267 kg even without Starlink.
---

# Satellites stopped shrinking in 2017

![Every payload launched since 1990 by year and mass with the median marked, and the median with and without Starlink since 2005](chart.png)

The story most people know is that satellites got small: shoebox CubeSats, cheap rides, thousands of them. That was true for about five years. Then it reversed.

I took every payload in Jonathan McDowell's GCAT catalog launched since 1990 (23,320 of them, nearly all with a known mass) and found the median mass for each launch year.

- From 2008 to 2011 the median satellite weighed 1,450 kg. The plateau is Russia's GLONASS navigation satellites, which weigh exactly that and happened to sit in the middle.
- It fell to 100 kg in 2013 and bottomed at 5 kg in 2017, when 63% of everything launched weighed 10 kg or less.
- Since then it has climbed: 148 kg in 2019, 730 kg in 2024 and 575 kg so far in 2026. That's 122 times the 2017 low.
- Starlink is most of that, at 66% of this year's payloads. Take it out and the median still goes from 5 kg to 267 kg.
- Payloads of 10 kg or less are down to 5% of launches this year.

Cheap launch first made it worth flying tiny satellites. Now it makes big ones cheap to fly too.

**How I did it.** GCAT's satellite catalog, updated 15 November 2026, filtered to payloads with pandas and grouped by launch year. I used the median because a handful of 20-tonne station modules would swamp a mean. Masses are at launch, and some are GCAT's estimates. 2026 is a partial year. Thanks to McDowell for keeping the catalog open.

[Code](analysis.py) · [Data](data/) · [SVG](chart.svg)
