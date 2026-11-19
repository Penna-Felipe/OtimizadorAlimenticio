
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

from .ecc import (
    validar_ecc,
    calcular_ecc_escala_9,
    calcular_proporcao_gordura,
    calcular_proporcao_proteina,
    calcular_peso_corporal_vazio,
    calcular_gordura_corporal,
    calcular_proteina_corporal,
    calcular_peso_corporal_vazio_por_ecc,
    calcular_variacao_tecidos_por_ecc,
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
    "validar_ecc",
    "calcular_ecc_escala_9",
    "calcular_proporcao_gordura",
    "calcular_proporcao_proteina",
    "calcular_peso_corporal_vazio",
    "calcular_gordura_corporal",
    "calcular_proteina_corporal",
    "calcular_peso_corporal_vazio_por_ecc",
    "calcular_variacao_tecidos_por_ecc",
]