import json
import csv
import os
import time
from datetime import datetime


class Assistente:

    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.carregar_historico()
        self.avaliacoes = []
        self.carregar_avaliacoes()

    def carregar_historico(self):
        try:
            with open("data/historico.json", "r", encoding="utf-8") as arquivo:
                self.historico = json.load(arquivo)

            if not isinstance(self.historico, list):
                self.historico = []

        except (FileNotFoundError, json.JSONDecodeError):
            self.historico = []

    def dados_pessoais(self, pergunta):
        if "@" in pergunta:
            return True

        numeros = 0

        for letra in pergunta:
            if letra.isdigit():
                numeros += 1

        return numeros >= 8

    def registrar(self, origem, pergunta, orientacao, encontrou,
                  ajudou, tentativas, tempo):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo
        }

        self.historico.append(atendimento)

        os.makedirs("data", exist_ok=True)

        with open("data/historico.json", "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, indent=4, ensure_ascii=False)

    def avaliar(self):
        while True:
            resposta = input("\nEssa orientação ajudou? (s/n): ").lower().strip()

            if resposta == "s":
                return True

            if resposta == "n":
                return False

            print("Digite apenas s ou n.")

    def perguntar(self):
        tentativas = 0
        inicio = time.time()

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("Digite uma pergunta.")
                continue

            if self.dados_pessoais(pergunta):
                print("Atenção: não informe CPF, telefone ou e-mail.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if resultados:
                pontos, orientacao = resultados[0]

                if pontos >= 6:
                    confianca = "ALTA"
                else:
                    confianca = "MÉDIA"

                print("\nConfiança da resposta:", confianca)
                print("Pontuação:", pontos)

                orientacao.exibir()

                if len(resultados) > 1:
                    print("\nOutras orientações relacionadas:")

                    for pontos_alt, alternativa in resultados[1:3]:
                        print("-", alternativa.titulo, "(", pontos_alt, "pontos)")

                ajudou = self.avaliar()
                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    "pergunta", pergunta, orientacao.id,
                    True, ajudou, tentativas, tempo
                )

                print("\nAtendimento registrado!")
                return

            else:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou navegue pelas categorias.")

                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    "pergunta", pergunta, None,
                    False, False, tentativas, tempo
                )

                return

    def navegar(self):
        categorias = self.base.categorias()

        while True:
            print("\n===== CATEGORIAS =====")

            for i, categoria in enumerate(categorias, 1):
                print(i, "-", categoria)

            print("0 - Voltar")

            opcao = input("Escolha uma categoria: ").strip()

            if opcao == "0":
                return

            if not opcao.isdigit() or int(opcao) not in range(1, len(categorias) + 1):
                print("Opção inválida.")
                continue

            categoria = categorias[int(opcao) - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print("\nCategoria:", categoria)

                for i, orientacao in enumerate(orientacoes, 1):
                    print(i, "-", orientacao.titulo)

                print("0 - Voltar")

                escolha = input("Escolha uma orientação: ").strip()

                if escolha == "0":
                    break

                if not escolha.isdigit() or int(escolha) not in range(1, len(orientacoes) + 1):
                    print("Opção inválida.")
                    continue

                inicio = time.time()
                orientacao = orientacoes[int(escolha) - 1]

                orientacao.exibir()
                ajudou = self.avaliar()

                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    "categoria", "", orientacao.id,
                    True, ajudou, 1, tempo
                )

                print("\nAtendimento registrado!")

    def indicadores(self):
        total = len(self.historico)

        if total == 0:
            print("\nNenhum atendimento registrado.")
            return

        encontrados = 0
        ajudaram = 0
        tempo_total = 0
        tentativas_total = 0
        sem_solucao = []

        for atendimento in self.historico:
            if atendimento["encontrou"]:
                encontrados += 1

            if atendimento["ajudou"]:
                ajudaram += 1

            if not atendimento["encontrou"]:
                sem_solucao.append(atendimento["pergunta"])

            tempo_total += atendimento["tempo_segundos"]
            tentativas_total += atendimento["tentativas"]

        print("\n===== INDICADORES =====")
        print("Total de atendimentos:", total)
        print("Respostas encontradas:", round(encontrados / total * 100, 1), "%")
        print("Taxa de acerto:", round(ajudaram / total * 100, 1), "%")
        print("Tempo médio:", round(tempo_total / total, 1), "segundos")
        print("Tentativas por atendimento:", round(tentativas_total / total, 1))

        print("\nDúvidas sem solução:")

        if sem_solucao:
            for pergunta in sem_solucao:
                print("-", pergunta)
        else:
            print("Nenhuma.")

        if self.avaliacoes:
            media = sum(self.avaliacoes) / len(self.avaliacoes)
            print("\nFacilidade de uso:", round(media, 1), "de 5")
        else:
            print("\nFacilidade de uso: ainda não avaliada.")

    def exportar_csv(self):
        if not self.historico:
            print("Nenhum atendimento para exportar.")
            return

        campos = [
            "data", "origem", "pergunta", "id_orientacao",
            "encontrou", "ajudou", "tentativas", "tempo_segundos"
        ]

        with open("data/atendimentos.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(self.historico)

        print("\nCSV exportado para data/atendimentos.csv")

    
    def carregar_avaliacoes(self):
        try:
            with open("data/avaliacoes.json", "r", encoding="utf-8") as arquivo:
                self.avaliacoes = json.load(arquivo)

            if not isinstance(self.avaliacoes, list):
                self.avaliacoes = []

        except (FileNotFoundError, json.JSONDecodeError):
            self.avaliacoes = []

    
    def avaliar_facilidade(self):
        print("\nComo foi sua experiência com o assistente?")
        print("Avalie a facilidade de uso de 1 a 5.")

        while True:
            nota = input("Sua nota: ").strip()

            if nota in ["1", "2", "3", "4", "5"]:
                self.avaliacoes.append(int(nota))

                os.makedirs("data", exist_ok=True)

                with open("data/avaliacoes.json", "w", encoding="utf-8") as arquivo:
                    json.dump(self.avaliacoes, arquivo, indent=4)

                print("Obrigado pela avaliação!")
                break

            print("Nota inválida. Digite um número de 1 a 5.")

