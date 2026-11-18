
"""
Submódulo: atividade.py

Calcula a exigência adicional de energia associada
à atividade física de vacas leiteiras.

Referência:
    NRC (2001).
    Nutrient Requirements of Dairy Cattle.
    7th Revised Edition.

Componentes considerados:
    - Caminhada horizontal adicional.
    - Atividade de pastejo.
    - Ajuste para terreno montanhoso.

Unidades:
    Peso vivo: kg
    Distância: km/dia
    Energia adicional: Mcal/dia

Observações:
    A energia de manutenção já contempla a atividade
    habitual prevista pelo modelo.

    Os ajustes de pastejo e terreno representam
    cenários específicos, não uma estimativa universal
    para qualquer sistema de produção.
"""

import math

from nutricional.validacoes import validar_nao_negativo


def calcular_energia_atividade(
    peso_vivo: float,
    distancia_km_dia: float = 0.0,
    pastejo: bool = False,
    terreno_montanhoso: bool = False
) -> float:
    """
    Calcula a exigência energética adicional de atividade.

    Referência:
        NRC (2001), Activity Requirements.

    Equações:
        Caminhada = 0.00045 * BW * distância

        Pastejo = 0.0012 * BW

        Terreno montanhoso = 0.006 * BW

    Parâmetros:
        peso_vivo (float):
            Peso corporal do animal (kg).

        distancia_km_dia (float):
            Distância horizontal adicional percorrida
            diariamente (km/dia).

        pastejo (bool):
            Indica se o ajuste de pastejo deve ser aplicado.

        terreno_montanhoso (bool):
            Indica se o ajuste adicional de terreno
            montanhoso deve ser aplicado.

    Retorna:
        float:
            Energia adicional de atividade (Mcal/dia).

    Exceções:
        ValueError:
            Para peso inválido, distância negativa
            ou terreno montanhoso sem pastejo.

        TypeError:
            Para indicadores que não sejam booleanos.
    """

    # Valida o peso corporal.
    if not math.isfinite(peso_vivo) or peso_vivo <= 0:
        raise ValueError(
            "O peso vivo deve ser finito e maior que zero."
        )

    # A distância não pode ser negativa ou não finita.
    validar_nao_negativo(
        "Distância percorrida",
        distancia_km_dia
    )

    # Garante que os indicadores sejam booleanos.
    if not isinstance(pastejo, bool):
        raise TypeError("pastejo deve ser booleano.")

    if not isinstance(terreno_montanhoso, bool):
        raise TypeError(
            "terreno_montanhoso deve ser booleano."
        )

    # O ajuste de terreno montanhoso foi definido
    # para o cenário de pastejo.
    if terreno_montanhoso and not pastejo:
        raise ValueError(
            "O ajuste de terreno montanhoso exige pastejo."
        )

    # Energia para caminhada horizontal adicional.
    energia_caminhada = (
        0.00045 * peso_vivo * distancia_km_dia
    )

    # Energia associada à atividade de pastejo.
    energia_pastejo = (
        0.0012 * peso_vivo if pastejo else 0.0
    )

    # Ajuste adicional para terreno montanhoso.
    energia_terreno = (
        0.006 * peso_vivo
        if terreno_montanhoso else 0.0
    )

    # Soma dos componentes adicionais.
    energia_total = (
        energia_caminhada
        + energia_pastejo
        + energia_terreno
    )

    return energia_total
