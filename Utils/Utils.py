import pandas as pd

def analisar_dados(df):
    info = []
    
    for coluna in df.columns:
        tipo = df[coluna].dtype
        num_nulos = df[coluna].isnull().sum()
        perc_nulos = (num_nulos / len(df)) * 100
        num_zeros = (df[coluna] == 0).sum() if tipo != 'object' else None
        categoria = "Categórica" if tipo == 'object' else "Numérica"

        info.append({
            'Coluna': coluna,
            'Tipo': categoria,
            'Nulos (%)': round(perc_nulos, 2),
            'Zeros': "Não se aplica" if num_zeros is None else num_zeros
        })
    
    return pd.DataFrame(info)

# Exemplo de uso:
# df = pd.read_csv("seu_arquivo.csv")
# resultado = analisar_dados(df)
# print(resultado)
