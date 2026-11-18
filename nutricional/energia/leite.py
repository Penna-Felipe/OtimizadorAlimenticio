
"""
Submódulo: leite.py

Responsável pelo cálculo da energia líquida associada
à produção de leite em vacas leiteiras.

Referência:
    NRC (2001).
    Nutrient Requirements of Dairy Cattle.
    7th Revised Edition.

Equações implementadas:
    1. Energia líquida por quilograma de leite.
    2. Energia diária necessária para lactação.

Unidades:
    Produção de leite: kg/dia
    Gordura do leite: %
    Proteína verdadeira do leite: %
    Lactose do leite: %
    Energia do leite: Mcal/kg
    Energia de lactação: Mcal/dia

Observações:
    - As porcentagens devem ser informadas como
      números percentuais (ex.: 3.5 para 3.5%).
    - Utiliza proteína verdadeira, não proteína bruta.
    - Não calcula manutenção, gestação ou crescimento.
"""

from nutricional.validacoes import (
    validar_nao_negativo,
    validar_percentual,
)


def calcular_nel_leite(
    taxa_gordura: float,
    proteina_verdadeira: float,
    taxa_lactose: float
) -> float:
    """
    Calcula a energia líquida contida em 1 kg de leite.

    Referência:
        NRC (2001), sistema de energia líquida
        para vacas leiteiras.

    Equação:
        NEL = 0.0929*G + 0.0563*P + 0.0395*L

    Variáveis:
        G: Porcentagem de gordura do leite.
        P: Porcentagem de proteína verdadeira.
        L: Porcentagem de lactose.

    Parâmetros:
        taxa_gordura (float):
            Teor de gordura do leite (%).

        proteina_verdadeira (float):
            Teor de proteína verdadeira do leite (%).

        taxa_lactose (float):
            Teor de lactose do leite (%).

    Retorna:
        float:
            Energia líquida do leite (Mcal/kg).

    Exceções:
        ValueError:
            Quando algum percentual é inválido.

    Exemplo:
        >>> calcular_nel_leite(3.5, 3.2, 4.8)
        0.69491
    """

    # Valida os componentes informados em porcentagem.
    validar_percentual("Gordura", taxa_gordura)
    validar_percentual(
        "Proteína verdadeira",
        proteina_verdadeira
    )
    validar_percentual("Lactose", taxa_lactose)

    # Soma as contribuições energéticas de cada
    # componente do leite.
    nel_leite = (
        0.0929 * taxa_gordura
        + 0.0563 * proteina_verdadeira
        + 0.0395 * taxa_lactose
    )

    return nel_leite


def calcular_energia_lactacao(
    producao_leite: float,
    nel_leite: float
) -> float:
    """
    Calcula a exigência diária de energia para lactação.

    Equação:
        Energia_lactacao = PL * NEL_leite

    Variáveis:
        PL: Produção diária de leite (kg/dia).
        NEL_leite: Energia líquida por kg de leite.

    Parâmetros:
        producao_leite (float):
            Produção diária de leite (kg/dia).

        nel_leite (float):
            Energia líquida do leite (Mcal/kg).

    Retorna:
        float:
            Energia diária para lactação (Mcal/dia).

    Exceções:
        ValueError:
            Quando algum parâmetro é inválido.

    Exemplo:
        >>> calcular_energia_lactacao(35, 0.69491)
        24.32185
    """

    # A produção e a energia por kg não podem
    # assumir valores negativos ou não finitos.
    validar_nao_negativo(
        "Produção de leite",
        producao_leite
    )
    validar_nao_negativo(
        "Energia líquida do leite",
        nel_leite
    )

    # Multiplica a produção diária pela energia
    # contida em cada quilograma de leite.
    return producao_leite * nel_leite
