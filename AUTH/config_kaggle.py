import os
import json

# Obtém o diretório do script atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KAGGLE_AUTH = os.path.join(BASE_DIR, "kaggle.json")

# Verifica se o arquivo kaggle.json existe
if not os.path.exists(KAGGLE_AUTH):
    raise FileNotFoundError(f"❌ Arquivo kaggle.json não encontrado em {KAGGLE_AUTH}")

# Lê o arquivo JSON
with open(KAGGLE_AUTH, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Define as variáveis de ambiente
os.environ["KAGGLE_USERNAME"] = dados["username"]
os.environ["KAGGLE_KEY"] = dados["key"]