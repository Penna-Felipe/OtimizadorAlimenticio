
import pytest

from nutricional.energia import (
    calcular_nel_leite,
    calcular_energia_lactacao,
)


def test_nel_leite():
    """Verifica a energia líquida por kg de leite."""

    resultado = calcular_nel_leite(3.5, 3.2, 4.8)

    assert resultado == pytest.approx(0.69491)


def test_energia_lactacao():
    """Verifica a exigência diária de energia para lactação."""

    resultado = calcular_energia_lactacao(35, 0.69491)

    assert resultado == pytest.approx(24.32185)
