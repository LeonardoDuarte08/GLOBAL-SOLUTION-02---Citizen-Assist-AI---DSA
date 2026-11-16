# Citizen Assist AI — Global Solution 2026.2

**Disciplina:** Data Structures and Algorithms (DSA)  
**Tema:** Citizen Tech  
**Integrantes:** Leonardo Duarte (RM 569029) e Enzo de Nadai (RM 569985)

## 1. Sobre o projeto

O **Citizen Assist AI** é um sistema que desenvolvemos em Python para facilitar a consulta a informações sobre segurança digital, direitos do consumidor e serviços públicos digitais. Nele, o usuário pode fazer perguntas, navegar por categorias e encontrar orientações de forma simples, direto pelo terminal.

Começamos o projeto na disciplina de Python e, para **Data Structures and Algorithms (DSA)**, aproveitamos o que já estava pronto e adicionamos o gerenciamento das orientações: cadastro, consulta, atualização e exclusão (CRUD), além de **lista simplesmente encadeada**, **busca sequencial** e **Bubble Sort**.

O sistema roda no terminal. Usamos um arquivo JSON para guardar as informações entre as execuções, mas, enquanto o programa está funcionando, **as orientações ficam na lista encadeada que nós implementamos**.

## 2. Funcionalidades

### Assistente — funcionalidades reaproveitadas de Python

| Opção | Funcionalidade | Descrição |
|---|---|---|
| 1 | Fazer uma pergunta | Identifica orientações por palavras-chave e pontuação de relevância. |
| 2 | Navegar por categorias | Mostra categorias e permite consultar orientações. |
| 3 | Verificar URL suspeita | Consulta o Google Safe Browsing, quando configurado. |
| 4 | Visualizar indicadores | Exibe indicadores dos atendimentos registrados. |
| 5 | Exportar atendimentos | Gera um arquivo CSV a partir do histórico. |

### Gerenciamento — funcionalidades implementadas para DSA

| Opção | Funcionalidade | Descrição |
|---|---|---|
| 6 | Cadastrar orientação | Insere um registro, validando ID duplicado e campos obrigatórios. |
| 7 | Consultar por ID | Localiza um registro por busca sequencial. |
| 8 | Listar orientações | Percorre todos os nós da lista encadeada. |
| 9 | Atualizar orientação | Modifica título, categoria, descrição, público-alvo e canal/local de atendimento. |
| 10 | Excluir orientação | Remove o registro e atualiza as referências dos nós. |
| 11 | Pesquisar por título | Procura correspondências parciais no título. |
| 12 | Ordenar por título | Organiza as orientações alfabeticamente usando Bubble Sort. |
| 0 | Sair | Salva as alterações no JSON e encerra o programa. |

## 3. Estrutura dos arquivos

```text
GLOBAL-SOLUTION-02---Citizen-Assist-AI---DSA/
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
├── validador_url.py
├── no.py
├── lista_encadeada.py
├── teste_lista.py
├── README.md
└── data/
    └── base_conhecimento.json
└── evidencias/
    └── vídeo/
        └── GS - DSA - Demo.mp4
```

**Responsabilidades:**

- `main.py`: menu, validações de entrada e integração das funcionalidades.
- `orientacao.py`: classe que representa cada orientação.
- `no.py`: classe `No`, com o registro armazenado e a referência `proximo`.
- `lista_encadeada.py`: operações da lista, busca por ID, pesquisa por título e Bubble Sort.
- `base_conhecimento.py`: carregamento e salvamento do JSON, além de categorias e busca por relevância.
- `assistente.py`: perguntas, navegação, histórico, indicadores, CSV e avaliações.
- `validador_url.py`: consulta opcional ao serviço Google Safe Browsing.
- `teste_lista.py`: testes locais das operações da lista encadeada.
- `data/base_conhecimento.json`: dados iniciais e persistência das alterações.

Os arquivos `data/historico.json`, `data/avaliacoes.json` e `data/atendimentos.csv` podem ser gerados durante o uso do assistente.

## 4. Modelo dos registros

Cada orientação é representada pela classe `Orientacao`.

| Campo | Finalidade |
|---|---|
| `id` | Identificador numérico único. |
| `titulo` | Nome da orientação. |
| `categoria` | Assunto ao qual pertence. |
| `resposta` | Descrição e orientação apresentada ao usuário. |
| `publico_alvo` | Público a quem a orientação se destina. |
| `onde` | Local ou canal de atendimento. |
| `palavras_chave` | Termos utilizados na busca do assistente. |
| `documentos` | Documentos relacionados à orientação, quando houver. |
| `fonte` | Referência da informação. |
| `verificado_em` | Data de verificação da informação. |

