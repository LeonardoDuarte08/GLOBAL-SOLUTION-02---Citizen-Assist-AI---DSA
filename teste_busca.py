from base_conhecimento import BaseConhecimento

base = BaseConhecimento("data/base_conhecimento.json")
base.carregar()

while True:
    pergunta = input("\nDigite sua dúvida (0 para sair): ")

    if pergunta == "0":
        break

    resultados = base.buscar(pergunta)

    if resultados:
        pontos, orientacao = resultados[0]

        print("\nOrientação encontrada:", orientacao.titulo)
        print("Pontuação:", pontos)

        if pontos >= 6:
            print("Confiança: ALTA")
        else:
            print("Confiança: MÉDIA")

        orientacao.exibir()

    else:
        print("\nNenhuma orientação encontrada.")
        print("Tente utilizar outras palavras.")
