import os
import webbrowser
import time

#API's e Frameworks
import shap
import matplotlib.pyplot as plt
import pandas as pd
import dtale
from ydata_profiling import ProfileReport

#Modulos
from Models.Logger.Logging import setup_logging

logger = setup_logging()

class Profiling:
    def __init__(self, nome_arquivo: str, df: pd.DataFrame):
        self.nome_arquivo = nome_arquivo
        self.df = df

        # Define a pasta para os relatórios como 'Views'
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Views"))
        os.makedirs(self.output_dir, exist_ok=True)  # Garante que 'Views' exista
        
    def gerar_shap(self, saida_arquivo="shap_summary_plot.png"):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(self.X_test)
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, self.X_test, show=False)
        plt.savefig(saida_arquivo, dpi=300, bbox_inches="tight")
        print(f"✅ Gráfico SHAP salvo em: {saida_arquivo}")



    def generate_dtale(self):
        """ Inicia a interface interativa D-Tale e abre no navegador """
        try:
            instancia = dtale.show(self.df)
            # Espera o servidor iniciar (ajuste se necessário)
            time.sleep(2)
            instancia.open_browser()  # tenta abrir no navegador

            logger.info(f"D-Tale iniciado para {self.nome_arquivo}.")
        except Exception as e:
            logger.error(f"Erro ao iniciar D-Tale para {self.nome_arquivo}: {e}")


    def generate_ydata(self, sample_frac: float = 0.01, min_rows: int = 500, random_state: int = 50):
        """ Gera relatório YData Profiling com controle de amostragem """
        try:
            if len(self.df) > min_rows:
                dataset_amostrado = self.df.sample(frac=sample_frac, random_state=random_state)
            else:
                dataset_amostrado = self.df.copy()

            profile = ProfileReport(dataset_amostrado, explorative=True)
            output_path = os.path.join(self.output_dir, f"ydata_{self.nome_arquivo}.html")
            profile.to_file(output_path)

            logger.info(f"Relatório YData Profiling salvo em {output_path} com {len(dataset_amostrado)} linhas.")
        except Exception as e:
            logger.error(f"Erro ao gerar relatório YData para {self.nome_arquivo}: {e}")