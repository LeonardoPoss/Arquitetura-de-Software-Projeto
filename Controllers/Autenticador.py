import os
import json

from kaggle.api.kaggle_api_extended import KaggleApi  

class KaggleAuthenticator:
    def __init__(self, cred_path="Login_kaggle/kaggle.json"):
        """Inicializa o autenticador Kaggle com um caminho específico para as credenciais."""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.cred_path = os.path.join(self.base_dir, cred_path)

    def carregar_credenciais(self):
        """Carrega as credenciais do arquivo JSON e define as variáveis de ambiente."""
        if not os.path.exists(self.cred_path):
            raise FileNotFoundError(f" Arquivo {self.cred_path} não encontrado.")

        with open(self.cred_path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        os.environ["KAGGLE_USERNAME"] = dados["username"]
        os.environ["KAGGLE_KEY"] = dados["key"]
  
    def get_api(self):
        """Retorna uma instância autenticada da API do Kaggle."""
        self.carregar_credenciais() 
        api = KaggleApi()
        api.authenticate()  
        return api  