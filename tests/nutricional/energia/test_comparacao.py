import pytest

from nutricional.energia.ecc import (
    calcular_variacao_tecidos_por_ecc,
)

from nutricional.energia.reservas import (
    calcular_energia_reservas,
    calcular_energia_mobilizacao,
    calcular_energia_reposicao,
)


def test_comparacao_mobilizacao_nrc():
    """
    Explora a mobilização de reservas de uma
    vaca de 600 kg, passando de ECC 3 para 2.

    O resultado será comparado com a referência
    publicada pelo NRC (2001).
    """

    variacoes = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=2.0,
    )

    gordura_mobilizada = -variacoes["variacao_gordura_kg"]
    proteina_mobilizada = -variacoes["variacao_proteina_kg"]

    energia_tecidos = calcular_energia_reservas(
        gordura_corporal=gordura_mobilizada,
        proteina_corporal=proteina_mobilizada,
    )

    energia_disponivel = calcular_energia_mobilizacao(
        energia_reservas=energia_tecidos,
    )

    print("\n--- COMPARAÇÃO NRC (2001) ---")
    print(f"Gordura mobilizada: {gordura_mobilizada:.2f} kg")
    print(f"Proteína mobilizada: {proteina_mobilizada:.2f} kg")
    print(f"Energia dos tecidos: {energia_tecidos:.2f} Mcal")
    print(f"Energia disponível: {energia_disponivel:.2f} Mcal")

    def test_validacao_mobilizacao_nrc():
        variacoes = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=2.0,
    )

    energia_tecidos = calcular_energia_reservas(
        gordura_corporal=-variacoes["variacao_gordura_kg"],
        proteina_corporal=-variacoes["variacao_proteina_kg"],
    )

    resultado = calcular_energia_mobilizacao(
        energia_reservas=energia_tecidos
    )

    referencia_nrc = 368.0

    assert resultado == pytest.approx(
        referencia_nrc,
        rel=0.01
    )


def test_comparacao_reposicao_nrc():
    """
    Compara a energia estimada para reposição
    de reservas corporais entre ECC 2 e ECC 3.

    Peso vivo inicial: 600 kg
    ECC inicial: 2
    ECC desejado: 3
    """

    variacoes = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=2.0,
        ecc_desejado=3.0,
    )

    gordura_reposta = variacoes["variacao_gordura_kg"]
    proteina_reposta = variacoes["variacao_proteina_kg"]

    energia_tecidos = calcular_energia_reservas(
        gordura_corporal=gordura_reposta,
        proteina_corporal=proteina_reposta,
    )

    energia_reposicao = calcular_energia_reposicao(
        energia_reservas=energia_tecidos,
        em_lactacao=True,
    )

    print("\n--- REPOSIÇÃO NRC (2001) ---")
    print(f"Gordura reposta: {gordura_reposta:.2f} kg")
    print(f"Proteína reposta: {proteina_reposta:.2f} kg")
    print(f"Energia dos tecidos: {energia_tecidos:.2f} Mcal")
    print(f"Energia de reposição: {energia_reposicao:.2f} Mcal")


import pytest

from nutricional.energia.ecc import (
    calcular_variacao_tecidos_por_ecc,
)

from nutricional.energia.reservas import (
    calcular_energia_reservas,
    calcular_energia_mobilizacao,
    calcular_energia_reposicao,
)


@pytest.mark.parametrize(
    "ecc_atual, ecc_desejado, referencia_nrc",
    [
        (3.0, 2.0, 368.0),
        (4.0, 3.0, 385.0),
        (2.0, 3.0, 447.0),
        (3.0, 4.0, 459.0),
    ],
)
def test_comparacao_multiplos_ecc(
    ecc_atual,
    ecc_desejado,
    referencia_nrc,
):
    """
    Compara as estimativas energéticas da biblioteca
    com quatro valores de referência atribuídos
    à tabela 2-5 do NRC (2001).

    Peso vivo inicial:
        600 kg.

    Observação:
        Este é um teste exploratório de concordância.
        Ainda não estabelece equivalência completa
        com o procedimento original do NRC.
    """

    variacoes = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=ecc_atual,
        ecc_desejado=ecc_desejado,
    )

    gordura = abs(variacoes["variacao_gordura_kg"])
    proteina = abs(variacoes["variacao_proteina_kg"])

    energia_tecidos = calcular_energia_reservas(
        gordura_corporal=gordura,
        proteina_corporal=proteina,
    )

    if ecc_desejado < ecc_atual:
        processo = "Mobilização"

        energia_calculada = calcular_energia_mobilizacao(
            energia_reservas=energia_tecidos,
        )

    else:
        processo = "Reposição"

        energia_calculada = calcular_energia_reposicao(
            energia_reservas=energia_tecidos,
            em_lactacao=True,
        )

    erro_percentual = (
        abs(energia_calculada - referencia_nrc)
        / referencia_nrc
        * 100
    )

    print(f"\n--- {processo.upper()} ---")
    print(f"ECC: {ecc_atual} -> {ecc_desejado}")
    print(f"Gordura: {gordura:.2f} kg")
    print(f"Proteína: {proteina:.2f} kg")
    print(f"Energia dos tecidos: {energia_tecidos:.2f} Mcal")
    print(f"Biblioteca: {energia_calculada:.2f} Mcal")
    print(f"Referência NRC: {referencia_nrc:.2f} Mcal")
    print(f"Erro relativo: {erro_percentual:.2f}%")

    # Verifica se a energia calculada é positiva.
    assert energia_calculada > 0

    # Critério provisório de concordância:
    # diferença relativa máxima de 1% da referência.
    assert energia_calculada == pytest.approx(
        referencia_nrc,
        rel=0.01
    )
