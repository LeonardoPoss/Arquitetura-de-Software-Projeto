import shap
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OrdinalEncoder

class FraudClassifier:
    def __init__(self, df: pd.DataFrame, target_col: str = "Fraud_Label"):
        self.df = df
        self.target_col = target_col
        self.model = xgb.XGBClassifier()
        self.X = None
        self.y = None

    def preparar_dados(self):
        self.X = self.df.drop(columns=[self.target_col, "Transaction_ID", "User_ID"])
        categorical_cols = self.X.select_dtypes(include=['object']).columns
        # Converte colunas categóricas usando Ordinal Encoding 
        if len(categorical_cols) > 0:
            encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
            self.X[categorical_cols] = encoder.fit_transform(self.X[categorical_cols])
        self.X = self.X.fillna(0)
        self.y = self.df[self.target_col].astype(int)
        print(f"Shape dos dados de entrada: {self.X.shape}")

    def treinar_modelo(self):
        self.preparar_dados()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        self.model.fit(self.X_train, self.y_train)

    def avaliar_modelo(self):
        y_pred = self.model.predict(self.X_test)
        print("📈 Relatório de Classificação:")
        print(classification_report(self.y_test, y_pred))

    def gerar_shap(self, saida_arquivo="shap_summary_plot.png"):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(self.X_test)

        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, self.X_test, show=False)
        plt.savefig(saida_arquivo, dpi=300, bbox_inches="tight")
        print(f"✅ Gráfico SHAP salvo em: {saida_arquivo}")
