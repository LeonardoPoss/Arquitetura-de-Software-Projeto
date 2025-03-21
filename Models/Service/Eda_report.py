import os
import logging
import pandas as pd
import sweetviz as sv
import dtale
from autoviz.AutoViz_Class import AutoViz_Class
from ydata_profiling import ProfileReport

def setup_logging():
    """ Configura o sistema de logs """
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "eda_project.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),
            logging.StreamHandler() 
        ]
    )
    return logging.getLogger("EDA_Project")

logger = setup_logging()

class EDAReport:
    def __init__(self, nome_arquivo: str, df: pd.DataFrame, output_dir: str):
        self.nome_arquivo = nome_arquivo
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_autoviz(self):
        """ Gera relatório AutoViz """
        try:
            av = AutoViz_Class()
            av.AutoViz(filename="", dfte=self.df)
            logger.info(f"Relatório AutoViz gerado para {self.nome_arquivo}.")
        except Exception as e:
            logger.error(f"Erro ao gerar relatório AutoViz para {self.nome_arquivo}: {e}")

    def generate_sweetviz(self):
        """ Gera relatório Sweetviz """
        try:
            report = sv.analyze(self.df)
            output_path = os.path.join(self.output_dir, f"sweetviz_{self.nome_arquivo}.html")
            report.show_html(output_path)
            logger.info(f"Relatório Sweetviz salvo em {output_path}.")
        except Exception as e:
            logger.error(f"Erro ao gerar relatório Sweetviz para {self.nome_arquivo}: {e}")

    def generate_dtale(self):
        """ Inicia a interface interativa D-Tale """
        try:
            dtale.show(self.df)
            logger.info(f"D-Tale iniciado para {self.nome_arquivo}.")
        except Exception as e:
            logger.error(f"Erro ao iniciar D-Tale para {self.nome_arquivo}: {e}")

    def generate_ydata(self, sample_frac: float = 0.1, min_rows: int = 500, random_state: int = 50):
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