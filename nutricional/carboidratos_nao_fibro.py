def calcular_cnf(
        pb:float, 
        fdn:float, 
        ee:float, 
        cinzas:float
    ) -> float:
    """
    Calcula a fração de carboidratos não fibrosos (CNF).

    Parâmetros:
        pb: Proteína bruta (fração da MS).
        fdn: Fibra em detergente neutro (fração da MS).
        ee: Extrato etéreo (fração da MS).
        cinzas: Matéria mineral (fração da MS).

    Retorna:
        float: CNF como fração da matéria seca.
    """

    return 1.0 - (pb + fdn + ee + cinzas)