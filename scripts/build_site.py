#!/usr/bin/env python3
"""Builds index.html and methodology.html (EN/PT) from the CSVs in data/. CSV is the source of truth."""
import csv, json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data"

def rows(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

SPEC = ["far_right","right","centre_right","centre","centre_left","left","far_left"]
COLOR = {"far_right":"#2a78d6","right":"#85b7eb","centre_right":"#b5d4f4","centre":"#b4b2a9",
         "centre_left":"#f7c1c1","left":"#f09595","far_left":"#e24b4a"}
UFNAME = {"AC":"Acre","AL":"Alagoas","AP":"Amapá","AM":"Amazonas","BA":"Bahia","CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás","MA":"Maranhão","MT":"Mato Grosso","MS":"Mato Grosso do Sul","MG":"Minas Gerais","PA":"Pará","PB":"Paraíba","PR":"Paraná","PE":"Pernambuco","PI":"Piauí","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte","RS":"Rio Grande do Sul","RO":"Rondônia","RR":"Roraima","SC":"Santa Catarina","SP":"São Paulo","SE":"Sergipe","TO":"Tocantins"}

# ---------------- strings ----------------
STR = {
 "en": {
  "title":"Brazilian General Elections after Redemocratization (1990 to 2026)","subtitle":"A data driven look at what shapes our choices","author":"Author","by":"By","footer_repo":"Source code and data on GitHub","pres_h":"Presidential elections: winner and runner up","pres_exp":"Each election since redemocratization, with the winner and the runner up, their share of valid votes in the first round and, where there was one, in the run off. The dot is the party family of each candidate at that election. 1989 elected the president who governed during the 1990 Congress.","round1":"1st round","round2":"2nd round","winner":"Winner","runner":"Runner up","pending_run":"run off pending","region":"Region","brazil":"Brazil","nav_data":"Election results per spectrum","nav_pol":"Politicians sample by spectrum","tab_camara":"Chamber of Deputies","tab_senado":"Senate","intro_h":"What this project is","intro":"A single place to read the ideological composition of the Brazilian Congress since redemocratisation across every election from 1990 to 2026, nationally and for each state, next to the social and economic indicators most often used to explain it. Pick Brazil or a state; switch between the Chamber and the Senate; everything follows. The spectrum classification is explicit and editable (see Methodology).","exp_bars":"Each bar is one election. It shows how the seats won that year split across the seven ideological families, from far left (red, on the left) to far right (blue, on the right). The dot at the start of the bar is the party family of the governor elected that year (the president, when Brazil is selected). Hover a segment for seats and percentage.","exp_lines":"The same data as lines: one line per family, so you can follow how each one grew or shrank across elections. The vertical scale is the share of the delegation; for a state it runs to 100% because small delegations swing hard.","exp_tables":"First table: seats and share per family at each election, with the governor (or president) elected that year. Second table: the seats won by each party, which is what the spectrum columns are built from.","gov":"Governor","pres":"President","pending":"run-off pending","sen_elected":"Senators elected","ctx_intro":"How {name} looks on twenty-seven indicators, as national series 1990 to 2026. The black marker is {name}'s latest value; the curve is Brazil. Sources and caveats per series are on the Methodology page.","ctx_intro_br":"Twenty-seven national series, 1990 to 2026, chosen because they are the ones most often invoked to explain the political shifts. Sources and caveats per series are on the Methodology page.","theme":"Theme","theme_dark":"Dark","theme_light":"Light","senate_note":"Senate: seats elected in that year (one per state in 1990, 1998, 2006, 2014, 2022; two in 1994, 2002, 2010, 2018, 2026; Amapá and Roraima elected three in 1990 as new states).","nav_method":"Methodology",
  "pol_h":"A politician from each spectrum, at every election","pol_intro":"One figure per ideological family for each of the ten elections since 1990, chosen for being emblematic of where the party sat <em>at that election</em>, with a short biography: education, what they did, trajectory. Where a spectrum had no seats that year the card says so. Several people changed bins over their careers (Roberto Freire, Jair Bolsonaro, the PSDB of Fernando Henrique): the mapping follows the party and the period, not the person.","f_year":"Election","f_era":"Period","f_spec":"Spectrum","f_text":"Search name, party or text","f_all":"All","f_clear":"Clear filters","f_count":"{n} of {t} shown","pol_more":"See the full set on the Politicians page.","src":"Source page","src_h":"Pages used for the biographies",
  "sub_br":"513 seats · elections 1990 to 2026","sub_uf":"{name} · {n} seats · elections 1990 to 2026",
  "h_comp":"Composition by ideological spectrum","h_bars":"Seat share per election","h_lines":"Trajectory of each spectrum (% of delegation)",
  "election":"Election","all_spec":"All","how_lspec":"Tap a family to show only it; tap more to add them; All brings every line back. Each line is labelled at its latest value.","seats_by_party":"Seats by party","party":"Party","seats":"seats",
  "note_comp":"Party → spectrum mapping by period is in <code>data/historical/partido_espectro_por_periodo.csv</code> and explained on the methodology page. State Chamber data covers 1990 to 2026 (TSE via HubPolítico, with 1990 and 1994 from the state election pages on Wikipedia, checked against the 503 and 513 seat totals).",
  "h_ctx":"Context indicators","snap":"{name} snapshot (latest available) vs Brazil","latest":"latest","vs":"Brazil",
  "note_ctx":"National series: <code>data/national/indicadores_nacionais.csv</code> (source per point). State snapshot: <code>data/states/estados_2026.csv</code>, latest available year, rounded; the black marker places the state's latest value against the national curve. Per-state historical series are not yet loaded — see <code>scripts/fetch_states.py</code>.",
  "h_scatter":"States: indicators vs the 2026 first-round presidential vote","indicator":"Indicator","corr":"Pearson r = {r} across 27 units","yaxis":"Flávio Bolsonaro % (1st round, 2026)",
  "spec":{"far_right":"Far right","right":"Right","centre_right":"Centre-right","centre":"Centre","centre_left":"Centre-left","left":"Left","far_left":"Far left"},
  "panels":{"religion":"Religion (% population)","internet":"Internet (%)","mobile":"Mobile lines /100 · smartphone %","social":"Facebook and Instagram (millions)","gdp":"GDP per capita (current US$)","growth":"GDP growth (%)","hdi":"HDI","unemployment":"Unemployment (%)","schooling":"Years of schooling (adults 25+)","gini":"Gini index","prisoners":"Prisoners per 100,000","homicides":"Homicides per 100,000","women":"Women and work (%)","family":"Family (% households)","fertility":"Fertility (children per woman)","vehicles":"Vehicles per 100 inhabitants","labour":"CLT vs informal (% of employed)","mei":"MEI registrations (millions)","sanitation":"Basic sanitation (% households)","ideb": "IDEB (0 to 10)", "saeb_mt": "Saeb, mathematics (scale score)", "saeb_lp": "Saeb, Portuguese (scale score)", "school_flow": "Failure and dropout (% of students)", "age_grade": "Age-grade distortion (% of students)", "teachers": "Teachers with adequate training (% of classes)", "higher_access": "Higher education enrolment, 18 to 24 (%)", "higher_quality": "Higher education with score 4 or 5 (%)"},
  "series":{"sewage_network":"Sewage network","water_network":"Water network","catholic":"Catholic","evangelical":"Evangelical","no_religion":"No religion","internet_individuals":"Individuals online","internet_households":"Households connected","mobile_lines":"Lines per 100","smartphone_users":"Smartphone users %","facebook_users":"Facebook","instagram_users":"Instagram","gdp_per_capita":"GDP per capita","gdp_growth":"Growth","hdi":"HDI","unemployment":"Unemployment","years_schooling":"Years","gini":"Gini","prisoners_rate":"Prisoners /100k","homicide_rate":"Homicides /100k","women_pay_ratio":"Pay as % of men's","female_participation":"Participation rate","female_headed_households":"Female-headed","one_person_households":"One-person","fertility_rate":"Fertility","vehicles_per_100":"Vehicles /100","clt_share":"CLT","informal_share":"Informal","mei":"MEI","ideb_ef_iniciais": "Primary, early years", "ideb_ef_finais": "Primary, final years", "ideb_em": "Secondary", "saeb_mt_5": "5th grade", "saeb_mt_9": "9th grade", "saeb_mt_em": "Secondary, final year", "saeb_lp_5": "5th grade", "saeb_lp_9": "9th grade", "saeb_lp_em": "Secondary, final year", "taxa_reprovacao_ef_af": "Failure, primary final years", "taxa_abandono_ef_af": "Dropout, primary final years", "taxa_reprovacao_em": "Failure, secondary", "taxa_abandono_em": "Dropout, secondary", "distorcao_ef_af": "Primary, final years", "distorcao_em": "Secondary", "formacao_docente_ef_ai": "Primary, early years", "formacao_docente_ef_af": "Primary, final years", "formacao_docente_em": "Secondary", "taxa_bruta_superior": "Gross rate", "taxa_liquida_ajustada_superior": "Adjusted net rate", "igc_4_5_pct": "Institutions (IGC)", "cpc_4_5_pct": "Courses (CPC)"},
  "cards":{"population_millions":"Population (millions)","flavio_pct_1st_round":"Flávio Bolsonaro 2026, 1st round","lula_pct_1st_round":"Lula 2026, 1st round","evangelical_pct":"Evangelical","hdi":"HDI","gdp_per_capita_brl_thousands":"GDP per capita","unemployment_pct":"Unemployment","informal_pct":"Informality","years_schooling":"Years of schooling","homicides_per_100k":"Homicides /100k","prisoners_per_100k":"Prisoners /100k","internet_households_pct":"Households online","vehicles_per_100":"Vehicles /100","female_headed_households_pct":"Female-headed households","sewage_network_pct":"Sewage network (% households)","ideb_ef_iniciais": "IDEB, primary early years", "ideb_ef_finais": "IDEB, primary final years", "ideb_em": "IDEB, secondary", "saeb_mt_5": "Saeb maths, 5th grade", "saeb_mt_9": "Saeb maths, 9th grade", "saeb_mt_em": "Saeb maths, secondary", "saeb_lp_5": "Saeb Portuguese, 5th grade", "saeb_lp_9": "Saeb Portuguese, 9th grade", "saeb_lp_em": "Saeb Portuguese, secondary", "taxa_reprovacao_ef_af": "Failure, primary final years", "taxa_abandono_ef_af": "Dropout, primary final years", "taxa_reprovacao_em": "Failure, secondary", "taxa_abandono_em": "Dropout, secondary", "distorcao_ef_af": "Age-grade distortion, primary final years", "distorcao_em": "Age-grade distortion, secondary"},
 },
 "pt": {
  "title":"Eleições Gerais Brasileiras pós redemocratização (1990 a 2026)","subtitle":"Um olhar data driven sobre o que faz nossas escolhas","author":"Autor","by":"Por","footer_repo":"Código e dados no GitHub","pres_h":"Eleições presidenciais: vencedor e segundo colocado","pres_exp":"Cada eleição desde a redemocratização, com o vencedor e o segundo colocado, sua parcela dos votos válidos no primeiro turno e, quando houve, no segundo. O ponto é a família partidária de cada candidato naquela eleição. 1989 elegeu o presidente que governou durante o Congresso de 1990.","round1":"1º turno","round2":"2º turno","winner":"Vencedor","runner":"Segundo colocado","pending_run":"2º turno pendente","region":"Região","brazil":"Brasil","nav_data":"Resultados eleitorais por espectro","nav_pol":"Amostra de políticos por espectro","tab_camara":"Câmara dos Deputados","tab_senado":"Senado","intro_h":"O que é este projeto","intro":"Um lugar único para ler a composição ideológica do Congresso brasileiro desde a redemocratização em todas as eleições de 1990 a 2026, no país e em cada estado, ao lado dos indicadores sociais e econômicos mais usados para explicá-la. Escolha o Brasil ou um estado; alterne entre Câmara e Senado; tudo acompanha. A classificação por espectro é explícita e editável (ver Metodologia).","exp_bars":"Cada barra é uma eleição. Mostra como as cadeiras conquistadas naquele ano se dividem entre as sete famílias ideológicas, da extrema esquerda (vermelho, à esquerda) à extrema direita (azul, à direita). O ponto no início da barra é a família do governador eleito naquele ano (o presidente, quando Brasil está selecionado). Passe o mouse sobre um segmento para ver cadeiras e percentual.","exp_lines":"Os mesmos dados em linhas: uma por família, para acompanhar como cada uma cresceu ou encolheu ao longo das eleições. A escala vertical é a participação na bancada; para um estado vai até 100% porque bancadas pequenas oscilam muito.","exp_tables":"Primeira tabela: cadeiras e participação por família em cada eleição, com o governador (ou presidente) eleito naquele ano. Segunda tabela: as cadeiras de cada partido, de onde as colunas de espectro são construídas.","gov":"Governador","pres":"Presidente","pending":"2º turno pendente","sen_elected":"Senadores eleitos","ctx_intro":"Como {name} aparece em vinte e sete indicadores, com as séries nacionais 1990 a 2026. O marcador preto é o valor mais recente de {name}; a curva é o Brasil. Fontes e ressalvas por série estão na página de Metodologia.","ctx_intro_br":"Vinte e sete séries nacionais, 1990 a 2026, escolhidas por serem as mais invocadas para explicar as mudanças políticas. Fontes e ressalvas por série estão na página de Metodologia.","theme":"Tema","theme_dark":"Escuro","theme_light":"Claro","senate_note":"Senado: cadeiras eleitas naquele ano (uma por estado em 1990, 1998, 2006, 2014, 2022; duas em 1994, 2002, 2010, 2018, 2026; Amapá e Roraima elegeram três em 1990 como estados novos).","nav_method":"Metodologia",
  "pol_h":"Um político de cada espectro, em cada eleição","pol_intro":"Uma figura por família ideológica em cada uma das dez eleições desde 1990, escolhida por ser emblemática de onde o partido estava <em>naquela eleição</em>, com uma biografia curta: formação, o que fez, trajetória. Quando um espectro não teve cadeiras naquele ano, o cartão diz isso. Várias pessoas mudaram de faixa ao longo da carreira (Roberto Freire, Jair Bolsonaro, o PSDB de Fernando Henrique): o mapeamento segue o partido e o período, não a pessoa.","f_year":"Eleição","f_era":"Período","f_spec":"Espectro","f_text":"Buscar nome, partido ou texto","f_all":"Todos","f_clear":"Limpar filtros","f_count":"{n} de {t} exibidos","pol_more":"Veja o conjunto completo na página Políticos.","src":"Página-fonte","src_h":"Páginas usadas nas biografias",
  "sub_br":"513 cadeiras · eleições 1990 a 2026","sub_uf":"{name} · {n} cadeiras · eleições 1990 a 2026",
  "h_comp":"Composição por espectro ideológico","h_bars":"Participação nas cadeiras por eleição","h_lines":"Trajetória de cada espectro (% da bancada)",
  "election":"Eleição","all_spec":"Todos","how_lspec":"Toque em uma família para ver só ela; toque em outras para somar; Todos traz todas as linhas de volta. Cada linha tem o rótulo no valor mais recente.","seats_by_party":"Cadeiras por partido","party":"Partido","seats":"cadeiras",
  "note_comp":"O mapeamento partido → espectro por período está em <code>data/historical/partido_espectro_por_periodo.csv</code> e é explicado na página de metodologia. Os dados da Câmara por estado cobrem 1990 a 2026 (TSE via HubPolítico, com 1990 e 1994 das páginas das eleições estaduais na Wikipédia, conferidas com os totais de 503 e 513 cadeiras).",
  "h_ctx":"Indicadores de contexto","snap":"Retrato de {name} (dado mais recente) vs Brasil","latest":"mais recente","vs":"Brasil",
  "note_ctx":"Séries nacionais: <code>data/national/indicadores_nacionais.csv</code> (fonte por ponto). Retrato estadual: <code>data/states/estados_2026.csv</code>, ano mais recente disponível, arredondado; o marcador preto posiciona o valor mais recente do estado sobre a curva nacional. As séries históricas por estado ainda não foram carregadas — ver <code>scripts/fetch_states.py</code>.",
  "h_scatter":"Estados: indicadores vs voto presidencial no 1º turno de 2026","indicator":"Indicador","corr":"r de Pearson = {r} entre 27 unidades","yaxis":"Flávio Bolsonaro % (1º turno, 2026)",
  "spec":{"far_right":"Extrema direita","right":"Direita","centre_right":"Centro-direita","centre":"Centro","centre_left":"Centro-esquerda","left":"Esquerda","far_left":"Extrema esquerda"},
  "panels":{"religion":"Religião (% da população)","internet":"Internet (%)","mobile":"Linhas móveis /100 · smartphone %","social":"Facebook e Instagram (milhões)","gdp":"PIB per capita (US$ correntes)","growth":"Crescimento do PIB (%)","hdi":"IDH","unemployment":"Desemprego (%)","schooling":"Anos de estudo (adultos 25+)","gini":"Índice de Gini","prisoners":"Presos por 100 mil","homicides":"Homicídios por 100 mil","women":"Mulheres e trabalho (%)","family":"Família (% dos domicílios)","fertility":"Fecundidade (filhos por mulher)","vehicles":"Veículos por 100 habitantes","labour":"CLT vs informal (% dos ocupados)","mei":"Registros de MEI (milhões)","sanitation":"Saneamento básico (% dos domicílios)","ideb": "IDEB (0 a 10)", "saeb_mt": "Saeb, matemática (proficiência)", "saeb_lp": "Saeb, língua portuguesa (proficiência)", "school_flow": "Reprovação e abandono (% dos alunos)", "age_grade": "Distorção idade-série (% dos alunos)", "teachers": "Docentes com formação adequada (% das turmas)", "higher_access": "Matrícula no ensino superior, 18 a 24 anos (%)", "higher_quality": "Ensino superior com conceito 4 ou 5 (%)"},
  "series":{"sewage_network":"Rede de esgoto","water_network":"Rede de água","catholic":"Católicos","evangelical":"Evangélicos","no_religion":"Sem religião","internet_individuals":"Pessoas conectadas","internet_households":"Domicílios conectados","mobile_lines":"Linhas por 100","smartphone_users":"Usuários de smartphone %","facebook_users":"Facebook","instagram_users":"Instagram","gdp_per_capita":"PIB per capita","gdp_growth":"Crescimento","hdi":"IDH","unemployment":"Desemprego","years_schooling":"Anos","gini":"Gini","prisoners_rate":"Presos /100 mil","homicide_rate":"Homicídios /100 mil","women_pay_ratio":"Renda como % da dos homens","female_participation":"Taxa de participação","female_headed_households":"Chefiados por mulheres","one_person_households":"Unipessoais","fertility_rate":"Fecundidade","vehicles_per_100":"Veículos /100","clt_share":"CLT","informal_share":"Informal","mei":"MEI","ideb_ef_iniciais": "Fundamental, anos iniciais", "ideb_ef_finais": "Fundamental, anos finais", "ideb_em": "Ensino médio", "saeb_mt_5": "5º ano", "saeb_mt_9": "9º ano", "saeb_mt_em": "Ensino médio, série final", "saeb_lp_5": "5º ano", "saeb_lp_9": "9º ano", "saeb_lp_em": "Ensino médio, série final", "taxa_reprovacao_ef_af": "Reprovação, fundamental anos finais", "taxa_abandono_ef_af": "Abandono, fundamental anos finais", "taxa_reprovacao_em": "Reprovação, ensino médio", "taxa_abandono_em": "Abandono, ensino médio", "distorcao_ef_af": "Fundamental, anos finais", "distorcao_em": "Ensino médio", "formacao_docente_ef_ai": "Fundamental, anos iniciais", "formacao_docente_ef_af": "Fundamental, anos finais", "formacao_docente_em": "Ensino médio", "taxa_bruta_superior": "Taxa bruta", "taxa_liquida_ajustada_superior": "Taxa líquida ajustada", "igc_4_5_pct": "Instituições (IGC)", "cpc_4_5_pct": "Cursos (CPC)"},
  "cards":{"population_millions":"População (milhões)","flavio_pct_1st_round":"Flávio Bolsonaro 2026, 1º turno","lula_pct_1st_round":"Lula 2026, 1º turno","evangelical_pct":"Evangélicos","hdi":"IDH","gdp_per_capita_brl_thousands":"PIB per capita","unemployment_pct":"Desemprego","informal_pct":"Informalidade","years_schooling":"Anos de estudo","homicides_per_100k":"Homicídios /100 mil","prisoners_per_100k":"Presos /100 mil","internet_households_pct":"Domicílios conectados","vehicles_per_100":"Veículos /100","female_headed_households_pct":"Domicílios chefiados por mulheres","sewage_network_pct":"Rede de esgoto (% domicílios)","ideb_ef_iniciais": "IDEB, fundamental anos iniciais", "ideb_ef_finais": "IDEB, fundamental anos finais", "ideb_em": "IDEB, ensino médio", "saeb_mt_5": "Saeb matemática, 5º ano", "saeb_mt_9": "Saeb matemática, 9º ano", "saeb_mt_em": "Saeb matemática, ensino médio", "saeb_lp_5": "Saeb português, 5º ano", "saeb_lp_9": "Saeb português, 9º ano", "saeb_lp_em": "Saeb português, ensino médio", "taxa_reprovacao_ef_af": "Reprovação, fundamental anos finais", "taxa_abandono_ef_af": "Abandono, fundamental anos finais", "taxa_reprovacao_em": "Reprovação, ensino médio", "taxa_abandono_em": "Abandono, ensino médio", "distorcao_ef_af": "Distorção idade-série, fundamental anos finais", "distorcao_em": "Distorção idade-série, ensino médio"},
 }
}


CMP_STR = {
 "en": {"nav_exp":"Elections vs context","exp_h":"Follow an election, pick the context","exp_intro":"Left: how the seats of Brazil or of one state split by ideological family at each election, one line per family; pick the families to show. Right: pick one or two context charts to read next to it. Both use the same timeline, 1990 to 2026; hover a year to line them up.","exp_pick":"Context charts (pick up to two; a third replaces the oldest)","exp_view_bars":"Bars","exp_view_lines":"Lines","exp_place":"Place","exp_none":"Pick a context chart above.","exp_marker":"Big dots: the selected state's latest value, in the colour of its series, against the Brazil curve.","nav_cmp":"Compare states (and Brazil)","cmp_h":"Compare two places","cmp_intro":"Pick any two: Brazil or a state, on each side. Both columns use the same elections (1990 to 2026) and the same scales, so bars and lines can be read against each other. Below the columns, the same data overlaid on one chart, and the latest indicators side by side.","side_a":"Place A","side_b":"Place B","house":"House","overlay_h":"Head to head","overlay_exp":"One spectrum at a time, both places on the same chart.","spectrum":"Spectrum","ind_h":"Indicators, latest available","ind_exp":"Latest year available for each indicator, with Brazil as reference. Per state historical series are not loaded yet, so this is a snapshot, not a trend. Facebook, Instagram, mobile lines and MEI have no published state breakdown, so they appear only on the main page.","nodata":"no data","vote_h":"2026 presidential vote, first round","brasil_ref":"Brazil","how_bars":"How to read: one bar per election, the same years on both sides. Compare the length of each color between the two columns; the dot on the left is the governor (or president) elected that year. Place B is drawn in lighter colors.","how_lines":"How to read: one line per spectrum. Both charts share the 0 to 100% scale, so a line higher on one side means that family holds a bigger share there. Place B uses dashed, lighter lines.","how_ov":"How to use: pick a spectrum below. Solid blue is place A, dashed orange is place B, grey dotted is Brazil when two states are compared.","how_ind":"How to use: each block compares place A (blue), place B (orange) and Brazil (grey) on one indicator. The year in brackets is the year of the data.","nat_only":"Brazil only, no state data","latest_year":"latest","all_el":"All elections","pres_cmp_exp":"Share of valid votes won in each place by the candidates who finished first and second nationally. Pick one election or see them all; switch between first and second round.","how_pres":"How to read: blue is place A, orange is place B, grey is Brazil. In the table the bigger number in each pair shows who won that place. 1994 and 1998 had no run off; the 2026 run off is still to come.","no_run":"no run off","win_share":"Winner's share of valid votes","show_lbl":"Choose what to show","sec_seat":"Seat share","sec_traj":"Trajectory","sec_ov":"Head to head","sec_ind":"Indicators","sec_pres":"Presidential","how_mbars":"Each election shows place A (top) and place B (bottom) as one bar split by family, far left on the left. The dot is the governor (or president) elected that year; numbers inside are the share of seats.","how_mpres":"Each election: the share of valid votes won in each place by the national winner and runner up. The longest bar in each block won that place."},
 "pt": {"nav_exp":"Eleição × contexto","exp_h":"Acompanhe a eleição, escolha o contexto","exp_intro":"À esquerda: como as cadeiras do Brasil ou de um estado se dividem entre as famílias ideológicas em cada eleição, uma linha por família; escolha as famílias a exibir. À direita: escolha um ou dois gráficos de contexto para ler ao lado. Os dois usam a mesma linha do tempo, 1990 a 2026; passe o mouse sobre um ano para alinhá-los.","exp_pick":"Gráficos de contexto (escolha até dois; um terceiro substitui o mais antigo)","exp_view_bars":"Barras","exp_view_lines":"Linhas","exp_place":"Lugar","exp_none":"Escolha um gráfico de contexto acima.","exp_marker":"Pontos grandes: o valor mais recente do estado escolhido, na cor da sua série, sobre a curva do Brasil.","nav_cmp":"Comparar estados (e o Brasil)","cmp_h":"Compare dois lugares","cmp_intro":"Escolha quaisquer dois: o Brasil ou um estado, em cada lado. As duas colunas usam as mesmas eleições (1990 a 2026) e as mesmas escalas, para que barras e linhas possam ser lidas uma contra a outra. Abaixo das colunas, os mesmos dados sobrepostos num só gráfico, e os indicadores mais recentes lado a lado.","side_a":"Lugar A","side_b":"Lugar B","house":"Casa","overlay_h":"Frente a frente","overlay_exp":"Um espectro de cada vez, os dois lugares no mesmo gráfico.","spectrum":"Espectro","ind_h":"Indicadores, dado mais recente","ind_exp":"Ano mais recente disponível para cada indicador, com o Brasil como referência. As séries históricas por estado ainda não foram carregadas, então isto é um retrato, não uma tendência. Facebook, Instagram, linhas móveis e MEI não têm recorte estadual publicado, por isso aparecem só na página principal.","nodata":"sem dados","vote_h":"Voto presidencial 2026, primeiro turno","brasil_ref":"Brasil","how_bars":"Como ler: uma barra por eleição, os mesmos anos dos dois lados. Compare o tamanho de cada cor entre as duas colunas; o ponto à esquerda é o governador (ou presidente) eleito naquele ano. O lugar B aparece em cores mais claras.","how_lines":"Como ler: uma linha por espectro. Os dois gráficos usam a mesma escala de 0 a 100%, então uma linha mais alta de um lado significa que aquela família tem fatia maior ali. O lugar B usa linhas tracejadas e mais claras.","how_ov":"Como usar: escolha um espectro abaixo. Azul contínuo é o lugar A, laranja tracejado é o lugar B, cinza pontilhado é o Brasil quando dois estados são comparados.","how_ind":"Como usar: cada bloco compara o lugar A (azul), o lugar B (laranja) e o Brasil (cinza) em um indicador. O ano entre parênteses é o ano do dado.","nat_only":"Apenas Brasil, sem dado estadual","latest_year":"mais recente","all_el":"Todas as eleições","pres_cmp_exp":"Parcela dos votos válidos obtida em cada lugar pelos candidatos que terminaram em primeiro e segundo no país. Escolha uma eleição ou veja todas; alterne entre primeiro e segundo turno.","how_pres":"Como ler: azul é o lugar A, laranja é o lugar B, cinza é o Brasil. Na tabela, o maior número de cada par mostra quem venceu naquele lugar. Em 1994 e 1998 não houve segundo turno; o de 2026 ainda vai acontecer.","no_run":"sem 2º turno","win_share":"Parcela do vencedor nos votos válidos","show_lbl":"Escolha o que mostrar","sec_seat":"Cadeiras","sec_traj":"Trajetória","sec_ov":"Frente a frente","sec_ind":"Indicadores","sec_pres":"Presidenciais","how_mbars":"Cada eleição mostra o lugar A (em cima) e o lugar B (embaixo) como uma barra dividida por família, extrema esquerda à esquerda. O ponto é o governador (ou presidente) eleito naquele ano; os números dentro são a parcela das cadeiras.","how_mpres":"Cada eleição: a parcela dos votos válidos obtida em cada lugar pelo vencedor e pelo segundo colocado nacionais. A barra mais longa de cada bloco venceu naquele lugar."},
}
for _l in ("en","pt"):
    STR[_l].update(CMP_STR[_l])

import re as _re
def nodash(t, lang):
    if not isinstance(t, str): return t
    t = t.replace(" — ", ", ").replace(" —", ",").replace("— ", "")
    t = _re.sub(r"(\d{4})–\)", r"\1 onward)" if lang == "en" else r"\1 em diante)", t)
    t = _re.sub(r"(\d)–(\d)", r"\1 to \2" if lang == "en" else r"\1 a \2", t)
    return t.replace("–", " ")
def nodash_tree(o, lang):
    if isinstance(o, dict): return {k: nodash_tree(v, lang) for k, v in o.items()}
    if isinstance(o, list): return [nodash_tree(v, lang) for v in o]
    return nodash(o, lang)
STR = {lang: nodash_tree(d, lang) for lang, d in STR.items()}

# ---------------- data ----------------
mapping = rows(D/"historical"/"partido_espectro_por_periodo.csv")
def spectrum(party, year):
    for r in mapping:
        if r["party"] == party and int(r["from_year"]) <= year <= int(r["to_year"]):
            return r["spectrum"]
    raise SystemExit(f"unmapped party {party} {year}")

comp = {"BR": {}}
for r in rows(D/"historical"/"camara_espectro_1990_2026.csv"):
    comp["BR"][r["election"]] = {"total": int(r["total_seats"]), **{k: int(r[k]) for k in SPEC}}
parties = collections.defaultdict(lambda: collections.defaultdict(dict))
for r in rows(D/"states"/"camara_estado_partido_1990_2026.csv"):
    uf, y, n = r["uf"], r["election"], int(r["seats"])
    comp.setdefault(uf, {}).setdefault(y, {"total": 0, **{k: 0 for k in SPEC}})
    comp[uf][y][spectrum(r["party"], int(y))] += n
    comp[uf][y]["total"] += n
    parties[uf][y][r["party"]] = n

nat = collections.defaultdict(list)
for r in rows(D/"national"/"indicadores_nacionais.csv"):
    nat[r["indicator"]].append({"x": int(r["year"]), "y": float(r["value"])})
PANELS = {
 "religion": ([("catholic","#7a5c2e"),("evangelical","#0ca30c"),("no_religion","#b4b2a9")], 0, 100, "evangelical_pct"),
 "internet": ([("internet_individuals","#5a3fd6"),("internet_households","#a58cf0")], 0, 100, "internet_households_pct"),
 "mobile": ([("mobile_lines","#d97706"),("smartphone_users","#f5c26b")], 0, 150, None),
 "social": ([("facebook_users","#1877f2"),("instagram_users","#d6336c")], 0, 150, None),
 "gdp": ([("gdp_per_capita","#5a3fd6")], 0, 14000, None),
 "growth": ([("gdp_growth","#9fc49f")], -6, 9, None),
 "hdi": ([("hdi","#0ca30c")], 0.5, 0.85, "hdi"),
 "unemployment": ([("unemployment","#d97706")], 0, 16, "unemployment_pct"),
 "schooling": ([("years_schooling","#0ca30c")], 0, 12, "years_schooling"),
 "gini": ([("gini","#7a5c2e")], 0.4, 0.65, None),
 "prisoners": ([("prisoners_rate","#b91c1c")], 0, 700, "prisoners_per_100k"),
 "homicides": ([("homicide_rate","#b91c1c")], 0, 45, "homicides_per_100k"),
 "women": ([("women_pay_ratio","#d6336c"),("female_participation","#f09595")], 40, 100, None),
 "family": ([("female_headed_households","#5a3fd6"),("one_person_households","#a58cf0")], 0, 60, "female_headed_households_pct"),
 "fertility": ([("fertility_rate","#7a5c2e")], 0, 4, None),
 "vehicles": ([("vehicles_per_100","#d97706")], 0, 100, "vehicles_per_100"),
 "labour": ([("clt_share","#0ca30c"),("informal_share","#ec835a")], 0, 65, "informal_pct"),
 "mei": ([("mei","#5a3fd6")], 0, 20, None),
 "sanitation": ([("sewage_network","#0ca30c"),("water_network","#5a3fd6")], 0, 100, "sewage_network_pct"),
 "ideb": ([("ideb_ef_iniciais","#0ca30c"),("ideb_ef_finais","#5a3fd6"),("ideb_em","#d97706")], 2, 7, None),
 "saeb_mt": ([("saeb_mt_5","#0ca30c"),("saeb_mt_9","#5a3fd6"),("saeb_mt_em","#d97706")], 180, 300, None),
 "saeb_lp": ([("saeb_lp_5","#0ca30c"),("saeb_lp_9","#5a3fd6"),("saeb_lp_em","#d97706")], 180, 300, None),
 "school_flow": ([("taxa_reprovacao_ef_af","#5a3fd6"),("taxa_abandono_ef_af","#a58cf0"),("taxa_reprovacao_em","#b91c1c"),("taxa_abandono_em","#ec835a")], 0, 15, None),
 "age_grade": ([("distorcao_ef_af","#5a3fd6"),("distorcao_em","#d97706")], 0, 40, None),
 "teachers": ([("formacao_docente_ef_ai","#0ca30c"),("formacao_docente_ef_af","#5a3fd6"),("formacao_docente_em","#d97706")], 40, 100, None),
 "higher_access": ([("taxa_bruta_superior","#5a3fd6"),("taxa_liquida_ajustada_superior","#a58cf0")], 0, 50, None),
 "higher_quality": ([("igc_4_5_pct","#0ca30c"),("cpc_4_5_pct","#d97706")], 0, 50, None),
}
STV = {}
for r in rows(D/"states"/"indicadores_estado_extra.csv"):
    k = r["indicator"].replace("_pct","") if r["indicator"].endswith("_pct") and r["indicator"] not in ("igc_4_5_pct","cpc_4_5_pct") else r["indicator"]
    k = {"fertility_rate":"fertility_rate","gini":"gini"}.get(k, k)
    STV.setdefault(k, {"y": int(r["year"][:4]), "v": {}})["v"][r["uf"]] = float(r["value"])
panels = {key: {"lo": lo, "hi": hi, "stateCol": sc, "ds": [{"key": k, "color": c, "data": nat.get(k, [])} for k, c in ss]} for key, (ss, lo, hi, sc) in PANELS.items()}
govs = collections.defaultdict(dict)
for r in rows(D/"states"/"governadores_1998_2026.csv"):
    govs[r["uf"]][r["election"]] = {"name": r["governor"], "party": r["party"], "spec": None if r["party"]=="PENDING" else spectrum(r["party"], int(r["election"]))}
for r in rows(D/"historical"/"presidentes.csv"):
    govs["BR"][r["election"]] = {"name": r["president"], "party": r["party"], "spec": None if r["party"]=="PENDING" else spectrum(r["party"], int(r["election"]))}
sen_comp, sen_names = {}, collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows(D/"states"/"senadores_1990_2026.csv"):
    uf, y = r["uf"], r["election"]; sp = spectrum(r["party"], int(y))
    for key in (uf, "BR"):
        sen_comp.setdefault(key, {}).setdefault(y, {"total": 0, **{k: 0 for k in SPEC}})
        sen_comp[key][y][sp] += 1; sen_comp[key][y]["total"] += 1
    sen_names[uf][y].append(r["senator"] + " (" + r["party"] + ")")
pres = []
for r in rows(D/"historical"/"presidenciais_1989_2026.csv"):
    y = int(r["election"]); ym = max(y, 1990)
    pres.append({"y": r["election"], "w": r["winner"], "wp": r["winner_party"], "ws": spectrum(r["winner_party"], ym), "r": r["runner_up"], "rp": r["runner_up_party"], "rs": spectrum(r["runner_up_party"], ym),
                 "w1": float(r["winner_1st_pct"]), "r1": float(r["runner_up_1st_pct"]), "w2": float(r["winner_2nd_pct"]) if r["winner_2nd_pct"] else None, "r2": float(r["runner_up_2nd_pct"]) if r["runner_up_2nd_pct"] else None, "pending": "pending" in r["note"]})
sen_parties = collections.defaultdict(lambda: collections.defaultdict(dict))
for r in rows(D/"states"/"senadores_1990_2026.csv"):
    d = sen_parties[r["uf"]][r["election"]]; d[r["party"]] = d.get(r["party"], 0) + 1
    d2 = sen_parties["BR"][r["election"]]; d2[r["party"]] = d2.get(r["party"], 0) + 1
states = rows(D/"states"/"estados_2026.csv")
statecols = list(states[0].keys())
BR_REF = {"flavio_pct_1st_round":47.0,"lula_pct_1st_round":45.2,"evangelical_pct":26.9,"hdi":0.76,"gdp_per_capita_brl_thousands":50,"unemployment_pct":6.6,"informal_pct":38.7,"years_schooling":8.6,"homicides_per_100k":21.2,"prisoners_per_100k":400,"internet_households_pct":83,"vehicles_per_100":57,"female_headed_households_pct":49.1}
UNIT = {"flavio_pct_1st_round":"%","lula_pct_1st_round":"%","evangelical_pct":"%","unemployment_pct":"%","informal_pct":"%","internet_households_pct":"%","female_headed_households_pct":"%","gdp_per_capita_brl_thousands":" R$k"}

CSS = """
.chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}.chip{font-size:12px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--bg);cursor:pointer;color:var(--ink)}.chip.on{background:var(--acc);color:#fff;border-color:var(--acc)}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}
:root{--ink:#1e1e1c;--mut:#777;--line:#e5e5e2;--bg:#fff;--card:#f7f7f5;--acc:#2a78d6;--grid:rgba(128,128,128,.18)}
:root[data-theme=dark]{--acc:#5b9bf0;--ink:#ecebe6;--mut:#9b9a93;--line:#2e2e2b;--bg:#161615;--card:#1f1f1d;--grid:rgba(200,200,200,.14)}
body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;color:var(--ink);background:var(--bg);line-height:1.5}
header{background:var(--bg);border-bottom:1px solid var(--line);padding:14px 24px 12px;display:flex;flex-direction:column;gap:12px}.hrow1{display:grid;grid-template-columns:1fr auto;grid-template-areas:"t l" "th .";align-items:start;gap:10px 16px}.hrow1 .tblock{grid-area:t}.hrow1 .langs{grid-area:l}.hrow1 .ctl-theme{grid-area:th;justify-self:start}.hrow1 label#regionlbl{grid-column:1/-1}
.seg{display:inline-flex;align-items:stretch;border:0;border-radius:999px;overflow:hidden;background:var(--card);padding:3px;gap:2px}.seg button{border:0;background:transparent;color:var(--ink);font:inherit;font-size:12.6px;font-weight:600;padding:7px 12.5px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;min-height:34px}.ctlrow{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0 0 14px}.seg button{border-radius:999px}.seg button.on{background:var(--acc);color:#fff}.seg button:not(.on):hover{background:var(--line)}.segic{display:inline-flex;align-items:center;padding:0 4px 0 12px;color:var(--acc)}.tblock{display:flex;flex-direction:column;align-items:flex-start;gap:4px}.byline{font-size:12px;color:var(--mut);margin:8px 0 0;opacity:.8}.byline a{color:inherit;text-decoration:none}.byline a:hover{text-decoration:underline}.subt{font-size:14px;color:var(--mut)}.tabsnav{justify-content:center;flex-wrap:wrap}.tabsnav .btn{text-align:center;font-size:14px;padding:8px 14px}.hrow3{display:flex;justify-content:center;align-items:center;gap:14px;flex-wrap:wrap}.hrow3:empty{display:none}
header h1{font-size:20px;font-weight:600;margin:0}select{font-size:14px;padding:6px 10px}
.btn{font-size:13px;padding:5px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);cursor:pointer;color:var(--ink);text-decoration:none;white-space:nowrap}
.btn.on{background:var(--acc);color:#fff;border-color:var(--acc)}.sp{flex:1}
nav{display:flex;gap:6px;flex-wrap:wrap}.themewrap{margin-left:10px}
input,select{background:var(--bg);color:var(--ink);border:1px solid var(--line)}
.tabs{display:flex;gap:6px;margin:0 0 12px}.tab{font-size:14px;padding:8px 14px;border:1px solid var(--line);border-bottom:none;border-radius:8px 8px 0 0;background:var(--card);cursor:pointer;color:var(--mut)}.tab.on{background:var(--bg);color:var(--ink);font-weight:500}
main{margin:0;padding:16px 24px 48px}
.cols{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:0 32px}.sec{border-top:1px solid var(--line);padding:22px 0 26px}.sec:first-child{border-top:none}
.two{display:grid;grid-template-columns:minmax(0,1fr);gap:28px}
#panels{grid-template-columns:repeat(2,minmax(0,1fr))}@media (max-width:640px){#panels{grid-template-columns:minmax(0,1fr)}}
.lg{align-items:center}a{color:var(--acc)}.btn.on,.chip.on{color:#fff}.lg span{display:inline-flex;align-items:center}h2,h3{display:block}.tab,.btn,.chip{display:inline-flex;align-items:center;justify-content:center}
.foot{text-align:center;font-size:13px;color:var(--mut);padding:18px 12px 28px;border-top:1px solid var(--line);margin-top:12px}
.intro{background:var(--card);border-radius:10px;padding:14px 18px;margin:0 0 8px;font-size:14px;line-height:1.55}
@media (max-width:1100px){.cols{grid-template-columns:minmax(0,1fr)}.two{grid-template-columns:minmax(0,1fr)}}
.cols>div,.two>div{min-width:0}.wrap{min-width:0;max-width:100%}canvas{max-width:100%}
@media (max-width:640px){header{position:static}#sub{width:100%;text-align:center}table th.gc,table td.gc{display:none}table tr.govm{display:table-row}table tr.govm td .govc{position:sticky;left:0;width:calc(100vw - 36px);text-align:center}table tr.govm td{text-align:left;font-size:12px;padding:2px 6px 10px;border-bottom:1px solid var(--line)}main{padding:12px 12px 40px}header{padding:10px 12px;gap:8px;justify-content:center;text-align:center}header h1{font-size:15px;width:100%;text-align:center}.hrow1{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}.hrow1 .tblock{width:100%}.seg button{font-size:11.7px;padding:6px 10px;min-height:32px}.tblock{align-items:center;text-align:center}header nav{justify-content:center;flex-wrap:nowrap;width:100%}header nav .btn{flex:1;font-size:11px;padding:6px 4px;white-space:normal;line-height:1.2}.two{gap:36px}.cap{text-align:center}.wrap{height:260px!important}.doc p,.doc li{font-size:14px}h2,h3,.intro,.note,.lg,.tabs{text-align:center}.lg,.tabs{justify-content:center}th,td,td.l,th.l{text-align:center}.govm{display:none}.pol .c{text-align:center}.chips{justify-content:center}.filters{text-align:center}}
h2{font-size:17px;font-weight:500;margin:28px 0 4px}h3{font-size:13px;font-weight:500;margin:0 0 2px}
.cap{font-size:12px;color:var(--mut);margin:0 0 8px}.wrap{position:relative;width:100%}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px 24px}
.lg{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:#555;margin:6px 0}.sw{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:4px;vertical-align:-2px}
table{border-collapse:collapse;font-size:12px;width:100%}th,td{padding:6px 6px;border-bottom:1px solid var(--line);text-align:center;vertical-align:middle}td.l,th.l{text-align:center}.govm{display:none}.gov{display:inline-block;width:9px;height:9px;border-radius:50%;vertical-align:-1px;margin-right:4px}.tw{overflow-x:auto}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:8px 0 16px}
.card{background:var(--card);border-radius:8px;padding:10px 12px}.card .l{font-size:11px;color:var(--mut)}.card .v{font-size:20px;font-weight:500}.card .b{font-size:11px;color:var(--mut)}
.note{font-size:12px;color:var(--mut);background:var(--card);padding:8px 12px;border-radius:8px;margin:8px 0}
.doc{max-width:1100px;margin:0 auto;text-align:center}.doc table{margin:0 auto;width:100%}.doc th,.doc td{text-align:center!important;vertical-align:middle}.doc ul,.doc ol{display:block;max-width:900px;margin:8px auto;text-align:left}.doc code{word-break:break-word}.srcs{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 14px;font-size:13px;margin:8px auto 4px;max-width:1000px}.srcs a{color:var(--acc)}main{padding-bottom:24px}.doc p,.doc li{font-size:15px}.doc table{font-size:13px}.doc th,.doc td{text-align:left}.doc h2{margin-top:36px}.doc h3{font-size:15px;margin:18px 0 6px}
.pol{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:12px 0}
.pol .c{border:1px solid var(--line);border-radius:10px;padding:14px 16px;border-top:4px solid;background:var(--card);display:flex;flex-direction:column;justify-content:center;text-align:center}.pol .n{font-size:16px;font-weight:500}.pol .p{font-size:12px;color:var(--mut);margin-bottom:6px}.pol .c p{font-size:13px;margin:6px 0}
[data-lang]{display:none}html[lang=en] [data-lang=en],html[lang=pt] [data-lang=pt]{display:block}
"""

SITE = "https://antonioaurel.github.io/statics-brazilian-congress/"
SITE_TITLE = "Brazilian General Elections after Redemocratization (1990 to 2026)"
SITE_DESC = "A data driven look at what shapes our choices: Chamber, Senate, governors and presidents by ideological spectrum, for Brazil and every state, next to the social and economic indicators used to explain them. - antonioaurel.github.io"
def meta(page, prefix=""):
    t = (prefix + " · " if prefix else "") + SITE_TITLE
    url = SITE + ("" if page == "index" else page + ".html")
    return (f'<title>{t}</title><meta name="description" content="{SITE_DESC}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE_TITLE}"><meta property="og:title" content="{t}">'
            f'<meta property="og:description" content="{SITE_DESC}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}assets/og-image.png">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Seat share of the Chamber of Deputies by ideological family, 1990 to 2026">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{SITE_DESC}"><meta name="twitter:image" content="{SITE}assets/og-image.png">'
            f'<link rel="canonical" href="{url}">')
CTLS = '<div class="ctlrow"><div class="seg ctl-theme" role="group" aria-label="Theme"><button id="th-light" onclick="setTheme(\'light\')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg><span data-i="theme_light"></span></button><button id="th-dark" onclick="setTheme(\'dark\')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg><span data-i="theme_dark"></span></button></div><div class="seg langs" role="group" aria-label="Language"><button id="lang-en" onclick="setLang(\'en\')">English</button><button id="lang-pt" onclick="setLang(\'pt\')">Português</button></div></div>'
def header(active):
    def nav(page, key):
        return f'<a class="btn{" on" if active==page or (active=="method" and page=="methodology") else ""}" href="{page}.html" data-i="{key}"></a>'
    return f"""<header><div class="hrow1"><div class="tblock"><h1 data-i="title"></h1><div class="subt" data-i="subtitle"></div></div>
<label id="regionlbl" style="{'' if active=='index' else 'display:none'}"><span data-i="region"></span>: <select id="uf"></select></label>
</div>
<nav class="tabsnav">{nav('index','nav_data')}{nav('compare','nav_cmp')}{nav('explore','nav_exp')}{nav('politicians','nav_pol')}{nav('methodology','nav_method')}</nav>
<div class="hrow3"><span id="sub" class="cap"></span></div></header>
<script>(function(){{var r=document.getElementById('regionlbl');var h=document.querySelector('.hrow3');if(r&&h&&r.style.display!=='none')h.insertBefore(r,h.firstChild);}})();</script>"""

I18N_JS = f"""
const STR={json.dumps(STR, ensure_ascii=False)};const SPEC={json.dumps(SPEC)},COLOR={json.dumps(COLOR)},UFNAME={json.dumps(UFNAME, ensure_ascii=False)};
let LANG='en';try{{LANG=new URLSearchParams(location.search).get('lang')==='pt'?'pt':'en'}}catch(e){{}}
function T(k){{return STR[LANG][k]}}
function applyStrings(){{document.documentElement.lang=LANG;document.querySelectorAll('[data-i]').forEach(e=>{{e.innerHTML=T(e.dataset.i)}});
 document.getElementById('lang-en').classList.toggle('on',LANG==='en');document.getElementById('lang-pt').classList.toggle('on',LANG==='pt');document.title=T('title');const a=document.getElementById('th-light'),b=document.getElementById('th-dark');if(a){{a.classList.toggle('on',!isDark());b.classList.toggle('on',isDark())}}}}
function keepUrl(){{try{{const u=new URL(location.href);u.searchParams.set('lang',LANG);u.searchParams.set('theme',THEME);history.replaceState(null,'',u)}}catch(e){{}}}}
function setLang(l){{LANG=l;keepUrl();applyStrings();if(typeof render==='function')render(true);}}
let THEME='light';try{{THEME=new URLSearchParams(location.search).get('theme')||'light'}}catch(e){{}}if(THEME!=='dark')THEME='light';
document.addEventListener('click',e=>{{const a=e.target.closest('nav a');if(!a)return;e.preventDefault();const u=new URL(a.getAttribute('href'),location.href);u.searchParams.set('lang',LANG);u.searchParams.set('theme',isDark()?'dark':'light');try{{const h=localStorage.getItem('house');if(h)u.searchParams.set('house',h)}}catch(e){{}}location.href=u.toString();}});
function applyTheme(){{document.documentElement.setAttribute('data-theme',THEME);}}
function isDark(){{return THEME==='dark'}}
function setTheme(t){{if(t===THEME)return;THEME=t;keepUrl();applyTheme();applyStrings();if(typeof render==='function')render(true);}}
applyTheme();
"""

# ---------------- index.html ----------------
INDEX_JS = r"""
const PRES=__PRES__;let presch;
function drawPres(){const dot=s=>'<span class="gov" style="background:'+COLOR[s]+'"></span>';const f=v=>v==null?'':v.toFixed(1)+'%';
 let h='<div class="tw"><table><tr><th>'+T('election')+'</th><th>'+T('winner')+'</th><th>'+T('round1')+'</th><th>'+T('round2')+'</th><th>'+T('runner')+'</th><th>'+T('round1')+'</th><th>'+T('round2')+'</th></tr>';
 PRES.forEach(p=>{h+='<tr><td>'+p.y+'</td><td>'+dot(p.ws)+p.w+' <span style="color:var(--mut)">('+p.wp+')</span></td><td><b>'+f(p.w1)+'</b></td><td><b>'+(p.pending?'<span style="color:var(--mut)">'+T('pending_run')+'</span>':f(p.w2))+'</b></td><td>'+dot(p.rs)+p.r+' <span style="color:var(--mut)">('+p.rp+')</span></td><td>'+f(p.r1)+'</td><td>'+(p.pending?'':f(p.r2))+'</td></tr>'});
 document.getElementById('prestable').innerHTML=h+'</table></div>';
 if(presch)presch.destroy();const L=PRES.map(p=>p.y);
 presch=new Chart(document.getElementById('presch'),{type:'bar',data:{labels:L,datasets:[{label:T('winner')+' · '+T('round1'),data:PRES.map(p=>p.w1),backgroundColor:PRES.map(p=>COLOR[p.ws]),barThickness:10},{label:T('runner')+' · '+T('round1'),data:PRES.map(p=>p.r1),backgroundColor:PRES.map(p=>COLOR[p.rs]+'99'),barThickness:10},{type:'line',label:T('winner')+' · '+T('round2'),data:PRES.map(p=>p.w2),borderColor:ink(),backgroundColor:ink(),pointRadius:4,showLine:false},{type:'line',label:T('runner')+' · '+T('round2'),data:PRES.map(p=>p.r2),borderColor:mut(),backgroundColor:mut(),pointRadius:4,pointStyle:'rectRot',showLine:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:ink(),usePointStyle:true}},tooltip:{callbacks:{label:t=>{const p=PRES[t.dataIndex];const who=t.datasetIndex%2===0?p.w:p.r;return t.dataset.label+': '+who+' '+(t.raw==null?'':t.raw+'%')}}}},scales:{x:{ticks:{color:mut()},grid:{display:false}},y:{min:0,max:70,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}}}}});}
const COMP={camara:__COMP__,senado:__SENCOMP__},PARTIES={camara:__PARTIES__,senado:__SENPARTIES__},SENNAMES=__SENNAMES__,GOVS=__GOVS__,PANELS=__PANELS__,STV=__STV__,STATES=__STATES__,SCOLS=__SCOLS__;
let bars,lines,pcharts={},sc,HOUSE='camara';try{HOUSE=new URLSearchParams(location.search).get('house')||localStorage.getItem('house')||'camara'}catch(e){}
let lastComp='',lastPanels='',lastScatter='';
function ink(){return getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()}
function mut(){return getComputedStyle(document.documentElement).getPropertyValue('--mut').trim()}
function grid(){return getComputedStyle(document.documentElement).getPropertyValue('--grid').trim()}
function ufSel(){return document.getElementById('uf')}
function fillSel(){const s=ufSel(),cur=s.value;s.innerHTML='<option value="BR">'+T('brazil')+'</option>'+Object.keys(UFNAME).sort((a,b)=>UFNAME[a].localeCompare(UFNAME[b])).map(u=>'<option value="'+u+'">'+UFNAME[u]+' ('+u+')</option>').join('');s.value=cur||'BR';}
function govOf(uf,y){return (GOVS[uf]||{})[y]}
function govChip(g){if(!g)return'';if(!g.spec)return'<span class="gov" style="background:transparent;border:1px dashed '+mut()+'"></span><span style="color:var(--mut)">'+T('pending')+'</span>';return'<span class="gov" style="background:'+COLOR[g.spec]+'"></span>'+g.name+' <span style="color:var(--mut)">('+g.party+')</span>'}
const govPlugin={id:'gov',afterDatasetsDraw(c,args,opts){const y=c.scales.y,ctx=c.ctx;c.data.labels.forEach((lab,i)=>{const g=govOf(opts.uf,lab);if(!g)return;const py=y.getPixelForValue(i);ctx.save();ctx.beginPath();ctx.arc(c.chartArea.left-52,py,5,0,Math.PI*2);if(g.spec){ctx.fillStyle=COLOR[g.spec];ctx.fill()}else{ctx.strokeStyle=mut();ctx.setLineDash([2,2]);ctx.stroke()}ctx.restore();});}};
function compData(uf){const c=COMP[HOUSE][uf]||{};const yrs=Object.keys(c).sort();return{yrs,ds:[...SPEC].reverse().map(k=>({key:k,label:T('spec')[k],backgroundColor:COLOR[k],borderColor:COLOR[k],seats:yrs.map(y=>c[y][k]),data:yrs.map(y=>c[y].total?+(c[y][k]/c[y].total*100).toFixed(1):0)}))}}
let LSPEC=null;try{LSPEC=JSON.parse(localStorage.getItem('lspec')||'null')}catch(e){}if(!Array.isArray(LSPEC))LSPEC=[...SPEC];
function lchips(){const all=LSPEC.length===SPEC.length;document.getElementById('lspec').innerHTML='<button class="chip'+(all?' on':'')+'" onclick="LSPEC=[...SPEC];applyL()">'+T('all_spec')+'</button>'+[...SPEC].reverse().map(k=>'<button class="chip'+(LSPEC.includes(k)&&!all?' on':'')+'" onclick="togL(\''+k+'\')"><span class="dot" style="background:'+COLOR[k]+'"></span>'+T('spec')[k]+'</button>').join('')}
function togL(k){const all=LSPEC.length===SPEC.length;if(all)LSPEC=[k];else if(LSPEC.includes(k)){LSPEC=LSPEC.filter(x=>x!==k);if(!LSPEC.length)LSPEC=[...SPEC]}else LSPEC.push(k);applyL()}
function applyL(){try{localStorage.setItem('lspec',JSON.stringify(LSPEC))}catch(e){}lchips();if(lines){lines.data.datasets.forEach(d=>d.hidden=!LSPEC.includes(d.key));lines.update()}}
const endLabels={id:'endl',afterDatasetsDraw(c){const ctx=c.ctx,a=c.chartArea;const small=c.width<520;const it=[];c.data.datasets.forEach((d,i)=>{if(d.hidden)return;const m=c.getDatasetMeta(i);let j=d.data.length-1;while(j>=0&&d.data[j]==null)j--;if(j<0)return;const pt=m.data[j];it.push({y:pt.y,x:pt.x,t:d.label+' '+d.data[j]+'%',c:d.borderColor})});
 it.sort((p,q)=>p.y-q.y);const gap=small?11:13;for(let i=1;i<it.length;i++)if(it[i].y-it[i-1].y<gap)it[i].y=it[i-1].y+gap;
 ctx.save();ctx.font=(small?'10':'11')+'px sans-serif';ctx.textBaseline='middle';it.forEach(o=>{ctx.fillStyle=o.c;ctx.fillText(o.t,o.x+8,Math.min(o.y,a.bottom))});ctx.restore()}};
function drawComp(uf){const {yrs,ds}=compData(uf);const tip={callbacks:{label:t=>t.dataset.label+': '+t.dataset.seats[t.dataIndex]+' '+T('seats')+' ('+t.raw+'%)'}};
 document.getElementById('speclg').innerHTML=[...SPEC].reverse().map(k=>'<span><span class="sw" style="background:'+COLOR[k]+'"></span>'+T('spec')[k]+'</span>').join('');
 document.getElementById('senote').textContent=HOUSE==='senado'?T('senate_note'):'';
 if(bars)bars.destroy();if(lines)lines.destroy();
 lchips();bars=new Chart(document.getElementById('bars'),{type:'bar',data:{labels:yrs,datasets:ds.map(d=>({...d,barThickness:22}))},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:{left:34}},plugins:{legend:{display:false},tooltip:tip,gov:{uf}},scales:{x:{stacked:true,max:100,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}},y:{stacked:true,ticks:{color:ink()},grid:{display:false}}}},plugins:[govPlugin]});
 lines=new Chart(document.getElementById('lines'),{type:'line',data:{labels:yrs,datasets:ds.map(d=>({...d,fill:false,tension:.25,pointRadius:3,hidden:!LSPEC.includes(d.key)}))},plugins:[endLabels],options:{responsive:true,maintainAspectRatio:false,layout:{padding:{right:innerWidth<640?92:120}},interaction:{mode:'index',intersect:false},plugins:{legend:{display:false},tooltip:tip},scales:{x:{ticks:{color:mut()},grid:{display:false}},y:{min:0,max:uf==='BR'&&HOUSE==='camara'?45:100,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}}}}});
 const c=COMP[HOUSE][uf]||{};const gl=uf==='BR'?T('pres'):T('gov');
 let h='<div class="tw"><table><tr><th>'+T('election')+'</th>'+SPEC.map(k=>'<th>'+T('spec')[k]+'</th>').join('')+'<th class="l gc">'+gl+'</th></tr>';
 yrs.forEach(y=>{const gc=govChip(govOf(uf,y));h+='<tr><td>'+y+'<br><small style="color:var(--mut)">'+c[y].total+' '+T('seats')+'</small></td>'+SPEC.map(k=>'<td>'+c[y][k]+'<br><small style="color:var(--mut)">'+(c[y].total?(c[y][k]/c[y].total*100).toFixed(1):0)+'%</small></td>').join('')+'<td class="l gc">'+gc+'</td></tr>'+(gc?'<tr class="govm"><td colspan="8"><div class="govc">'+gl+': '+gc+'</div></td></tr>':'')});
 document.getElementById('comptable').innerHTML=h+'</table></div>';
 const pt=document.getElementById('partytable');
 if(HOUSE==='senado'&&uf!=='BR'){const N=SENNAMES[uf]||{};pt.innerHTML='<h3>'+T('sen_elected')+'</h3><div class="tw"><table><tr><th>'+T('election')+'</th><th class="l">'+T('sen_elected')+'</th></tr>'+yrs.map(y=>'<tr><td>'+y+'</td><td class="l">'+(N[y]||[]).join('<br>')+'</td></tr>').join('')+'</table></div>';return}
 const P=PARTIES[HOUSE][uf]||{};const all=[...new Set(Object.values(P).flatMap(o=>Object.keys(o)))].sort();
 if(!all.length){pt.innerHTML='';return}
 let g='<h3>'+T('seats_by_party')+'</h3><div class="tw"><table><tr><th class="l">'+T('party')+'</th>'+yrs.map(y=>'<th>'+y+'</th>').join('')+'</tr>';
 all.forEach(p=>{g+='<tr><td class="l">'+p+'</td>'+yrs.map(y=>'<td>'+((P[y]||{})[p]||'')+'</td>').join('')+'</tr>'});pt.innerHTML=g+'</table></div>';}
function drawPanels(uf){const host=document.getElementById('panels');host.innerHTML='';Object.values(pcharts).forEach(c=>c.destroy());pcharts={};const st=STATES.find(s=>s.uf===uf);
 document.getElementById('ctxintro').textContent=(uf==='BR'?T('ctx_intro_br'):T('ctx_intro').split('{name}').join(UFNAME[uf]));
 const keys=Object.keys(PANELS).sort((a,b)=>T('panels')[a].localeCompare(T('panels')[b]));
 keys.forEach(key=>{const p=PANELS[key];const lg=p.ds.map(d=>'<span><span class="sw" style="background:'+d.color+'"></span>'+T('series')[d.key]+'</span>').join('');const sm=uf==='BR'?[]:p.ds.map(d=>{const e=STV[d.key];const v=e?e.v[uf]:null;return v==null?null:{x:Math.min(e.y,2026),y:v,c:d.color,l:T('series')[d.key]}}).filter(Boolean);const sv=(st&&p.stateCol&&!sm.length)?st[p.stateCol]:null;
  host.insertAdjacentHTML('beforeend','<div><h3>'+T('panels')[key]+'</h3><div class="wrap" style="height:210px"><canvas id="p_'+key+'"></canvas></div><div class="lg">'+lg+(sv!==null?'<span><span class="sw" style="background:'+ink()+';border-radius:50%"></span>'+UFNAME[uf]+' ('+T('latest')+'): '+sv+'</span>':'')+'</div>'+(sm.length?'<div class="cap" style="text-align:left">'+UFNAME[uf]+': '+sm.map(m=>m.l+' '+m.y+' ('+m.x+')').join(' · ')+'</div>':'')+'</div>');
  const isBar=key==='growth';const ds=p.ds.map(d=>({label:T('series')[d.key],data:d.data,borderColor:d.color,backgroundColor:isBar?(c=>c.parsed&&c.parsed.y<0?'#ec835a':'#9fc49f'):d.color,tension:.25,pointRadius:2,borderWidth:2,barThickness:5}));
  if(sv!==null)ds.push({label:UFNAME[uf],data:[{x:2024,y:+sv}],pointRadius:7,borderColor:ink(),backgroundColor:ink(),showLine:false});sm.forEach(m=>ds.push({type:'line',label:UFNAME[uf]+' · '+m.l,data:[{x:m.x,y:m.y}],pointRadius:6,pointBorderWidth:2,pointBorderColor:ink(),backgroundColor:m.c,borderColor:m.c,showLine:false}));
  pcharts[key]=new Chart(document.getElementById('p_'+key),{type:isBar?'bar':'line',data:{datasets:ds},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},plugins:{legend:{display:false},tooltip:{callbacks:{title:t=>t[0].parsed.x,label:t=>t.dataset.label+': '+t.parsed.y}}},scales:{x:{type:'linear',min:1990,max:2026,ticks:{color:mut(),stepSize:6,callback:v=>v},grid:{display:false}},y:{min:p.lo,max:p.hi,ticks:{color:mut()},grid:{color:grid()}}}}});});}
function corr(x,y){const n=x.length,mx=x.reduce((a,b)=>a+b)/n,my=y.reduce((a,b)=>a+b)/n;let sxy=0,sx=0,sy=0;for(let i=0;i<n;i++){sxy+=(x[i]-mx)*(y[i]-my);sx+=(x[i]-mx)**2;sy+=(y[i]-my)**2}return sxy/Math.sqrt(sx*sy)}
const isel=document.getElementById('isel');SCOLS.slice(3).forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;isel.appendChild(o)});isel.value='evangelical_pct';
function drawScatter(uf){const k=isel.value;[...isel.options].forEach(o=>o.textContent=T('cards')[o.value]||o.value);const kl=T('cards')[k]||k;const pts=STATES.map(r=>({x:+r[k],y:+r.flavio_pct_1st_round,uf:r.uf}));
 document.getElementById('corr').textContent=T('corr').replace('{r}',corr(pts.map(p=>p.x),pts.map(p=>p.y)).toFixed(2));if(sc)sc.destroy();
 sc=new Chart(document.getElementById('sc'),{type:'scatter',data:{datasets:[{data:pts,pointRadius:pts.map(p=>p.uf===uf?9:5),pointBackgroundColor:pts.map(p=>p.uf===uf?ink():(p.y>=50?'#2a78d6':'#e24b4a'))}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:t=>t.raw.uf+': '+kl+' '+t.raw.x+' · Flávio '+t.raw.y+'%'}}},scales:{x:{title:{display:true,text:kl,color:mut()},ticks:{color:mut()},grid:{color:grid()}},y:{min:20,max:75,title:{display:true,text:T('yaxis'),color:mut()},ticks:{color:mut()},grid:{color:grid()}}}},plugins:[{id:'lbl',afterDatasetsDraw:c=>{const ctx=c.ctx;ctx.font='10px sans-serif';ctx.fillStyle=ink();c.getDatasetMeta(0).data.forEach((p,i)=>ctx.fillText(pts[i].uf,p.x+7,p.y+3))}}]});}
function setHouse(h){HOUSE=h;try{localStorage.setItem('house',h)}catch(e){}render();}
function render(force){fillSel();const uf=ufSel().value;
 document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.h===HOUSE));
 document.getElementById('sub').textContent=uf==='BR'?T('sub_br'):T('sub_uf').replace('{name}',UFNAME[uf]).replace('{n}',(COMP.camara[uf]['2026']||{}).total||'');
 const ck=uf+'|'+HOUSE+'|'+LANG+'|'+isDark();if(force||ck!==lastComp){drawComp(uf);lastComp=ck}
 const pk=uf+'|'+LANG+'|'+isDark();if(force||pk!==lastPanels){drawPanels(uf);lastPanels=pk}
 const sk=uf+'|'+isel.value+'|'+LANG+'|'+isDark();if(force||sk!==lastScatter){drawScatter(uf);lastScatter=sk}
 try{localStorage.setItem('uf',uf)}catch(e){}}
fillSel();try{const u=localStorage.getItem('uf');if(u&&COMP.camara[u])ufSel().value=u}catch(e){}
ufSel().addEventListener('change',()=>render());isel.addEventListener('change',()=>render());
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>{if(THEME==='auto')render(true)});
applyStrings();render(true);
"""
def _fill(js):
    for k,v in {"__COMP__":comp,"__SENCOMP__":sen_comp,"__PARTIES__":parties,"__SENPARTIES__":sen_parties,"__SENNAMES__":sen_names,"__GOVS__":govs,"__PANELS__":panels,"__STV__":STV,"__STATES__":states,"__SCOLS__":statecols,"__PRES__":pres}.items():
        js=js.replace(k,json.dumps(v,ensure_ascii=False))
    return js
index = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>(function(){{try{{var q=new URLSearchParams(location.search);var t=q.get('theme'),l=q.get('lang'),h=q.get('house');if(h)localStorage.setItem('house',h);document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');document.documentElement.lang=l==='pt'?'pt':'en';}}catch(e){{}}}})();</script>
{meta("index")}<script src="assets/chart.umd.js"></script><style>{CSS}</style></head><body>
{header('index')}
<main>
{CTLS}
<div class="intro"><strong data-i="intro_h"></strong><br><span data-i="intro"></span><div class="byline"><a href="https://antonioaurel.github.io/" target="_blank" rel="noopener">antonioaurel.github.io</a></div></div>
<div class="cols">
<div>
<div class="tabs"><button class="tab" data-h="camara" onclick="setHouse('camara')" data-i="tab_camara"></button><button class="tab" data-h="senado" onclick="setHouse('senado')" data-i="tab_senado"></button></div>
<section class="sec" style="border-top:none;padding-top:0"><h2 data-i="h_comp" style="margin-top:0"></h2><div class="lg" id="speclg"></div><p class="cap" id="senote"></p>
<h3 data-i="h_bars"></h3><p class="cap" data-i="exp_bars"></p><div class="wrap" style="height:380px"><canvas id="bars"></canvas></div></section>
<section class="sec"><h3 data-i="h_lines"></h3><p class="cap" data-i="exp_lines"></p><p class="cap" data-i="how_lspec"></p><div class="chips" id="lspec" style="justify-content:center;margin:6px 0 10px"></div><div class="wrap" style="height:340px"><canvas id="lines"></canvas></div></section>
<section class="sec"><p class="cap" data-i="exp_tables"></p><div class="two"><div id="comptable"></div><div id="partytable"></div></div></section>
<section class="sec"><h2 data-i="h_scatter"></h2><div style="text-align:center"><label><span data-i="indicator"></span>: <select id="isel"></select></label><br><span id="corr" class="cap"></span></div>
<div class="wrap" style="height:680px"><canvas id="sc"></canvas></div></section>
</div>
<div>
<section class="sec" style="border-top:none;padding-top:0"><h2 data-i="h_ctx" style="margin-top:0"></h2><p class="cap" id="ctxintro"></p><div class="grid panels" id="panels"></div></section>
</div>
</div>
</main>
<footer class="foot"><a href="https://antonioaurel.github.io/" target="_blank" rel="noopener">antonioaurel.github.io</a></footer>
<script>{I18N_JS}</script><script>{_fill(INDEX_JS)}</script></body></html>"""
(ROOT/"index.html").write_text(index, encoding="utf-8")
print("wrote index.html", len(index)//1024, "KB")

# ---------------- methodology.html ----------------
import sys; sys.path.insert(0, str(ROOT / "scripts")); from politicians_data import SOURCES as _S
SRCLIST = "<div class=\"srcs\">" + "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in _S.items()) + "</div>"
POL = [
 ("far_right","Nikolas Ferreira","PL · MG",
  "Born 1996, Belo Horizonte. Law degree, PUC Minas (2022). City councillor in Belo Horizonte (2020), federal deputy in 2022 (1.49 million votes, the most voted in the country) and again in 2026 (3.1 million). Built his following on social media around moral conservatism, gun rights and confrontation with the Supreme Court.",
  "Nascido em 1996, Belo Horizonte. Bacharel em Direito pela PUC Minas (2022). Vereador de Belo Horizonte (2020), deputado federal em 2022 (1,49 milhão de votos, o mais votado do país) e em 2026 (3,1 milhões). Construiu sua base nas redes sociais em torno do conservadorismo moral, do armamento e do confronto com o STF.",
  "Why here: PL after 2021 is the party Bolsonaro and the former PSL bloc moved into; its voting record (8 January amnesty, attacks on the courts) is what places it at the edge rather than with the classic right.",
  "Por que aqui: o PL pós-2021 é o partido para onde migraram Bolsonaro e o antigo bloco do PSL; o comportamento em plenário (anistia do 8 de janeiro, confronto com o Judiciário) é o que o coloca na ponta, e não na direita clássica."),
 ("right","Hugo Motta","Republicanos · PB",
  "Born 1989, João Pessoa; political heir of an MDB family from Patos. Trained as a physician. Federal deputy since 2010 (elected at 21), MDB until 2018, then Republicanos. President of the Chamber of Deputies since February 2025.",
  "Nascido em 1989, João Pessoa; herdeiro político de uma família do MDB de Patos. Formado em Medicina. Deputado federal desde 2010 (eleito aos 21 anos), no MDB até 2018, depois no Republicanos. Presidente da Câmara dos Deputados desde fevereiro de 2025.",
  "Why here: Republicanos is the party of the Universal Church's political arm, conservative on customs and pragmatic in coalitions; with Novo (economic liberalism) and the small evangelical parties it forms the non-Bolsonarist right.",
  "Por que aqui: o Republicanos é o braço político da Igreja Universal, conservador nos costumes e pragmático nas coalizões; com o Novo (liberalismo econômico) e os pequenos partidos evangélicos forma a direita não bolsonarista."),
 ("centre_right","Gilberto Kassab","PSD · SP",
  "Born 1960, São Paulo. Civil engineer and economist, University of São Paulo. City councillor, state and federal deputy (PFL), mayor of São Paulo 2006–2012 (DEM), founder of PSD in 2011, minister under Dilma Rousseff (Cities) and Michel Temer (Science and Communications), São Paulo state secretary under Tarcísio de Freitas.",
  "Nascido em 1960, São Paulo. Engenheiro civil e economista pela USP. Vereador, deputado estadual e federal (PFL), prefeito de São Paulo 2006–2012 (DEM), fundador do PSD em 2011, ministro de Dilma Rousseff (Cidades) e de Michel Temer (Ciência e Comunicações), secretário estadual no governo Tarcísio de Freitas.",
  "Why here: the centrão in one career — allied with PT, MDB and PL governments in sequence. Centre-right here means market-friendly, socially flexible, and organised around access to the executive rather than programme.",
  "Por que aqui: o centrão em uma biografia — aliado de governos do PT, do MDB e do PL em sequência. Centro-direita aqui significa pró-mercado, flexível nos costumes e organizado em torno do acesso ao Executivo, não do programa."),
 ("centre","Simone Tebet","MDB · MS",
  "Born 1970, Três Lagoas. Law degree, Federal University of Rio de Janeiro; master's in constitutional law, PUC-SP. State deputy, mayor of Três Lagoas, vice-governor of Mato Grosso do Sul, senator 2015–2023, third place in the 2022 presidential election, Minister of Planning since 2023.",
  "Nascida em 1970, Três Lagoas. Bacharel em Direito pela UFRJ; mestre em Direito do Estado pela PUC-SP. Deputada estadual, prefeita de Três Lagoas, vice-governadora de Mato Grosso do Sul, senadora 2015–2023, terceira colocada na eleição presidencial de 2022, ministra do Planejamento desde 2023.",
  "Why here: MDB is the party that has sat in every governing coalition since 1985 and has never had a stable ideological identity; expert surveys place it closest to the midpoint of the scale.",
  "Por que aqui: o MDB participou de todas as coalizões de governo desde 1985 e nunca teve identidade ideológica estável; as pesquisas com especialistas o colocam mais perto do ponto médio da escala."),
 ("centre_left","Tabata Amaral","PSB · SP",
  "Born 1993, São Paulo (Vila Missionária). Harvard University, degrees in astrophysics and political science (2016). Federal deputy in 2018 (PDT), 2022 and 2026 (PSB), focused on education policy; ran for mayor of São Paulo in 2024.",
  "Nascida em 1993, São Paulo (Vila Missionária). Formada em Astrofísica e Ciência Política pela Universidade Harvard (2016). Deputada federal em 2018 (PDT), 2022 e 2026 (PSB), com atuação concentrada em educação; candidata à prefeitura de São Paulo em 2024.",
  "Why here: PSB, PDT and PV are social-democratic in origin, govern with PT but keep distance on fiscal and security issues, and regularly ally with centre-right governors in the states.",
  "Por que aqui: PSB, PDT e PV têm origem social-democrata, governam com o PT mas mantêm distância em temas fiscais e de segurança, e aliam-se com frequência a governadores de centro-direita nos estados."),
 ("left","Fernando Haddad","PT · SP",
  "Born 1963, São Paulo. Law degree, master's in economics and PhD in philosophy, all at the University of São Paulo, where he taught political science. Minister of Education 2005–2012, mayor of São Paulo 2013–2016, presidential candidate in 2018, Minister of Finance since 2023.",
  "Nascido em 1963, São Paulo. Bacharel em Direito, mestre em Economia e doutor em Filosofia pela USP, onde foi professor de ciência política. Ministro da Educação 2005–2012, prefeito de São Paulo 2013–2016, candidato à Presidência em 2018, ministro da Fazenda desde 2023.",
  "Why here: PT was founded in 1980 by the union movement with a socialist programme and moderated sharply after 2002; it is kept at 'left' rather than 'centre-left' to preserve the distinction from PSB and PDT.",
  "Por que aqui: o PT nasceu em 1980 do movimento sindical com programa socialista e moderou-se fortemente após 2002; é mantido em 'esquerda', e não 'centro-esquerda', para preservar a distinção em relação a PSB e PDT."),
 ("far_left","Guilherme Boulos","PSOL · SP",
  "Born 1982, São Paulo. Philosophy degree, University of São Paulo; specialisation in clinical psychology, PUC; master's in psychiatry, USP. National coordinator of the Homeless Workers' Movement (MTST), presidential candidate in 2018, runner-up for mayor of São Paulo in 2020 and 2024, federal deputy in 2022 (most voted in São Paulo), minister of the General Secretariat of the Presidency since October 2025.",
  "Nascido em 1982, São Paulo. Formado em Filosofia pela USP; especialização em Psicologia Clínica pela PUC; mestre em Psiquiatria pela USP. Coordenador nacional do MTST, candidato à Presidência em 2018, segundo colocado na prefeitura de São Paulo em 2020 e 2024, deputado federal em 2022 (o mais votado de São Paulo), ministro da Secretaria-Geral da Presidência desde outubro de 2025.",
  "Why here: PSOL was founded in 2004 by PT members expelled for voting against the pension reform; it keeps an anti-capitalist programme and opposes PT governments on economic policy, which places it at the far end. PSTU and UP would be there too but have never won a seat; the PCB's three seats date from 1990, before its 1992 refoundation as PPS.",
  "Por que aqui: o PSOL foi fundado em 2004 por petistas expulsos por votarem contra a reforma da previdência; mantém programa anticapitalista e faz oposição aos governos do PT na economia, o que o coloca na ponta. PSTU e UP estariam ali também, mas nunca elegeram deputado; as três cadeiras do PCB são de 1990, antes da refundação como PPS em 1992."),
]
ERAS = [("1990-1998", "1990–1998", "Collor · Itamar · FHC I"), ("2002-2010", "2002–2010", "FHC II · Lula · Dilma I"), ("2014-2026", "2014–2026", "Dilma II · Temer · Bolsonaro · Lula III")]
POL_ERA = {
"1990-1998": [
 ("far_right","Enéas Carneiro","PRONA · SP",
  "Born 1938, Rio Branco. Physician and cardiologist (Faculty of Medicine, Rio de Janeiro), with further degrees in mathematics and physics. Founded PRONA in 1989 and ran for president in 1989, 1994 (third place, 7.4%) and 1998 on a nationalist, anti-globalisation, pro-nuclear platform; elected federal deputy in 2002 with 1.57 million votes, then a national record.",
  "Nascido em 1938, Rio Branco. Médico cardiologista (Faculdade de Medicina do Rio de Janeiro), com formação adicional em matemática e física. Fundou o PRONA em 1989 e disputou a Presidência em 1989, 1994 (terceiro lugar, 7,4%) e 1998 com plataforma nacionalista, antiglobalização e pró-nuclear; eleito deputado federal em 2002 com 1,57 milhão de votos, então recorde nacional.",
  "Why here: PRONA was the only far-right party with a national presence in the 1990s; it elected its first deputy in 1998 and never participated in a governing coalition.",
  "Por que aqui: o PRONA foi o único partido de extrema direita com presença nacional nos anos 1990; elegeu seu primeiro deputado em 1998 e nunca integrou coalizão de governo."),
 ("right","Antônio Carlos Magalhães","PFL · BA",
  "Born 1927, Salvador; died 2007. Physician (Federal University of Bahia). Federal deputy from 1958, mayor of Salvador (appointed, 1967–70), governor of Bahia three times (two under the military regime, one elected in 1990), Minister of Communications under Sarney, senator from 1995, president of the Senate 1997–2001. Built the PFL's Bahia machine and was FHC's main ally in Congress.",
  "Nascido em 1927, Salvador; morreu em 2007. Médico (UFBA). Deputado federal a partir de 1958, prefeito de Salvador (nomeado, 1967–70), governador da Bahia três vezes (duas no regime militar, uma eleito em 1990), ministro das Comunicações de Sarney, senador a partir de 1995, presidente do Senado 1997–2001. Construiu a máquina do PFL na Bahia e foi o principal aliado de FHC no Congresso.",
  "Why here: PFL was the direct heir of ARENA/PDS, the party of the military regime, and the largest right-wing bench of the decade (83–105 seats).",
  "Por que aqui: o PFL foi o herdeiro direto da ARENA/PDS, o partido do regime militar, e a maior bancada de direita da década (83–105 cadeiras)."),
 ("centre_right","Fernando Henrique Cardoso","PSDB · SP",
  "Born 1931, Rio de Janeiro. Sociologist, University of São Paulo (doctorate 1961), exiled in 1964, professor at USP and abroad, a founder of CEBRAP. Senator for São Paulo 1983–1992, co-founder of PSDB in 1988, Foreign Minister and then Finance Minister (1993–94, the Real Plan), president 1995–2002.",
  "Nascido em 1931, Rio de Janeiro. Sociólogo pela USP (doutorado em 1961), exilado em 1964, professor na USP e no exterior, fundador do CEBRAP. Senador por São Paulo 1983–1992, cofundador do PSDB em 1988, ministro das Relações Exteriores e depois da Fazenda (1993–94, Plano Real), presidente 1995–2002.",
  "Why here: PSDB began as a centre-left split from PMDB in 1988; governing with PFL from 1994 on a privatisation and fiscal-stability agenda is what moves it to centre-right in the mapping.",
  "Por que aqui: o PSDB nasceu em 1988 como dissidência de centro-esquerda do PMDB; governar com o PFL a partir de 1994, com agenda de privatizações e estabilidade fiscal, é o que o move para a centro-direita no mapeamento."),
 ("centre","Ulysses Guimarães","PMDB · SP",
  "Born 1916, Rio Claro; died 1992. Law degree, University of São Paulo. Federal deputy continuously from 1951, president of the Chamber, leader of the MDB opposition to the military regime, 'anti-candidate' for president in 1973, president of the Constituent Assembly that wrote the 1988 Constitution, PMDB presidential candidate in 1989.",
  "Nascido em 1916, Rio Claro; morreu em 1992. Bacharel em Direito pela USP. Deputado federal ininterruptamente desde 1951, presidente da Câmara, líder da oposição do MDB ao regime militar, 'anticandidato' a presidente em 1973, presidente da Assembleia Constituinte que escreveu a Constituição de 1988, candidato do PMDB à Presidência em 1989.",
  "Why here: PMDB was the umbrella opposition to the regime, holding everything from liberals to socialists; after 1985 it became the pivot of every coalition without a programme of its own.",
  "Por que aqui: o PMDB foi o guarda-chuva da oposição ao regime, abrigando de liberais a socialistas; depois de 1985 virou o pivô de todas as coalizões sem programa próprio."),
 ("centre_left","Leonel Brizola","PDT · RJ",
  "Born 1922, Carazinho; died 2004. Civil engineer, Federal University of Rio Grande do Sul. Mayor of Porto Alegre, governor of Rio Grande do Sul 1959–63 (led the 1961 'Legality' campaign), federal deputy, exiled 1964–79, founded PDT in 1980, governor of Rio de Janeiro 1983–87 and 1991–94, presidential candidate in 1989 (third, 16%) and 1994.",
  "Nascido em 1922, Carazinho; morreu em 2004. Engenheiro civil pela UFRGS. Prefeito de Porto Alegre, governador do Rio Grande do Sul 1959–63 (liderou a Campanha da Legalidade em 1961), deputado federal, exilado 1964–79, fundou o PDT em 1980, governador do Rio de Janeiro 1983–87 e 1991–94, candidato à Presidência em 1989 (terceiro, 16%) e 1994.",
  "Why here: PDT claimed Vargas's labourist (trabalhista) tradition — nationalist, pro-welfare, non-Marxist — the clearest centre-left identity of the period.",
  "Por que aqui: o PDT reivindicava a tradição trabalhista de Vargas — nacionalista, pró-bem-estar social, não marxista — a identidade de centro-esquerda mais nítida do período."),
 ("left","Luiz Inácio Lula da Silva","PT · SP",
  "Born 1945, Caetés (PE); raised in São Paulo. Trained as a lathe operator at SENAI; no university. Metalworkers' union president in São Bernardo during the 1978–80 strikes, founder of PT in 1980 and of the CUT in 1983, federal deputy 1987–91 (most voted in the country), presidential candidate in 1989, 1994 and 1998 before winning in 2002.",
  "Nascido em 1945, Caetés (PE); criado em São Paulo. Formado torneiro mecânico pelo SENAI; sem curso superior. Presidente do sindicato dos metalúrgicos de São Bernardo nas greves de 1978–80, fundador do PT em 1980 e da CUT em 1983, deputado federal 1987–91 (o mais votado do país), candidato à Presidência em 1989, 1994 e 1998 antes de vencer em 2002.",
  "Why here: PT in the 1990s was a party of unions, Catholic base communities and Marxist tendencies with an explicitly socialist programme; this is the PT the 'left' bin was built around.",
  "Por que aqui: o PT dos anos 1990 era um partido de sindicatos, comunidades eclesiais de base e tendências marxistas com programa explicitamente socialista; é o PT em torno do qual a faixa 'esquerda' foi construída."),
 ("far_left","Roberto Freire","PCB → PPS · PE",
  "Born 1942, Recife. Law degree, Federal University of Pernambuco. Federal deputy from 1979 (MDB, then PCB after legalisation in 1985), president of the Brazilian Communist Party, its presidential candidate in 1989; led the party's 1992 refoundation as PPS, senator for Pernambuco 1995–2003, Minister of Culture under Temer (2016–17). Today in Cidadania, at the centre.",
  "Nascido em 1942, Recife. Bacharel em Direito pela UFPE. Deputado federal desde 1979 (MDB, depois PCB após a legalização em 1985), presidente do Partido Comunista Brasileiro e seu candidato à Presidência em 1989; conduziu a refundação do partido como PPS em 1992, senador por Pernambuco 1995–2003, ministro da Cultura de Temer (2016–17). Hoje no Cidadania, no centro.",
  "Why here: the three PCB deputies of 1990 are the only far-left seats of the decade. Freire's own path — from the Communist Party to a Temer ministry — is the clearest example of why the mapping is by period.",
  "Por que aqui: os três deputados do PCB em 1990 são as únicas cadeiras de extrema esquerda da década. A trajetória do próprio Freire — do Partido Comunista a um ministério de Temer — é o exemplo mais claro de por que o mapeamento é por período."),
],
"2002-2010": [
 ("far_right","Jair Bolsonaro","PPB / PP / PTB · RJ",
  "Born 1955, Glicério (SP). Army officer, Military Academy of Agulhas Negras (1977), paratrooper, retired as captain in 1988 after a disciplinary case. City councillor in Rio (1989), federal deputy 1991–2018 through nine parties (PDC, PPR, PPB, PP, PTB, PFL, PSC, PSL), a low-profile corporatist voice for the military and police until 2014; president 2019–2022.",
  "Nascido em 1955, Glicério (SP). Oficial do Exército, formado na Academia Militar das Agulhas Negras (1977), paraquedista, reformado como capitão em 1988 após processo disciplinar. Vereador no Rio (1989), deputado federal 1991–2018 por nove partidos (PDC, PPR, PPB, PP, PTB, PFL, PSC, PSL), voz corporativa de militares e policiais com pouca projeção até 2014; presidente 2019–2022.",
  "Why here: in this era his parties (PPB, PP, PTB) sit in the right/centre-right columns and PRONA's small bench, led by Enéas (deputy 2002–07), holds the only far-right seats. Bolsonaro is listed to show that the far-right persona existed inside the centrão long before it had a party of its own — which is why the far-right column stays small until 2018.",
  "Por que aqui: neste período seus partidos (PPB, PP, PTB) ficam nas colunas direita/centro-direita, e a pequena bancada do PRONA, liderada por Enéas (deputado 2002–07), detém as únicas cadeiras de extrema direita. Bolsonaro é listado para mostrar que a persona de extrema direita existia dentro do centrão muito antes de ter partido próprio — por isso a coluna de extrema direita fica pequena até 2018."),
 ("right","Paulo Maluf","PPB / PP · SP",
  "Born 1931, São Paulo. Civil engineer, Polytechnic School of the University of São Paulo. Mayor of São Paulo (appointed 1969–71; elected 1993–96), governor of São Paulo 1979–82 (indirectly elected), presidential candidate in 1985 (electoral college) and 1989, federal deputy 2007–2018; convicted of money laundering in 2017.",
  "Nascido em 1931, São Paulo. Engenheiro civil pela Escola Politécnica da USP. Prefeito de São Paulo (nomeado 1969–71; eleito 1993–96), governador de São Paulo 1979–82 (eleição indireta), candidato à Presidência em 1985 (colégio eleitoral) e 1989, deputado federal 2007–2018; condenado por lavagem de dinheiro em 2017.",
  "Why here: PPB/PP under Maluf was the hard right of the regime's ARENA lineage — 'rouba mas faz' populism, law-and-order, pro-business — before it dissolved into the centrão after 2010.",
  "Por que aqui: o PPB/PP de Maluf era a direita dura da linhagem da ARENA — populismo do 'rouba mas faz', lei e ordem, pró-empresariado — antes de se diluir no centrão depois de 2010."),
 ("centre_right","José Serra","PSDB · SP",
  "Born 1942, São Paulo. Engineering student at USP and student-union president in 1963, exiled after the coup; master's in economics (Chile) and PhD in economics (Cornell). Federal deputy and senator, Minister of Planning and of Health under FHC (generic drugs, anti-tobacco law), presidential candidate in 2002 and 2010, mayor of São Paulo 2005–06, governor of São Paulo 2007–10, Foreign Minister under Temer.",
  "Nascido em 1942, São Paulo. Estudante de engenharia na USP e presidente da UNE em 1963, exilado após o golpe; mestre em Economia (Chile) e doutor em Economia (Cornell). Deputado federal e senador, ministro do Planejamento e da Saúde de FHC (genéricos, lei antifumo), candidato à Presidência em 2002 e 2010, prefeito de São Paulo 2005–06, governador de São Paulo 2007–10, ministro das Relações Exteriores de Temer.",
  "Why here: Serra personifies the PSDB of this era — technocratic, fiscally orthodox, socially moderate — the main opposition to the PT governments from the centre-right.",
  "Por que aqui: Serra personifica o PSDB deste período — tecnocrático, ortodoxo na economia, moderado nos costumes — a principal oposição aos governos do PT pela centro-direita."),
 ("centre","Michel Temer","PMDB · SP",
  "Born 1940, Tietê (SP). Law degree, University of São Paulo; doctorate in public law, PUC-SP, where he taught constitutional law. São Paulo state prosecutor and public-security secretary, federal deputy from 1987, president of the Chamber 1997–2001 and 2009–10, PMDB national president from 2001, vice-president 2011–16, president 2016–18 after Dilma Rousseff's impeachment.",
  "Nascido em 1940, Tietê (SP). Bacharel em Direito pela USP; doutor em Direito Público pela PUC-SP, onde foi professor de Direito Constitucional. Procurador do Estado e secretário de Segurança Pública de São Paulo, deputado federal desde 1987, presidente da Câmara 1997–2001 e 2009–10, presidente nacional do PMDB a partir de 2001, vice-presidente 2011–16, presidente 2016–18 após o impeachment de Dilma Rousseff.",
  "Why here: Temer's PMDB was vice-president to Lula's coalition, then to Dilma's, then replaced her — the centre as the permanent governing partner of whoever wins.",
  "Por que aqui: o PMDB de Temer foi vice na coalizão de Lula, depois na de Dilma, e depois a substituiu — o centro como sócio permanente de quem governa."),
 ("centre_left","Eduardo Campos","PSB · PE",
  "Born 1965, Recife; died 2014. Economist, Federal University of Pernambuco; grandson of Miguel Arraes. State and federal deputy, Minister of Science and Technology under Lula (2004–05), governor of Pernambuco 2007–2014 (re-elected with 82%), PSB national president; presidential candidate in 2014, killed in a plane crash during the campaign.",
  "Nascido em 1965, Recife; morreu em 2014. Economista pela UFPE; neto de Miguel Arraes. Deputado estadual e federal, ministro da Ciência e Tecnologia de Lula (2004–05), governador de Pernambuco 2007–2014 (reeleito com 82%), presidente nacional do PSB; candidato à Presidência em 2014, morreu em acidente aéreo durante a campanha.",
  "Why here: PSB governed with Lula, then broke with Dilma in 2013 to run its own candidate — the centre-left as ally-but-not-subordinate of PT.",
  "Por que aqui: o PSB governou com Lula e rompeu com Dilma em 2013 para lançar candidato próprio — a centro-esquerda como aliada, mas não subordinada, do PT."),
 ("left","Dilma Rousseff","PT · RS",
  "Born 1947, Belo Horizonte. Economist, Federal University of Rio Grande do Sul (graduate studies at Unicamp, uncompleted). Member of armed resistance groups (Colina, VAR-Palmares), imprisoned and tortured 1970–72. PDT until 2001, then PT. Minister of Mines and Energy 2003–05, Chief of Staff 2005–10, president 2011–16, removed by impeachment in 2016.",
  "Nascida em 1947, Belo Horizonte. Economista pela UFRGS (pós-graduação na Unicamp, não concluída). Militante de organizações da luta armada (Colina, VAR-Palmares), presa e torturada em 1970–72. No PDT até 2001, depois no PT. Ministra de Minas e Energia 2003–05, ministra-chefe da Casa Civil 2005–10, presidente 2011–16, afastada por impeachment em 2016.",
  "Why here: the PT of the governing years — developmentalist state, income transfers, coalition with the centrão. 'Left' in this era means the party of government, not of protest.",
  "Por que aqui: o PT dos anos de governo — Estado desenvolvimentista, transferência de renda, coalizão com o centrão. 'Esquerda' neste período significa o partido do governo, não o do protesto."),
 ("far_left","Heloísa Helena","PSOL · AL",
  "Born 1962, Pão de Açúcar (AL). Nurse, Federal University of Alagoas, where she taught. City councillor in Maceió, state deputy, senator for Alagoas 2003–2011 (elected by PT); expelled from PT in 2003 for voting against Lula's pension reform and co-founded PSOL in 2004; presidential candidate in 2006 (third, 6.85%). Later in Rede.",
  "Nascida em 1962, Pão de Açúcar (AL). Enfermeira pela UFAL, onde foi professora. Vereadora de Maceió, deputada estadual, senadora por Alagoas 2003–2011 (eleita pelo PT); expulsa do PT em 2003 por votar contra a reforma da previdência de Lula e cofundadora do PSOL em 2004; candidata à Presidência em 2006 (terceira, 6,85%). Depois na Rede.",
  "Why here: PSOL's founding act was the refusal to follow PT into pension reform and coalition with the centrão; Heloísa Helena was its first national face.",
  "Por que aqui: o ato fundador do PSOL foi a recusa em acompanhar o PT na reforma da previdência e na coalizão com o centrão; Heloísa Helena foi seu primeiro rosto nacional."),
],
"2014-2026": POL,
}
def polcards(lang):
    out = ""
    for key, label, govs in ERAS:
        out += f'<h4 style="margin:22px 0 2px;font-size:14px;font-weight:500">{label} <span style="color:#777;font-weight:400">· {govs}</span></h4><div class="pol">'
        for k, name, party, en, pt, wen, wpt in POL_ERA[key]:
            bio, why = (en, wen) if lang == "en" else (pt, wpt)
            out += f'<div class="c" style="border-top-color:{COLOR[k]}"><div class="n">{name}</div><div class="p">{party} · {STR[lang]["spec"][k]}</div><p>{bio}</p><p style="color:#555">{why}</p></div>'
        out += "</div>"
    return out

maptable_en = "<table><tr><th>Party</th><th>Years</th><th>Spectrum</th><th>Note</th></tr>" + "".join(
    f"<tr><td>{r['party']}</td><td>{r['from_year']}–{min(int(r['to_year']),2026)}</td><td>{STR['en']['spec'][r['spectrum']]}</td><td>{r['note']}</td></tr>" for r in mapping) + "</table>"
maptable_pt = "<table><tr><th>Partido</th><th>Anos</th><th>Espectro</th><th>Nota</th></tr>" + "".join(
    f"<tr><td>{r['party']}</td><td>{r['from_year']}–{min(int(r['to_year']),2026)}</td><td>{STR['pt']['spec'][r['spectrum']]}</td><td>{r['note']}</td></tr>" for r in mapping) + "</table>"

EN = f"""
<h2>What this page shows</h2>
<p>The share of seats in the Chamber of Deputies won by parties of each ideological family, at every election since redemocratisation (1990–2026), nationally and for each state's delegation. Below the composition sit the social and economic indicators most often invoked to explain the political shifts, so that the two can be read side by side. The page does not test causation; it lines up series so you can see what moved together and what did not.</p>

<h2>How the spectrum is defined</h2>
<p>Brazil has no official left–right classification of parties, and the parties themselves change position over time: PL was an unremarkable centrão party until Bolsonaro joined it in 2021; PP was Paulo Maluf's hard right in the 1990s and the archetypal centrão party by 2014. So the mapping is by <em>party and period</em>, not by party alone. Seven bins are used:</p>
<table><tr><th>Bin</th><th>Working definition</th><th>Typical members (latest period)</th></tr>
<tr><td>Far right</td><td>Nationalist-authoritarian programme; hostility to the courts and press as institutions; rehabilitation of the military regime; organised around a leader rather than a platform.</td><td>PL (2022–), PSL (2018), PRONA</td></tr>
<tr><td>Right</td><td>Conservative on customs and/or economically liberal, operating inside the institutional consensus.</td><td>Republicanos, Novo, PFL/DEM, PP (to 2010), PR, PSC, PTB (2011–)</td></tr>
<tr><td>Centre-right</td><td>Market-friendly, socially flexible, coalition-driven; the "centrão".</td><td>PSDB, PSD, PP (2011–), União Brasil, Podemos, Solidariedade, PTB (to 2010), PL (to 2006)</td></tr>
<tr><td>Centre</td><td>No stable programme; participates in every governing coalition.</td><td>MDB, Avante, Cidadania, PMN</td></tr>
<tr><td>Centre-left</td><td>Social-democratic origin; governs with PT but keeps distance on fiscal and security policy.</td><td>PSB, PDT, PV, Rede</td></tr>
<tr><td>Left</td><td>Labour- or socialist-origin parties that have governed through broad coalitions.</td><td>PT, PCdoB</td></tr>
<tr><td>Far left</td><td>Anti-capitalist programme; opposes PT governments on economics.</td><td>PSOL (PSTU, PCB, UP have no seats)</td></tr></table>

<h3>What the placement is based on</h3>
<ol>
<li><strong>Expert and legislator surveys.</strong> The Brazilian Legislative Surveys (Timothy Power and Cesar Zucco, run every legislature since 1990) ask deputies to place every party on a 1–10 left–right scale; the 2023 expert survey by Bolognesi, Ribeiro and Codato (<em>Dados</em>) does the same with political scientists for 33 parties. Both consistently order the parties as above, with PSOL and PT at one end, Novo and PL at the other, and MDB closest to the midpoint. The cut-offs between bins are this project's, chosen so that each bin holds parties that actually vote together.</li>
<li><strong>Voting record and coalition behaviour.</strong> Roll-call cohesion in the Chamber and participation in presidential coalitions, which is what the 2024 "GPS Partidário" study uses to place 28 parties. This is what moves PP from right to centre-right after 2010 and PL from right to far right after 2022.</li>
<li><strong>Programme and origin.</strong> Party statutes and founding history, used mainly at the extremes (PSOL's split from PT in 2004; PRONA; the integralist lineage of PRP in 1962).</li>
<li><strong>Press convention.</strong> Poder360, Congresso em Foco and Folha use a three-block version (left / centre / right) that this mapping reproduces when the seven bins are collapsed.</li>
</ol>

<h3>Judgement calls that move the most seats</h3>
<ul>
<li><strong>PL as far right from 2022.</strong> The most consequential call: moving PL to "right" empties the far-right column in 2022 and 2026 and puts the right at 154 and 178 seats. It is kept at the edge because the bloc that votes together after 2022 is PL plus Novo and the evangelical parties, not PL plus the centrão.</li>
<li><strong>PT as left, not centre-left.</strong> Expert surveys place PT near the centre-left after 2002; it is kept one bin further out to preserve the distinction from PSB and PDT, which have social-democratic rather than socialist origins.</li>
<li><strong>PSDB as centre-right from 1994</strong> (it was centre-left in 1988–1990, before governing with PFL).</li>
<li><strong>PP from right to centre-right in 2011</strong>, when it became a centrão party rather than Maluf's PPB; <strong>PTB</strong> moves the other way under Roberto Jefferson.</li>
<li><strong>PPS/Cidadania</strong> from centre-left to centre in 2011.</li>
</ul>

<h3>A politician from each bin, by period</h3>
<p>One figure per family in each of the three periods of the mapping table, chosen for being emblematic of where the party sat <em>at that time</em>, with education and trajectory. Several of them changed bins over their careers (Roberto Freire, Jair Bolsonaro, Fernando Henrique Cardoso's PSDB), which is the point: the mapping follows the party-period, not the person.</p>
<p><a class="btn" href="politicians.html" data-i="pol_more"></a></p>

<h3>Full mapping by period</h3>
<p>State Chamber data covers 1990 to 2026 (TSE via HubPolítico; 1990 and 1994 from the state election pages on Wikipedia, checked against the 503 and 513 seat totals). The national indicator series carry a source per point in <code>data/national/indicadores_nacionais.csv</code>; the state values in <code>data/states/estados_2026.csv</code> are the latest available year, rounded, and the black marker on each chart places that value against the national curve. Per state historical series are not yet loaded; see <code>scripts/fetch_states.py</code>.</p>
<p>Further state values used on the compare page are in <code>data/states/indicadores_estado_extra.csv</code>, one source link per row: religion, fertility, one person households and water network from Censo 2022; Gini, CLT share, women's participation and pay ratio from PNAD Contínua (SIDRA); internet and mobile phone use from PNAD TIC 2025; state GDP growth from IBGE Contas Regionais 2023. Per state presidential results (winner and runner up, both rounds) are in <code>data/states/presidenciais_estado_1989_2026.csv</code>, compiled from Wikipedia results pages, Electoral Geography, the Georgetown Political Database of the Americas and Fundação Ulysses Guimarães, with a few values recalculated from vote counts where sources disagreed.</p>
<p>This is the table the build script applies (<code>data/historical/partido_espectro_por_periodo.csv</code>). Edit it and rebuild to test another convention.</p>
{maptable_en}

<h2>Sources</h2>
<h3>Chamber composition</h3>
<ul>
<li>National totals 1990–2026: TSE results per election; 2026 from the TSE totalisation of 4 October as published by <a href="https://hubpolitico.com.br/eleicoes/2026/apuracao/camara">HubPolítico</a>, <a href="https://www.congressoemfoco.com.br/noticia/122927/nova-camara-veja-os-513-deputados-federais-eleitos-em-2026">Congresso em Foco</a> and <a href="https://www.poder360.com.br/poder-eleicoes-2026/partidos-mais-a-direita-terao-276-deputados-na-camara/">Poder360</a>.</li>
<li>Per state by party, 1990–2026. 1990 and 1994: Portuguese Wikipedia state-election pages, checked against the 503 and 513 seat totals. 1998–2026: HubPolítico result pages (<code>hubpolitico.com.br/eleicoes/{{year}}/apuracao/{{uf}}/deputado-federal</code>), which republish TSE data. All 216 state-elections were checked to sum to the state's seat count. Federations in 2022–2026 are split into their component parties.</li>
<li>1962 Chamber: Schmitt (2000) via <a href="https://jus.com.br/artigos/18962/trajetoria-do-partido-trabalhista-brasileiro-entre-1946-e-1964/3">jus.com.br</a>; Fundação Ulysses Guimarães on the 1965 ARENA/MDB split.</li>
<li>Senate 2023 and 2027: <a href="https://www12.senado.leg.br/radio/1/noticia/2026/10/04/pl-elege-19-senadores-e-tera-a-maior-bancada-do-senado">Agência Senado</a>.</li>
</ul>
<h3>Classification literature</h3>
<ul>
<li>Power, T. &amp; Zucco, C. — Brazilian Legislative Surveys, 1990–2021 (legislator placements, 1–10 scale).</li>
<li>Bolognesi, B., Ribeiro, E. &amp; Codato, A. (2023), "Uma nova classificação ideológica dos partidos políticos brasileiros", <em>Dados</em> 66(2) (expert survey, 33 parties).</li>
<li>"GPS Partidário" (2024) as summarised by the <a href="https://www.braziloffice.org/pt/observatorio-2">Washington Brazil Office</a> (migration, caucus membership, roll calls, coalitions).</li>
<li>Poder360's three-block methodology for 2022 and 2026.</li>
</ul>
<h3>Indicators</h3>
<ul>
<li>Religion: IBGE censuses 1991, 2000, 2010, <a href="https://agenciagov.ebc.com.br/noticias/202506/censo-2022-catolicos-seguem-em-queda-evangelicos-e-sem-religiao-crescem-no-pais">2022</a>.</li>
<li>Internet, mobile, smartphones: ITU, Anatel, Cetic.br TIC Domicílios, <a href="https://datareportal.com/reports/digital-2025-brazil">DataReportal</a>; Facebook and Instagram from Meta ad reach via DataReportal and <a href="https://napoleoncat.com/stats/social-media-users-in-brazil/2025">NapoleonCat</a> (the two sources differ by ~60% because they count different things).</li>
<li>GDP, growth, Gini: World Bank, IBGE Contas Nacionais. HDI and years of schooling: UNDP, Atlas Brasil. Unemployment, informality, CLT, women and family: IBGE PME (to 2011) and PNAD Contínua (2012–). Homicides: Atlas da Violência (IPEA/FBSP). Prisons: Depen/SISDEPEN. Vehicles: Denatran/Senatran. MEI: Receita Federal/Sebrae.</li>
<li>2026 presidential vote by state: TSE via <a href="https://tvtnews.com.br/onde-lula-flavio-bolsonaro-venceram-primeiro-turno/">TVT News</a>.</li>
</ul>
<h3>Education</h3>
<ul>
<li>IDEB, early and final years of primary school and secondary school, all networks, 2005 to 2025: <a href="https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb">Inep, Ideb</a>. State values are the 2025 edition.</li>
<li>Saeb, average proficiency in mathematics and Portuguese (5th grade, 9th grade, final year of secondary), 2011 to 2025: <a href="https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb">Inep, Saeb</a>. Earlier editions are left out because their published averages were not reachable in a comparable form.</li>
<li>Failure, dropout and age-grade distortion, 2015 to 2025, all networks: <a href="https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-escolar">Inep, Censo Escolar</a>, as compiled by the Todos Pela Educação yearbook. 2020 and 2021 are distorted by automatic promotion during the pandemic.</li>
<li>Teachers with adequate training (Inep indicator, group 1), 2015 to 2025, national only: <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais">Inep, Indicadores Educacionais</a>. Teacher effort and the socioeconomic level index (Inse) are published per school, not per state, so they are not charted.</li>
<li>Higher education: gross and adjusted net enrolment rates for ages 18 to 24 (Inep and IBGE PNAD), and the share of institutions (IGC) and courses (CPC) scoring 4 or 5, from Inep releases as reported in the press: <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-fluxo-da-educacao-superior">Inep, higher education indicators</a>. Gaps in the years are years with no published total.</li>
<li>Indicadores da Qualidade na Educação (<a href="https://acaoeducativa.org.br/projeto/indicadores-da-qualidade-na-educacao/">Ação Educativa, Indique</a>; <a href="https://www.unicef.org/brazil/indicadores-da-qualidade-da-educacao">UNICEF</a>) is a participatory self-assessment done school by school, with no national or state figures, so it is cited as a reference and not charted.</li>
</ul>
<h3 data-i="src_h"></h3>
__SRCLIST__
<h3>Caveats</h3>
<ul>
<li>Every row in <code>data/national/indicadores_nacionais.csv</code> carries its source; rows marked <code>approx</code> were rounded from secondary summaries and should be re-pulled before citation.</li>
<li>State indicator columns in <code>estados_2026.csv</code> are latest-available, rounded, and indicative — good for correlations, not for quoting.</li>
<li>Per-state historical indicators and the 1990/1994 state delegations are pending: the IBGE, IPEA and TSE APIs were unreachable from the build environment. <code>scripts/fetch_states.py</code> documents the endpoints.</li>
<li>Unemployment changes methodology in 2012; HDI 2023 comes from UNDP's revised series; 1990 had 503 seats.</li>
</ul>
"""

PT = f"""
<h2>O que esta página mostra</h2>
<p>A participação de cada família ideológica nas cadeiras da Câmara dos Deputados, em todas as eleições desde a redemocratização (1990–2026), no país e em cada bancada estadual. Abaixo da composição ficam os indicadores sociais e econômicos mais usados para explicar as mudanças políticas, para que as duas coisas possam ser lidas lado a lado. A página não testa causalidade; alinha séries para que se veja o que se moveu junto e o que não se moveu.</p>

<h2>Como o espectro é definido</h2>
<p>O Brasil não tem classificação oficial dos partidos no eixo esquerda–direita, e os partidos mudam de posição ao longo do tempo: o PL era um partido comum do centrão até Bolsonaro se filiar em 2021; o PP era a direita dura de Paulo Maluf nos anos 1990 e o partido-símbolo do centrão em 2014. Por isso o mapeamento é por <em>partido e período</em>, não apenas por partido. Usam-se sete faixas:</p>
<table><tr><th>Faixa</th><th>Definição operacional</th><th>Integrantes típicos (período mais recente)</th></tr>
<tr><td>Extrema direita</td><td>Programa nacionalista-autoritário; hostilidade ao Judiciário e à imprensa como instituições; reabilitação do regime militar; organização em torno de um líder, não de um programa.</td><td>PL (2022–), PSL (2018), PRONA</td></tr>
<tr><td>Direita</td><td>Conservadora nos costumes e/ou liberal na economia, operando dentro do consenso institucional.</td><td>Republicanos, Novo, PFL/DEM, PP (até 2010), PR, PSC, PTB (2011–)</td></tr>
<tr><td>Centro-direita</td><td>Pró-mercado, flexível nos costumes, movida por coalizões; o "centrão".</td><td>PSDB, PSD, PP (2011–), União Brasil, Podemos, Solidariedade, PTB (até 2010), PL (até 2006)</td></tr>
<tr><td>Centro</td><td>Sem programa estável; participa de todas as coalizões de governo.</td><td>MDB, Avante, Cidadania, PMN</td></tr>
<tr><td>Centro-esquerda</td><td>Origem social-democrata; governa com o PT mas mantém distância em política fiscal e segurança.</td><td>PSB, PDT, PV, Rede</td></tr>
<tr><td>Esquerda</td><td>Partidos de origem trabalhista ou socialista que governaram por meio de coalizões amplas.</td><td>PT, PCdoB</td></tr>
<tr><td>Extrema esquerda</td><td>Programa anticapitalista; faz oposição aos governos do PT na economia.</td><td>PSOL (PSTU, PCB e UP não têm cadeiras)</td></tr></table>

<h3>Em que se baseia a classificação</h3>
<ol>
<li><strong>Pesquisas com especialistas e parlamentares.</strong> As Brazilian Legislative Surveys (Timothy Power e Cesar Zucco, aplicadas a cada legislatura desde 1990) pedem aos deputados que posicionem cada partido numa escala de 1 a 10; a pesquisa de Bolognesi, Ribeiro e Codato (2023, <em>Dados</em>) faz o mesmo com cientistas políticos para 33 partidos. Ambas ordenam os partidos de forma consistente com a tabela acima, com PSOL e PT numa ponta, Novo e PL na outra, e o MDB mais próximo do ponto médio. Os cortes entre as faixas são deste projeto, escolhidos para que cada faixa reúna partidos que de fato votam juntos.</li>
<li><strong>Votações e comportamento em coalizões.</strong> Coesão nas votações nominais da Câmara e participação nas coalizões presidenciais, que é o que o estudo "GPS Partidário" (2024) usa para posicionar 28 partidos. É isso que move o PP da direita para a centro-direita depois de 2010 e o PL da direita para a extrema direita depois de 2022.</li>
<li><strong>Programa e origem.</strong> Estatutos e história de fundação, usados sobretudo nos extremos (a cisão do PSOL em 2004; o PRONA; a linhagem integralista do PRP em 1962).</li>
<li><strong>Convenção da imprensa.</strong> Poder360, Congresso em Foco e Folha usam uma versão em três blocos (esquerda / centro / direita) que este mapeamento reproduz quando as sete faixas são agregadas.</li>
</ol>

<h3>Decisões que mais movem cadeiras</h3>
<ul>
<li><strong>PL como extrema direita a partir de 2022.</strong> A decisão de maior impacto: mover o PL para "direita" esvazia a coluna da extrema direita em 2022 e 2026 e leva a direita a 154 e 178 cadeiras. Ele é mantido na ponta porque o bloco que vota junto depois de 2022 é PL mais Novo e partidos evangélicos, não PL mais centrão.</li>
<li><strong>PT como esquerda, não centro-esquerda.</strong> As pesquisas com especialistas colocam o PT perto da centro-esquerda depois de 2002; ele é mantido uma faixa mais à esquerda para preservar a distinção em relação a PSB e PDT, de origem social-democrata e não socialista.</li>
<li><strong>PSDB como centro-direita desde 1994</strong> (era centro-esquerda em 1988–1990, antes de governar com o PFL).</li>
<li><strong>PP da direita para a centro-direita em 2011</strong>, quando virou partido do centrão e deixou de ser o PPB de Maluf; o <strong>PTB</strong> faz o caminho inverso sob Roberto Jefferson.</li>
<li><strong>PPS/Cidadania</strong> da centro-esquerda para o centro em 2011.</li>
</ul>

<h3>Um político de cada faixa, por período</h3>
<p>Uma figura por família em cada um dos três períodos da tabela de mapeamento, escolhida por ser emblemática de onde o partido estava <em>naquele momento</em>, com formação e trajetória. Vários mudaram de faixa ao longo da carreira (Roberto Freire, Jair Bolsonaro, o PSDB de Fernando Henrique), e esse é o ponto: o mapeamento segue o partido-período, não a pessoa.</p>
<p><a class="btn" href="politicians.html" data-i="pol_more"></a></p>

<h3>Mapeamento completo por período</h3>
<p>Os dados da Câmara por estado cobrem 1990 a 2026 (TSE via HubPolítico; 1990 e 1994 das páginas das eleições estaduais na Wikipédia, conferidas com os totais de 503 e 513 cadeiras). As séries nacionais de indicadores trazem fonte por ponto em <code>data/national/indicadores_nacionais.csv</code>; os valores estaduais em <code>data/states/estados_2026.csv</code> são do ano mais recente disponível, arredondados, e o marcador preto em cada gráfico posiciona esse valor sobre a curva nacional. Séries históricas por estado ainda não foram carregadas; ver <code>scripts/fetch_states.py</code>.</p>
<p>Os demais valores estaduais usados na página de comparação estão em <code>data/states/indicadores_estado_extra.csv</code>, com um link de fonte por linha: religião, fecundidade, domicílios unipessoais e rede de água do Censo 2022; Gini, participação CLT, participação e razão salarial das mulheres da PNAD Contínua (SIDRA); uso de internet e celular da PNAD TIC 2025; crescimento do PIB estadual das Contas Regionais do IBGE 2023. Os resultados presidenciais por estado (vencedor e segundo colocado, nos dois turnos) estão em <code>data/states/presidenciais_estado_1989_2026.csv</code>, compilados das páginas de resultados da Wikipédia, Electoral Geography, Political Database of the Americas (Georgetown) e Fundação Ulysses Guimarães, com alguns valores recalculados a partir das contagens de votos onde as fontes divergiam.</p>
<p>Esta é a tabela que o script de build aplica (<code>data/historical/partido_espectro_por_periodo.csv</code>). Edite-a e reconstrua a página para testar outra convenção.</p>
{maptable_pt}

<h2>Fontes</h2>
<h3>Composição da Câmara</h3>
<ul>
<li>Totais nacionais 1990–2026: resultados do TSE por eleição; 2026 pela totalização do TSE de 4 de outubro conforme publicada por <a href="https://hubpolitico.com.br/eleicoes/2026/apuracao/camara">HubPolítico</a>, <a href="https://www.congressoemfoco.com.br/noticia/122927/nova-camara-veja-os-513-deputados-federais-eleitos-em-2026">Congresso em Foco</a> e <a href="https://www.poder360.com.br/poder-eleicoes-2026/partidos-mais-a-direita-terao-276-deputados-na-camara/">Poder360</a>.</li>
<li>Por estado e partido, 1990–2026. 1990 e 1994: páginas das eleições estaduais na Wikipédia, conferidas com os totais de 503 e 513 cadeiras. 1998–2026: páginas de resultado do HubPolítico (<code>hubpolitico.com.br/eleicoes/{{ano}}/apuracao/{{uf}}/deputado-federal</code>), que republicam dados do TSE. As 216 combinações estado-eleição foram conferidas contra o número de cadeiras de cada estado. As federações de 2022–2026 foram desagregadas nos partidos componentes.</li>
<li>Câmara de 1962: Schmitt (2000) via <a href="https://jus.com.br/artigos/18962/trajetoria-do-partido-trabalhista-brasileiro-entre-1946-e-1964/3">jus.com.br</a>; Fundação Ulysses Guimarães sobre a divisão ARENA/MDB de 1965.</li>
<li>Senado 2023 e 2027: <a href="https://www12.senado.leg.br/radio/1/noticia/2026/10/04/pl-elege-19-senadores-e-tera-a-maior-bancada-do-senado">Agência Senado</a>.</li>
</ul>
<h3>Literatura de classificação</h3>
<ul>
<li>Power, T. &amp; Zucco, C. — Brazilian Legislative Surveys, 1990–2021 (posicionamento por parlamentares, escala 1–10).</li>
<li>Bolognesi, B., Ribeiro, E. &amp; Codato, A. (2023), "Uma nova classificação ideológica dos partidos políticos brasileiros", <em>Dados</em> 66(2) (pesquisa com especialistas, 33 partidos).</li>
<li>"GPS Partidário" (2024), conforme resumido pelo <a href="https://www.braziloffice.org/pt/observatorio-2">Washington Brazil Office</a> (migração, frentes parlamentares, votações nominais, coalizões).</li>
<li>Metodologia em três blocos do Poder360 para 2022 e 2026.</li>
</ul>
<h3>Indicadores</h3>
<ul>
<li>Religião: Censos IBGE de 1991, 2000, 2010 e <a href="https://agenciagov.ebc.com.br/noticias/202506/censo-2022-catolicos-seguem-em-queda-evangelicos-e-sem-religiao-crescem-no-pais">2022</a>.</li>
<li>Internet, celular, smartphones: UIT, Anatel, Cetic.br TIC Domicílios, <a href="https://datareportal.com/reports/digital-2025-brazil">DataReportal</a>; Facebook e Instagram pelo alcance publicitário da Meta via DataReportal e <a href="https://napoleoncat.com/stats/social-media-users-in-brazil/2025">NapoleonCat</a> (as duas fontes diferem em ~60% porque contam coisas diferentes).</li>
<li>PIB, crescimento, Gini: Banco Mundial, IBGE Contas Nacionais. IDH e anos de estudo: PNUD, Atlas Brasil. Desemprego, informalidade, CLT, mulheres e família: IBGE PME (até 2011) e PNAD Contínua (2012–). Homicídios: Atlas da Violência (IPEA/FBSP). Prisões: Depen/SISDEPEN. Veículos: Denatran/Senatran. MEI: Receita Federal/Sebrae.</li>
<li>Voto presidencial 2026 por estado: TSE via <a href="https://tvtnews.com.br/onde-lula-flavio-bolsonaro-venceram-primeiro-turno/">TVT News</a>.</li>
</ul>
<h3>Educação</h3>
<ul>
<li>IDEB, anos iniciais e finais do fundamental e ensino médio, todas as redes, 2005 a 2025: <a href="https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb">Inep, Ideb</a>. Os valores estaduais são da edição de 2025.</li>
<li>Saeb, proficiência média em matemática e língua portuguesa (5º ano, 9º ano, série final do ensino médio), 2011 a 2025: <a href="https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb">Inep, Saeb</a>. Edições anteriores ficaram de fora porque as médias publicadas não estavam acessíveis de forma comparável.</li>
<li>Reprovação, abandono e distorção idade-série, 2015 a 2025, todas as redes: <a href="https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-escolar">Inep, Censo Escolar</a>, compilados pelo Anuário do Todos Pela Educação. 2020 e 2021 são afetados pela aprovação automática na pandemia.</li>
<li>Docentes com formação adequada (indicador do Inep, grupo 1), 2015 a 2025, apenas nacional: <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais">Inep, Indicadores Educacionais</a>. Esforço docente e o Indicador de Nível Socioeconômico (Inse) são publicados por escola, não por estado, por isso não viraram gráfico.</li>
<li>Ensino superior: taxas bruta e líquida ajustada de matrícula de 18 a 24 anos (Inep e PNAD do IBGE) e a parcela de instituições (IGC) e cursos (CPC) com conceito 4 ou 5, a partir de divulgações do Inep noticiadas na imprensa: <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-fluxo-da-educacao-superior">Inep, indicadores da educação superior</a>. Os anos que faltam são anos sem total publicado.</li>
<li>Indicadores da Qualidade na Educação (<a href="https://acaoeducativa.org.br/projeto/indicadores-da-qualidade-na-educacao/">Ação Educativa, Indique</a>; <a href="https://www.unicef.org/brazil/indicadores-da-qualidade-da-educacao">UNICEF</a>) é uma autoavaliação participativa feita escola por escola, sem números nacionais ou estaduais, por isso aparece como referência e não como gráfico.</li>
</ul>
<h3 data-i="src_h"></h3>
__SRCLIST__
<h3>Ressalvas</h3>
<ul>
<li>Cada linha de <code>data/national/indicadores_nacionais.csv</code> traz sua fonte; linhas marcadas <code>approx</code> foram arredondadas a partir de resumos secundários e devem ser reobtidas antes de citação.</li>
<li>As colunas de indicadores estaduais em <code>estados_2026.csv</code> são o dado mais recente disponível, arredondado e indicativo — servem para correlações, não para citação.</li>
<li>Séries históricas por estado e as bancadas estaduais de 1990/1994 estão pendentes: as APIs do IBGE, IPEA e TSE não eram alcançáveis do ambiente de construção. <code>scripts/fetch_states.py</code> documenta os endpoints.</li>
<li>O desemprego muda de metodologia em 2012; o IDH de 2023 vem da série revisada do PNUD; 1990 teve 503 cadeiras.</li>
</ul>
"""

method = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>(function(){{try{{var q=new URLSearchParams(location.search);var t=q.get('theme'),l=q.get('lang'),h=q.get('house');if(h)localStorage.setItem('house',h);document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');document.documentElement.lang=l==='pt'?'pt':'en';}}catch(e){{}}}})();</script>
{meta("methodology","Methodology")}<style>{CSS}</style></head><body>
{header('method')}
<main class="doc">{CTLS}<div data-lang="en">{nodash(EN,"en")}</div><div data-lang="pt">{nodash(PT,"pt")}</div></main>
<footer class="foot"><a href="https://antonioaurel.github.io/" target="_blank" rel="noopener">antonioaurel.github.io</a></footer>
<script>{I18N_JS}applyStrings();</script></body></html>"""
(ROOT/"methodology.html").write_text(method.replace("__SRCLIST__", SRCLIST), encoding="utf-8")

import sys; sys.path.insert(0, str(ROOT / "scripts")); from politicians_data import P as POLROWS, SOURCES as POLSRC
GOV = {1990:"Collor",1994:"Itamar → FHC",1998:"FHC I → FHC II",2002:"FHC II → Lula",2006:"Lula I → Lula II",2010:"Lula II → Dilma",2014:"Dilma I → Dilma II, Temer",2018:"Temer → Bolsonaro",2022:"Bolsonaro → Lula III",2026:"Lula III → ?"}
def era_of(y): return "1990-1998" if y <= 1998 else ("2002-2010" if y <= 2010 else "2014-2026")
POLDATA = [{"year": y, "era": era_of(y), "spec": k, "name": name, "party": party, "src": POLSRC.get(name, ""), "bio": {"en": nodash(en,"en"), "pt": nodash(pt,"pt")}, "why": {"en": nodash(wen,"en"), "pt": nodash(wpt,"pt")}} for y, k, name, party, en, pt, wen, wpt in POLROWS]
missing = [r["name"] for r in POLDATA if not r["src"]]
if missing: raise SystemExit("no source for: " + ", ".join(missing))
YEARS = sorted({r["year"] for r in POLDATA})
ERAJS = [{"key": k, "label": l, "govs": g} for k, l, g in ERAS]
with open(D/"historical"/"politicos_amostra.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["election","era","spectrum","name","party","source_url","bio_en","bio_pt","why_en","why_pt"])
    for r in POLDATA: w.writerow([r["year"], r["era"], r["spec"], r["name"], r["party"], r["src"], r["bio"]["en"], r["bio"]["pt"], r["why"]["en"], r["why"]["pt"]])
pol_page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>(function(){{try{{var q=new URLSearchParams(location.search);var t=q.get('theme'),l=q.get('lang'),h=q.get('house');if(h)localStorage.setItem('house',h);document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');document.documentElement.lang=l==='pt'?'pt':'en';}}catch(e){{}}}})();</script>
{meta("politicians","Politicians sample by spectrum")}<style>{CSS}
.chips{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}.chip{{font-size:12px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--bg);cursor:pointer;color:var(--ink)}}.chip.on{{background:var(--acc);color:#fff;border-color:var(--acc)}}
.chip .dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}}
.filters{{display:grid;gap:10px;background:var(--card);padding:12px 14px;border-radius:10px;margin:12px 0 18px;font-size:13px;color:var(--ink);text-align:center}}.filters input{{font-size:13px;padding:6px 8px;width:100%;max-width:420px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}}.filters .chips{{justify-content:center}}.filters>div>div[style]{{justify-content:center}}
.erah{{margin:22px 0 4px;font-size:14px;font-weight:500}}.erah span{{color:#777;font-weight:400}}
</style></head><body>
{header('politicians')}
<main class="doc" style="max-width:1200px">{CTLS}
<h2 data-i="pol_h"></h2><p class="cap" data-i="pol_intro"></p>
<div class="filters">
<div><strong data-i="f_year"></strong><div class="chips" id="year-chips"></div></div>
<div><strong data-i="f_era"></strong><div class="chips" id="era-chips"></div></div>
<div><strong data-i="f_spec"></strong><div class="chips" id="spec-chips"></div></div>
<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center"><input id="q" type="search"><button class="btn" id="clear" data-i="f_clear"></button><span id="count" class="cap"></span></div>
</div>
<div id="list"></div>
</main>
<footer class="foot"><a href="https://antonioaurel.github.io/" target="_blank" rel="noopener">antonioaurel.github.io</a></footer>
<script>{I18N_JS}
const POL={json.dumps(POLDATA, ensure_ascii=False)},ERAS={json.dumps(ERAJS, ensure_ascii=False)},YEARS={json.dumps(YEARS)},GOV={json.dumps(GOV, ensure_ascii=False)};
const F={{year:new Set(),era:new Set(),spec:new Set(),q:''}};
function chip(host,items,set,color){{host.innerHTML='';const all=document.createElement('button');all.className='chip'+(set.size?'':' on');all.textContent=T('f_all');all.onclick=()=>{{set.clear();draw()}};host.appendChild(all);
 items.forEach(it=>{{const b=document.createElement('button');b.className='chip'+(set.has(it.key)?' on':'');b.innerHTML=(color?'<span class="dot" style="background:'+COLOR[it.key]+'"></span>':'')+it.label;b.onclick=()=>{{set.has(it.key)?set.delete(it.key):set.add(it.key);draw()}};host.appendChild(b)}});}}
function draw(){{chip(document.getElementById('year-chips'),YEARS.map(y=>({{key:y,label:String(y)}})),F.year,false);chip(document.getElementById('era-chips'),ERAS.map(e=>({{key:e.key,label:e.key.split('-').join(LANG==='pt'?' a ':' to ')}})),F.era,false);
 chip(document.getElementById('spec-chips'),SPEC.map(k=>({{key:k,label:T('spec')[k]}})),F.spec,true);
 const q=F.q.toLowerCase();let n=0,h='';
 YEARS.forEach(y=>{{if(F.year.size&&!F.year.has(y))return;const rows=POL.filter(p=>p.year===y&&(!F.era.size||F.era.has(p.era))&&(!F.spec.size||F.spec.has(p.spec))&&(!q||(p.name+' '+p.party+' '+p.bio[LANG]+' '+p.why[LANG]).toLowerCase().includes(q)));
  if(!rows.length)return;n+=rows.length;h+='<div class="erah">'+y+' <span>· '+GOV[y]+'</span></div><div class="pol">'+rows.sort((a,b)=>SPEC.indexOf(a.spec)-SPEC.indexOf(b.spec)).map(p=>'<div class="c" style="border-top-color:'+COLOR[p.spec]+'"><div class="n">'+p.name+'</div><div class="p">'+p.party+' · '+T('spec')[p.spec]+'</div><p>'+p.bio[LANG]+'</p><p style="color:#555">'+p.why[LANG]+'</p><p style="margin:4px 0 0"><a href="'+p.src+'" target="_blank" rel="noopener" style="font-size:12px;color:#2a78d6;text-decoration:none">'+T('src')+' ↗</a></p></div>').join('')+'</div>'}});
 document.getElementById('list').innerHTML=h||'<p class="cap">—</p>';document.getElementById('count').textContent=T('f_count').replace('{{n}}',n).replace('{{t}}',POL.length);
 document.getElementById('q').placeholder=T('f_text');}}
document.getElementById('q').addEventListener('input',e=>{{F.q=e.target.value;draw()}});
document.getElementById('clear').onclick=()=>{{F.year.clear();F.era.clear();F.spec.clear();F.q='';document.getElementById('q').value='';draw()}};
function render(){{draw()}}
applyStrings();draw();
</script></body></html>"""
(ROOT/"politicians.html").write_text(pol_page, encoding="utf-8")
print("wrote politicians.html", len(pol_page)//1024, "KB")
print("wrote methodology.html", len(method)//1024, "KB")

CMP_JS = r"""
const COMP={camara:__COMP__,senado:__SENCOMP__},GOVS=__GOVS__,STATES=__STATES__,BR_REF=__BRREF__,UNIT=__UNIT__,NATL=__NATL__,EXTRA=__EXTRA__,PRES=__PRES__,PRES_ST=__PRESST__;let PEL='all',PRD=1;try{const q=JSON.parse(localStorage.getItem('cmpres')||'{}');if(q.e)PEL=q.e;if(q.r)PRD=q.r}catch(e){}
const YEARS=['1990','1994','1998','2002','2006','2010','2014','2018','2022','2026'];
let HOUSE='camara',SIDE={a:'PE',b:'BA'},OSPEC='far_right',charts={};
try{const s=JSON.parse(localStorage.getItem('cmp')||'{}');if(s.a)SIDE.a=s.a;if(s.b)SIDE.b=s.b;if(s.o)OSPEC=s.o;HOUSE=new URLSearchParams(location.search).get('house')||localStorage.getItem('house')||'camara'}catch(e){}
function save(){try{localStorage.setItem('cmp',JSON.stringify({a:SIDE.a,b:SIDE.b,o:OSPEC}));localStorage.setItem('house',HOUSE)}catch(e){}}
function fade(hex,a){const n=parseInt(hex.slice(1),16);return 'rgba('+(n>>16)+','+((n>>8)&255)+','+(n&255)+','+a+')'}
const ALPHA={a:1,b:.5};
function ink(){return getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()}
function mut(){return getComputedStyle(document.documentElement).getPropertyValue('--mut').trim()}
function grid(){return getComputedStyle(document.documentElement).getPropertyValue('--grid').trim()}
function nm(k){return k==='BR'?T('brazil'):UFNAME[k]}
function opts(cur){return '<option value="BR">'+T('brazil')+'</option>'+Object.keys(UFNAME).sort((a,b)=>UFNAME[a].localeCompare(UFNAME[b])).map(u=>'<option value="'+u+'"'+(u===cur?' selected':'')+'>'+UFNAME[u]+' ('+u+')</option>').join('')}
function kill(id){if(charts[id]){charts[id].destroy();delete charts[id]}}
function series(k){const c=COMP[HOUSE][k]||{};return YEARS.map(y=>c[y]?c[y]:null)}
const govPlugin={id:'gov',afterDatasetsDraw(c,a,o){const y=c.scales.y,ctx=c.ctx;c.data.labels.forEach((lab,i)=>{const g=(GOVS[o.k]||{})[lab];if(!g)return;const py=y.getPixelForValue(i);ctx.save();ctx.beginPath();ctx.arc(c.chartArea.left-52,py,5,0,Math.PI*2);if(g.spec){ctx.fillStyle=COLOR[g.spec];ctx.fill()}else{ctx.strokeStyle=mut();ctx.setLineDash([2,2]);ctx.stroke()}ctx.restore()})}};
function drawSide(s){const k=SIDE[s];const ser=series(k);
 const al=ALPHA[s];const ds=[...SPEC].reverse().map(sp=>({label:T('spec')[sp],backgroundColor:fade(COLOR[sp],al),borderColor:fade(COLOR[sp],Math.max(al,.7)),borderDash:s==='b'?[5,3]:[],seats:ser.map(r=>r?r[sp]:null),data:ser.map(r=>r&&r.total?+(r[sp]/r.total*100).toFixed(1):null)}));
 const tip={callbacks:{label:t=>t.dataset.label+': '+(t.dataset.seats[t.dataIndex]??'')+' '+T('seats')+' ('+t.raw+'%)'}};
 kill('bar_'+s);kill('line_'+s);
 charts['bar_'+s]=new Chart(document.getElementById('bar_'+s),{type:'bar',data:{labels:YEARS,datasets:ds.map(d=>({...d,barThickness:18}))},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:{left:34}},plugins:{legend:{display:false},tooltip:tip,gov:{k}},scales:{x:{stacked:true,min:0,max:100,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}},y:{stacked:true,ticks:{color:ink()},grid:{display:false}}}},plugins:[govPlugin]});
 charts['line_'+s]=new Chart(document.getElementById('line_'+s),{type:'line',data:{labels:YEARS,datasets:ds.map(d=>({...d,fill:false,tension:.25,pointRadius:3,spanGaps:false}))},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{display:false},tooltip:tip},scales:{x:{ticks:{color:mut()},grid:{display:false}},y:{min:0,max:100,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}}}}});
 document.getElementById('title_'+s).textContent=nm(k);}
function drawOverlay(){kill('ov');const mk=k=>{const ser=series(k);return ser.map(r=>r&&r.total?+(r[OSPEC]/r.total*100).toFixed(1):null)};
 const ds=[{label:nm(SIDE.a),data:mk(SIDE.a),borderColor:'#2a78d6',backgroundColor:'#2a78d6',borderWidth:2.5,pointRadius:4,tension:.25},{label:nm(SIDE.b),data:mk(SIDE.b),borderColor:'#eb6834',backgroundColor:'#eb6834',borderWidth:2.5,pointRadius:4,tension:.25,borderDash:[6,4]}];
 if(SIDE.a!=='BR'&&SIDE.b!=='BR'){const br=COMP[HOUSE].BR||{};ds.push({label:T('brazil'),data:YEARS.map(y=>br[y]&&br[y].total?+(br[y][OSPEC]/br[y].total*100).toFixed(1):null),borderColor:mut(),backgroundColor:mut(),borderWidth:1.5,pointRadius:2,borderDash:[2,3],tension:.25})}
 charts.ov=new Chart(document.getElementById('ov'),{type:'line',data:{labels:YEARS,datasets:ds},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{color:ink(),usePointStyle:true}},tooltip:{callbacks:{label:t=>t.dataset.label+': '+(t.raw==null?T('nodata'):t.raw+'%')}}},scales:{x:{ticks:{color:mut()},grid:{display:false}},y:{min:0,max:100,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}}}}});
 document.getElementById('ospec').innerHTML=SPEC.map(sp=>'<button class="chip'+(sp===OSPEC?' on':'')+'" onclick="OSPEC=\''+sp+'\';save();drawOverlay()"><span class="dot" style="background:'+COLOR[sp]+'"></span>'+T('spec')[sp]+'</button>').join('');}
const IND=['flavio_pct_1st_round','lula_pct_1st_round','gdp_per_capita_brl_thousands','hdi','unemployment_pct','informal_pct','years_schooling','homicides_per_100k','prisoners_per_100k','evangelical_pct','internet_households_pct','vehicles_per_100','female_headed_households_pct','sewage_network_pct','population_millions'].concat(Object.keys(EXTRA));
function val(k,ind){if(EXTRA[ind]){const v=EXTRA[ind].v[k];return v==null?null:v}if(k==='BR')return BR_REF[ind]??null;const r=STATES.find(s=>s.uf===k);return r?+r[ind]:null}
function drawInd(){const host=document.getElementById('ind');host.innerHTML='';IND.forEach(ind=>{kill('i_'+ind)});
 const names=[nm(SIDE.a),nm(SIDE.b)];const showBR=SIDE.a!=='BR'&&SIDE.b!=='BR';if(showBR)names.push(T('brazil'));
 IND.forEach(ind=>{const nat=null;if(nat){host.insertAdjacentHTML('beforeend','<div><h3>'+T('series')[ind]+' <span class="cap" style="display:inline">('+T('nat_only')+', '+nat.y+')</span></h3><div class="wrap" style="height:56px"><canvas id="i_'+ind+'"></canvas></div></div>');charts['i_'+ind]=new Chart(document.getElementById('i_'+ind),{type:'bar',data:{labels:[T('brazil')],datasets:[{data:[nat.v],backgroundColor:[mut()],barThickness:16,borderRadius:3}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{beginAtZero:true,grace:'18%',ticks:{color:mut()},grid:{color:grid()}},y:{ticks:{color:ink()},grid:{display:false}}}},plugins:[{id:'v',afterDatasetsDraw(c){const ctx=c.ctx;ctx.save();ctx.font='11px sans-serif';ctx.fillStyle=ink();c.getDatasetMeta(0).data.forEach(b=>ctx.fillText(nat.v,b.x+6,b.y+4));ctx.restore()}}]});return}
  const label=EXTRA[ind]?(T('cards')[ind]||T('series')[ind])+' <span class="cap" style="display:inline">('+EXTRA[ind].y+')</span>':(T('cards')[ind]||ind);const U=EXTRA[ind]?EXTRA[ind].u:(UNIT[ind]||'');host.insertAdjacentHTML('beforeend','<div><h3>'+label+'</h3><div class="wrap" style="height:'+(showBR?120:96)+'px"><canvas id="i_'+ind+'"></canvas></div></div>');
  const vals=[val(SIDE.a,ind),val(SIDE.b,ind)];if(showBR)vals.push(val('BR',ind));const cols=['#2a78d6','#eb6834',mut()];
  charts['i_'+ind]=new Chart(document.getElementById('i_'+ind),{type:'bar',data:{labels:names,datasets:[{data:vals,backgroundColor:cols.slice(0,vals.length),barThickness:16,borderRadius:3}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:t=>(t.raw==null?T('nodata'):t.raw+U)}}},scales:{x:{beginAtZero:true,grace:'18%',ticks:{color:mut()},grid:{color:grid()}},y:{ticks:{color:ink()},grid:{display:false}}}},plugins:[{id:'v',afterDatasetsDraw(c){const ctx=c.ctx;ctx.save();ctx.font='11px sans-serif';ctx.fillStyle=ink();c.getDatasetMeta(0).data.forEach((b,i)=>{const v=vals[i];ctx.fillText(v==null?T('nodata'):v+U,b.x+6,b.y+4)});ctx.restore()}}]});});}
let presc;
function pv(k,y){if(k==='BR'){const p=PRES.find(q=>q.y===y);return [p.w1,p.r1,p.w2,p.r2]}return (PRES_ST[y]||{})[k]||[null,null,null,null]}
function drawPresCmp(){const ys=PRES.map(p=>p.y);const sel=document.getElementById('pel');sel.innerHTML='<option value="all">'+T('all_el')+'</option>'+ys.map(y=>'<option'+(y===PEL?' selected':'')+'>'+y+'</option>').join('');if(PEL==='all')sel.value='all';
 document.getElementById('prd').innerHTML=[1,2].map(r=>'<button class="chip'+(r===PRD?' on':'')+'" onclick="PRD='+r+';savePres();drawPresCmp()">'+T(r===1?'round1':'round2')+'</button>').join('');
 const places=[SIDE.a,SIDE.b];if(SIDE.a!=='BR'&&SIDE.b!=='BR')places.push('BR');const cols=['#2a78d6','#eb6834',mut()];
 const list=PRES.filter(p=>PEL==='all'||p.y===PEL);const iw=PRD===1?0:2;
 const dot=sp=>'<span class="gov" style="background:'+COLOR[sp]+'"></span>';
 const cell=(v,o,c,p)=>{if(PRD===2&&v==null)return '<td style="color:var(--mut)">'+(p.pending?T('pending_run'):T('no_run'))+'</td>';if(v==null)return '<td style="color:var(--mut)">'+T('nodata')+'</td>';const win=o!=null&&v>o;return '<td style="color:'+c+(win?';font-weight:700':'')+'">'+v.toFixed(1)+'%</td>'};
 let h='<div class="tw"><table><tr><th rowspan="2">'+T('election')+'</th><th colspan="'+places.length+'">'+T('winner')+'</th><th colspan="'+places.length+'">'+T('runner')+'</th></tr><tr>'+places.map((k,i)=>'<th style="color:'+cols[i]+'">'+(k==='BR'?T('brazil'):k)+'</th>').join('')+places.map((k,i)=>'<th style="color:'+cols[i]+'">'+(k==='BR'?T('brazil'):k)+'</th>').join('')+'</tr>';
 list.forEach(p=>{const V=places.map(k=>pv(k,p.y));h+='<tr><td><b>'+p.y+'</b></td>';
  h+=V.map((v,i)=>cell(v[iw],v[iw+1],cols[i],p)).join('').replace('<td','<td title="'+p.w+'"');
  h+=V.map((v,i)=>cell(v[iw+1],v[iw],cols[i],p)).join('');h+='</tr><tr class="pn"><td></td><td colspan="'+places.length+'" style="font-size:12px">'+dot(p.ws)+p.w+' ('+p.wp+')</td><td colspan="'+places.length+'" style="font-size:12px">'+dot(p.rs)+p.r+' ('+p.rp+')</td></tr>'});
 document.getElementById('prestab').innerHTML=h+'</table></div>';drawMPres(list,iw,places,cols);
 kill('presc');const L=list.map(p=>p.y);
 charts.presc=new Chart(document.getElementById('presc'),{type:'bar',data:{labels:L,datasets:places.map((k,i)=>({label:(k==='BR'?T('brazil'):nm(k)),data:list.map(p=>pv(k,p.y)[iw]),backgroundColor:cols[i],borderRadius:3,maxBarThickness:28}))},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:ink()}},tooltip:{callbacks:{title:t=>{const p=list[t[0].dataIndex];return p.y+' · '+p.w},label:t=>t.dataset.label+': '+(t.raw==null?(PRD===2?T('no_run'):T('nodata')):t.raw+'%')}}},scales:{x:{ticks:{color:mut()},grid:{display:false}},y:{min:0,max:100,title:{display:true,text:T('win_share'),color:mut()},ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}}}}});}
