import os

from Controllers.Autenticador import KaggleAuthenticator  # Certifique-se que o nome do arquivo está correto!

class KaggleDownloader:
    def __init__(self, dataset_name, pasta_destino="../Arquitetura-de-Software-Projeto/Models/Dataset"):
        """
        Inicializa o downloader com o nome do dataset e pasta destino.
        """
        self.dataset_name = dataset_name
        self.pasta_destino = os.path.abspath(pasta_destino)  # Caminho absoluto correto
        self.authenticator = KaggleAuthenticator()
        self.api = self.authenticator.get_api()

        # Criar diretório com tratamento de erro
        try:
            os.makedirs(self.pasta_destino, exist_ok=True)
            print(f"📂 Diretório para download: {self.pasta_destino}")
        except Exception as e:
            print(f"❌ Erro ao criar diretório {self.pasta_destino}: {e}")
            exit(1)  # Encerra o programa em caso de erro crítico

    def verificar_e_baixar_dataset(self):
        """
        Verifica se o dataset já existe localmente e, se não, baixa do Kaggle.
        """
        extensoes_validas = {".csv", ".json", ".xlsx", ".zip", ".txt"}
        arquivos_existentes = [
            f for f in os.listdir(self.pasta_destino)
            if os.path.isfile(os.path.join(self.pasta_destino, f)) 
            and os.path.splitext(f)[1] in extensoes_validas
        ]

        if arquivos_existentes:
            print(f"✅ O dataset já foi baixado em '{self.pasta_destino}'.")
            return

        try:
            print(f"📥 Baixando dataset: {self.dataset_name}...")
            self.api.dataset_download_files(self.dataset_name, path=self.pasta_destino, unzip=True)

            arquivos_existentes = [
                f for f in os.listdir(self.pasta_destino)
                if os.path.isfile(os.path.join(self.pasta_destino, f)) 
                and os.path.splitext(f)[1] in extensoes_validas
            ]

            if arquivos_existentes:
                print(f"✅ Download concluído! Arquivos salvos em '{self.pasta_destino}'.")
            else:
                print("⚠️ O download foi feito, mas nenhum arquivo válido foi encontrado na pasta.")
        except Exception as e:
            print(f"❌ Erro ao baixar o dataset: {e}")
