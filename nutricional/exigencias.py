from nutricional.marteria_seca import calcular_materia_seca
from nutricional.energia import calcular_energia
from nutricional.fibra_det_neutro import calcular_fibra_det_neutro
from nutricional.proteina_bruta import calcular_proteina_bruta


def calcular_exigencias(vaca: dict) -> dict:
    """
    Calcula as exigências nutricionais estimadas de uma vaca.

    Parâmetros:
        vaca (dict): Dicionário contendo os dados produtivos
                     e fisiológicos do animal.

    Retorna:
        dict: Exigências nutricionais contendo:
            - dmi: Matéria seca estimada (kg/dia).
            - pb: Proteína bruta exigida (kg/dia).
            - nel: Energia líquida exigida (Mcal/dia).
            - fdn: Fibra mínima exigida (kg/dia).
    """

    # 1. Matéria seca
    resultado_ms = calcular_materia_seca(
        producao_leite=vaca["producao_leite"],
        taxa_gordura=vaca["taxa_gordura"],
        peso_vivo=vaca["peso_vivo"],
        dias_lactacao=vaca["dias_lactacao"]
    )

    dmi = resultado_ms["dmi_kg_dia"]

    # 2. Proteína bruta
    resultado_pb = calcular_proteina_bruta(
        peso_vivo=vaca["peso_vivo"],
        producao_leite=vaca["producao_leite"],
        proteina_verdadeira=vaca["proteina_verdadeira"]
    )

    pb = resultado_pb["pb_exigida_g_dia"] / 1000

    # 3. Energia líquida
    resultado_nel = calcular_energia(
        peso_vivo=vaca["peso_vivo"],
        producao_leite=vaca["producao_leite"],
        taxa_gordura=vaca["taxa_gordura"],
        proteina_verdadeira=vaca["proteina_verdadeira"],
        taxa_lactose=vaca["taxa_lactose"]
    )

    nel = resultado_nel["nel_total_mcal_dia"]

    # 4. Fibra
    fdn = calcular_fibra_det_neutro(
        materia_seca=dmi
    )

    return {
        "dmi": dmi,
        "pb": pb,
        "nel": nel,
        "fdn": fdn
    }