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
