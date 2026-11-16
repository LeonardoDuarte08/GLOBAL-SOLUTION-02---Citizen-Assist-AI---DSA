from lista_encadeada import ListaEncadeada
from orientacao import Orientacao


lista = ListaEncadeada()

print("TESTE 1 - Lista vazia")
lista.listar()

orientacao1 = Orientacao(
    1, "Seguranca Digital", "Golpes de phishing",
    ["phishing", "golpe", "email falso"],
    "Desconfie de links suspeitos.",
    [], "Canais oficiais",
    "https://www.gov.br", "2026-11-15"
)

orientacao2 = Orientacao(
    2, "Direitos do Consumidor", "Compras online",
    ["compra", "cancelamento", "reclamacao"],
    "Procure a loja ou o Procon.",
    [], "Procon",
    "https://www.procon.sp.gov.br", "2026-11-15"
)

print("\nTESTE 2 - Inserir")
lista.inserir(orientacao1)
lista.inserir(orientacao2)
lista.listar()

print("\nTESTE 3 - Buscar ID 2")
resultado = lista.buscar(2)

if resultado is not None:
    print("Encontrado:", resultado.titulo)
else:
    print("Nao encontrado.")

print("\nTESTE 4 - ID duplicado")
lista.inserir(orientacao1)

print("\nTESTE 5 - Buscar ID 99")
resultado = lista.buscar(99)

if resultado is None:
    print("Registro nao encontrado.")


print("\nTESTE 6 - Atualizar ID 1")

if lista.atualizar(1, "Como evitar golpes de phishing"):
    print("Orientacao atualizada!")
else:
    print("Orientacao nao encontrada.")

lista.listar()


print("\nTESTE 7 - Remover ID 2")

if lista.remover(2):
    print("Orientacao removida!")
else:
    print("Orientacao nao encontrada.")

lista.listar()


print("\nTESTE 8 - Remover ID 99")

if lista.remover(99):
    print("Orientacao removida!")
else:
    print("Orientacao nao encontrada.")


lista.inserir(orientacao2)

print("\nTESTE 9 - Pesquisar por título")

resultados = lista.pesquisar_titulo("compra")

for orientacao in resultados:
    print(orientacao.id, "-", orientacao.titulo)


print("\nTESTE 10 - Ordenar por título")

lista.ordenar()
lista.listar()

