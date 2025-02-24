import os
import kaggle
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AUTH.kaggle_connect import autenticar_kaggle

def verificar_e_baixar_dataset(dataset_name, pasta_destino="Dataset"):
    """
    Verifica se o dataset já existe localmente e, se não existir, faz o download do Kaggle.
    
    Parâmetros:
    - dataset_name (str): Nome do dataset no Kaggle no formato "autor/dataset".
    - pasta_destino (str): Pasta onde o dataset será salvo (padrão: "Dataset").
    """

    # Criar a pasta se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Lista arquivos relevantes no diretório
    extensoes_validas = {".csv", ".json", ".xlsx", ".zip", ".txt"}
    arquivos_existentes = [f for f in os.listdir(pasta_destino) 
                           if os.path.isfile(os.path.join(pasta_destino, f)) 
                           and os.path.splitext(f)[1] in extensoes_validas]

    if arquivos_existentes:
        print(f"✅ O dataset já foi baixado em '{pasta_destino}'.")
        return

    try:
        api = autenticar_kaggle()
        print(f"📥 Baixando dataset: {dataset_name}...")
        api.dataset_download_files(dataset_name, path=pasta_destino, unzip=True)

        # Revalidar a existência de arquivos após o download
        arquivos_existentes = [f for f in os.listdir(pasta_destino) 
                               if os.path.isfile(os.path.join(pasta_destino, f)) 
                               and os.path.splitext(f)[1] in extensoes_validas]

        if arquivos_existentes:
            print(f"✅ Download concluído! Arquivos salvos em '{pasta_destino}'.")
        else:
            print("⚠️ O download foi feito, mas nenhum arquivo válido foi encontrado na pasta.")
    except kaggle.rest.ApiException as e:
        print(f"❌ Erro ao baixar o dataset: {e}")

# Exemplo de uso:
# verificar_e_baixar_dataset("samayashar/fraud-detection-transactions-dataset")
