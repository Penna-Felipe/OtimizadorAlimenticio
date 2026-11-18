
import pytest

from nutricional.energia.reservas import (
    calcular_energia_reservas,
    calcular_energia_mobilizacao,
    calcular_energia_reposicao
)


def test_energia_reservas():
    """
    Verifica o conteúdo energético dos tecidos.
    """

    resultado = calcular_energia_reservas(
        gordura_corporal=2.0,
        proteina_corporal=1.0
    )

    esperado = (9.4 * 2.0) + (5.55 * 1.0)

    assert resultado == pytest.approx(24.35)


def test_reservas_sem_tecidos():
    """
    Sem gordura ou proteína, não existe
    energia armazenada nesses tecidos.
    """

    resultado = calcular_energia_reservas(
        gordura_corporal=0.0,
        proteina_corporal=0.0
    )

    assert resultado == pytest.approx(0.0)


def test_gordura_negativa():
    """
    Rejeita massa de gordura negativa.
    """

    with pytest.raises(ValueError):
        calcular_energia_reservas(
            gordura_corporal=-1.0,
            proteina_corporal=1.0
        )


def test_proteina_negativa():
    """
    Rejeita massa de proteína negativa.
    """

    with pytest.raises(ValueError):
        calcular_energia_reservas(
            gordura_corporal=1.0,
            proteina_corporal=-1.0
        )


from nutricional.energia.reservas import (
    calcular_energia_reservas,
    calcular_energia_mobilizacao,
)


def test_energia_mobilizacao():
    resultado = calcular_energia_mobilizacao(10.0)

    assert resultado == pytest.approx(8.2)


def test_mobilizacao_sem_reservas():
    resultado = calcular_energia_mobilizacao(0.0)

    assert resultado == pytest.approx(0.0)


def test_mobilizacao_negativa():
    with pytest.raises(ValueError):
        calcular_energia_mobilizacao(-10.0)


def test_reposicao_lactacao():
    resultado = calcular_energia_reposicao(
        energia_reservas=10.0,
        em_lactacao=True
    )

    assert resultado == pytest.approx(8.5)


def test_reposicao_vaca_seca():
    resultado = calcular_energia_reposicao(
        energia_reservas=10.0,
        em_lactacao=False
    )

    assert resultado == pytest.approx(10.7)


def test_reposicao_sem_energia():
    resultado = calcular_energia_reposicao(
        energia_reservas=0.0,
        em_lactacao=True
    )

    assert resultado == pytest.approx(0.0)


def test_reposicao_energia_negativa():
    with pytest.raises(ValueError):
        calcular_energia_reposicao(
            energia_reservas=-10.0,
            em_lactacao=True
        )


def test_reposicao_lactacao_invalida():
    with pytest.raises(ValueError):
        calcular_energia_reposicao(
            energia_reservas=10.0,
            em_lactacao="sim"
        )
