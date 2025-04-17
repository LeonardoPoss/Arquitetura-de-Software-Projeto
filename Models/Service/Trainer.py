import pandas as pd
from pycaret.classification import setup as class_setup, compare_models as class_compare
from pycaret.regression import setup as reg_setup, compare_models as reg_compare
from pycaret.clustering import setup as clus_setup, create_model as clus_create

class PyCaretTrainer:
    def __init__(self):
        self.model = None

    def train_model(self, df: pd.DataFrame, target: str, task_type: str):
        if task_type == "classification":
            class_setup(data=df, target=target, session_id=123, html=False)
            self.model = class_compare()
            print("✅ Modelo de Classificação:", self.model)

        elif task_type == "regression":
            reg_setup(data=df, target=target, session_id=123, html=False)
            self.model = reg_compare()
            print("✅ Modelo de Regressão:", self.model)

        elif task_type == "clustering":
            clus_setup(data=df, session_id=123, html=False)
            self.model = clus_create("kmeans")
            print("✅ Modelo de Cluster:", self.model)

        else:
            raise ValueError("Tipo de tarefa inválido: classification, regression ou clustering")

        return self.model
