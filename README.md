# WANA Solar Investment Analysis

A six-lens framework for evaluating utility-scale solar investment opportunities across 17 West Asia and North Africa countries.

**Live dashboard:** [View on Tableau Public](https://public.tableau.com/views/WANAProject/Dashboard1?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

<img width="2872" height="1372" alt="image" src="https://github.com/user-attachments/assets/350939b3-0813-452b-8f82-3c12a473c467" />


## Motivation

The MENA region holds some of the world's best solar resources but lags in deployment. Different investor types — development banks, IPP developers, hyperscaler PPAs, ESG funds — have different priorities, so a single "best country" ranking is misleading. This project builds a multi-lens framework that surfaces the right country for the right investor.

## Data sources

- **[Global Solar Atlas](https://globalsolaratlas.info/download/world)** — country-level solar irradiation and PV potential (World Bank).
- **[World Bank Open Data](https://data.worldbank.org/)** — socio-economic indicators via the `wbgapi` Python API.
- **[Our World in Data](https://ourworldindata.org/grapher/share-electricity-solar)** — current solar share of electricity generation.

## Methodology

**Six analytical lenses** (each normalized 0-100):
1. Resource — solar PV potential (kWh/kWp/day)
2. Market scale — GDP × population × electricity consumption
3. Untapped potential — resource ÷ current solar share
4. Execution readiness — urbanization, grid access, consumption maturity
5. Trajectory — 5-year change in solar share
6. Demand pressure — population growth + per-capita electricity

**Four investor archetypes** (weighted combinations of the six lenses):
- Development Bank — prioritizes execution + demand pressure
- IPP Developer — prioritizes resource + execution
- Hyperscaler PPA — prioritizes resource + market scale
- ESG Fund — prioritizes untapped potential + trajectory

**Robustness check:** Each archetype's top 3 was tested against 100 Monte Carlo perturbations of the weights (±20%) to confirm rankings are stable.

## Key findings

- **Development Banks:** Bahrain, Kuwait, Saudi Arabia top the list — high grid maturity and rising consumption. Small Gulf states score artificially well on per-capita indicators; a real DFI would weigh population scale more heavily.
- **IPP Developers:** Saudi Arabia, Bahrain, UAE — the expected Gulf trio. Sensitivity shows Jordan creeping into top 3 in 11% of perturbations, making it a credible fourth pick.
- **Hyperscaler PPAs:** Saudi, UAE, Bahrain are 100% stable across all perturbations — the most robust result in the model.
- **ESG Funds:** Libya tops the ranking on paper (top resource + near-zero current adoption) but political risk is not modeled — the obvious next layer to add.

## Limitations

- Political and regulatory risk not modeled.
- GSA data is 2018; World Bank indicators are latest available (mostly 2022-2023).
- Per-capita indicators favor small Gulf states; absolute scale would shift rankings.

## AI-assisted narrative layer

`wana_ai_narrative.py` adds an optional layer on top of the ranking output: 
for each investor archetype, it sends the top-3 ranked countries and their 
scores to Claude (Anthropic API) and generates a short, decision-ready 
written recommendation — the kind of note a real analyst would hand to an 
investment committee, including one honest caveat (data limitation, 
concentration risk, or a runner-up worth watching).

Requires an `ANTHROPIC_API_KEY` environment variable.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python wana_ai_narrative.py
```

## How to run

```bash
git clone https://github.com/nubar-mamedova/wana-solar-investment-analysis.git
cd wana-solar-investment-analysis
pip install -r requirements.txt
jupyter notebook wana_solar_analysis.ipynb
```

The notebook is designed to run on Google Colab with the data files mounted from Google Drive. To run locally, edit the `DATAPATH` and `PROCESSEDPATH` variables in cell 2.

## Repository structure

```bash
├── wana_solar_analysis.ipynb    # main notebook
├── wana_ai_narrative.py         # LLM narrative layer (Claude API)
├── data/
│   ├── raw/                     # input data (GSA Excel)
│   └── processed/               # output CSVs (master, rankings, archetypes)
├── requirements.txt
├── dashboard.png
└── README.md
```

## Tech stack

Python (pandas, wbgapi, openpyxl) · Tableau Public · World Bank API
