
import pytest

from nutricional.energia.gestacao import (
    calcular_energia_retida_gestacao,
    calcular_energia_metabolizavel_gestacao,
    calcular_energia_gestacao,
)


def test_energia_retida_gestacao():
    resultado = calcular_energia_retida_gestacao(
        250, 45
    )

    assert resultado == pytest.approx(0.7598)


def test_energia_metabolizavel_gestacao():
    resultado = calcular_energia_metabolizavel_gestacao(
        0.7598
    )

    assert resultado == pytest.approx(
        0.7598 / 0.14
    )


def test_energia_gestacao():
    resultado = calcular_energia_gestacao(
        250, 45
    )

    esperado = 0.7598 / 0.218

    assert resultado == pytest.approx(esperado)



def test_gestacao_antes_190_dias():
    resultado = calcular_energia_gestacao(
        150, 45
    )

    assert resultado == pytest.approx(0.0)


def test_gestacao_dia_190():
    resultado = calcular_energia_retida_gestacao(
        190, 45
    )

    assert resultado == pytest.approx(
        0.00318 * 190 - 0.0352
    )


def test_dias_gestacao_invalidos():
    with pytest.raises(ValueError):
        calcular_energia_gestacao(300, 45)


def test_peso_bezerro_invalido():
    with pytest.raises(ValueError):
        calcular_energia_gestacao(250, -45)
