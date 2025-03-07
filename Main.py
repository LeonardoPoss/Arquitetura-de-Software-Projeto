# Main.py
from Infraestrutura.kaggle.kaggle_downloader import KaggleDownloader

# Exemplo de uso
dataset_name = "samayashar/fraud-detection-transactions-dataset"
downloader = KaggleDownloader(dataset_name)
downloader.verificar_e_baixar_dataset()
