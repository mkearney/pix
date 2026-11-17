<sub>**pix** · one visual analysis of the world, every day · No. 10 · 2026-11-17 · Migration · [archive →](archive/)</sub>

# Israel is outgrowing its immigrants

![Foreign-born share of the population in 1990 and 2024 for 51 high-income countries, and Israel's and Latvia's populations split into native-born and foreign-born](archive/2026-11-17-israel-outgrows-immigrants/chart.png)

Almost every rich country has a bigger foreign-born share than it did in 1990. I wanted to see the exceptions, and why.

I took the UN's migrant stock estimates for the 51 high-income countries with at least a million people, and split each population into foreign-born and native-born.

- The foreign-born share rose in 43 of the 51. The median change was +6.0 points, and Qatar's was +27.7.
- Israel's fell the most: from 35.7% in 1990 to 22.3% in 2024, a little lower in every five-year step.
- Yet Israel has more immigrants than ever: 2.09 million, up 29% from 1.62 million. The native-born population grew 2.5 times, from 2.92 million to 7.30 million.
- Latvia, Estonia and Lithuania fell too, the opposite way. Their foreign-born populations shrank by 66%, 47% and 50%.
- Only Saudi Arabia and Costa Rica joined Israel in having more immigrants but a smaller share, and both by less than 2 points.

In Israel the native-born population, which includes immigrants' children and grandchildren, simply grew much faster than new arrivals. No other rich country's share fell this way by more than 2 points. In the Baltics the usual explanation is that people who came in Soviet times have left or died, and few have replaced them. That fits the counts, but this data can't show it directly.

**How I did it.** UN DESA's International Migrant Stock 2024, via Our World in Data, with the World Bank's 2025 income groups. I took total population as the UN migrant count divided by the UN migrant share, so both parts come from one release, and did the rest in pandas. "Foreign-born" falls back to foreign citizenship where a country doesn't record birthplace.

[Code](archive/2026-11-17-israel-outgrows-immigrants/analysis.py) · [Data](archive/2026-11-17-israel-outgrows-immigrants/data/) · [SVG](archive/2026-11-17-israel-outgrows-immigrants/chart.svg)

---

<sub>Previously: [Satellites stopped shrinking in 2017](archive/2026-11-16-satellites-heavier-again/post.md) · [By length, most new undersea cable has a Big Tech owner](archive/2026-11-15-big-tech-long-cables/post.md) · [Cocoa doubled its harvest by doubling its land](archive/2026-11-14-cocoa-needs-new-land/post.md) · [full archive](archive/) · [how this works](CLAUDE.md)</sub>
