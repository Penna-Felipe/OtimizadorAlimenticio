def calcular_fibra_det_neutro(
    materia_seca: float,
    percentual_fdn: float = 29.0
) -> float:
    """
        Calcula a quantidade mínima de FDN na dieta.

        materia_seca: Consumo de matéria seca (kg/dia).
        percentual_fdn: Percentual mínimo de FDN na MS.
    """
    if materia_seca < 0:
        raise ValueError("A matéria seca não pode ser negativa.")

    if not 0 <= percentual_fdn <= 100:
        raise ValueError("O percentual de FDN deve estar entre 0 e 100.")

    return materia_seca * (percentual_fdn / 100)