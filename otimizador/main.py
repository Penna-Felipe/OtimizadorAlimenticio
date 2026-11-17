from dados.animais import vaca1
from dados.ingredientes import ingredientes

from nutricional.exigencias import calcular_exigencias
from nutricional.carboidratos_nao_fibro import calcular_cnf

from otimizador.solver import otimizar_dieta
from otimizador.relatorio import gerar_relatorio


def main():

    # Calcula as exigências nutricionais da vaca.
    exigencias = calcular_exigencias(vaca1)

    # Calcula o CNF dos ingredientes.
    for nome, dados in ingredientes.items():
        dados["cnf"] = calcular_cnf(
            pb=dados["pb"],
            fdn=dados["fdn"],
            ee=dados["ee"],
            cinzas=dados["cinzas"]
        )

    # Executa a otimização.
    resultado = otimizar_dieta(
        ingredientes=ingredientes,
        exigencias=exigencias
    )

    # Apresenta os resultados.
    gerar_relatorio(
        resultado=resultado,
        ingredientes=ingredientes,
        exigencias=exigencias
    )


if __name__ == "__main__":
    main()