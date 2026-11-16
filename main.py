from orientacao import Orientacao
from base_conhecimento import BaseConhecimento
from assistente import Assistente
from validador_url import verificar_url


base = BaseConhecimento("data/base_conhecimento.json")

if not base.carregar():
    print("Nao foi possivel iniciar o sistema.")
    raise SystemExit

lista = base.orientacoes

assistente = Assistente("Citizen Assist AI", base)


def ler_id():
    valor = input("Digite o ID: ").strip()

    if not valor.isdigit() or int(valor) <= 0:
        print("ID invalido. Digite um numero maior que zero.")
        return None

    return int(valor)


def ler_campo(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("Esse campo nao pode ficar vazio.")


def cadastrar():
    print("\n===== CADASTRAR ORIENTACAO =====")

    id = ler_id()

    if id is None:
        return

    if lista.buscar(id) is not None:
        print("Erro: ID ja cadastrado.")
        return

    titulo = ler_campo("Titulo: ")
    categoria = ler_campo("Categoria: ")
    resposta = ler_campo("Descricao: ")
    publico = ler_campo("Publico-alvo: ")
    onde = ler_campo("Local ou canal de atendimento: ")
    fonte = ler_campo("Fonte: ")
    data = ler_campo("Data de verificacao: ")

    while True:
        texto = ler_campo("Palavras-chave separadas por virgula: ")
        palavras = [p.strip() for p in texto.split(",") if p.strip()]

        if len(palavras) >= 3:
            break

        print("Informe pelo menos 3 palavras-chave.")

    orientacao = Orientacao(
        id, categoria, titulo, palavras,
        resposta, [], onde, fonte, data, publico
    )

    if lista.inserir(orientacao):
        print("Orientacao cadastrada com sucesso!")


def consultar():
    print("\n===== CONSULTAR ORIENTACAO =====")

    id = ler_id()

    if id is None:
        return

    orientacao = lista.buscar(id)

    if orientacao is not None:
        orientacao.exibir()
        print("Publico-alvo:", orientacao.publico_alvo)
    else:
        print("Orientacao nao encontrada.")



def atualizar():
    print("\n===== ATUALIZAR ORIENTACAO =====")

    id = ler_id()

    if id is None:
        return

    orientacao = lista.buscar(id)

    if orientacao is None:
        print("Orientacao nao encontrada.")
        return

    print("\nDeixe em branco para manter o valor atual.")

    titulo = input("Novo titulo: ").strip()
    categoria = input("Nova categoria: ").strip()
    resposta = input("Nova descricao: ").strip()
    publico = input("Novo publico-alvo: ").strip()
    onde = input("Novo local ou canal: ").strip()

    if titulo:
        orientacao.titulo = titulo

    if categoria:
        orientacao.categoria = categoria

    if resposta:
        orientacao.resposta = resposta

    if publico:
        orientacao.publico_alvo = publico

    if onde:
        orientacao.onde = onde

    print("Orientacao atualizada com sucesso!")



def excluir():
    print("\n===== EXCLUIR ORIENTACAO =====")

    id = ler_id()

    if id is None:
        return

    if lista.remover(id):
        print("Orientacao excluida com sucesso!")
    else:
        print("Orientacao nao encontrada.")


def pesquisar():
    print("\n===== PESQUISAR ORIENTACAO =====")

    texto = ler_campo("Digite parte do titulo: ")
    resultados = lista.pesquisar_titulo(texto)

    if resultados:
        for orientacao in resultados:
            print(orientacao.id, "-", orientacao.titulo)
    else:
        print("Nenhuma orientacao encontrada.")


while True:
    print("\n================================")
    print("        CITIZEN ASSIST AI")
    print("================================")
    print("1  - Fazer uma pergunta")
    print("2  - Navegar por categorias")
    print("3  - Verificar URL suspeita")
    print("4  - Visualizar indicadores")
    print("5  - Exportar atendimentos")
    print("--------------------------------")
    print("     GERENCIAR ORIENTACOES")
    print("--------------------------------")
    print("6  - Cadastrar orientacao")
    print("7  - Consultar por ID")
    print("8  - Listar orientacoes")
    print("9  - Atualizar orientacao")
    print("10 - Excluir orientacao")
    print("11 - Pesquisar por titulo")
    print("12 - Ordenar por titulo")
    print("0  - Sair")
    print("================================")

    opcao = input("Escolha uma opcao: ").strip()


    if opcao == "1":
        assistente.perguntar()

    elif opcao == "2":
        assistente.navegar()

    elif opcao == "3":
        url = input(
            "\nDigite a URL que deseja verificar (0 para voltar): "
        ).strip()

        if url == "0":
            continue

        elif not url:
            print("Digite uma URL valida.")

        elif assistente.dados_pessoais(url):
            print("Atencao: nao informe URLs com dados pessoais.")
            print("Remova informacoes pessoais antes de consultar.")

        else:
            verificar_url(url)

    elif opcao == "4":
        assistente.indicadores()

    elif opcao == "5":
        assistente.exportar_csv()


    elif opcao == "6":
        cadastrar()

    elif opcao == "7":
        consultar()

    elif opcao == "8":
        lista.listar()

    elif opcao == "9":
        atualizar()

    elif opcao == "10":
        excluir()

    elif opcao == "11":
        pesquisar()

    elif opcao == "12":
        lista.ordenar()
        print("Orientacoes ordenadas por titulo!")
        lista.listar()

    elif opcao == "0":
        if base.salvar():
            assistente.avaliar_facilidade()
            print("\nObrigado por utilizar o Citizen Assist AI!")
            break
        else:
            print("Nao foi possivel salvar as orientacoes.")
            print("Tente novamente antes de encerrar.")

    else:
        print("\nOpcao invalida. Tente novamente.")
