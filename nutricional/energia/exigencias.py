
"""
Submódulo: exigencias.py

Responsável por consolidar as exigências energéticas
de vacas leiteiras, utilizando os submódulos de energia.

Modelo nutricional:
    NRC (2001)

Componentes implementados:
    1. Energia líquida de manutenção.
    2. Energia líquida para lactação.
    3. Energia adicional de atividade física.

Componentes futuros:
    - Gestação.
    - Crescimento.
    - Mobilização e deposição de reservas corporais.

Unidades:
    Peso vivo: kg
    Produção de leite: kg/dia
    Componentes do leite: %
    Distância adicional: km/dia
    Energia: Mcal/dia

Observação:
    A função não implementa diretamente as equações
    nutricionais. Ela utiliza os submódulos responsáveis
    por cada componente energético.
"""

from .leite import (
    calcular_nel_leite,
    calcular_energia_lactacao,
)

from .crescimento import (
    calcular_energia_retida_crescimento,
    calcular_energia_metabolizavel_crescimento,
)

from .constantes_nrc import EFICIENCIA_GANHO_NRC2001

from .manutencao import calcular_energia_manutencao

from .atividade import calcular_energia_atividade

from .gestacao import calcular_energia_gestacao

from nutricional.validacoes import validar_nao_negativo


def calcular_energia(
    peso_vivo: float,
    producao_leite: float,
    taxa_gordura: float,
    proteina_verdadeira: float,
    taxa_lactose: float,
    distancia_km_dia: float = 0.0,
    pastejo: bool = False,
    terreno_montanhoso: bool = False,
    dias_gestacao: int = 0,
    peso_bezerro_nascimento: float = 45.0,
    peso_adulto: float | None = None,
    ganho_peso_reduzido: float = 0.0,
) -> dict:
    """
    Consolida as exigências energéticas parciais.

    Parâmetros:
        peso_vivo (float):
            Peso corporal do animal (kg).

        producao_leite (float):
            Produção diária de leite (kg/dia).

        taxa_gordura (float):
            Teor de gordura do leite (%).

        proteina_verdadeira (float):
            Teor de proteína verdadeira do leite (%).

        taxa_lactose (float):
            Teor de lactose do leite (%).

        distancia_km_dia (float):
            Distância horizontal adicional (km/dia).

        pastejo (bool):
            Indica aplicação do ajuste de pastejo.

        terreno_montanhoso (bool):
            Indica aplicação do ajuste de terreno
            montanhoso.

    Retorna:
        dict:
            modelo:
                Identificação do modelo nutricional.

            nel_leite_mcal_kg:
                Energia líquida por kg de leite.

            energia_manutencao_mcal_dia:
                Exigência de manutenção.

            energia_lactacao_mcal_dia:
                Exigência de lactação.

            energia_atividade_mcal_dia:
                Exigência adicional de atividade.

            energia_total_parcial_mcal_dia:
                Soma dos componentes implementados.

    Observação:
        Não representa a exigência energética completa
        de todos os estados fisiológicos do animal.
    """

    # 1. Calcula a energia líquida por kg de leite.
    nel_leite = calcular_nel_leite(
        taxa_gordura,
        proteina_verdadeira,
        taxa_lactose
    )

    # 2. Calcula a energia diária para lactação.
    energia_lactacao = calcular_energia_lactacao(
        producao_leite,
        nel_leite
    )

    # 3. Calcula a energia basal de manutenção.
    energia_manutencao = calcular_energia_manutencao(
        peso_vivo
    )

    # 4. Calcula a energia adicional de atividade.
    energia_atividade = calcular_energia_atividade(
        peso_vivo,
        distancia_km_dia,
        pastejo,
        terreno_montanhoso
    )

    # 5. Calcula a exigência energética de gestação.
    # Para animais não gestantes, dias_gestacao=0
    # resulta em exigência adicional igual a zero.
    energia_gestacao = calcular_energia_gestacao(
        dias_gestacao,
        peso_bezerro_nascimento
    )

    # 6. Consolida as exigências implementadas.
    energia_total = (
        energia_manutencao
        + energia_lactacao
        + energia_atividade
        + energia_gestacao
    )

    # 7. Calculo para exigencia de crescimento
    # Inicialmente, considera que não existe
    # crescimento corporal planejado.
    energia_retida_crescimento = 0.0
    energia_metabolizavel_crescimento = 0.0

    # Verifica se o ganho de peso informado é válido.
    validar_nao_negativo(
        "ganho_peso_reduzido",
        ganho_peso_reduzido
    )

    # Calcula a exigência de crescimento somente
    # quando existe ganho de peso planejado.
    if ganho_peso_reduzido > 0:

        if peso_adulto is None:
            raise ValueError(
                "O peso adulto deve ser informado "
                "quando houver crescimento."
            )

        # Energia armazenada nos novos tecidos.
        energia_retida_crescimento = (
            calcular_energia_retida_crescimento(
                peso_vivo=peso_vivo,
                peso_adulto=peso_adulto,
                ganho_peso_reduzido=ganho_peso_reduzido
            )
        )

        # Energia metabolizável necessária para
        # sustentar o crescimento planejado.
        energia_metabolizavel_crescimento = (
            calcular_energia_metabolizavel_crescimento(
                energia_retida=energia_retida_crescimento,
                eficiencia_ganho=EFICIENCIA_GANHO_NRC2001
            )
        )

    # 8. Retorna os componentes separadamente.
    return {
        "nel_leite_mcal_kg": nel_leite,
        "energia_manutencao_mcal_dia": energia_manutencao,
        "energia_lactacao_mcal_dia": energia_lactacao,
        "energia_atividade_mcal_dia": energia_atividade,
        "energia_total_parcial_mcal_dia": energia_total,
        "energia_gestacao_mcal_dia": energia_gestacao,
        "energia_retida_crescimento_mcal_dia": energia_retida_crescimento,
        "energia_metabolizavel_crescimento_mcal_dia": energia_metabolizavel_crescimento,
    }