function savePres(){try{localStorage.setItem('cmpres',JSON.stringify({e:PEL,r:PRD}))}catch(e){}}
const SECS=['seat','traj','ov','ind','pres'];let MSEC={seat:1,traj:0,ov:1,ind:0,pres:1};try{Object.assign(MSEC,JSON.parse(localStorage.getItem('cmpsec')||'{}'))}catch(e){}
function applySecs(){SECS.forEach(k=>document.body.classList.toggle('off-'+k,!MSEC[k]));document.getElementById('secs').innerHTML=SECS.map(k=>'<button class="chip'+(MSEC[k]?' on':'')+'" onclick="MSEC.'+k+'=MSEC.'+k+'?0:1;try{localStorage.setItem(\'cmpsec\',JSON.stringify(MSEC))}catch(e){};applySecs()">'+T('sec_'+k)+'</button>').join('');}
function mbarRow(k,side,y){const r=(COMP[HOUSE][k]||{})[y];const g=(GOVS[k]||{})[y];const al=ALPHA[side];
 const dot='<span class="gdot'+(g&&!g.spec?' pend':'')+'" style="background:'+(g&&g.spec?COLOR[g.spec]:'transparent')+'"></span>';
 let bar='';if(r&&r.total){[...SPEC].reverse().forEach(sp=>{const v=r[sp]||0;if(!v)return;const pc=v/r.total*100;bar+='<span style="width:'+pc+'%;background:'+fade(COLOR[sp],al)+'">'+(pc>=9?Math.round(pc):'')+'</span>'})}else bar='<span style="width:100%;color:var(--mut)">'+T('nodata')+'</span>';
 return '<div class="mrow"><span class="mlab" style="color:'+(side==='a'?'#2a78d6':'#eb6834')+'">'+k+'</span>'+dot+'<div class="mbar">'+bar+'</div></div>'}
