import pulp
from nutricional.marteria_seca import calcular_materia_seca
from nutricional.energia import calcular_energia
from nutricional.fibra import calcular_fibra_det_neutro
from nutricional.proteina_bruta import calcular_proteina_bruta 

resultado_ms = calcular_materia_seca(
    producao_leite=30,
    taxa_gordura=3.8,
    peso_vivo=600,
    dias_lactacao=120
)
DMI = resultado_ms["dmi_kg_dia"]

resultado_pb = calcular_proteina_bruta(
    peso_vivo=600,
    producao_leite=30,
    proteina_verdadeira=3.2
)
PB = resultado_pb["pb_exigida_g_dia"]/1000 #como está em gramas transforma em Kg

resultado_nel = calcular_energia(
    peso_vivo=600,
    producao_leite=30,
    taxa_gordura=3.8,
    proteina_verdadeira=3.2,
    taxa_lactose=4.8
)
NEL = resultado_nel["nel_total_mcal_dia"]

resultado_fdn = calcular_fibra_det_neutro(
    materia_seca=DMI
)
FDN = resultado_fdn
model = pulp.LpProblem("Otimizador Alimentar", sense=pulp.LpMinimize)

# Preços fictícios em R$/kg de MS
preco_milho = 1.50
preco_soja = 2.30
preco_silagem = 0.65

x = model.add_variable_dicts(
    name="x",
    indices=[1, 2, 3],
    lowBound=0,
    cat="Continuous"
)

model += (
    preco_milho * x[1]
    + preco_soja * x[2]
    + preco_silagem * x[3]
), "Custo_Total"


