# statics-brazilian-congress

Composition of the Brazilian Chamber of Deputies by ideological spectrum, 1990–2026, nationally and per state, alongside the social and economic indicators that are usually invoked to explain it.

**Live pages:** `index.html` (data), `politicians.html` (one politician per spectrum per period, with filters) and `methodology.html` (sources and how the spectrum is defined). Both are bilingual — EN/PT toggle in the header, remembered per browser. On GitHub Pages: enable Pages on the `main` branch, root folder. Pick Brazil or a state in the header; the composition charts, the indicator panels and the state scatter plot all follow the selection.

## Layout
```
index.html                     built data page, EN/PT (do not edit by hand)
politicians.html               built politician samples page with filters, EN/PT (do not edit by hand)
methodology.html               built sources & methodology page, EN/PT (do not edit by hand)
assets/chart.umd.js            Chart.js 4.4.1, vendored so the page works offline
data/
  historical/                  Chamber 1990–2026 by spectrum, 1962, party→spectrum mapping, presidents, Senate 2023/2027, politician samples
  national/                    national indicator time series (long format, source per row)
  states/                      per-state Chamber and Senate results 1998–2026, governors elected, 2026 cross-section
charts/                        standalone HTML charts built from the same CSVs
scripts/build_site.py          CSV → index.html + politicians.html + methodology.html (UI strings, prose and politician bios live here)
scripts/build_charts.py        CSV → charts/*.html
scripts/fetch_states.py        pulls per-state historical series from IBGE/IPEA/TSE (needs open internet)
docs/SOURCES.md                sources, methodology and caveats
```

## Rebuild
```
python3 scripts/build_site.py
python3 scripts/build_charts.py
```
CSV files are the source of truth; edit them and rebuild.

## Status
- Chamber composition: complete nationally 1990–2026; per state 1998–2026 (1990 and 1994 per state pending TSE fetch).
- Senate: seats elected per election by state and nationally, 1998–2026 (Wikipedia PT state-election pages); governors elected per state 1998–2026 (HubPolítico); presidents by election.
- National indicators: 20 series, 1990–2026; rows flagged `approx` need re-sourcing.
- Per-state indicators: 2026 cross-section only; historical series pending `fetch_states.py`.

See `docs/SOURCES.md` before citing any number.
