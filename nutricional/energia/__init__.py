
"""
Pacote de exigências energéticas.

Modelo nutricional:
    NRC (2001)

Disponibiliza uma interface pública para os cálculos
energéticos utilizados pela biblioteca nutricional.
"""

from .leite import (
    calcular_nel_leite,
    calcular_energia_lactacao,
)

from .gestacao import (
    calcular_energia_retida_gestacao,
    calcular_energia_metabolizavel_gestacao,
    calcular_energia_gestacao,
)

from .crescimento import (
    calcular_peso_reduzido,
    calcular_peso_equivalente,
    calcular_energia_retida_crescimento,
    calcular_energia_metabolizavel_crescimento,
)

from .reservas import (
    calcular_energia_reservas,
    calcular_energia_mobilizacao,
    calcular_energia_reposicao,
)

from .manutencao import calcular_energia_manutencao

from .atividade import calcular_energia_atividade

from .exigencias import calcular_energia

__all__ = [
    "calcular_nel_leite",
    "calcular_energia_lactacao",
    "calcular_energia_manutencao",
    "calcular_energia_atividade",
    "calcular_energia_retida_gestacao",
    "calcular_energia_metabolizavel_gestacao",
    "calcular_energia_gestacao",
    "calcular_energia",
    "calcular_peso_reduzido",
    "calcular_peso_equivalente",
    "calcular_energia_retida_crescimento",
    "calcular_energia_metabolizavel_crescimento",
    "calcular_energia_reservas",
    "calcular_energia_mobilizacao",
    "calcular_energia_reposicao",
]
