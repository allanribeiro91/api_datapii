import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Definir credenciais de teste
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

# URL da API
BASE_URL = "http://127.0.0.1:8000"

# Endpoint para autenticação e obtenção do token JWT
TOKEN_URL = f"{BASE_URL}/token"
ENDPOINT = f"{BASE_URL}/general-numbers/all"

# Passo 1: Obter o token JWT
try:
    token_response = requests.post(
        TOKEN_URL,
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise ValueError("❌ Token não encontrado na resposta da API.")

        print("\n✅ Token obtido com sucesso!")

        # Criar cabeçalho com o token JWT
        HEADERS = {
            "Authorization": f"Bearer {access_token}"
        }

        # Passo 2: Fazer requisição à API com o token
        response = requests.get(ENDPOINT, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            print("\n✅ Resposta da API:")
            print(data)
        else:
            print(f"\n❌ Erro na requisição: Status Code {response.status_code}")
            print(response.text)

    else:
        print(f"\n❌ Erro ao obter token: {token_response.status_code}")
        print(token_response.text)

except requests.exceptions.RequestException as e:
    print(f"\n❌ Erro ao conectar com a API: {e}")
