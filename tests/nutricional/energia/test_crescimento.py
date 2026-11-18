
import pytest

from nutricional.energia.crescimento import (
    calcular_peso_reduzido,
    calcular_peso_equivalente,
    calcular_energia_retida_crescimento,
    calcular_energia_metabolizavel_crescimento,
)


def test_peso_reduzido():
    resultado = calcular_peso_reduzido(500)

    assert resultado == pytest.approx(480.0)


def test_peso_equivalente():
    resultado = calcular_peso_equivalente(
        peso_vivo=500,
        peso_adulto=650
    )

    esperado = 0.891 * (480 * 478 / 624)

    assert resultado == pytest.approx(esperado)


def test_energia_retida_crescimento():
    resultado = calcular_energia_retida_crescimento(
        peso_vivo=500,
        peso_adulto=650,
        ganho_peso_reduzido=0.8
    )

    peso_equivalente = (
        0.891 * (480 * 478 / 624)
    )

    ganho_equivalente = 0.956 * 0.8

    esperado = (
        0.0635
        * peso_equivalente ** 0.75
        * ganho_equivalente ** 1.097
    )

    assert resultado == pytest.approx(esperado)


def test_crescimento_sem_ganho():
    resultado = calcular_energia_retida_crescimento(
        peso_vivo=500,
        peso_adulto=650,
        ganho_peso_reduzido=0
    )

    assert resultado == pytest.approx(0.0)


def test_peso_invalido():
    with pytest.raises(ValueError):
        calcular_peso_reduzido(-500)


def test_peso_adulto_invalido():
    with pytest.raises(ValueError):
        calcular_peso_equivalente(500, 0)


def test_ganho_negativo():
    with pytest.raises(ValueError):
        calcular_energia_retida_crescimento(
            peso_vivo=500,
            peso_adulto=650,
            ganho_peso_reduzido=-0.5
        )



def test_energia_metabolizavel_crescimento():
    """
    Verifica a conversão de energia retida
    para energia metabolizável.
    """
    resultado = calcular_energia_metabolizavel_crescimento(
        energia_retida=4.0,
        eficiencia_ganho=0.40
    )

    assert resultado == pytest.approx(10.0)


def test_energia_metabolizavel_sem_crescimento():
    """
    Sem energia retida, não há exigência
    adicional de EM para crescimento.
    """
    resultado = calcular_energia_metabolizavel_crescimento(
        energia_retida=0.0,
        eficiencia_ganho=0.40
    )

    assert resultado == pytest.approx(0.0)


@pytest.mark.parametrize(
    "eficiencia",
    [0, -0.1, 1.1, float("nan"), float("inf")]
)
def test_eficiencia_ganho_invalida(eficiencia):
    """
    Rejeita eficiências fora do intervalo válido.
    """
    with pytest.raises(ValueError):
        calcular_energia_metabolizavel_crescimento(
            energia_retida=4.0,
            eficiencia_ganho=eficiencia
        )


def test_energia_retida_negativa():
    """
    Rejeita energia retida negativa.
    """
    with pytest.raises(ValueError):
        calcular_energia_metabolizavel_crescimento(
            energia_retida=-4.0,
            eficiencia_ganho=0.40
        )
