"""
Módulo: consumo.py

Estimativa do consumo de matéria seca para vacas leiteiras
em lactação.

Referência:
    NRC (2001).
    Nutrient Requirements of Dairy Cattle.
    7th Revised Edition.

Modelo:
    NRC 2001 - equação de predição de DMI para
    vacas leiteiras em lactação.

Unidades:
    Produção de leite: kg/dia
    Gordura do leite: %
    Peso corporal: kg
    Dias em lactação: dias
    FCM: kg/dia
    DMI: kg/dia
"""

import math


def calcular_fcm(
    producao_leite: float,
    taxa_gordura: float
) -> float:
    """
    Calcula o leite corrigido para 4% de gordura (FCM).

    Fórmula:
        FCM = 0.4 * PL + 15 * PL * (TG / 100)
    """

    if producao_leite < 0:
        raise ValueError("A produção de leite não pode ser negativa.")

    if not 0 <= taxa_gordura <= 100:
        raise ValueError("A taxa de gordura deve estar entre 0 e 100.")

    fcm = (
        0.4 * producao_leite
        + 15.0 * producao_leite * (taxa_gordura / 100.0)
    )

    return fcm


def calcular_dmi(
    fcm: float,
    peso_vivo: float,
    dias_lactacao: float
) -> float:
    """
    Calcula a ingestão estimada de matéria seca (DMI).

    Fórmula NRC (2001):
        DMI = (0.372 * FCM + 0.0968 * BW^0.75)
              * (1 - e(-0.192 * (WOL + 3.67)))

    Onde:
        WOL = dias_lactacao / 7 (dias em semanas)

    Returns:
        Ingestão estimada de matéria seca em kg/dia.
    """

    if fcm < 0:
        raise ValueError("FCM não pode ser negativo.")

    if peso_vivo <= 0:
        raise ValueError("O peso vivo deve ser maior que zero.")

    if dias_lactacao < 0:
        raise ValueError("Dias em lactação não podem ser negativos.")

    # Converte dias de lactação em semanas.
    semanas_lactacao = dias_lactacao / 7.0

    # Calcula o peso metabólico.
    peso_metabolico = peso_vivo ** 0.75

    # Fator de ajuste para o estágio de lactação.
    fator_lactacao = (
        1.0 - math.exp(
            -0.192 * (semanas_lactacao + 3.67)
        )
    )

    # Calcula a ingestão estimada de matéria seca.
    dmi = (
        0.372 * fcm
        + 0.0968 * peso_metabolico
    ) * fator_lactacao

    return dmi


def calcular_consumo(
    producao_leite: float,
    taxa_gordura: float,
    peso_vivo: float,
    dias_lactacao: float
) -> dict:
    """
    Calcula a ingestão estimada de matéria seca do animal.

    Etapas:
        1. Calcula o FCM.
        2. Calcula o DMI conforme NRC (2001).

    Returns:
        Dicionário contendo FCM e DMI em kg/dia.
    """

    fcm = calcular_fcm(
        producao_leite,
        taxa_gordura
    )

    dmi = calcular_dmi(
        fcm,
        peso_vivo,
        dias_lactacao
    )

    return {
        "fcm_kg_dia": fcm,
        "dmi_kg_dia": dmi
    }
