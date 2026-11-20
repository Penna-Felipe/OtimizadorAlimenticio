
"""
Submódulo: crescimento.py

Calcula a energia retida no crescimento corporal
de bovinos leiteiros.

Referência:
    NRC (2001)

Unidades:
    Pesos corporais: kg
    Ganho diário: kg/dia
    Energia retida: Mcal/dia

Observações:
    - Utiliza o peso adulto esperado do animal.
    - O ganho informado deve ser o ganho de
      peso reduzido (SWG).
    - Não representa mobilização de reservas.
    - Não converte energia retida para NEL.
"""

import math

def calcular_peso_reduzido(
    peso_vivo: float
) -> float:
    """
    Converte peso vivo em peso corporal reduzido.

    Equação:
        SBW = 0.96 * BW

    Retorna:
        Peso reduzido (kg).
    """

    if not math.isfinite(peso_vivo) or peso_vivo <= 0:
        raise ValueError(
            "O peso vivo deve ser finito e maior que zero."
        )

    return 0.96 * peso_vivo


def calcular_peso_equivalente(
    peso_vivo: float,
    peso_adulto: float
) -> float:
    """
    Calcula o peso corporal vazio equivalente.

    Equações:
        SBW = 0.96 * BW
        MSBW = 0.96 * MBW
        EQSBW = SBW * (478 / MSBW)
        EQEBW = 0.891 * EQSBW

    Parâmetros:
        peso_vivo:
            Peso atual do animal (kg).

        peso_adulto:
            Peso esperado na maturidade (kg).

    Retorna:
        Peso corporal vazio equivalente (kg).
    """

    peso_reduzido = calcular_peso_reduzido(
        peso_vivo
    )

    peso_adulto_reduzido = calcular_peso_reduzido(
        peso_adulto
    )

    # Ajusta o peso ao animal de referência
    # utilizado pelo modelo NRC (2001).
    peso_reduzido_equivalente = (
        peso_reduzido
        * (478 / peso_adulto_reduzido)
    )

    # Converte para peso corporal vazio equivalente.
    peso_vazio_equivalente = (
        0.891 * peso_reduzido_equivalente
    )

    return peso_vazio_equivalente


def calcular_energia_retida_crescimento(
    peso_vivo: float,
    peso_adulto: float,
    ganho_peso_reduzido: float
) -> float:
    """
    Calcula a energia retida diariamente no crescimento.

    Referência:
        NRC (2001)

    Equação:
        RE = 0.0635 * EQEBW**0.75 * EQEBG**1.097

    Parâmetros:
        peso_vivo:
            Peso corporal atual (kg).

        peso_adulto:
            Peso esperado na maturidade (kg).

        ganho_peso_reduzido:
            Ganho diário de peso reduzido (kg/dia).

    Retorna:
        Energia retida no crescimento (Mcal/dia).

    Observações:
        - Ganho zero resulta em energia retida zero.
        - Ganhos negativos não são aceitos.
        - O resultado ainda não está convertido
          para a base NEL da dieta.
    """

    # Obtém o peso corporal vazio equivalente.
    peso_equivalente = calcular_peso_equivalente(
        peso_vivo,
        peso_adulto
    )

    # Valida o ganho de peso reduzido.
    if (
        not math.isfinite(ganho_peso_reduzido)
        or ganho_peso_reduzido < 0
    ):
        raise ValueError(
            "O ganho de peso reduzido deve ser "
            "finito e não negativo."
        )

    # Converte o ganho de peso reduzido para
    # ganho de peso corporal vazio equivalente.
    ganho_vazio_equivalente = (
        0.956 * ganho_peso_reduzido
    )

    # Calcula a energia retida no crescimento.
    energia_retida = (
        0.0635
        * peso_equivalente ** 0.75
        * ganho_vazio_equivalente ** 1.097
    )

    return energia_retida


def calcular_energia_metabolizavel_crescimento(
    energia_retida: float,
    eficiencia_ganho: float
) -> float:
    """
    Calcula a energia metabolizável necessária
    para o crescimento corporal.

    Equação:
        EM_crescimento = RE / kg

    Parâmetros:
        energia_retida (float):
            Energia retida no crescimento (Mcal/dia).

        eficiencia_ganho (float):
            Eficiência de utilização da energia
            metabolizável para ganho corporal (kg).

            Deve ser maior que 0 e menor ou igual a 1.
            Exemplo: 0.40 representa 40%.

    Retorna:
        float:
            Energia metabolizável necessária
            ao crescimento (Mcal/dia).

    Observações:
        A função não determina a eficiência de ganho.
        Esse parâmetro deverá ser obtido a partir
        do modelo nutricional adotado.

        O resultado está expresso em EM, não em NEL.
    """

    # Verifica se a energia retida é válida.
    if (
        not math.isfinite(energia_retida)
        or energia_retida < 0
    ):
        raise ValueError(
            "A energia retida deve ser finita "
            "e não negativa."
        )

    # Verifica se a eficiência está no intervalo válido.
    if (
        not math.isfinite(eficiencia_ganho)
        or not 0 < eficiencia_ganho <= 1
    ):
        raise ValueError(
            "A eficiência de ganho deve ser "
            "maior que 0 e menor ou igual a 1."
        )

    # Converte a energia retida em energia metabolizável.
    energia_metabolizavel = (
        energia_retida / eficiencia_ganho
    )

    return energia_metabolizavel

