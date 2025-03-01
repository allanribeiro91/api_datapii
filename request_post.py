import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Definir a API Key esperada
API_KEY = os.getenv("API_KEY")

# URL base da API
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/general-numbers"


# Cabeçalho com autenticação
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# Dados a serem inseridos
data = {
    "data_reference": "2025-01-02",
    "name": "Novo Indicador",
    "value": 123.45,
    "descricao": "Registro de teste via API"
}

# Fazendo a requisição POST
try:
    response = requests.post(BASE_URL + ENDPOINT, json=data, headers=HEADERS)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 201:
        print("\n✅ Registro inserido com sucesso!")
        print(response.json())
    else:
        print(f"\n❌ Erro: Status Code {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"\n❌ Erro ao conectar com a API: {e}")
