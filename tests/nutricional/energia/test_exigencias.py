
import pytest

from nutricional.energia import calcular_energia


def test_energia_completa_parcial():
    """
    Verifica a soma das exigências de manutenção
    e lactação, sem atividade adicional.
    """

    resultado = calcular_energia(
        peso_vivo=600,
        producao_leite=35,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8
    )

    energia_manutencao = 0.08 * 600 ** 0.75
    energia_lactacao = 35 * 0.69491

    esperado = energia_manutencao + energia_lactacao

    assert resultado[
        "energia_total_parcial_mcal_dia"
    ] == pytest.approx(esperado)


def test_energia_com_atividade():
    """
    Verifica a integração de manutenção,
    lactação e atividade física.
    """

    resultado = calcular_energia(
        peso_vivo=600,
        producao_leite=35,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8,
        distancia_km_dia=2.0,
        pastejo=True
    )

    assert resultado[
        "energia_atividade_mcal_dia"
    ] == pytest.approx(1.26)

    esperado = (
        resultado["energia_manutencao_mcal_dia"]
        + resultado["energia_lactacao_mcal_dia"]
        + resultado["energia_atividade_mcal_dia"]
    )

    assert resultado[
        "energia_total_parcial_mcal_dia"
    ] == pytest.approx(esperado)


def test_energia_producao_zero():
    """
    Uma vaca sem produção de leite não deve
    apresentar exigência energética de lactação.
    """

    resultado = calcular_energia(
        peso_vivo=600,
        producao_leite=0,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8
    )

    assert resultado[
        "energia_lactacao_mcal_dia"
    ] == pytest.approx(0.0)

    assert resultado[
        "energia_total_parcial_mcal_dia"
    ] == pytest.approx(
        resultado["energia_manutencao_mcal_dia"]
    )


def test_energia_peso_invalido():
    """Verifica a propagação de erros de validação."""

    with pytest.raises(ValueError):
        calcular_energia(
            peso_vivo=-600,
            producao_leite=35,
            taxa_gordura=3.5,
            proteina_verdadeira=3.2,
            taxa_lactose=4.8
        )


def test_energia_com_gestacao():
    """Verifica a integração da energia gestacional."""

    resultado = calcular_energia(
        peso_vivo=600,
        producao_leite=35,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8,
        dias_gestacao=250,
        peso_bezerro_nascimento=45
    )

    energia_gestacao_esperada = 0.7598 / 0.218

    assert resultado[
        "energia_gestacao_mcal_dia"
    ] == pytest.approx(energia_gestacao_esperada)

    energia_total_esperada = (
        resultado["energia_manutencao_mcal_dia"]
        + resultado["energia_lactacao_mcal_dia"]
        + resultado["energia_atividade_mcal_dia"]
        + energia_gestacao_esperada
    )

    assert resultado[
        "energia_total_parcial_mcal_dia"
    ] == pytest.approx(energia_total_esperada)


def test_energia_sem_gestacao():
    """Verifica compatibilidade com animais não gestantes."""

    resultado = calcular_energia(
        peso_vivo=600,
        producao_leite=35,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8
    )

    assert resultado[
        "energia_gestacao_mcal_dia"
    ] == pytest.approx(0.0)



def test_energia_com_crescimento():
    """
    Verifica a integração da energia de crescimento
    sem misturar EM com o total de NEL.
    """

    resultado = calcular_energia(
        peso_vivo=500,
        producao_leite=30,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8,
        peso_adulto=650,
        ganho_peso_reduzido=0.8
    )

    energia_retida = (
        resultado["energia_retida_crescimento_mcal_dia"]
    )

    energia_metabolizavel = (
        resultado["energia_metabolizavel_crescimento_mcal_dia"]
    )

    assert energia_retida > 0

    assert energia_metabolizavel == pytest.approx(
        energia_retida / 0.40
    )

    # O crescimento não deve alterar a soma
    # dos componentes expressos em NEL.
    assert resultado["energia_total_parcial_mcal_dia"] == (
        pytest.approx(
            resultado["energia_manutencao_mcal_dia"]
            + resultado["energia_lactacao_mcal_dia"]
            + resultado["energia_atividade_mcal_dia"]
            + resultado["energia_gestacao_mcal_dia"]
        )
    )


def test_energia_sem_crescimento():
    """
    Verifica que, sem crescimento planejado,
    não existe exigência adicional de crescimento.
    """

    resultado = calcular_energia(
        peso_vivo=500,
        producao_leite=30,
        taxa_gordura=3.5,
        proteina_verdadeira=3.2,
        taxa_lactose=4.8
    )

    assert (
        resultado["energia_retida_crescimento_mcal_dia"]
        == 0.0
    )

    assert (
        resultado["energia_metabolizavel_crescimento_mcal_dia"]
        == 0.0
    )


def test_crescimento_sem_peso_adulto():
    """
    Verifica que o peso adulto é obrigatório
    quando existe crescimento planejado.
    """

    with pytest.raises(ValueError):
        calcular_energia(
            peso_vivo=500,
            producao_leite=30,
            taxa_gordura=3.5,
            proteina_verdadeira=3.2,
            taxa_lactose=4.8,
            ganho_peso_reduzido=0.8
        )

