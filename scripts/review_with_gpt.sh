#!/usr/bin/env bash
# Fact-check the published data with ChatGPT via the Codex CLI (uses your ChatGPT login).
# Each topic runs as a separate read-only Codex session with live web search;
# reports land in reviews/<topic>.md.
#
#   scripts/review_with_gpt.sh                 # all topics
#   scripts/review_with_gpt.sh chamber senate  # only these
#   MODEL=gpt-5.5 scripts/review_with_gpt.sh     # pick a model
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/reviews"
mkdir -p "$OUT"

COMMON='You are fact-checking a public bilingual (EN/PT) website about the Brazilian Chamber of
Deputies, 1990-2026. Read docs/SOURCES.md first: it defines the left-right spectrum and lists caveats.
CSV files under data/ are the source of truth for every number shown on the site.

Rules:
- Verify against primary sources by browsing (TSE, camara.leg.br, senado.leg.br, IBGE/SIDRA, IPEA,
  Banco Central, Atlas da Violência, Wikipedia PT election pages). Do not rely on memory.
- Also check internal consistency (totals, percentages, the same party mapped the same way).
- Do NOT modify any file. Only report.
- Report ONLY problems. Do not restate rows that are correct.
- Output Markdown: a short summary line, then a table with columns
  file | row/key | field | site value | proposed value | source URL | confidence (high/med/low) | note
- If you could not verify something, list it in a final "Unverified" section rather than guessing.

Your task:'

declare -a TOPICS=(chamber mapping states_chamber senate_governors presidents indicators politicians prose)

prompt_for() {
  case "$1" in
    chamber) echo "Review data/historical/camara_espectro_1990_2026.csv, data/historical/camara_1962.csv and
data/historical/congresso_2022_2026_por_partido.csv. Check seat counts per party/spectrum per election
against TSE/Câmara results; totals must match the Chamber size of that year (503 in 1990, 513 from 1994).";;
    mapping) echo "Review data/historical/partidos_espectro_mapeamento.csv and
data/historical/partido_espectro_por_periodo.csv. Check party names, mergers/renames (e.g. PFL->DEM->União,
PMDB->MDB, PL/PR) and whether each spectrum label is defensible against the literature cited in SOURCES.md
(e.g. Bolognesi/Ribeiro/Codato 2023 survey, Power & Zucco). Flag inconsistencies across periods.";;
    states_chamber) echo "Review data/states/camara_estado_partido_1990_2026.csv. Check each state's bench size
(must match the constitutional allocation per state) and spot-check party seats per state for at least
2002, 2014, 2018 and 2022 against TSE. Note which states/years you checked.";;
    senate_governors) echo "Review data/states/senadores_1990_2026.csv and data/states/governadores_1998_2026.csv.
Check winners, parties and the number of Senate seats elected per state per election (1 or 2 alternating).";;
    presidents) echo "Review data/historical/presidentes.csv, data/historical/presidenciais_1989_2026.csv and
data/states/estados_2026.csv (2026 cross-section). Check names, parties, vote shares and dates.";;
    indicators) echo "Review data/national/indicadores_nacionais.csv. For every row whose note says approx,
find a sourced value and propose it. For other rows, check value, unit and the named source.";;
    politicians) echo "Review data/historical/politicos_amostra.csv (76 politician bios, EN+PT). For each person check
birth year/place, education, offices and dates, party and state, and that EN and PT say the same thing.
Also check the 'why' sentence is factually correct. Use the source_url and other sources.";;
    prose) echo "Review the prose of the site: the EN and PT text in scripts/build_site.py (STR, EN, PT, POL_ERA,
GOV) and docs/SOURCES.md. Look for factual errors, claims not supported by the CSVs, and places where EN and PT
disagree. Quote the exact sentence for each problem.";;
    *) return 1;;
  esac
}

[ $# -gt 0 ] && TOPICS=("$@")
MODEL_ARGS=(-m "${MODEL:-gpt-5.5}")

for t in "${TOPICS[@]}"; do
  task="$(prompt_for "$t")" || { echo "unknown topic: $t" >&2; continue; }
  echo "==> $t  ($(date +%H:%M:%S))"
  codex --search exec \
    -C "$ROOT" --skip-git-repo-check \
    -s read-only \
    ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} \
    -o "$OUT/$t.md" \
    "$COMMON $task" > "$OUT/$t.log" 2>&1 \
    && echo "    done -> reviews/$t.md" \
    || echo "    FAILED (see reviews/$t.log)"
done
