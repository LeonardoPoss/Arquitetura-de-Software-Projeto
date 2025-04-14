import shap
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OrdinalEncoder
from imblearn.over_sampling import SMOTE

class FraudClassifier:
    def __init__(self, df: pd.DataFrame, target_col: str = "IP_Address_Flag"):
        self.df = df
        self.target_col = target_col
        self.model = xgb.XGBClassifier(
            max_depth=4,         # Árvores menos profundas
            learning_rate=0.05,  # Treinamento mais lento (evita overfitting)
            n_estimators=200,    # Mais árvores para aprendizado mais distribuído
            reg_lambda=10,       # Aumenta regularização L2 (evita overfitting)
            use_label_encoder=False,
            eval_metric="logloss"
        )
        self.X = None
        self.y = None

    def preparar_dados(self):
        self.X = self.df.drop(columns=[self.target_col, "Transaction_ID", "User_ID"], errors='ignore')
        
        # Filtrar apenas colunas numéricas antes de calcular a correlação
        numeric_df = self.df.select_dtypes(include=['number'])
        if self.target_col in numeric_df:
            correlation_matrix = numeric_df.corr()
            high_corr_features = correlation_matrix[self.target_col][correlation_matrix[self.target_col].abs() > 0.95].index.tolist()
            if self.target_col in high_corr_features:
                high_corr_features.remove(self.target_col)
            
            if high_corr_features:
                print(f"⚠️ Removendo colunas altamente correlacionadas com o alvo: {high_corr_features}")
                self.X = self.X.drop(columns=high_corr_features, errors='ignore')
        
        # Converte colunas categóricas usando Ordinal Encoding
        categorical_cols = self.X.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
            self.X[categorical_cols] = encoder.fit_transform(self.X[categorical_cols])
        
        self.X = self.X.fillna(0)
        self.y = self.df[self.target_col].astype(int)
        print(f"✅ Shape dos dados de entrada: {self.X.shape}")


    def treinar_modelo(self):
        self.preparar_dados()
        
        # Verificar desbalanceamento
        class_distribution = self.y.value_counts(normalize=True)
        print("📊 Distribuição das classes:")
        print(class_distribution)
        
        if class_distribution.min() < 0.05:
            print("⚠️ Dados desbalanceados! Aplicando SMOTE para balancear as classes.")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Aplicar SMOTE para balancear as classes
        smote = SMOTE(random_state=42)
        self.X_train, self.y_train = smote.fit_resample(self.X_train, self.y_train)
        print(f"✅ Dados balanceados! Novo tamanho do treino: {self.X_train.shape}")
        
        # Treina o modelo
        self.model.fit(self.X_train, self.y_train)
        
        # Verificar overfitting
        train_accuracy = self.model.score(self.X_train, self.y_train)
        test_accuracy = self.model.score(self.X_test, self.y_test)
        print(f"🎯 Acurácia no Treino: {train_accuracy:.4f}")
        print(f"🎯 Acurácia no Teste: {test_accuracy:.4f}")
        
        if train_accuracy > 0.98 and test_accuracy < 0.90:
            print("⚠️ POSSÍVEL OVERFITTING DETECTADO! Considere aumentar a regularização.")

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
