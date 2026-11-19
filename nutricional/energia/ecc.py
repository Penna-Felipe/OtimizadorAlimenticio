
from nutricional.validacoes import validar_nao_negativo


def validar_ecc(ecc: float) -> None:
    """
    Valida o Escore de Condição Corporal (ECC).

    O ECC deve estar na escala de 1 a 5.

    Parâmetros:
        ecc (float):
            Escore de condição corporal.

    Retorna:
        None.

    Levanta:
        ValueError:
            Se o ECC estiver fora do intervalo
            permitido ou não for finito.
    """

    validar_nao_negativo("ecc", ecc)

    if not 1.0 <= ecc <= 5.0:
        raise ValueError(
            "O ECC deve estar entre 1 e 5."
        )


def calcular_ecc_escala_9(ecc: float) -> float:
    """
    Converte o ECC da escala 1-5 para 1-9.

    Referência:
        NRC (2001), equação 2-22.

    Equação:
        ECC_9 = 2 * (ECC_5 - 1) + 1

    Parâmetros:
        ecc (float):
            ECC na escala de 1 a 5.

    Retorna:
        float:
            ECC convertido para escala de 1 a 9.
    """

    validar_ecc(ecc)

    return 2 * (ecc - 1) + 1


def calcular_proporcao_gordura(ecc: float) -> float:
    """
    Estima a proporção de gordura no corpo vazio
    a partir do Escore de Condição Corporal.

    Referência:
        NRC 2001

    Equação:
        P_gordura = 0.037683 * ECC_9

    Parâmetros:
        ecc (float):
            ECC na escala de 1 a 5.

    Retorna:
        float:
            Proporção estimada de gordura corporal
            (kg de gordura/kg de corpo vazio).
    """

    ecc_9 = calcular_ecc_escala_9(ecc)

    return 0.037683 * ecc_9


def calcular_proporcao_proteina(ecc: float) -> float:
    """
    Estima a proporção de proteína no corpo vazio
    a partir do Escore de Condição Corporal.

    Referência:
        NRC 2001

    Equação:
        P_proteina = 0.200886 - 0.0066762 * ECC_9

    Parâmetros:
        ecc (float):
            ECC na escala de 1 a 5.

    Retorna:
        float:
            Proporção estimada de proteína corporal
            (kg de proteína/kg de corpo vazio).
    """

    ecc_9 = calcular_ecc_escala_9(ecc)

    return 0.200886 - 0.0066762 * ecc_9


def calcular_peso_corporal_vazio(
    peso_vivo: float
) -> float:
    """
    Estima o peso corporal vazio (EBW) de bovinos leiteiros.

    Referência:
        NRC 2001

    Metodologia:
        O NRC utiliza duas etapas para estimar
        o peso corporal vazio:

        1. Peso vivo reduzido (SBW):
            SBW = 0.96 * BW

        2. Peso corporal vazio (EBW):
            EBW = 0.851 * SBW

        Combinando as duas equações:
            EBW = 0.96 * 0.851 * BW
            EBW = 0.81696 * BW

        Utiliza-se o coeficiente arredondado
        de 0.817.

    Parâmetros:
        peso_vivo (float):
            Peso vivo do animal (kg).

    Retorna:
        float:
            Peso corporal vazio estimado (kg).

    Observações:
        - O peso corporal vazio exclui o conteúdo
          gastrointestinal.
        - O coeficiente é uma aproximação e não
          representa uma medição direta.
        - A relação pode variar conforme a condição
          fisiológica e características do animal.
        - O resultado será utilizado posteriormente
          para estimar a composição corporal a
          partir do ECC.
    """

    validar_nao_negativo(
        "peso_vivo",
        peso_vivo
    )

    return 0.817 * peso_vivo


def calcular_gordura_corporal(
    peso_vivo: float,
    ecc: float
) -> float:
    """
    Estima a massa de gordura do corpo vazio.

    Referência:
        NRC

    Equação:
        Gordura = PCV * P_gordura

    Parâmetros:
        peso_vivo (float):
            Peso vivo do animal (kg).

        ecc (float):
            Escore de condição corporal,
            na escala de 1 a 5.

    Retorna:
        float:
            Massa estimada de gordura corporal (kg).

    Observações:
        - Utiliza o peso corporal vazio estimado.
        - A proporção de gordura depende do ECC.
        - Não representa exclusivamente a gordura
          disponível para mobilização.
    """

    peso_corporal_vazio = calcular_peso_corporal_vazio(
        peso_vivo
    )

    proporcao_gordura = calcular_proporcao_gordura(ecc)

    return peso_corporal_vazio * proporcao_gordura


