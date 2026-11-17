def gerar_relatorio(resultado: dict, ingredientes: dict, exigencias: dict):
    """
    Apresenta a composição e o balanço nutricional da dieta otimizada.

    Parâmetros:
        resultado (dict): Resultado retornado pelo solver.
        ingredientes (dict): Composição nutricional dos ingredientes.
        exigencias (dict): Exigências nutricionais calculadas.

    Retorna:
        None: Exibe o relatório no terminal.
    """

    if not resultado["sucesso"]:
        print("Não foi possível gerar o relatório.")
        print("Status:", resultado["status"])
        return

    quantidades = resultado["quantidades"]
    dmi = exigencias["dmi"]

    # Calcula os nutrientes fornecidos pela dieta.
    pb_fornecida = sum(
        ingredientes[i]["pb"] * quantidades[i]
        for i in ingredientes
    )

    nel_fornecida = sum(
        ingredientes[i]["nel"] * quantidades[i]
        for i in ingredientes
    )

    fdn_fornecida = sum(
        ingredientes[i]["fdn"] * quantidades[i]
        for i in ingredientes
    )

    cnf_fornecido = sum(
        ingredientes[i]["cnf"] * quantidades[i]
        for i in ingredientes
    )

    # FDN proveniente exclusivamente de volumosos.
    fdn_forragem = sum(
        ingredientes[i]["fdn"] * quantidades[i]
        for i in ingredientes
        if ingredientes[i]["volumoso"]
    )

    # Percentuais em relação à matéria seca total.
    cnf_percentual = (cnf_fornecido / dmi) * 100
    fdn_forragem_percentual = (fdn_forragem / dmi) * 100

    print("\n--- BALANÇO NUTRICIONAL ---")
    print(f'PB:  {pb_fornecida:.2f} / {exigencias["pb"]:.2f} kg/dia')
    print(f'NEL: {nel_fornecida:.2f} / {exigencias["nel"]:.2f} Mcal/dia')
    print(f'FDN: {fdn_fornecida:.2f} / {exigencias["fdn"]:.2f} kg/dia')

    print("\n--- COMPOSIÇÃO DA DIETA ---")
    print(f"CNF: {cnf_percentual:.2f}%")
    print(f"FDN de forragens: {fdn_forragem_percentual:.2f}%")

    print("\n--- EXCEDENTES NUTRICIONAIS ---")
    print(f'PB: {pb_fornecida - exigencias["pb"]:.2f} kg/dia')
    print(f'NEL: {nel_fornecida - exigencias["nel"]:.2f} Mcal/dia')
    print(f'FDN: {fdn_fornecida - exigencias["fdn"]:.2f} kg/dia')

    print("\n--- INGREDIENTES ---")
    for nome, quantidade in quantidades.items():
        print(f"{nome}: {quantidade:.2f} kg MS/dia")

    print(f'\nCusto total: R$ {resultado["custo"]:.2f}/dia')