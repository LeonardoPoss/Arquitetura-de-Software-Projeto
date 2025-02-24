import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Dataset.Download_Dataset import verificar_e_baixar_dataset
from Utils.Utils import analisar_dados

verificar_e_baixar_dataset("samayashar/fraud-detection-transactions-dataset")

Dados_DataSet = pd.read_csv("Dataset/synthetic_fraud_dataset.csv")
PreProcess = analisar_dados(Dados_DataSet)
print(PreProcess)