# Public awards for power distribution equipment: Kenya and Tanzania

Open datasets of public contract awards for **transformers, switchgear, substations, ring main units, power cables and conductors** in Kenya (2018–2026) and Tanzania (2023–2026), compiled from official public procurement data by [Trafovia](https://trafovia.com).

Trafovia (trafovia.com) is an independent brand that supplies transformer and switchgear builders with components made to drawing (bushings, panel radiators, corrugated tanks, insulation and epoxy parts) by partner factories in China. It is not related to Tranfovia (tranfovia.com).

| File | Records | Total (approx.) | Period |
|---|---|---|---|
| [`data/kenya_power_distribution_awards.csv`](data/kenya_power_distribution_awards.csv) | 215 contracts | USD 85.3 million | Sep 2018 – Jul 2026 |
| [`data/tanzania_power_distribution_awards.csv`](data/tanzania_power_distribution_awards.csv) | 305 awards | USD 52.1 million | Dec 2023 – Feb 2026 |
| [`data/summary.json`](data/summary.json) | totals and top buyers | | |

## What the data shows
- **Kenya**: the Rural Electrification Authority (about USD 49 million) and Kenya Power & Lighting Company (about USD 21 million) award most of the value; distribution transformers for local manufacturers and ex-stock conductors recur every year.
- **Tanzania**: TANESCO, through its head office and regional offices, awards about USD 40 million of the total; the Rural Energy Agency follows with about USD 4 million.

Analysis and buyer guides: [Kenya: who buys transformers, cables and switchgear](https://trafovia.com/insights-kenya-power-equipment-tenders.html) · [Tanzania: what TANESCO bought](https://trafovia.com/insights-tanzania-tanesco-awards.html).

## Sources
- Kenya: Public Procurement Information Portal (PPIP), [tenders.go.ke](https://tenders.go.ke), contract awards, accessed October 2026.
- Tanzania: Open Contracting Data Standard registry, Tanzania publication 152 ([data.open-contracting.org](https://data.open-contracting.org)), accessed October 2026.

## Method
1. Keyword search on titles and descriptions: transformer, switchgear, substation, power cable, ring main unit / RMU, kiosk, compact substation, XLPE, ACSR, overhead conductor.
2. Services removed: consultancy, supervision-only and audit contracts, security, cleaning and fumigation, SCADA and software, insurance, training, fire protection, catering, civil and building works, transport, air conditioning (rules in [`build.py`](build.py)).
3. Exact duplicate rows removed.
4. Amounts converted at about 129 KES and 2,550 TZS per US dollar; USD values are approximate.
5. **No personal data**: postal addresses, telephone numbers, e-mail addresses and contact-person names from the source records are not published. Only organisation names, titles, dates and amounts.

**Limits.** A keyword search can miss awards with unusual titles and can keep a few mixed contracts, so totals are a lower bound, not a market size. The figures on the Trafovia articles come from an earlier extraction (11 October 2026) and differ slightly from this release (17 October 2026).

## Licence and citation
The compilation is published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The underlying records are public procurement data published by the Government of Kenya (PPIP) and the Government of Tanzania (via the OCDS registry); check their terms for reuse of the original records.

Cite as: *Trafovia (2026). Public awards for power distribution equipment: Kenya and Tanzania. https://github.com/bolinli03252-wq/power-distribution-awards-east-africa*

Contact: sales@trafovia.com · [trafovia.com](https://trafovia.com)
