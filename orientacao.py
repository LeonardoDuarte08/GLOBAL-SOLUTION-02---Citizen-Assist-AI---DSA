class Orientacao:

    def __init__(self, id, categoria, titulo, palavras_chave,
                 resposta, documentos, onde, fonte, verificado_em, 
                 publico_alvo="Público em geral"):

        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        self.publico_alvo = publico_alvo

    def exibir(self):
        print("\n================================")
        print(self.titulo)
        print("Categoria:", self.categoria)
        print("================================")

        print("\nOrientação:")
        print(self.resposta)

        print("\nDocumentos necessários:")

        if self.documentos:
            for documento in self.documentos:
                print("-", documento)
        else:
            print("Nenhum documento necessário.")

        print("\nOnde procurar ajuda:")
        print(self.onde)

        print("\nFonte:", self.fonte)
        print("Verificado em:", self.verificado_em)

        print("\nAVISO: Este assistente não é um canal oficial.")
