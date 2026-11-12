# Sources

- `owid-energy-data.csv`: Our World in Data energy dataset, https://github.com/owid/energy-data (`owid-energy-data.csv`), downloaded 2026-11-12 UTC. CC BY 4.0. Electricity generation and solar generation come from Ember and the Energy Institute Statistical Review, compiled by OWID.
- Columns used: `solar_electricity` and `electricity_generation` (TWh) for "World" and for countries (rows with an ISO code that isn't an OWID aggregate).

Derived:
- `solar_ladder.csv`: each year's change in world solar generation, the closest-sized country by total generation, and solar's share of world electricity.