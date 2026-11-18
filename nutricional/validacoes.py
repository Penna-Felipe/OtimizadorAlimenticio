
"""
Módulo: validacoes.py

Funções auxiliares para validação de parâmetros
utilizados nos cálculos nutricionais.
"""

import math


def validar_nao_negativo(
    nome: str,
    valor: float
) -> None:
    """
    Verifica se um valor numérico é finito e não negativo.

    Lança:
        ValueError: Se o valor for negativo, NaN ou infinito.
    """
    if not math.isfinite(valor) or valor < 0:
        raise ValueError(
            f"{nome} deve ser finito e não negativo."
        )


def validar_percentual(
    nome: str,
    valor: float
) -> None:
    """
    Verifica se um percentual está no intervalo [0, 100].

    Lança:
        ValueError: Se o percentual estiver fora do
        intervalo ou não for finito.
    """
    if not math.isfinite(valor) or not 0 <= valor <= 100:
        raise ValueError(
            f"{nome} deve estar entre 0 e 100%."
        )
