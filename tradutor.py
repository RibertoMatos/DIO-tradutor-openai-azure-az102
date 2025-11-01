from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path=".env", override=True)

print("\n🔍 Variáveis carregadas:")
for key, value in os.environ.items():
    if "AZURE" in key:
        print(f"{key} = {value}")

azureai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_KEY")

# Verificar se as variáveis foram carregadas corretamente
if not azureai_endpoint or not API_KEY:
    raise ValueError("As variáveis AZURE_OPENAI_ENDPOINT ou AZURE_OPENAI_KEY não estão definidas! Verifique o arquivo .env.")

print("Endpoint carregado:", azureai_endpoint)
print("API Key carregada:", "*****" if API_KEY else None)

# Função para extrair texto de uma URL
def extract_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(" ", strip=True)
        return text
    else:
        print("Falha ao buscar a URL. Código de status:", response.status_code)
        return None

# Função para traduzir texto usando Azure OpenAI
def translate_article(text, lang):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Você atua como tradutor de textos"
            },
            {
                "role": "user",
                "content": f"Traduza: {text} para o idioma {lang} e responda apenas com a tradução no formato markdown"
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 900
    }

    try:
        response = requests.post(azureai_endpoint, headers=headers, json=payload)
        print("Status:", response.status_code)
        print("Texto da resposta:", response.text)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        raise SystemExit(f"Falha ao fazer a requisição: {e}")
    except Exception as e:
        raise SystemExit(f"Erro ao interpretar a resposta: {e}")

# URL do artigo que você quer traduzir
url = "https://dev.to/ryan-mathews/ai-in-devops-how-intelligent-automation-is-redefining-software-delivery-1odj"

# Extrair texto
text = extract_text(url)
if text:
    # Traduzir e mostrar o artigo
    artigo = translate_article(text, "português")
    print("\n📝 Tradução:\n")
    print(artigo)
else:
    print("Não foi possível extrair o texto do artigo.")