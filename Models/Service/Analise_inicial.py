import pandas as pd

class AnalisadorDados:
    def __init__(self, dataframe):
        """
        Inicializa o analisador de dados com um DataFrame do pandas.
        
        :param dataframe: pd.DataFrame - O DataFrame a ser analisado
        """
        self.df = dataframe

    def analisar(self):
        """
        Analisa os dados do DataFrame fornecido e retorna um resumo das colunas.
        
        :return: pd.DataFrame - DataFrame com informações sobre cada coluna
        """
        info = []
        for coluna in self.df.columns:
            tipo = self.df[coluna].dtype
            num_nulos = self.df[coluna].isnull().sum()
            perc_nulos = (num_nulos / len(self.df)) * 100
            num_zeros = (self.df[coluna] == 0).sum() if tipo != 'object' else None
            categoria = "Categórica" if tipo == 'object' else "Numérica"

            info.append({
                'Coluna': coluna,
                'Tipo': categoria,
                'Nulos (%)': round(perc_nulos, 2),
                'Zeros': "Não se aplica" if num_zeros is None else num_zeros
            })
        return pd.DataFrame(info)
