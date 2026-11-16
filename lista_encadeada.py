from no import No


class ListaEncadeada:

    def __init__(self):
        self.inicio = None

    def inserir(self, orientacao):

        if self.buscar(orientacao.id) is not None:
            print("Erro: ID ja cadastrado.")
            return False

        novo_no = No(orientacao)

        if self.inicio is None:
            self.inicio = novo_no

        else:
            atual = self.inicio

            # Percorre ate o ultimo no
            while atual.proximo is not None:
                atual = atual.proximo

            atual.proximo = novo_no

        return True

    def buscar(self, id):
        atual = self.inicio

        while atual is not None:

            if atual.orientacao.id == id:
                return atual.orientacao

            atual = atual.proximo

        return None

    def listar(self):
        atual = self.inicio

        if atual is None:
            print("Nenhuma orientacao cadastrada.")
            return

        while atual is not None:
            print(
                atual.orientacao.id,
                "-",
                atual.orientacao.titulo
            )

            atual = atual.proximo

    
    def atualizar(self, id, novo_titulo):
        atual = self.inicio

        while atual is not None:

            if atual.orientacao.id == id:
                atual.orientacao.titulo = novo_titulo
                return True

            atual = atual.proximo

        return False

    
    def remover(self, id):
        atual = self.inicio
        anterior = None

        while atual is not None:

            if atual.orientacao.id == id:

                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                return True

            anterior = atual
            atual = atual.proximo

        return False


    def pesquisar_titulo(self, texto):
        atual = self.inicio
        resultados = []

        while atual is not None:
            if texto.lower() in atual.orientacao.titulo.lower():
                resultados.append(atual.orientacao)

            atual = atual.proximo

        return resultados

    
    def ordenar(self):
        if self.inicio is None:
            return

        trocou = True

        while trocou:
            trocou = False
            atual = self.inicio

            while atual.proximo is not None:
                titulo1 = atual.orientacao.titulo.lower()
                titulo2 = atual.proximo.orientacao.titulo.lower()

                if titulo1 > titulo2:
                    auxiliar = atual.orientacao
                    atual.orientacao = atual.proximo.orientacao
                    atual.proximo.orientacao = auxiliar
                    trocou = True

                atual = atual.proximo


