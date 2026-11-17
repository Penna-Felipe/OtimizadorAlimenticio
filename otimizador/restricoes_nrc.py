import pulp


def adicionar_restricoes(model, x, ingredientes, exigencias):
    """
    Adiciona as restrições nutricionais ao modelo de otimização.

    Parâmetros:
        model: Modelo de programação linear do PuLP.
        x: Variáveis de decisão dos ingredientes (kg de MS/dia).
        ingredientes (dict): Composição nutricional dos alimentos.
        exigencias (dict): Exigências nutricionais da vaca.

    Retorna:
        None: As restrições são adicionadas diretamente ao modelo.
    """

    dmi = exigencias["dmi"]
    pb = exigencias["pb"]
    nel = exigencias["nel"]
    fdn = exigencias["fdn"]

    # Matéria seca total
    model += pulp.lpSum(
        x[i] for i in ingredientes
    ) == dmi, "Materia_Seca"

    # Proteína bruta mínima
    model += pulp.lpSum(
        ingredientes[i]["pb"] * x[i]
        for i in ingredientes
    ) >= pb, "Proteina_Bruta"

    # Energia líquida mínima
    model += pulp.lpSum(
        ingredientes[i]["nel"] * x[i]
        for i in ingredientes
    ) >= nel, "Energia"

    # FDN total mínima
    model += pulp.lpSum(
        ingredientes[i]["fdn"] * x[i]
        for i in ingredientes
    ) >= fdn, "Fibra"

    # FDN mínima proveniente de forragens
    model += pulp.lpSum(
        ingredientes[i]["fdn"] * x[i]
        for i in ingredientes
        if ingredientes[i]["volumoso"]
    ) >= 0.17 * dmi, "FDN_Forragem_Minima"

    # CNF máximo
    model += pulp.lpSum(
        ingredientes[i]["cnf"] * x[i]
        for i in ingredientes
    ) <= 0.40 * dmi, "CNF_Maximo"