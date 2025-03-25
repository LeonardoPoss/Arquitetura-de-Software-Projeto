import os
import pandas as pd
from Controllers.Downloader import KaggleDownloader
from Models.Service.Eda_report import EDAReport
from Models.Service.Analise_inicial import AnalisadorDados
from Models.Service.Eda_report import setup_logging
from Models.Service.Classificador import FraudClassifier

# Caminhos
dataset_name = "samayashar/fraud-detection-transactions-dataset"
dataset_path = os.path.join("Models/Dataset", "synthetic_fraud_dataset.csv")
logger = setup_logging()

# # Autenticação
logger.info("Iniciando autenticação no Kaggle.")
API  = KaggleDownloader(dataset_name)

if API:
    logger.info("Autenticação bem-sucedida! Fazendo download do dataset.")
    KaggleDownloader.verificar_e_baixar_dataset(API)
else:
    logger.error("Falha na autenticação do Kaggle. Encerrando aplicação.")
    exit()

# # Verifica se o dataset foi baixado corretamente
if not os.path.exists(dataset_path):
    logger.error(f"Arquivo {dataset_path} não encontrado após o download.")
    exit()

#Análise Incial
df = pd.read_csv(dataset_path)  
# analisador = AnalisadorDados(df)
# resultado_analise = analisador.analisar()

# # # Exibir o resumo da análise
# print("📊 Resumo da Análise do Dataset:")
# print(resultado_analise)


# # Análise exploratória
# logger.info("Dataset baixado com sucesso! Gerando relatórios de EDA.")
# eda = EDAReport(nome_arquivo="synthetic_fraud_dataset", df=df)
# eda.generate_autoviz()
# eda.generate_dtale()
# eda.generate_ydata()
# logger.info("Processo concluído com sucesso.")

#Aplicação do Algoritmo de Classificação
logger.info("Inicio do algoritmo de Classificação")
classificador = FraudClassifier(df)
classificador.treinar_modelo()
classificador.avaliar_modelo()
classificador.gerar_shap()
logger.info("Classificação finalizada com sucesso")