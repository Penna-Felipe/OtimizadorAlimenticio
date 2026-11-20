
import pytest

from nutricional.energia.exigencias import calcular_energia


def test_integracao_reservas_mobilizacao():
    resultado = calcular_energia(
        peso_vivo=600.0,
        producao_leite=30.0,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8,
        ecc_atual=3.0,
        ecc_desejado=2.0,
        dias_variacao_ecc=60,
    )

    assert resultado["energia_reservas_mcal_dia"] == pytest.approx(
        -368.78 / 60,
        abs=0.01,
    )


def test_integracao_reservas_reposicao():
    resultado = calcular_energia(
        peso_vivo=600.0,
        producao_leite=30.0,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8,
        ecc_atual=2.0,
        ecc_desejado=3.0,
        dias_variacao_ecc=60,
    )

    assert resultado["energia_reservas_mcal_dia"] == pytest.approx(
        442.95 / 60,
        abs=0.01,
    )


def test_integracao_reservas_nao_informadas():
    resultado = calcular_energia(
        peso_vivo=600.0,
        producao_leite=30.0,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8,
    )

    assert resultado["energia_reservas_mcal_dia"] == 0.0


def test_integracao_reservas_parametros_incompletos():
    with pytest.raises(ValueError):
        calcular_energia(
            peso_vivo=600.0,
            producao_leite=30.0,
            taxa_gordura=3.5,
            proteina_verdadeira=3.2,
            taxa_lactose=4.8,
            ecc_atual=3.0,
        )