function drawMBars(){let h='';YEARS.forEach(y=>{h+='<div class="my">'+y+'</div>'+mbarRow(SIDE.a,'a',y)+mbarRow(SIDE.b,'b',y)});document.getElementById('mbars').innerHTML=h;
 ['a','b'].forEach(s=>{document.getElementById('msel_'+s).innerHTML=opts(SIDE[s])});}
function drawMPres(list,iw,places,cols){const dot=sp=>'<span class="gdot" style="display:inline-block;background:'+COLOR[sp]+'"></span> ';
 let h='';list.forEach(p=>{const V=places.map(k=>pv(k,p.y));h+='<div class="mpb"><div class="mph"><b>'+p.y+'</b> · '+dot(p.ws)+p.w+' <span style="color:var(--mut)">('+p.wp+')</span> vs '+dot(p.rs)+p.r+' <span style="color:var(--mut)">('+p.rp+')</span></div>';
  if(PRD===2&&V.every(v=>v[2]==null)){h+='<div class="mpg">'+(p.pending?T('pending_run'):T('no_run'))+'</div></div>';return}
  [[T('winner')+' · '+p.w,0],[T('runner')+' · '+p.r,1]].forEach(([lab,o])=>{h+='<div class="mpg">'+lab+'</div>';V.forEach((v,i)=>{const a=v[iw+o],b=v[iw+1-o];const k=places[i];h+='<div class="mpr'+(a!=null&&b!=null&&a>b?' win':'')+'"><span class="lab" style="color:'+cols[i]+'">'+(k==='BR'?T('brazil'):k)+'</span><span class="tr"><i style="width:'+(a||0)+'%;background:'+cols[i]+(o?';opacity:.55':'')+'"></i></span><span class="v">'+(a==null?'':a.toFixed(1)+'%')+'</span></div>'})});h+='</div>'});
 document.getElementById('mpres').innerHTML=h}
