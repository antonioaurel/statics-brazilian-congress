#!/usr/bin/env python3
"""Pulls per-state historical series from official APIs into data/states/indicadores_estados.csv.

Run on a machine with open internet (the IBGE, IPEA and TSE hosts are not reachable from
the environment this repo was assembled in). Each block below documents the exact source
so the numbers are traceable. Output is long format: uf,indicator,year,value,unit,source.

  python3 scripts/fetch_states.py            # fetch everything
  python3 scripts/fetch_states.py hdi gini   # fetch selected indicators
"""
import csv, json, sys, urllib.request, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "states" / "indicadores_estados.csv"
UF_CODE = {11:"RO",12:"AC",13:"AM",14:"RR",15:"PA",16:"AP",17:"TO",21:"MA",22:"PI",23:"CE",24:"RN",25:"PB",26:"PE",27:"AL",28:"SE",29:"BA",31:"MG",32:"ES",33:"RJ",35:"SP",41:"PR",42:"SC",43:"RS",50:"MS",51:"MT",52:"GO",53:"DF"}

def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

def sidra(table, variable, periods, classif=""):
    """IBGE SIDRA: https://apisidra.ibge.gov.br/ — n3 = states."""
    url = f"https://apisidra.ibge.gov.br/values/t/{table}/n3/all/v/{variable}/p/{periods}{classif}?formato=json"
    data = get(url)[1:]
    for d in data:
        yield UF_CODE[int(d["D1C"])], int(d["D3C"][:4]), float(d["V"]) if d["V"] not in ("...", "-", "X") else None

def ipea(serie):
    """IPEAdata: http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='X') — TERCODIGO = IBGE UF code (2 digits) for state series."""
    url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{serie}')"
    for d in get(url)["value"]:
        if d["NIVNOME"] == "Estados":
            yield UF_CODE[int(d["TERCODIGO"])], int(d["VALDATA"][:4]), d["VALVALOR"]

# indicator -> (unit, source, generator). Table/variable IDs verified against the SIDRA catalogue as of 2026.
FETCHERS = {
 # Unemployment, PNAD Contínua quarterly, annual avg computed by SIDRA table 4099 (var 4099 = taxa de desocupação), 2012-
 "unemployment": ("pct", "IBGE SIDRA t4099 v4099", lambda: sidra(4099, 4099, "all")),
 # Informality share, PNAD Contínua: table 4097? use IBGE "Informalidade" indicator via SIDRA t6397 is for occupation; informality is published in the PNAD-C anual tables (t 6453?). Fill the table id after checking https://sidra.ibge.gov.br/pesquisa/pnadca
 # GDP per capita, Contas Regionais, table 5938 variable 6879 (PIB per capita, R$), 2002-
 "gdp_per_capita_brl": ("BRL", "IBGE SIDRA t5938 v6879", lambda: sidra(5938, 6879, "all")),
 # Population estimates, table 6579 var 9324, for per-capita conversions
 "population": ("persons", "IBGE SIDRA t6579 v9324", lambda: sidra(6579, 9324, "all")),
 # Evangelical share: census tables 137 (2000), 137 (2010), 2022 preliminary table 9xxx; religion is classified (c133). Easiest: download the census 'Religião' tables from https://sidra.ibge.gov.br/tabela/137 and compute shares.
 # Homicide rate by state: IPEAdata series 'HOMIC' (Atlas da Violência), per 100k, 1989-
 "homicide_rate": ("per_100k", "IPEAdata HOMIC (Atlas da Violência)", lambda: ipea("HOMIC")),
 # HDI by state 1991/2000/2010/2021: Atlas Brasil, no API; download the state table from http://www.atlasbrasil.org.br/ranking and save as data/states/raw/atlas_idh_uf.csv
 # Prison population by state: SISDEPEN, https://www.gov.br/senappen/pt-br/servicos/sisdepen — download the semestral XLSX and aggregate 'população prisional' per UF; rate = pop / population * 100000
 # Vehicle fleet by state: Senatran 'Frota por UF e tipo' monthly XLSX, https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-Senatran/frota-de-veiculos
 # Internet households by state: PNAD Contínua TIC (SIDRA t 6797?) or Cetic.br TIC Domicílios microdata
 # Chamber composition by state 1990 and 1994: TSE repositório, consulta_cand_1994.zip (https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/), count DS_SIT_TOT_TURNO in ('ELEITO','ELEITO POR QP','ELEITO POR MÉDIA') per SG_UF, SG_PARTIDO; 1990 is only partially available in the repository.
}

def main(selected):
    rows = []
    for name, (unit, source, gen) in FETCHERS.items():
        if selected and name not in selected:
            continue
        print("fetching", name)
        try:
            for uf, year, value in gen():
                if value is not None:
                    rows.append((uf, name, year, value, unit, source))
        except Exception as e:
            print("  failed:", e)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["uf","indicator","year","value","unit","source"]); w.writerows(sorted(rows))
    print("wrote", OUT, len(rows), "rows")

if __name__ == "__main__":
    main(set(sys.argv[1:]))
