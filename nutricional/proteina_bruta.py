
"""
Módulo: proteina_bruta.py

Responsável por calcular a exigência de proteína bruta
de vacas leiteiras.

Unidades:
- Peso vivo: kg
- Produção de leite: kg/dia
- Proteína verdadeira: %
- Proteína metabolizada: g/dia
- Proteína bruta exigida: g/dia
"""


def calcular_mp_manutencao(peso_vivo: float) -> float:
    """
    Calcula a exigência de proteína metabolizada
    para manutenção do animal.

    Fórmula:
        MPManutenção = 3.8 * BW^0.75

    Args:
        peso_vivo: Peso vivo do animal em kg.

    Returns:
        Exigência de proteína metabolizada em g/dia.
    """

    if peso_vivo <= 0:
        raise ValueError("O peso vivo deve ser maior que zero.")

    return 3.8 * (peso_vivo ** 0.75)


def calcular_yprot(
    producao_leite: float,
    proteina_verdadeira: float
) -> float:
    """
    Calcula a exigência líquida de proteína para
    produção de leite.

    Fórmula:
        Yprot = ProduçãoLeite * ProteínaVerdadeira / 100

    Args:
        producao_leite: Produção de leite em kg/dia.
        proteina_verdadeira: Percentual de proteína verdadeira.

    Returns:
        Proteína líquida em kg/dia.
    """

    if producao_leite < 0:
        raise ValueError("A produção de leite não pode ser negativa.")

    if not 0 <= proteina_verdadeira <= 100:
        raise ValueError("Percentual de proteína inválido.")

    return producao_leite * (proteina_verdadeira / 100)


def calcular_mp_lactacao(yprot: float, eficiencia: float = 0.67) -> float:
    """
    Calcula a proteína metabolizada necessária para lactação.

    Fórmula:
        MPLact = (Yprot / eficiência) * 1000

    Args:
        yprot: Proteína líquida para produção de leite (kg/dia).
        eficiencia: Eficiência de utilização da proteína metabolizada.

    Returns:
        Proteína metabolizada em g/dia.
    """

    if yprot < 0:
        raise ValueError("Yprot não pode ser negativo.")

    if not 0 < eficiencia <= 1:
        raise ValueError("A eficiência deve estar entre 0 e 1.")

    return (yprot / eficiencia) * 1000


def calcular_proteina_bruta(
    peso_vivo: float,
    producao_leite: float,
    proteina_verdadeira: float,
    eficiencia_pb_mp: float = 0.64,
    eficiencia_lactacao: float = 0.67
) -> dict:
    """
    Calcula a exigência total de proteína bruta do animal.

    Etapas:
        1. Calcula MP de manutenção.
        2. Calcula Yprot.
        3. Calcula MP de lactação.
        4. Soma as exigências de MP.
        5. Converte MP total em PB exigida.

    Fórmula:
        MPTotal = MPManutenção + MPLactação

        PBExigida = MPTotal / EficiênciaPB_MP

    Returns:
        Dicionário contendo os resultados dos cálculos em g/dia.
    """

    if not 0 < eficiencia_pb_mp <= 1:
        raise ValueError("A eficiência PB -> MP deve estar entre 0 e 1.")

    mp_manutencao = calcular_mp_manutencao(peso_vivo)

    yprot = calcular_yprot(
        producao_leite,
        proteina_verdadeira
    )

    mp_lactacao = calcular_mp_lactacao(
        yprot,
        eficiencia_lactacao
    )

    mp_total = mp_manutencao + mp_lactacao

    pb_exigida = mp_total / eficiencia_pb_mp

    return {
        "mp_manutencao_g_dia": mp_manutencao,
        "yprot_kg_dia": yprot,
        "mp_lactacao_g_dia": mp_lactacao,
        "mp_total_g_dia": mp_total,
        "pb_exigida_g_dia": pb_exigida
    }
