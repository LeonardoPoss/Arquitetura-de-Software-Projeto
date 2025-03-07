# Infra/kaggle/kaggle_downloader.py
import os
from Adapters.Repository.Connect_kaggle import KaggleAuthenticator  # Importa corretamente do arquivo Connect_kaggle
import kaggle

class KaggleDownloader:
    def __init__(self, dataset_name, pasta_destino="Dataset"):
        """
        Inicializa o downloader com o nome do dataset e pasta destino.
        """
        self.dataset_name = dataset_name
        self.pasta_destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), pasta_destino)  # Caminho completo

        # Cria a pasta de destino se ela não existir
        os.makedirs(self.pasta_destino, exist_ok=True)


    def verificar_e_baixar_dataset(self):
        """
        Verifica se o dataset já existe localmente e, se não, baixa do Kaggle.
        """
        extensoes_validas = {".csv", ".json", ".xlsx", ".zip", ".txt"}
        arquivos_existentes = [f for f in os.listdir(self.pasta_destino) 
                               if os.path.isfile(os.path.join(self.pasta_destino, f)) 
                               and os.path.splitext(f)[1] in extensoes_validas]

        if arquivos_existentes:
            print(f"✅ O dataset já foi baixado em '{self.pasta_destino}'.")
            return

        try:
        # Inicializa o autenticador e a API
            self.authenticator = KaggleAuthenticator()
            self.api = self.authenticator.get_api()
            print(f"📥 Baixando dataset: {self.dataset_name}...")
            self.api.dataset_download_files(self.dataset_name, path=self.pasta_destino, unzip=True)

            # Verifica se o download foi bem-sucedido
            arquivos_existentes = [f for f in os.listdir(self.pasta_destino) 
                                   if os.path.isfile(os.path.join(self.pasta_destino, f)) 
                                   and os.path.splitext(f)[1] in extensoes_validas]

            if arquivos_existentes:
                print(f"✅ Download concluído! Arquivos salvos em '{self.pasta_destino}'.")
            else:
                print("⚠️ O download foi feito, mas nenhum arquivo válido foi encontrado na pasta.")
        except kaggle.rest.ApiException as e:
            print(f"❌ Erro ao baixar o dataset: {e}")
