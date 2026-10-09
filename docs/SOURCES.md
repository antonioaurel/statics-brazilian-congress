# Sources and caveats

The same content, bilingual and with the politician samples, is rendered at `methodology.html`; this file is the plain-text version for the repo.

## Chamber composition
- **1990–2026 national totals** (`data/historical/camara_espectro_1990_2026.csv`): TSE results per election, aggregated with the party→spectrum mapping below. 1990 had 503 seats.
- **1998–2026 per state, by party** (`data/states/camara_estado_partido_1990_2026.csv`): HubPolítico result pages (`hubpolitico.com.br/eleicoes/{year}/apuracao/{uf}/deputado-federal`), which republish the TSE totalisation. Every state-year was checked to sum to the state's seat count (216/216 pass). Federations in 2022–2026 are split into their component parties.
- **1990 and 1994 per state**: not loaded. The TSE repository has `consulta_cand_1994.zip`; see `scripts/fetch_states.py`.
- **1962** (`data/historical/camara_1962.csv`): Wikipedia / Schmitt (2000) via jus.com.br; small-party counts vary by one or two between sources.

## Party → spectrum mapping (`data/historical/partido_espectro_por_periodo.csv`)
No official classification exists. The mapping follows the convention of the Brazilian Legislative Surveys and mainstream press. Judgement calls that move the most seats:
- PL: centre-right until 2006 (merged into PR), right 2007–2018, **far right from 2022** (Bolsonaro joined in 2021). Moving PL to "right" would empty the far-right column in 2022 and 2026.
- PSL: right until 2014, far right in 2018 only.
- PP: right (as PPB/PP) until 2010, centre-right from 2011 (centrão era). PTB moves the other way.
- PSDB: centre in 1990, centre-right from 1994.
- PPS: centre-left until 2010, centre from 2011 (Cidadania).
- PT and PCdoB: left. PSOL: far left. PSB, PDT, PV, Rede: centre-left.

## Senate and governors
- `data/states/senadores_1990_2026.csv`: senators elected per state per election, from the Portuguese Wikipedia "Eleições estaduais em {UF} em {ano}" pages (counts verified: 1 per state in 1998/2006/2014/2022, 2 in 2002/2010/2018/2026).
- `data/states/governadores_1998_2026.csv`: governor elected per state per election (2nd-round winner), HubPolítico; six 2026 run-offs (AC, AM, DF, ES, RJ, RN, TO) marked PENDING.
- `data/historical/presidentes.csv`: president elected per cycle; 1990 carries the 1989 winner.
- Sanitation (sewage/water network, national series and the per-state `sewage_network_pct` column) are rounded from PNAD and SNIS 2022 summaries — approx.

## Senate 2023/2027 (`data/historical/congresso_2022_2026_por_partido.csv`)
2027 projection from Agência Senado after the 4 Oct 2026 election (PL 28, PT 9, MDB 8…); 2023 composition at the start of the legislature (Agência Senado, Feb 2023). Party switching between election and inauguration is large in the Senate, so these are not "seats elected".

## National indicators (`data/national/indicadores_nacionais.csv`)
Source per row. IBGE (Censo, PNAD, PNAD Contínua, Contas Nacionais), ITU, Anatel, World Bank, UNDP, Atlas da Violência (IPEA/FBSP), Depen/SISDEPEN, Senatran, Receita Federal/Sebrae, DataReportal/Meta. Rows marked `approx` in the note column are rounded from secondary summaries (smartphone share, early Facebook/Instagram, 1990s labour shares) and should be re-pulled before citation. Unemployment changes methodology in 2012 (PME → PNAD Contínua); 2023 HDI is from UNDP's revised series.

## States, 2026 cross-section (`data/states/estados_2026.csv`)
- Presidential first-round percentages: TSE via TVT News, 5 Oct 2026 (exact).
- Other columns: latest available (census 2022 for religion and households; HDI 2021 Atlas Brasil; GDP per capita 2021; PNAD Contínua 2023–24 for unemployment, informality, schooling, internet; Atlas da Violência 2023; SISDEPEN 2023–24; Senatran 2024). These were assembled from published summaries and rounded; they are indicative, not citable. Re-pull with `scripts/fetch_states.py`.

## Per-state historical indicators
Not yet loaded (the IBGE/IPEA/TSE APIs were unreachable from the build environment). `scripts/fetch_states.py` documents the endpoints and writes `data/states/indicadores_estados.csv`; `scripts/build_site.py` will pick that file up once it exists.
