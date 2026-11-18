
"""
Submódulo: manutencao.py

Responsável pelo cálculo da exigência de energia
líquida de manutenção em vacas leiteiras.

Referência:
    NRC (2001).
    Nutrient Requirements of Dairy Cattle.
    7th Revised Edition.

Equação implementada:
    NEm = 0.08 * BW ** 0.75

Unidades:
    Peso vivo: kg
    Energia de manutenção: Mcal/dia

Observações:
    - Utiliza o peso metabólico (BW ** 0.75).
    - Não considera produção de leite, gestação
      ou crescimento.
    - A equação já contempla a atividade habitual
      considerada no modelo de manutenção.
"""

import math


def calcular_energia_manutencao(
    peso_vivo: float
) -> float:
    """
    Calcula a exigência diária de energia líquida
    para manutenção do animal.

    Referência:
        NRC (2001).

    Equação:
        NEm = 0.08 * BW ** 0.75

    Variáveis:
        NEm:
            Energia líquida de manutenção (Mcal/dia).

        BW:
            Peso vivo do animal (kg).

        BW ** 0.75:
            Peso metabólico do animal.

    Parâmetros:
        peso_vivo (float):
            Peso corporal do animal em quilogramas.

    Retorna:
        float:
            Energia líquida de manutenção (Mcal/dia).

    Exceções:
        ValueError:
            Se o peso for zero, negativo ou não finito.
    """

    # O peso vivo deve ser positivo e finito.
    if not math.isfinite(peso_vivo) or peso_vivo <= 0:
        raise ValueError(
            "O peso vivo deve ser finito e maior que zero."
        )

    # Calcula o peso metabólico do animal.
    peso_metabolico = peso_vivo ** 0.75

    # Calcula a energia líquida de manutenção.
    energia_manutencao = 0.08 * peso_metabolico

    return energia_manutencao