Na nossa implementação, os campos pedidos em DSA aparecem como `titulo`, `categoria`, `resposta` (descrição), `publico_alvo` e `onde` (canal/local), além do `id`.

## 5. Lista simplesmente encadeada

Criamos nossa própria lista encadeada, sem usar uma lista comum de Python para armazenar os registros principais.

Cada nó mantém uma orientação e uma referência para o nó seguinte:

```python
class No:
    def __init__(self, orientacao):
        self.orientacao = orientacao
        self.proximo = None
```

A classe `ListaEncadeada` possui a referência `inicio`, que indica o primeiro nó. Cada operação percorre a sequência por meio de `atual = atual.proximo`.

```text
inicio
  |
  v
[Orientação 1 | próximo] -> [Orientação 2 | próximo] -> [Orientação 3 | None]
```

**Inserção:** primeiro verificamos se o ID já existe. Depois percorremos até o último nó e conectamos o novo registro.  
**Consulta:** percorremos os nós até encontrar o identificador solicitado.  
**Atualização:** encontramos o objeto por ID e modificamos seus atributos.  
**Exclusão:** quando o registro é encontrado, ajustamos a referência `proximo` do nó anterior ou atualizamos `inicio`, se for o primeiro nó.  
**Listagem:** percorremos a lista desde `inicio` até encontrar `None`.

Usamos listas comuns apenas para reunir resultados de pesquisa, categorias e dados que serão gravados no JSON. O armazenamento principal das orientações continua sendo a lista encadeada.

## 6. Algoritmos de busca e ordenação

### Busca sequencial

A busca por identificador percorre a lista nó a nó, comparando `atual.orientacao.id` com o ID informado. A busca termina quando encontra o registro ou quando chega ao fim da lista.

A pesquisa por título segue a mesma estratégia de percurso e verifica se o texto informado está contido no título, desconsiderando diferenças entre letras maiúsculas e minúsculas.

### Bubble Sort

Implementamos o **Bubble Sort** no método `ordenar()` da lista encadeada. O algoritmo compara os títulos de orientações vizinhas e troca seus objetos quando estão fora da ordem alfabética. O processo é repetido até que nenhuma troca seja necessária.

Nessa implementação, os **objetos armazenados nos nós são trocados**, mas os vínculos `proximo` permanecem intactos. Não usamos `sort()` nem `sorted()` para ordenar os registros da lista encadeada.

O assistente também organiza os resultados de perguntas por pontuação usando comparações e trocas implementadas no código.

### Busca por relevância do assistente

Mantivemos a mesma lógica de perguntas da primeira versão:

- Cada correspondência de palavra-chave completa soma **3 pontos**.
- Cada palavra distinta da pergunta com pelo menos quatro caracteres que aparece no título soma **1 ponto**.
- Orientações com pelo menos **3 pontos** são consideradas resultados.
- Os resultados são apresentados por pontuação, da maior para a menor.

Essa funcionalidade usa os registros guardados na nossa lista encadeada, mas não substitui a busca sequencial exigida em DSA.

## 7. Análise de complexidade — Big-O

Consideramos **n** o número de orientações armazenadas na lista encadeada. A análise abaixo considera o pior caso, com comparações de campos de tamanho limitado.

| Operação | Complexidade | Justificativa |
|---|---|---|
| Inserir (`inserir`) | **O(n)** | Verifica se o ID já existe e percorre até o final para inserir. |
| Consultar por ID (`buscar`) | **O(n)** | Pode ser necessário examinar os n nós. |
| Listar (`listar`) | **O(n)** | Percorre todos os registros uma vez. |
| Atualizar | **O(n)** | Localiza o ID por busca sequencial; alterar os campos encontrados é constante para campos de tamanho limitado. |
| Remover (`remover`) | **O(n)** | Percorre a lista até encontrar o registro; ajustar a referência é O(1). |
| Pesquisar por título (`pesquisar_titulo`) | **O(n)** | Examina o título de cada orientação. |
| Ordenar (`ordenar`) | **O(n²)** | No pior caso, realiza várias passagens comparando nós vizinhos. |

O Bubble Sort usado no projeto encerra quando não há trocas: **no melhor caso, a ordenação pode ser O(n)**, quando a lista já está ordenada. Seu custo de memória auxiliar é **O(1)**, pois a troca utiliza uma variável temporária. A busca sequencial também utiliza memória auxiliar O(1), desconsiderando a lista de resultados criada pela pesquisa por título.

A inserção poderia ser O(1) em uma lista que sempre insere no início, sem validações, **mas essa não é a nossa implementação**. Nosso método valida IDs repetidos e insere no final, por isso seu custo é O(n).

## 8. Como executar

### Requisitos

