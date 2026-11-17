import pulp

from otimizador.restricoes_nrc import adicionar_restricoes


def otimizar_dieta(ingredientes: dict, exigencias: dict) -> dict:
    """
    Encontra uma dieta de menor custo que satisfaça
    as restrições nutricionais definidas.

    Parâmetros:
        ingredientes (dict): Composição e preço dos alimentos.
        exigencias (dict): Exigências nutricionais da vaca.

    Retorna:
        dict: Status, quantidades otimizadas, custo e modelo.
    """

    # Cria o problema de minimização.
    model = pulp.LpProblem(
        "Otimizador_Alimentar",
        sense=pulp.LpMinimize
    )

    # Cria as variáveis de decisão.
    # Cada variável representa kg de matéria seca/dia.
    x = model.add_variable_dicts(
        name="x",
        indices=ingredientes.keys(),
        lowBound=0,
        cat="Continuous"
    )

    # Função objetivo: minimizar o custo da dieta.
    model += pulp.lpSum(
        ingredientes[i]["preco"] * x[i]
        for i in ingredientes
    ), "Custo_Total"

    # Adiciona as restrições nutricionais.
    adicionar_restricoes(
        model=model,
        x=x,
        ingredientes=ingredientes,
        exigencias=exigencias
    )

    # Executa o solver.
    resultado = model.solve(pulp.COIN_CMD(msg=False))

    if not resultado.has_solution:
        return {
            "sucesso": False,
            "status": str(resultado),
            "quantidades": {},
            "custo": None,
            "modelo": model
        }

    # Recupera as quantidades encontradas.
    quantidades = {
        i: x[i].value()
        for i in ingredientes
    }

    return {
        "sucesso": True,
        "status": str(resultado),
        "quantidades": quantidades,
        "custo": resultado.objective,
        "modelo": model
    }