def calcular_proteina_corporal(
    peso_vivo: float,
    ecc: float
) -> float:
    """
    Estima a massa de proteína do corpo vazio.

    Referência:
        NRC

    Equação:
        Proteína = PCV * P_proteina

    Parâmetros:
        peso_vivo (float):
            Peso vivo do animal (kg).

        ecc (float):
            Escore de condição corporal,
            na escala de 1 a 5.

    Retorna:
        float:
            Massa estimada de proteína corporal (kg).

    Observações:
        - Utiliza o peso corporal vazio estimado.
        - A proporção de proteína depende do ECC.
        - Não representa exclusivamente a proteína
          mobilizável pelo animal.
    """

    peso_corporal_vazio = calcular_peso_corporal_vazio(
        peso_vivo
    )

    proporcao_proteina = calcular_proporcao_proteina(ecc)

    return peso_corporal_vazio * proporcao_proteina


def calcular_peso_corporal_vazio_por_ecc(
    peso_vivo_atual: float,
    ecc_atual: float,
    ecc_desejado: float
) -> float:
    """
    Estima o peso corporal vazio correspondente
    a um ECC desejado.

    Referência:
        NRC (2001), capítulo 2.
        Relação aproximada de 13,7% de variação
        do peso corporal vazio por unidade de ECC,
        utilizando ECC 3 como referência.

    Parâmetros:
        peso_vivo_atual (float):
            Peso vivo atual da vaca (kg).

        ecc_atual (float):
            ECC observado atualmente (escala 1-5).

        ecc_desejado (float):
            ECC para o qual desejamos estimar
            o peso corporal vazio (escala 1-5).

    Retorna:
        float:
            Peso corporal vazio estimado no
            ECC desejado (kg).

    Observações:
        - O peso informado corresponde ao ECC atual.
        - O cálculo considera uma relação aproximada
          entre ECC e peso corporal vazio.
        - Não representa uma previsão temporal
          de ganho ou perda de peso.
    """

    peso_corporal_vazio_atual = (
        calcular_peso_corporal_vazio(peso_vivo_atual)
    )

    validar_ecc(ecc_atual)
    validar_ecc(ecc_desejado)

    fator_atual = 1 + 0.137 * (ecc_atual - 3)
    fator_desejado = 1 + 0.137 * (ecc_desejado - 3)

    peso_corporal_vazio_referencia = (
        peso_corporal_vazio_atual / fator_atual
    )

    return (
        peso_corporal_vazio_referencia
        * fator_desejado
    )


def calcular_variacao_tecidos_por_ecc(
    peso_vivo_atual: float,
    ecc_atual: float,
    ecc_desejado: float
) -> dict:
    """
    Estima a variação das massas de gordura e
    proteína corporal entre dois valores de ECC.

    Referência:
        Modelo de composição corporal baseado
        nas relações do NRC (2001).

    Parâmetros:
        peso_vivo_atual (float):
            Peso vivo observado no ECC atual (kg).

        ecc_atual (float):
            ECC observado atualmente (escala 1-5).

        ecc_desejado (float):
            ECC de referência para a comparação
            (escala 1-5).

    Retorna:
        dict:
            variacao_gordura_kg:
                Alteração estimada de gordura (kg).

            variacao_proteina_kg:
                Alteração estimada de proteína (kg).

    Observações:
        - Resultados positivos indicam deposição.
        - Resultados negativos indicam mobilização.
        - Os resultados são estimativas, não
          medições diretas dos tecidos.
        - Não representa uma previsão temporal.
    """

    peso_vazio_atual = calcular_peso_corporal_vazio(
        peso_vivo_atual
    )

    peso_vazio_desejado = (
        calcular_peso_corporal_vazio_por_ecc(
            peso_vivo_atual,
            ecc_atual,
            ecc_desejado
        )
    )

    gordura_atual = (
        peso_vazio_atual
        * calcular_proporcao_gordura(ecc_atual)
    )

    gordura_desejada = (
        peso_vazio_desejado
        * calcular_proporcao_gordura(ecc_desejado)
    )

    proteina_atual = (
        peso_vazio_atual
        * calcular_proporcao_proteina(ecc_atual)
    )

    proteina_desejada = (
        peso_vazio_desejado
        * calcular_proporcao_proteina(ecc_desejado)
    )

    return {
        "variacao_gordura_kg": (
            gordura_desejada - gordura_atual
        ),
        "variacao_proteina_kg": (
            proteina_desejada - proteina_atual
        ),
    }