function syncSel(s,v){SIDE[s]=v;save();document.getElementById('sel_'+s).value=v;drawSide(s);drawOverlay();drawInd();drawPresCmp();drawMBars()}
document.getElementById('msel_a').addEventListener('change',e=>syncSel('a',e.target.value));
document.getElementById('msel_b').addEventListener('change',e=>syncSel('b',e.target.value));
function render(force){document.getElementById('sel_a').innerHTML=opts(SIDE.a);document.getElementById('sel_b').innerHTML=opts(SIDE.b);
 document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.h===HOUSE));
 document.getElementById('speclg').innerHTML=[...SPEC].reverse().map(k=>'<span><span class="sw" style="background:'+COLOR[k]+'"></span>'+T('spec')[k]+'</span>').join('');
 drawSide('a');drawSide('b');drawOverlay();drawInd();drawPresCmp();drawMBars();applySecs();}
document.getElementById('pel').addEventListener('change',e=>{PEL=e.target.value;savePres();drawPresCmp()});
function setHouse(h){HOUSE=h;save();drawSide('a');drawSide('b');drawOverlay();drawMBars();document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.h===HOUSE));}
document.getElementById('sel_a').addEventListener('change',e=>{SIDE.a=e.target.value;save();drawSide('a');drawOverlay();drawInd();drawPresCmp();drawMBars()});
document.getElementById('sel_b').addEventListener('change',e=>{SIDE.b=e.target.value;save();drawSide('b');drawOverlay();drawInd();drawPresCmp();drawMBars()});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>{if(THEME==='auto')render(true)});
applyStrings();render(true);
"""
def _cfill(js):
    for k,v in {"__COMP__":comp,"__SENCOMP__":sen_comp,"__GOVS__":govs,"__STATES__":states,"__BRREF__":BR_REF,"__UNIT__":UNIT,"__NATL__":NATL,"__EXTRA__":EXTRA,"__PRES__":pres,"__PRESST__":PRES_ST}.items():
        js=js.replace(k,json.dumps(v,ensure_ascii=False))
    return js
_statecovered = {"evangelical","internet_households","hdi","unemployment","years_schooling","prisoners_rate","homicide_rate","female_headed_households","vehicles_per_100","informal_share","sewage_network","gdp_per_capita"}
BR_REF["population_millions"] = round(sum(float(r["population_millions"]) for r in states), 1)
if "sewage_network" in nat: BR_REF["sewage_network_pct"] = nat["sewage_network"][-1]["y"]
UNIT["sewage_network_pct"] = "%"
NATL = {k: {"v": v[-1]["y"], "y": v[-1]["x"]} for k, v in nat.items() if k not in _statecovered and k in STR["en"]["series"] and k not in ("prisoners","vehicle_fleet","motorcycles","clt_employees","employees_no_contract","self_employed")}
EXTRA_MAP = {**{k:k for k in ["ideb_ef_iniciais","ideb_ef_finais","ideb_em","saeb_mt_5","saeb_mt_9","saeb_mt_em","saeb_lp_5","saeb_lp_9","saeb_lp_em","taxa_reprovacao_em","taxa_abandono_em","taxa_reprovacao_ef_af","taxa_abandono_ef_af","distorcao_ef_af","distorcao_em"]},"catholic_pct":"catholic","no_religion_pct":"no_religion","fertility_rate":"fertility_rate","one_person_households_pct":"one_person_households","water_network_pct":"water_network","gini":"gini","gdp_growth_pct":"gdp_growth","clt_share_pct":"clt_share","female_participation_pct":"female_participation","women_pay_ratio_pct":"women_pay_ratio","internet_individuals_pct":"internet_individuals","smartphone_users_pct":"smartphone_users"}
EXTRA = {}
for r in rows(D/"states"/"indicadores_estado_extra.csv"):
    k = EXTRA_MAP[r["indicator"]]
    e = EXTRA.setdefault(k, {"y": r["year"], "v": {}, "u": "%" if (r["indicator"].endswith("_pct") or r["indicator"].startswith(("taxa_","distorcao_"))) else ""})
    e["v"][r["uf"]] = float(r["value"])
_ord = [k for v in PANELS.values() for k, _ in v[0]]
EXTRA = {k: EXTRA[k] for k in sorted(EXTRA, key=lambda k: _ord.index(k) if k in _ord else 999)}
PRES_ST = {}
for r in rows(D/"states"/"presidenciais_estado_1989_2026.csv"):
    f = lambda x: float(x) if x else None
    PRES_ST.setdefault(r["election"], {})[r["uf"]] = [f(r["winner_1st_pct"]), f(r["runner_up_1st_pct"]), f(r["winner_2nd_pct"]), f(r["runner_up_2nd_pct"])]
CMP_CSS = ".monly{display:none}.mctl{text-align:center;margin:6px 0 4px}.msel{display:flex;gap:8px;justify-content:center;margin-bottom:10px}.msel label{flex:1;min-width:0;font-weight:600}.msel select{width:100%;margin-top:4px}.msel .ma{color:#2a78d6}.msel .mb{color:#eb6834}.mctl .chips{justify-content:center;margin-top:6px}"\
 ".my{margin:10px 0 2px;font-size:12px;font-weight:700;text-align:left}.mrow{display:flex;align-items:center;gap:6px;margin:2px 0}.mlab{width:26px;font-size:11px;font-weight:700;text-align:right}.gdot{width:9px;height:9px;border-radius:50%;flex:none}.gdot.pend{border:1px dashed var(--mut)}.mbar{flex:1;display:flex;height:20px;border-radius:3px;overflow:hidden;background:var(--card)}.mbar span{display:flex;align-items:center;justify-content:center;font-size:9px;color:#111;white-space:nowrap;overflow:hidden}"\
 ".mpb{border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:10px 0;text-align:left}.mph{font-size:13px;margin-bottom:4px}.mpg{font-size:11px;color:var(--mut);margin:6px 0 2px}.mpr{display:flex;align-items:center;gap:6px;margin:2px 0;font-size:12px}.mpr .lab{width:64px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.mpr .tr{flex:1;height:12px;background:var(--card);border-radius:3px;overflow:hidden}.mpr .tr i{display:block;height:100%}.mpr .v{width:44px;text-align:right}.mpr.win .v,.mpr.win .lab{font-weight:700}"\
 "@media (max-width:720px){.monly{display:block}.chips.monly{display:flex}.donly,.dbars,.side .dsel{display:none!important}.cmp2{grid-template-columns:minmax(0,1fr)}body.off-seat [data-sec=seat],body.off-traj [data-sec=traj],body.off-ov [data-sec=ov],body.off-ind [data-sec=ind],body.off-pres [data-sec=pres]{display:none!important}}"\
 ".cmp2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 36px}.side.sa{border-top:5px solid #2a78d6;border-radius:6px 6px 0 0;padding-top:8px}.side.sb{border-top:5px solid #eb6834;border-radius:6px 6px 0 0;padding-top:8px;background:linear-gradient(var(--card),transparent 160px)}.side.sa h2{color:#2a78d6}#prestab table{margin:0 auto}#prestab td,#prestab th{text-align:center}#prestab tr.pn td{border-top:none;padding-top:0;color:var(--mut)}.side.sb h2{color:#eb6834}.cmp2>div{min-width:0}.side h2{margin:0 0 6px}.side select{font-size:15px;padding:6px 10px;width:100%;max-width:340px}.chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}.chip{font-size:12px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--bg);cursor:pointer;color:var(--ink)}.chip.on{background:var(--acc);color:#fff;border-color:var(--acc)}.chip .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}#ind{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 36px}@media (max-width:900px){.cmp2,#ind{grid-template-columns:minmax(0,1fr)}.cmp2>div+div{border-top:1px solid var(--line);padding-top:18px;margin-top:18px}}"
compare = f"""<!doctype html><html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>(function(){{try{{var q=new URLSearchParams(location.search);var t=q.get('theme'),l=q.get('lang'),h=q.get('house');if(h)localStorage.setItem('house',h);document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');document.documentElement.lang=l==='pt'?'pt':'en';}}catch(e){{}}}})();</script>
{meta("compare","Compare states (and Brazil)")}<script src="assets/chart.umd.js"></script><style>{CSS}{CMP_CSS}</style></head><body>
{header('compare')}
<main>
{CTLS}
<div class="intro" style="text-align:center"><strong data-i="cmp_h"></strong><br><span data-i="cmp_intro"></span></div>
<div class="tabs" style="justify-content:center"><button class="tab" data-h="camara" onclick="setHouse('camara')" data-i="tab_camara"></button><button class="tab" data-h="senado" onclick="setHouse('senado')" data-i="tab_senado"></button></div>
<div class="lg" id="speclg" style="justify-content:center"></div>
<div class="monly mctl"><div class="msel"><label class="ma">A: <select id="msel_a"></select></label><label class="mb">B: <select id="msel_b"></select></label></div><div class="cap" data-i="show_lbl"></div><div class="chips" id="secs"></div></div>
<section class="sec monly" data-sec="seat" style="border-top:none"><h3 data-i="h_bars"></h3><p class="cap" data-i="how_mbars"></p><div id="mbars"></div></section>
<div class="cmp2" data-sec="traj">
<div class="side sa"><section class="sec" style="border-top:none;padding-top:6px;text-align:center"><label class="dsel"><span data-i="side_a"></span>: <select id="sel_a"></select></label><h2 id="title_a" style="margin-top:12px"></h2>
<div class="dbars"><h3 data-i="h_bars"></h3><p class="cap" data-i="how_bars"></p><div class="wrap" style="height:380px"><canvas id="bar_a"></canvas></div></div>
<h3 data-i="h_lines" style="margin-top:22px"></h3><p class="cap" data-i="how_lines"></p><div class="wrap" style="height:300px"><canvas id="line_a"></canvas></div></section></div>
<div class="side sb"><section class="sec" style="border-top:none;padding-top:6px;text-align:center"><label class="dsel"><span data-i="side_b"></span>: <select id="sel_b"></select></label><h2 id="title_b" style="margin-top:12px"></h2>
<div class="dbars"><h3 data-i="h_bars"></h3><p class="cap" data-i="how_bars"></p><div class="wrap" style="height:380px"><canvas id="bar_b"></canvas></div></div>
<h3 data-i="h_lines" style="margin-top:22px"></h3><p class="cap" data-i="how_lines"></p><div class="wrap" style="height:300px"><canvas id="line_b"></canvas></div></section></div>
</div>
<section class="sec" data-sec="ov" style="text-align:center"><h2 data-i="overlay_h"></h2><p class="cap" data-i="overlay_exp"></p><p class="cap" data-i="how_ov"></p><div class="chips" id="ospec" style="margin:8px 0 12px"></div><div class="wrap" style="height:340px"><canvas id="ov"></canvas></div></section>
<section class="sec" data-sec="ind" style="text-align:center"><h2 data-i="ind_h"></h2><p class="cap" data-i="ind_exp"></p><p class="cap" data-i="how_ind"></p><div id="ind" style="text-align:left"></div></section>
<section class="sec" data-sec="pres" style="text-align:center"><h2 data-i="pres_h"></h2><p class="cap donly" data-i="pres_cmp_exp"></p><p class="cap donly" data-i="how_pres"></p><p class="cap monly" data-i="how_mpres"></p>
<div style="display:flex;gap:12px;justify-content:center;align-items:center;flex-wrap:wrap;margin:8px 0 12px"><label><span data-i="election"></span>: <select id="pel"></select></label><div class="chips" id="prd"></div></div>
<div class="wrap donly" style="height:320px"><canvas id="presc"></canvas></div><div id="prestab" class="donly" style="margin-top:16px"></div><div id="mpres" class="monly"></div></section>
</main>
<footer class="foot"><a href="https://antonioaurel.github.io/" target="_blank" rel="noopener">antonioaurel.github.io</a></footer>
<script>{I18N_JS}</script><script>{_cfill(CMP_JS)}</script></body></html>"""
(ROOT/"compare.html").write_text(compare, encoding="utf-8")

SER_STATECOL = {"evangelical":"evangelical_pct","internet_households":"internet_households_pct","hdi":"hdi","unemployment":"unemployment_pct","years_schooling":"years_schooling","prisoners_rate":"prisoners_per_100k","homicide_rate":"homicides_per_100k","female_headed_households":"female_headed_households_pct","vehicles_per_100":"vehicles_per_100","informal_share":"informal_pct","sewage_network":"sewage_network_pct"}
STVAL = {}
for r in states:
    for k, col in SER_STATECOL.items():
        if r.get(col): STVAL.setdefault(k, {"y": 2024, "v": {}})["v"][r["uf"]] = float(r[col])
for k, e in EXTRA.items():
    STVAL[k] = {"y": int(str(e["y"])[:4]), "v": e["v"]}
EXP_JS = r"""
const COMP={camara:__COMP__,senado:__SENCOMP__},GOVS=__GOVS__,PANELS=__PANELS__,STVAL=__STVAL__;
function ink(){return getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()}
function mut(){return getComputedStyle(document.documentElement).getPropertyValue('--mut').trim()}
function grid(){return getComputedStyle(document.documentElement).getPropertyValue('--grid').trim()}
let PLACE='BR',HOUSE='camara',VIEW='lines',ESPEC=null,PICK=['religion','unemployment'],HY=null,charts={};
try{const q=new URLSearchParams(location.search);HOUSE=q.get('house')||localStorage.getItem('house')||'camara';const e=JSON.parse(localStorage.getItem('exp')||'{}');if(e.p)PLACE=e.p;if(Array.isArray(e.s))ESPEC=e.s;if(Array.isArray(e.k))PICK=e.k.filter(k=>PANELS[k]).slice(0,2)}catch(e){}
function save(){try{localStorage.setItem('exp',JSON.stringify({p:PLACE,k:PICK,s:ESPEC}));localStorage.setItem('house',HOUSE)}catch(e){}}
function nm(k){return k==='BR'?T('brazil'):UFNAME[k]}
const EY=[1990,1994,1998,2002,2006,2010,2014,2018,2022,2026];const X={type:'linear',min:1988,max:2028,afterBuildTicks:a=>{a.ticks=EY.map(v=>({value:v}))},ticks:{color:()=>mut(),autoSkip:false,maxRotation:0,font:{size:10},callback:v=>(innerWidth<640&&EY.indexOf(v)%2)?'':String(v)},grid:{display:false}};
const YW=s=>{s.width=46};
const sync={id:'sync',afterDraw(c){if(HY==null)return;const x=c.scales.x.getPixelForValue(HY),a=c.chartArea;if(x<a.left||x>a.right)return;const ctx=c.ctx;ctx.save();ctx.strokeStyle=mut();ctx.setLineDash([3,3]);ctx.beginPath();ctx.moveTo(x,a.top);ctx.lineTo(x,a.bottom);ctx.stroke();ctx.fillStyle=ink();ctx.font='11px sans-serif';ctx.fillText(Math.round(HY),x+4,a.top+10);ctx.restore()}};
function hover(e,els,c){const v=c.scales.x.getValueForPixel(e.x);const n=v==null?null:Math.round(v);if(n!==HY){HY=n;Object.values(charts).forEach(ch=>ch.draw())}}
document.addEventListener('mouseleave',()=>{HY=null;Object.values(charts).forEach(ch=>ch.draw())});
function kill(id){if(charts[id]){charts[id].destroy();delete charts[id]}}
const govDots={id:'govd',afterDatasetsDraw(c){const g=GOVS[PLACE]||{};const y=c.scales.y.getPixelForValue(VIEW==='bars'?100:c.scales.y.max);Object.keys(g).forEach(yr=>{const o=g[yr];const x=c.scales.x.getPixelForValue(+yr);const ctx=c.ctx;ctx.save();ctx.beginPath();ctx.arc(x,y-9,5,0,Math.PI*2);if(o.spec){ctx.fillStyle=COLOR[o.spec];ctx.fill()}else{ctx.strokeStyle=mut();ctx.setLineDash([2,2]);ctx.stroke()}ctx.restore()})}};
if(!Array.isArray(ESPEC))ESPEC=[...SPEC];
function schips(){const all=ESPEC.length===SPEC.length;document.getElementById('espec').innerHTML='<button class="chip'+(all?' on':'')+'" onclick="ESPEC=[...SPEC];applyS()">'+T('all_spec')+'</button>'+[...SPEC].reverse().map(k=>'<button class="chip'+(ESPEC.includes(k)&&!all?' on':'')+'" onclick="togS(\''+k+'\')"><span class="dot" style="background:'+COLOR[k]+'"></span>'+T('spec')[k]+'</button>').join('')}
function togS(k){const all=ESPEC.length===SPEC.length;if(all)ESPEC=[k];else if(ESPEC.includes(k)){ESPEC=ESPEC.filter(x=>x!==k);if(!ESPEC.length)ESPEC=[...SPEC]}else ESPEC.push(k);applyS()}
function applyS(){save();schips();if(charts.el){charts.el.data.datasets.forEach(d=>d.hidden=!ESPEC.includes(d.key));charts.el.update()}}
const endL={id:'endl',afterDatasetsDraw(c){const ctx=c.ctx,a=c.chartArea;const it=[];c.data.datasets.forEach((d,i)=>{if(d.hidden)return;const m=c.getDatasetMeta(i);const j=d.data.length-1;if(j<0)return;const pt=m.data[j];it.push({y:pt.y,x:pt.x,t:d.label+' '+d.data[j].y+'%',c:d.borderColor})});
 it.sort((p,q)=>p.y-q.y);for(let i=1;i<it.length;i++)if(it[i].y-it[i-1].y<12)it[i].y=it[i-1].y+12;ctx.save();ctx.font='10px sans-serif';ctx.textBaseline='middle';it.forEach(o=>{ctx.fillStyle=o.c;ctx.fillText(o.t,o.x+8,Math.min(o.y,a.bottom))});ctx.restore()}};
function drawElec(){kill('el');const c=COMP[HOUSE][PLACE]||{};const yrs=Object.keys(c).sort();
 const ds=[...SPEC].reverse().map(k=>({key:k,hidden:!ESPEC.includes(k),label:T('spec')[k],backgroundColor:COLOR[k],borderColor:COLOR[k],seats:yrs.map(y=>c[y][k]),data:yrs.map(y=>({x:+y,y:c[y].total?+(c[y][k]/c[y].total*100).toFixed(1):0}))}));
 const bars=VIEW==='bars';
 charts.el=new Chart(document.getElementById('el'),{type:bars?'bar':'line',data:{datasets:ds.map(d=>bars?{...d,barThickness:16}:{...d,fill:false,tension:.25,pointRadius:3,borderWidth:2})},plugins:[sync,govDots,endL],
  options:{responsive:true,maintainAspectRatio:false,layout:{padding:{top:20,right:innerWidth<640?84:104}},onHover:hover,interaction:{mode:'nearest',axis:'x',intersect:false},plugins:{legend:{display:false},tooltip:{callbacks:{title:t=>t[0].parsed.x+(GOVS[PLACE]&&GOVS[PLACE][t[0].parsed.x]?' · '+GOVS[PLACE][t[0].parsed.x].name:''),label:t=>t.dataset.label+': '+(t.dataset.seats[t.dataIndex]??'')+' '+T('seats')+' ('+t.parsed.y+'%)'}}},
  scales:{x:{...X,stacked:bars},y:{stacked:bars,min:0,max:bars?100:(PLACE==='BR'&&HOUSE==='camara'?45:100),afterFit:YW,ticks:{color:mut(),callback:v=>v+'%'},grid:{color:grid()}}}}});
 document.getElementById('eltitle').textContent=nm(PLACE)+' · '+T(HOUSE==='camara'?'tab_camara':'tab_senado');
 document.getElementById('senote').textContent=HOUSE==='senado'?T('senate_note'):'';}
function drawCtx(){Object.keys(charts).filter(k=>k.startsWith('c_')).forEach(kill);const host=document.getElementById('ctx');host.innerHTML='';
 if(!PICK.length){host.innerHTML='<p class="cap">'+T('exp_none')+'</p>';return}
 const h=PICK.length===1?440:260;
 PICK.forEach(key=>{const p=PANELS[key];const marks=p.ds.map(d=>{const sv=STVAL[d.key];const v=PLACE!=='BR'&&sv?sv.v[PLACE]:null;return v==null?null:{x:Math.min(sv.y,2026),y:v,c:d.color,l:T('series')[d.key]}}).filter(Boolean);
  const lg=p.ds.map(d=>'<span><span class="sw" style="background:'+d.color+'"></span>'+T('series')[d.key]+'</span>').join('');
  host.insertAdjacentHTML('beforeend','<div class="cbox"><h3>'+T('panels')[key]+'</h3><div class="wrap" style="height:'+h+'px"><canvas id="c_'+key+'"></canvas></div><div class="lg">'+lg+'</div>'+(marks.length?'<p class="cap">'+nm(PLACE)+': '+marks.map(m=>m.l+' '+m.y+' ('+m.x+')').join(' · ')+'</p>':'')+'</div>');
  const isBar=key==='growth';
  const ds=p.ds.map(d=>({label:T('series')[d.key],data:d.data,borderColor:d.color,backgroundColor:isBar?(c=>c.parsed&&c.parsed.y<0?'#ec835a':'#9fc49f'):d.color,tension:.25,pointRadius:2,borderWidth:2,barThickness:5}));
  marks.forEach(m=>ds.push({type:'line',label:nm(PLACE)+' · '+m.l,data:[{x:m.x,y:m.y}],pointRadius:7,pointBorderWidth:2,pointBorderColor:ink(),backgroundColor:m.c,borderColor:m.c,showLine:false}));
  charts['c_'+key]=new Chart(document.getElementById('c_'+key),{type:isBar?'bar':'line',data:{datasets:ds},plugins:[sync],options:{responsive:true,maintainAspectRatio:false,layout:{padding:{top:20}},onHover:hover,interaction:{mode:'nearest',axis:'x',intersect:false},plugins:{legend:{display:false},tooltip:{callbacks:{title:t=>t[0].parsed.x,label:t=>t.dataset.label+': '+t.parsed.y}}},scales:{x:X,y:{min:p.lo,max:p.hi,afterFit:YW,ticks:{color:mut()},grid:{color:grid()}}}}});});
 document.getElementById('mark').style.display=PLACE==='BR'?'none':'';}
function chips(){const keys=Object.keys(PANELS).sort((a,b)=>T('panels')[a].localeCompare(T('panels')[b]));
 document.getElementById('pick').innerHTML=keys.map(k=>'<button class="chip'+(PICK.includes(k)?' on':'')+'" onclick="toggle(\''+k+'\')">'+T('panels')[k]+'</button>').join('');}
function toggle(k){if(PICK.includes(k))PICK=PICK.filter(x=>x!==k);else{PICK.push(k);if(PICK.length>2)PICK.shift()}save();chips();drawCtx()}
function setHouse(h){HOUSE=h;save();tabs();drawElec()}
function setView(v){VIEW=v;save();tabs();drawElec()}
function tabs(){document.querySelectorAll('.tab[data-h]').forEach(t=>t.classList.toggle('on',t.dataset.h===HOUSE));document.querySelectorAll('.chip[data-v]').forEach(t=>t.classList.toggle('on',t.dataset.v===VIEW))}
function opts(){const s=document.getElementById('place');s.innerHTML='<option value="BR">'+T('brazil')+'</option>'+Object.keys(UFNAME).sort((a,b)=>UFNAME[a].localeCompare(UFNAME[b])).map(u=>'<option value="'+u+'">'+UFNAME[u]+' ('+u+')</option>').join('');s.value=PLACE}
document.getElementById('place').addEventListener('change',e=>{PLACE=e.target.value;save();drawElec();drawCtx()});
function render(){opts();tabs();chips();schips();drawElec();drawCtx()}
applyStrings();render();
"""
def _efill(js):
    for k,v in {"__COMP__":comp,"__SENCOMP__":sen_comp,"__GOVS__":govs,"__PANELS__":panels,"__STVAL__":STVAL}.items():
        js=js.replace(k,json.dumps(v,ensure_ascii=False))
    return js
EXP_CSS = ".exp2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 36px;align-items:start}.exp2>div{min-width:0}.cbox{margin-bottom:18px}.exp2 h3{text-align:center}.pickwrap .chips{justify-content:center}@media (max-width:900px){.exp2{grid-template-columns:minmax(0,1fr)}.elcol{position:static}}@media (min-width:901px){.elcol{position:sticky;top:8px}}"
explore = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>(function(){{try{{var q=new URLSearchParams(location.search);var t=q.get('theme'),l=q.get('lang'),h=q.get('house');if(h)localStorage.setItem('house',h);document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');document.documentElement.lang=l==='pt'?'pt':'en';}}catch(e){{}}}})();</script>
{meta("explore","Elections vs context")}<script src="assets/chart.umd.js"></script><style>{CSS}{EXP_CSS}</style></head><body>
{header('explore')}
<main>
{CTLS}
<div class="intro" style="text-align:center"><strong data-i="exp_h"></strong><br><span data-i="exp_intro"></span></div>
<div class="exp2">
<div class="elcol"><section class="sec" style="border-top:none;padding-top:0;text-align:center">
<label><span data-i="exp_place"></span>: <select id="place"></select></label>
<div class="tabs" style="justify-content:center;margin-top:10px"><button class="tab" data-h="camara" onclick="setHouse('camara')" data-i="tab_camara"></button><button class="tab" data-h="senado" onclick="setHouse('senado')" data-i="tab_senado"></button></div>
<h2 id="eltitle" style="margin:8px 0 4px"></h2><p class="cap" data-i="how_lspec"></p><div class="chips" id="espec" style="justify-content:center;margin:4px 0 8px"></div><p class="cap" id="senote"></p>
<div class="wrap" style="height:440px"><canvas id="el"></canvas></div></section></div>
<div><section class="sec pickwrap" style="border-top:none;padding-top:0;text-align:center"><p class="cap" data-i="exp_pick"></p><div class="chips" id="pick"></div><p class="cap" id="mark" data-i="exp_marker"></p></section>
<div id="ctx"></div></div>
</div>
</main>
<footer class="foot"><a href="https://antonioaurel.github.io/" target="_blank" rel="noopener">antonioaurel.github.io</a></footer>
<script>{I18N_JS}</script><script>{_efill(EXP_JS)}</script></body></html>"""
(ROOT/"explore.html").write_text(explore, encoding="utf-8")
print("wrote explore.html", len(explore)//1024, "KB")
print("wrote compare.html", len(compare)//1024, "KB")
