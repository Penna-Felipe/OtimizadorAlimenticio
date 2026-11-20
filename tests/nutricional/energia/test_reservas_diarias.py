
import pytest

from nutricional.energia.reservas import (
    calcular_energia_diaria_reservas,
)


def test_energia_diaria_mobilizacao():
    resultado = calcular_energia_diaria_reservas(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=2.0,
        dias=60,
    )

    assert resultado == pytest.approx(
        -368.78 / 60,
        abs=0.01,
    )


def test_energia_diaria_reposicao():
    resultado = calcular_energia_diaria_reservas(
        peso_vivo_atual=600.0,
        ecc_atual=2.0,
        ecc_desejado=3.0,
        dias=60,
        em_lactacao=True,
    )

    assert resultado == pytest.approx(
        442.95 / 60,
        abs=0.01,
    )


def test_energia_diaria_ecc_constante():
    resultado = calcular_energia_diaria_reservas(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=3.0,
        dias=60,
    )

    assert resultado == 0.0


def test_energia_diaria_periodo_invalido():
    with pytest.raises(ValueError):
        calcular_energia_diaria_reservas(
            peso_vivo_atual=600.0,
            ecc_atual=3.0,
            ecc_desejado=2.0,
            dias=0,
        )
