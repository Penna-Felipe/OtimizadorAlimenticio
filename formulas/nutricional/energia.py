
"""
Módulo: energia.py

Responsável por calcular a exigência de energia líquida
de lactação (NEL).

Unidades:
- Peso vivo: kg
- Produção de leite: kg/dia
- Gordura do leite: %
- Proteína verdadeira do leite: %
- Lactose do leite: %
- NEL do leite: Mcal/kg
- NEL de manutenção: Mcal/dia
- NEL total: Mcal/dia
"""

def calcular_nel_leite(
    taxa_gordura: float,
    proteina_verdadeira: float,
    taxa_lactose: float
) -> float:
    """
    Calcula a energia líquida por kg de leite.

    Fórmula:
        NEL_leite = 0.0929 * G + 0.0547 * P + 0.0395 * L

    Args:
        taxa_gordura: Percentual de gordura do leite.
        proteina_verdadeira: Percentual de proteína verdadeira.
        taxa_lactose: Percentual de lactose do leite.

    Returns:
        Energia líquida do leite em Mcal/kg.
    """

    for nome, valor in (
        ("Gordura", taxa_gordura),
        ("Proteína verdadeira", proteina_verdadeira),
        ("Lactose", taxa_lactose)
    ):
        if not 0 <= valor <= 100:
            raise ValueError(
                f"O percentual de {nome} deve estar entre 0 e 100."
            )

    nel_leite = (
        0.0929 * taxa_gordura
        + 0.0547 * proteina_verdadeira
        + 0.0395 * taxa_lactose
    )

    return nel_leite


def calcular_nel_manutencao(peso_vivo: float) -> float:
    """
    Calcula a energia líquida necessária para manutenção.

    Fórmula:
        NEL_manutencao = 0.08 * BW^0.75

    Args:
        peso_vivo: Peso vivo do animal em kg.

    Returns:
        Energia líquida de manutenção em Mcal/dia.
    """

    if peso_vivo <= 0:
        raise ValueError("O peso vivo deve ser maior que zero.")

    return 0.08 * (peso_vivo ** 0.75)


def calcular_nel_exigido(
    producao_leite: float,
    nel_leite: float,
    nel_manutencao: float
) -> float:
    """
    Calcula a energia líquida total exigida.

    Fórmula:
        NEL_total = PL * NEL_leite + NEL_manutencao

    Args:
        producao_leite: Produção de leite em kg/dia.
        nel_leite: Energia líquida por kg de leite (Mcal/kg).
        nel_manutencao: Energia de manutenção (Mcal/dia).

    Returns:
        Energia líquida total exigida em Mcal/dia.
    """

    if producao_leite < 0:
        raise ValueError("A produção de leite não pode ser negativa.")

    if nel_leite < 0:
        raise ValueError("NEL do leite não pode ser negativa.")

    if nel_manutencao < 0:
        raise ValueError("NEL de manutenção não pode ser negativa.")

    return (
        producao_leite * nel_leite
        + nel_manutencao
    )


def calcular_energia(
    peso_vivo: float,
    producao_leite: float,
    taxa_gordura: float,
    proteina_verdadeira: float,
    taxa_lactose: float
) -> dict:
    """
    Calcula as exigências de energia líquida do animal.

    Etapas:
        1. Calcula a NEL por kg de leite.
        2. Calcula a NEL de manutenção.
        3. Calcula a NEL total exigida.

    Returns:
        Dicionário contendo os resultados em Mcal/kg
        e Mcal/dia.
    """

    nel_leite = calcular_nel_leite(
        taxa_gordura,
        proteina_verdadeira,
        taxa_lactose
    )

    nel_manutencao = calcular_nel_manutencao(
        peso_vivo
    )

    nel_total = calcular_nel_exigido(
        producao_leite,
        nel_leite,
        nel_manutencao
    )

    return {
        "nel_leite_mcal_kg": nel_leite,
        "nel_manutencao_mcal_dia": nel_manutencao,
        "nel_producao_mcal_dia": producao_leite * nel_leite,
        "nel_total_mcal_dia": nel_total
    }
