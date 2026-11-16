import json
import unicodedata
from orientacao import Orientacao
from lista_encadeada import ListaEncadeada


def normalizar(texto):
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )

    for sinal in "?!.,;:()-_/":
        texto = texto.replace(sinal, " ")

    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = ListaEncadeada()

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            nova_lista = ListaEncadeada()
            total = 0

            for item in dados:
                orientacao = Orientacao(**item)
                nova_lista.inserir(orientacao)
                total += 1

            self.orientacoes = nova_lista

            print("Base de conhecimento carregada!")
            print("Total de orientacoes:", total)
            return True

        except (FileNotFoundError, json.JSONDecodeError,
                TypeError, ValueError, AttributeError) as erro:
            print("Erro ao carregar a base de conhecimento:", erro)
            return False

    def salvar(self):
        dados = []
        atual = self.orientacoes.inicio

        while atual is not None:
            orientacao = atual.orientacao

            dados.append({
                "id": orientacao.id,
                "categoria": orientacao.categoria,
                "titulo": orientacao.titulo,
                "palavras_chave": orientacao.palavras_chave,
                "resposta": orientacao.resposta,
                "documentos": orientacao.documentos,
                "onde": orientacao.onde,
                "fonte": orientacao.fonte,
                "verificado_em": orientacao.verificado_em,
                "publico_alvo": orientacao.publico_alvo
            })

            atual = atual.proximo

        try:
            with open(self.caminho, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)

            print("Base de conhecimento salva!")
            return True

        except OSError as erro:
            print("Erro ao salvar:", erro)
            return False

    def categorias(self):
        lista = []
        atual = self.orientacoes.inicio

        while atual is not None:
            categoria = atual.orientacao.categoria

            if categoria not in lista:
                lista.append(categoria)

            atual = atual.proximo

        return lista

    def por_categoria(self, categoria):
        resultado = []
        atual = self.orientacoes.inicio

        while atual is not None:
            orientacao = atual.orientacao

            if orientacao.categoria == categoria:
                resultado.append(orientacao)

            atual = atual.proximo

        return resultado

    def pontuar(self, pergunta, orientacao):
        pontos = 0

        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)

        palavras_pergunta = pergunta.split()

        for chave in orientacao.palavras_chave:
            chave = normalizar(chave)
            palavras_chave = chave.split()

            if all(palavra in palavras_pergunta for palavra in palavras_chave):
                pontos += 3

        for palavra in set(palavras_pergunta):
            if len(palavra) >= 4 and f" {palavra} " in titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        atual = self.orientacoes.inicio

        while atual is not None:
            orientacao = atual.orientacao
            pontos = self.pontuar(pergunta, orientacao)

            if pontos >= 3:
                resultados.append((pontos, orientacao))

            atual = atual.proximo

        for i in range(len(resultados)):
            for j in range(len(resultados) - 1 - i):
                if resultados[j][0] < resultados[j + 1][0]:
                    auxiliar = resultados[j]
                    resultados[j] = resultados[j + 1]
                    resultados[j + 1] = auxiliar

        return resultados
