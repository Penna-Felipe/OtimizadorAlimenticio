import pulp
from dados.limites_tcc import limites_tcc
from dados.animais import vaca1
from dados.ingredientes import ingredientes
from nutricional.marteria_seca import calcular_materia_seca
from nutricional.energia import calcular_energia
from nutricional.fibra_det_neutro import calcular_fibra_det_neutro
from nutricional.proteina_bruta import calcular_proteina_bruta 
from nutricional.carboidratos_nao_fibro import calcular_cnf

resultado_ms = calcular_materia_seca(
    producao_leite=vaca1["producao_leite"],
    taxa_gordura=vaca1["taxa_gordura"],
    peso_vivo=vaca1["peso_vivo"],
    dias_lactacao=vaca1["dias_lactacao"]
)
DMI = resultado_ms["dmi_kg_dia"]

resultado_pb = calcular_proteina_bruta(
    peso_vivo=vaca1["peso_vivo"],
    producao_leite=vaca1["producao_leite"],
    proteina_verdadeira=vaca1["proteina_verdadeira"]
)
PB = resultado_pb["pb_exigida_g_dia"]/1000 #como está em gramas transforma em Kg

resultado_nel = calcular_energia(
    peso_vivo=vaca1["peso_vivo"],
    producao_leite=vaca1["producao_leite"],
    taxa_gordura=vaca1["taxa_gordura"],
    proteina_verdadeira=vaca1["proteina_verdadeira"],
    taxa_lactose=vaca1["taxa_lactose"]
)
NEL = resultado_nel["nel_total_mcal_dia"]

resultado_fdn = calcular_fibra_det_neutro(
    materia_seca=DMI
)
FDN = resultado_fdn

#Preço ingredinetes vindo do dicionario de dados
preco_milho = ingredientes["milho"]["preco"]
preco_soja = ingredientes["farelo_soja"]["preco"]
preco_silagem = ingredientes["silagem_milho"]["preco"]

#Calcular CNF de cada ingrediente
for nome, dados in ingredientes.items():

    dados["cnf"] = calcular_cnf(
        pb=dados["pb"],
        fdn=dados["fdn"],
        ee=dados["ee"],
        cinzas=dados["cinzas"]
    )

#Reporta o CNF de cada ingrediente
for nome, dados in ingredientes.items():
    print(f"{nome}: CNF = {dados['cnf'] * 100:.2f}%")


model = pulp.LpProblem("Otimizador_Alimentar", sense=pulp.LpMinimize)


x = model.add_variable_dicts(
    name="x",
    indices=ingredientes.keys(),
    lowBound=0,
    cat="Continuous"
)

#Função Objetiva
model += pulp.lpSum(
    ingredientes[i]["preco"] * x[i]
    for i in ingredientes
), "Custo_Total"

#Restrição DMI
model += pulp.lpSum(
    x[i] for i in ingredientes
) == DMI, "Materia_Seca"

#Restrição Min. Proteina Bruta
model += pulp.lpSum(
    ingredientes[i]["pb"] * x[i]
    for i in ingredientes
) >= PB, "Proteina_Bruta"

#Restrição Min. Energia
model += pulp.lpSum(
    ingredientes[i]["nel"] * x[i]
    for i in ingredientes
) >= NEL, "Energia"

#Restrição Min. Fibra
model += pulp.lpSum(
    ingredientes[i]["fdn"] * x[i]
    for i in ingredientes
) >= FDN, "Fibra"

# FDN proveniente exclusivamente dos volumosos
fdn_forragem = pulp.lpSum(
    ingredientes[i]["fdn"] * x[i]
    for i in ingredientes
    if ingredientes[i]["volumoso"]
)
# Restrição mínima de FDN de forragens (18% da MS)
model += fdn_forragem >= 0.18 * DMI, "FDN_Forragem_Minima"
model += fdn_forragem <= 0.20 * DMI, "FDN_Forragem_Maxima"


#Restrições amido
amido_total = pulp.lpSum(
    ingredientes[i]["amido"] * x[i]
    for i in ingredientes
)
model += amido_total >= limites_tcc["amido"]["min"] * DMI, "Amido_Minimo" 
model += amido_total <= limites_tcc["amido"]["max"] * DMI, "Amido_Maximo" 

resultado = model.solve(pulp.COIN_CMD(msg=False))

if resultado.has_solution:

    # Nutrientes fornecidos pela dieta
    pb_fornecida = sum(
        ingredientes[i]["pb"] * x[i].value()
        for i in ingredientes
    )

    nel_fornecida = sum(
        ingredientes[i]["nel"] * x[i].value()
        for i in ingredientes
    )

    fdn_fornecida = sum(
        ingredientes[i]["fdn"] * x[i].value()
        for i in ingredientes
    )

    amido_fornecido = sum(
        ingredientes[i]["amido"] * x[i].value()
        for i in ingredientes
    )  

    #percentutal dieta
    amido_percentual = (amido_fornecido/DMI) * 100


    print("\n--- BALANÇO NUTRICIONAL ---")

    print(f"PB:  {pb_fornecida:.2f} / {PB:.2f} kg/dia")
    print(f"NEL: {nel_fornecida:.2f} / {NEL:.2f} Mcal/dia")
    print(f"FDN: {fdn_fornecida:.2f} / {FDN:.2f} kg/dia")
    print(f"Amido: {amido_fornecido:.2f} kg/dia")

    print("\n--- COMPOSIÇÃO DIETA ---")
    print(f"Amido: {amido_percentual:.2f}%")

    #Folga nutricional
    balanco = {
        "PB": pb_fornecida - PB,
        "NEL": nel_fornecida - NEL,
        "FDN": fdn_fornecida - FDN
    }

    print("\n--- EXCESSO NUTRICIONAL ---")
    for nutriente, folga in balanco.items():
        print(f"{nutriente}: {folga:.2f}")

    x_sol = {i: x[i].value() for i in ingredientes}
    print( f"{x_sol}")
    print(f"Custo = {resultado.objective}")
else:
    print("Não Foi possivel achar solução otimizada")