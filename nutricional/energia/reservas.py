
"""
Submódulo: reservas.py

Calcula a energia associada às alterações
das reservas corporais de bovinos leiteiros.

Referência:
    NRC (2001)

Unidades:
    Gordura corporal: kg
    Proteína corporal: kg
    Energia: Mcal

Observação:
    Este módulo diferencia a energia contida
    nos tecidos da energia efetivamente
    disponibilizada ou necessária na dieta.
"""

from nutricional.validacoes import validar_nao_negativo
from .ecc import calcular_variacao_tecidos_por_ecc

def calcular_energia_reservas(
    gordura_corporal: float,
    proteina_corporal: float
) -> float:
    """
    Calcula a energia contida em uma quantidade
    de gordura e proteína dos tecidos corporais.

    Equação:
        E = 9.4 * G + 5.55 * P

    Parâmetros:
        gordura_corporal:
            Massa de gordura (kg).

        proteina_corporal:
            Massa de proteína (kg).

    Retorna:
        Energia contida nos tecidos (Mcal).

    Observações:
        As massas devem representar os tecidos
        mobilizados ou depositados, e não
        necessariamente a composição corporal
        total do animal.
    """

    validar_nao_negativo(
        "gordura_corporal",
        gordura_corporal
    )

    validar_nao_negativo(
        "proteina_corporal",
        proteina_corporal
    )

    energia_gordura = 9.4 * gordura_corporal
    energia_proteina = 5.55 * proteina_corporal

    return energia_gordura + energia_proteina

def calcular_energia_mobilizacao(
    energia_reservas: float
) -> float:
    """
    Calcula a energia líquida disponibilizada
    pela mobilização de reservas corporais.

    Referência:
        NRC (2001)

    Equação:
        NEL_mobilizacao = E_reservas * 0.82

    Parâmetros:
        energia_reservas:
            Energia contida nos tecidos
            mobilizados (Mcal).

    Retorna:
        Energia líquida disponibilizada
        para lactação (Mcal).
    """

    validar_nao_negativo(
        "energia_reservas",
        energia_reservas
    )

    return energia_reservas * 0.82


def calcular_energia_reposicao(
    energia_reservas: float,
    em_lactacao: bool
) -> float:
    """
    Calcula a energia necessária para reposição
    das reservas corporais.

    Referência:
        NRC (2001)

    Parâmetros:
        energia_reservas:
            Energia a ser depositada nos tecidos
            corporais (Mcal).

        em_lactacao:
            True: vaca em lactação.
            False: vaca seca.

    Retorna:
        Energia necessária na base NEL (Mcal).

    Observações:
        Fatores utilizados:
            Lactação: 0.85
            Período seco: 1.07

        A energia_reservas deve representar a
        quantidade de energia que será depositada,
        não a energia total existente no animal.
    """

    validar_nao_negativo(
        "energia_reservas",
        energia_reservas
    )

    if not isinstance(em_lactacao, bool):
        raise ValueError(
            "em_lactacao deve ser True ou False."
        )

    fator = 0.85 if em_lactacao else 1.07

    return energia_reservas * fator


def calcular_energia_diaria_reservas(
    peso_vivo_atual: float,
    ecc_atual: float,
    ecc_desejado: float,
    dias: int,
    em_lactacao: bool = True,
) -> float:
    """
    Calcula a contribuição energética média diária
    associada à variação das reservas corporais.

    Modelo:
        Baseado nas equações de composição corporal
        e conversão energética do NRC (2001)
        implementadas nesta biblioteca.

    Parâmetros:
        peso_vivo_atual (float):
            Peso vivo observado no ECC atual (kg).

        ecc_atual (float):
            Escore de condição corporal inicial
            na escala de 1 a 5.

        ecc_desejado (float):
            Escore de condição corporal final
            na escala de 1 a 5.

        dias (int):
            Número de dias em que ocorrerá
            a alteração do ECC.

        em_lactacao (bool):
            Indica se a vaca está em lactação.
            Utilizado no cálculo de reposição.

    Retorna:
        float:
            Contribuição energética média (Mcal/dia).

            Positivo: reposição de reservas.
            Negativo: mobilização de reservas.
            Zero: ECC constante.

    Observações:
        O cálculo considera uma variação média
        uniforme das reservas durante o período.

        Não prevê automaticamente a evolução
        diária do ECC ou do peso corporal.
    """

    if dias <= 0:
        raise ValueError(
            "O período deve ser maior que zero."
        )

    variacoes = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=peso_vivo_atual,
        ecc_atual=ecc_atual,
        ecc_desejado=ecc_desejado,
    )

    if ecc_desejado == ecc_atual:
        return 0.0

    gordura = abs(variacoes["variacao_gordura_kg"])
    proteina = abs(variacoes["variacao_proteina_kg"])

    energia_tecidos = calcular_energia_reservas(
        gordura_corporal=gordura,
        proteina_corporal=proteina,
    )

    if ecc_desejado < ecc_atual:
        energia_total = calcular_energia_mobilizacao(
            energia_reservas=energia_tecidos,
        )

        return -energia_total / dias

    energia_total = calcular_energia_reposicao(
        energia_reservas=energia_tecidos,
        em_lactacao=em_lactacao,
    )

    return energia_total / dias
