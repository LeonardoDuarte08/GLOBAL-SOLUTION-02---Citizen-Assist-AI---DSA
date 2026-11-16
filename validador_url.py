import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from getpass import getpass

def carregar_chave():
    caminho = os.path.join(os.path.dirname(__file__), ".env")

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.startswith("GOOGLE_SAFE_BROWSING_KEY="):
                    return linha.strip().split("=", 1)[1].strip()

    except FileNotFoundError:
        return None

    return None


def verificar_url(url):
    chave_api = os.getenv("GOOGLE_SAFE_BROWSING_KEY") or carregar_chave()

    if not chave_api:
        print("\nChave do Google Safe Browsing não encontrada.")
        print("Informe sua chave para utilizar o verificador.")

        chave_api = getpass("Chave da API: ").strip()

        if not chave_api:
            print("Nenhuma chave informada.")
            return

    url = url.strip()
    endereco = urlparse(url)

    if endereco.scheme not in ("http", "https") or not endereco.hostname:
        print("URL inválida. Utilize http:// ou https://")
        return

    # API Google Safe Browsing v4
    api = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    api = api + "?key=" + chave_api

    dados = {
        "client": {
            "clientId": "citizen-assist-ai",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    requisicao = Request(
        api,
        data=json.dumps(dados).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(requisicao, timeout=10) as resposta:
            resultado = json.load(resposta)

        ameacas = resultado.get("matches", [])

        if ameacas:
            print("\nALERTA: URL potencialmente perigosa!")

            for ameaca in ameacas:
                print("Ameaça:", ameaca.get("threatType"))

            print("Recomendação: não acesse esse link.")
        else:
            print("\nNenhuma ameaça conhecida foi encontrada.")
            print("Isso não garante que o site seja seguro.")

        print("Fonte: Google Safe Browsing")

    except HTTPError as erro:
        print("Erro na API. Código:", erro.code)
        print("Detalhes:", erro.read().decode("utf-8"))

    except URLError as erro:
        print("Erro de conexão:", erro.reason)

    except (ValueError, TimeoutError) as erro:
        print("Erro na consulta:", str(erro))



if __name__ == "__main__":

    print("================================")
    print(" CITIZEN ASSIST AI")
    print(" Verificador de Links")
    print("================================")

    while True:
        url = input("\nDigite uma URL (0 para sair): ").strip()

        if url == "0":
            print("Encerrando verificador.")
            break

        if not url:
            print("Digite uma URL válida.")
            continue

        verificar_url(url)
