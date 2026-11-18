
import pytest

from nutricional.energia import calcular_energia_atividade


def test_atividade_confinamento():
    resultado = calcular_energia_atividade(600)
    assert resultado == pytest.approx(0.0)


def test_atividade_caminhada():
    resultado = calcular_energia_atividade(
        peso_vivo=600,
        distancia_km_dia=2.0
    )
    assert resultado == pytest.approx(0.54)


def test_atividade_pastejo():
    resultado = calcular_energia_atividade(
        peso_vivo=600,
        distancia_km_dia=2.0,
        pastejo=True
    )
    assert resultado == pytest.approx(1.26)


def test_atividade_terreno_montanhoso():
    resultado = calcular_energia_atividade(
        peso_vivo=600,
        distancia_km_dia=2.0,
        pastejo=True,
        terreno_montanhoso=True
    )
    assert resultado == pytest.approx(4.86)


def test_distancia_negativa():
    with pytest.raises(ValueError):
        calcular_energia_atividade(
            peso_vivo=600,
            distancia_km_dia=-2
        )


def test_montanhoso_sem_pastejo():
    with pytest.raises(ValueError):
        calcular_energia_atividade(
            peso_vivo=600,
            terreno_montanhoso=True
        )


def test_pastejo_invalido():
    with pytest.raises(TypeError):
        calcular_energia_atividade(
            peso_vivo=600,
            pastejo=1
        )
