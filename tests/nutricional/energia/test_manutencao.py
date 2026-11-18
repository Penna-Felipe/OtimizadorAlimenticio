
import pytest

from nutricional.energia import calcular_energia_manutencao


def test_energia_manutencao():
    """Verifica a exigência energética de manutenção."""

    resultado = calcular_energia_manutencao(600)

    esperado = 0.08 * 600 ** 0.75

    assert resultado == pytest.approx(esperado)


def test_peso_zero():
    """Verifica se peso igual a zero é rejeitado."""

    with pytest.raises(ValueError):
        calcular_energia_manutencao(0)


def test_peso_negativo():
    """Verifica se pesos negativos são rejeitados."""

    with pytest.raises(ValueError):
        calcular_energia_manutencao(-100)


def test_peso_infinito():
    """Verifica se valores infinitos são rejeitados."""

    with pytest.raises(ValueError):
        calcular_energia_manutencao(float("inf"))


def test_peso_nan():
    """Verifica se valores NaN são rejeitados."""

    with pytest.raises(ValueError):
        calcular_energia_manutencao(float("nan"))
