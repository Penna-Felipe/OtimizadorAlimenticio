
"""
Submódulo: gestacao.py

Calcula as exigências energéticas associadas
à gestação de vacas leiteiras.

Referência:
    NRC (2001).
    Nutrient Requirements of Dairy Cattle.
    7th Revised Edition.

Equações:
    ER = (0.00318 * D - 0.0352) * (CBW / 45)

    ME = ER / 0.14

    NEL = ME * 0.64

Unidades:
    D: dias de gestação
    CBW: peso esperado do bezerro (kg)
    ER: energia retida (Mcal/dia)
    ME: energia metabolizável (Mcal/dia)
    NEL: equivalente em energia líquida
         de lactação (Mcal/dia)

Limitações:
    - Modelo NRC (2001).
    - Exigência adicional considerada a partir
      do dia 190 de gestação.
    - Gestação limitada a 279 dias neste modelo.
"""

import math

from nutricional.validacoes import validar_nao_negativo


def calcular_energia_retida_gestacao(
    dias_gestacao: int,
    peso_bezerro_nascimento: float
) -> float:
    """
    Calcula a energia diariamente retida na gestação.

    Parâmetros:
        dias_gestacao (int):
            Dias decorridos desde a concepção.

        peso_bezerro_nascimento (float):
            Peso esperado do bezerro ao nascer (kg).

    Retorna:
        float:
            Energia retida (Mcal/dia).

    Observação:
        O NRC (2001) não contabiliza exigência
        adicional antes do dia 190.
    """

    # Valida o número de dias de gestação.
    if (
        isinstance(dias_gestacao, bool)
        or not isinstance(dias_gestacao, int)
        or not 0 <= dias_gestacao <= 279
    ):
        raise ValueError(
            "Dias de gestação devem ser um inteiro "
            "entre 0 e 279."
        )

    # Valida o peso esperado do bezerro.
    validar_nao_negativo(
        "Peso esperado do bezerro",
        peso_bezerro_nascimento
    )

    if peso_bezerro_nascimento == 0:
        raise ValueError(
            "O peso esperado do bezerro deve ser "
            "maior que zero."
        )

    # O modelo NRC (2001) considera exigência
    # adicional somente a partir do dia 190.
    if dias_gestacao < 190:
        return 0.0

    # Calcula a energia retida diariamente
    # nos tecidos associados à gestação.
    energia_retida = (
        (0.00318 * dias_gestacao - 0.0352)
        * (peso_bezerro_nascimento / 45)
    )

    return energia_retida


def calcular_energia_metabolizavel_gestacao(
    energia_retida: float
) -> float:
    """
    Converte a energia retida na gestação
    em exigência de energia metabolizável.

    Eficiência de utilização:
        0.14 (NRC, 2001).

    Retorna:
        Energia metabolizável (Mcal/dia).
    """

    validar_nao_negativo(
        "Energia retida",
        energia_retida
    )

    return energia_retida / 0.14


def calcular_energia_gestacao(
    dias_gestacao: int,
    peso_bezerro_nascimento: float
) -> float:
    """
    Calcula a exigência energética da gestação
    expressa em energia líquida de lactação (NEL).

    Referência:
        NRC (2001), equação 2-19.

    Equação:
        NEL = ER / 0.218

    Onde:
        ER: energia retida na gestação (Mcal/dia).

    Parâmetros:
        dias_gestacao (int):
            Dias decorridos desde a concepção.

        peso_bezerro_nascimento (float):
            Peso esperado do bezerro ao nascer (kg).

    Retorna:
        float:
            Exigência de gestação em Mcal NEL/dia.

    Observações:
        - Aplica o modelo NRC (2001).
        - Antes de 190 dias, retorna zero.
        - Usa o denominador publicado na equação 2-19.
    """

    # Calcula a energia retida na gestação.
    energia_retida = calcular_energia_retida_gestacao(
        dias_gestacao,
        peso_bezerro_nascimento
    )

    # Converte a energia retida para o equivalente
    # em energia líquida de lactação (NRC, 2001).
    energia_nel = energia_retida / 0.218

    return energia_nel