- Python 3 instalado.
- Terminal ou Visual Studio Code.
- Acesso aos arquivos do projeto e à pasta `data`.

### Execução

Abra o terminal na pasta principal do projeto e execute:

```bash
python main.py
```

No Windows, também é possível utilizar:

```powershell
py main.py
```

O programa carrega as orientações de `data/base_conhecimento.json` e abre o menu. Basta digitar a opção desejada. Ao sair pela opção `0`, salvamos as alterações no JSON.

Para testar cadastro, atualização e exclusão sem mudar os registros originais, vale guardar uma cópia do JSON antes.

### Verificação opcional de URLs

A opção 3 usa a integração com o Google Safe Browsing que já tínhamos feito em Python. Para consultar URLs, é necessário configurar a chave da API conforme o `validador_url.py`, sem colocá-la no GitHub. O restante do sistema funciona normalmente sem essa configuração.

## 9. Testes realizados e evidências

Durante o desenvolvimento, executamos testes pelo terminal para validar a lista encadeada e o menu integrado.

| Cenário | Entrada / procedimento | Resultado esperado | Resultado observado |
|---|---|---|---|
| Lista vazia | Executar `listar()` antes de inserir registros. | Informar que não há orientações. | **Funcionou**, conforme teste local. |
| Inserção | Inserir registros com IDs 1 e 2 em lista de teste. | Os dois registros aparecem na listagem. | **Funcionou**, conforme teste local. |
| Consulta por ID | Buscar ID 2. | Retornar a orientação do ID 2. | **Funcionou**, conforme teste local. |
| ID duplicado | Tentar inserir novamente o ID 1. | Rejeitar cadastro duplicado. | **Funcionou**, conforme teste local. |
| ID inexistente | Buscar ID 99. | Retornar registro não encontrado. | **Funcionou**, conforme teste local. |
| Atualização | Alterar título do ID 1 no teste da lista. | Exibir o título atualizado. | **Funcionou**, conforme teste local. |
| Exclusão | Remover ID 2 no teste da lista. | ID 2 deixa de aparecer na listagem. | **Funcionou**, conforme teste local. |
| Exclusão inexistente | Tentar remover ID 99. | Informar que o registro não existe. | **Funcionou**, conforme teste local. |
| Pesquisa por título | Pesquisar `compra` na lista de teste. | Encontrar o registro “Compras online”. | **Funcionou**, conforme teste local. |
| Ordenação | Executar `ordenar()` e listar. | Exibir títulos em ordem alfabética. | **Funcionou**, conforme teste local. |
| Carregamento integrado | Carregar base e listar categorias. | Apresentar as 10 orientações e três categorias. | **Funcionou**, conforme teste local. |
| Perguntas e categorias | Utilizar opções 1 e 2 do menu integrado. | Obter orientação e navegar pelas categorias. | **Funcionou**, conforme teste informado. |
| Atualização de campos | Alterar descrição e público-alvo pela opção 9. | Consultar e encontrar os novos valores. | **Funcionou**, conforme teste informado. |

Para completar a entrega, vamos incluir prints do terminal mostrando o menu, a lista vazia, o cadastro, a consulta, a atualização, a exclusão, a pesquisa, a ordenação e uma entrada inválida. Os testes acima já foram realizados; faltam apenas os registros visuais.

Podemos organizar os prints nesta pasta:

```text
evidencias/
├── lista_vazia.png
├── cadastro_e_consulta.png
├── atualizacao_e_exclusao.png
├── pesquisa_e_ordenacao.png
└── entrada_invalida.png
```



## 10. Relação com os requisitos da disciplina

| Requisito de DSA | Implementação no projeto |
|---|---|
| CRUD e menu interativo | `main.py` e métodos de `ListaEncadeada`. |
| Identificador único e campos obrigatórios | Validações no cadastro e pesquisa por ID. |
| Lista simplesmente encadeada própria | `No` e `ListaEncadeada`, com referências explícitas. |
| Busca implementada | Busca sequencial por ID e pesquisa por título. |
| Ordenação implementada | Bubble Sort por título. |
| Análise Big-O | Seção 7 deste README. |
| Testes e evidências | Seção 9; anexar capturas do terminal antes da entrega. |

## 11. Resultado final

Com essa versão, conseguimos aproveitar tudo o que já tínhamos desenvolvido em Python e acrescentar as funcionalidades de DSA sem precisar começar do zero. Implementamos a lista encadeada, fizemos as buscas e a ordenação manualmente e integramos tudo em um único menu.

No final, o Citizen Assist AI permite tanto consultar orientações quanto gerenciar os registros, com os dados salvos em JSON e as operações feitas pela nossa própria estrutura de dados.
