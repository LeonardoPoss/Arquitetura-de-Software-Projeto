import os
from kaggle.api.kaggle_api_extended import KaggleApi
from AUTH import config_kaggle

def autenticar_kaggle():
    """Autentica a API do Kaggle usando variáveis de ambiente."""
    
    # Importar explicitamente as variáveis de ambiente
    KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
    KAGGLE_KEY = os.getenv("KAGGLE_KEY")

    if not KAGGLE_USERNAME or not KAGGLE_KEY:
        raise ValueError("❌ Erro: As variáveis de ambiente KAGGLE_USERNAME e KAGGLE_KEY não estão definidas.")

    # Inicializa a API e autentica
    api = KaggleApi()
    api.authenticate()

    print("✅ Autenticação no Kaggle bem-sucedida!")
    return api  # Retorna a instância autenticada da API
