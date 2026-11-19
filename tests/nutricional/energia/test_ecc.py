
import pytest

from nutricional.energia.ecc import (
    validar_ecc,
    calcular_ecc_escala_9,
    calcular_proporcao_gordura,
    calcular_proporcao_proteina,
    calcular_peso_corporal_vazio,
    calcular_gordura_corporal,
    calcular_proteina_corporal,
    calcular_peso_corporal_vazio_por_ecc,
    calcular_variacao_tecidos_por_ecc,
)


@pytest.mark.parametrize(
    "ecc, esperado",
    [
        (1.0, 1.0),
        (2.0, 3.0),
        (2.5, 4.0),
        (3.0, 5.0),
        (4.0, 7.0),
        (5.0, 9.0),
    ]
)
def test_calcular_ecc_escala_9(ecc, esperado):
    resultado = calcular_ecc_escala_9(ecc)

    assert resultado == pytest.approx(esperado)


@pytest.mark.parametrize(
    "ecc",
    [
        -1.0,
        0.0,
        5.5,
        float("nan"),
        float("inf"),
    ]
)
def test_ecc_invalido(ecc):
    with pytest.raises(ValueError):
        validar_ecc(ecc)


def test_ecc_valido():
    assert validar_ecc(3.0) is None


@pytest.mark.parametrize(
    "ecc, esperado",
    [
        (1.0, 0.037683),
        (2.0, 0.113049),
        (3.0, 0.188415),
        (4.0, 0.263781),
        (5.0, 0.339147),
    ]
)
def test_calcular_proporcao_gordura(ecc, esperado):
    resultado = calcular_proporcao_gordura(ecc)

    assert resultado == pytest.approx(esperado)


@pytest.mark.parametrize(
    "ecc, esperado",
    [
        (1.0, 0.1942098),
        (2.0, 0.1808574),
        (3.0, 0.1675050),
        (4.0, 0.1541526),
        (5.0, 0.1408002),
    ]
)
def test_calcular_proporcao_proteina(ecc, esperado):
    resultado = calcular_proporcao_proteina(ecc)

    assert resultado == pytest.approx(esperado)


def test_proporcao_gordura_ecc_invalido():
    with pytest.raises(ValueError):
        calcular_proporcao_gordura(6.0)


def test_proporcao_proteina_ecc_invalido():
    with pytest.raises(ValueError):
        calcular_proporcao_proteina(0.0)


@pytest.mark.parametrize(
    "peso_vivo, esperado",
    [
        (0.0, 0.0),
        (400.0, 326.8),
        (500.0, 408.5),
        (600.0, 490.2),
        (700.0, 571.9),
    ]
)
def test_calcular_peso_corporal_vazio(
    peso_vivo,
    esperado
):
    resultado = calcular_peso_corporal_vazio(
        peso_vivo
    )

    assert resultado == pytest.approx(esperado)


def test_peso_corporal_vazio_negativo():
    with pytest.raises(ValueError):
        calcular_peso_corporal_vazio(-100.0)



def test_calcular_gordura_corporal():
    resultado = calcular_gordura_corporal(
        peso_vivo=600.0,
        ecc=3.0
    )

    esperado = 490.2 * 0.188415

    assert resultado == pytest.approx(esperado)


def test_calcular_proteina_corporal():
    resultado = calcular_proteina_corporal(
        peso_vivo=600.0,
        ecc=3.0
    )

    esperado = 490.2 * 0.167505

    assert resultado == pytest.approx(esperado)


def test_gordura_corporal_peso_negativo():
    with pytest.raises(ValueError):
        calcular_gordura_corporal(-100.0, 3.0)


def test_proteina_corporal_peso_negativo():
    with pytest.raises(ValueError):
        calcular_proteina_corporal(-100.0, 3.0)


def test_gordura_corporal_ecc_invalido():
    with pytest.raises(ValueError):
        calcular_gordura_corporal(600.0, 6.0)


def test_proteina_corporal_ecc_invalido():
    with pytest.raises(ValueError):
        calcular_proteina_corporal(600.0, 0.0)


def test_peso_corporal_vazio_mesmo_ecc():
    resultado = calcular_peso_corporal_vazio_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=3.0
    )

    assert resultado == pytest.approx(490.2)


def test_peso_corporal_vazio_reposicao():
    resultado = calcular_peso_corporal_vazio_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=2.5,
        ecc_desejado=3.0
    )

    esperado = 490.2 / (1 - 0.137 * 0.5)

    assert resultado == pytest.approx(esperado)


def test_peso_corporal_vazio_mobilizacao():
    resultado = calcular_peso_corporal_vazio_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=2.5
    )

    esperado = 490.2 * (1 - 0.137 * 0.5)

    assert resultado == pytest.approx(esperado)


def test_peso_corporal_vazio_ecc_invalido():
    with pytest.raises(ValueError):
        calcular_peso_corporal_vazio_por_ecc(
            peso_vivo_atual=600.0,
            ecc_atual=6.0,
            ecc_desejado=3.0
        )



def test_variacao_tecidos_mesmo_ecc():
    resultado = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=3.0
    )

    assert resultado["variacao_gordura_kg"] == pytest.approx(0.0)
    assert resultado["variacao_proteina_kg"] == pytest.approx(0.0)


def test_variacao_tecidos_reposicao():
    resultado = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=2.5,
        ecc_desejado=3.0
    )

    assert resultado["variacao_gordura_kg"] > 0
    assert resultado["variacao_proteina_kg"] > 0


def test_variacao_tecidos_mobilizacao():
    resultado = calcular_variacao_tecidos_por_ecc(
        peso_vivo_atual=600.0,
        ecc_atual=3.0,
        ecc_desejado=2.5
    )

    assert resultado["variacao_gordura_kg"] < 0
    assert resultado["variacao_proteina_kg"] < 0


def test_variacao_tecidos_ecc_invalido():
    with pytest.raises(ValueError):
        calcular_variacao_tecidos_por_ecc(
            peso_vivo_atual=600.0,
            ecc_atual=2.5,
            ecc_desejado=6.0
        )
