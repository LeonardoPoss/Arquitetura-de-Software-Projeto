import os

def escolher_dataset(pasta=None):
    # Se nenhum caminho for passado, usa o padrão
    if pasta is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pasta = os.path.abspath(os.path.join(base_dir, '..', 'Dataset'))

    # Lista arquivos com extensões válidas
    extensoes_validas = {".csv", ".json", ".xlsx"}
    try:
        arquivos = [
            f for f in os.listdir(pasta)
            if os.path.isfile(os.path.join(pasta, f))
            and os.path.splitext(f)[1] in extensoes_validas
        ]
    except FileNotFoundError:
        print(f"❌ A pasta especificada não foi encontrada: {pasta}")
        return None

    if not arquivos:
        print("❌ Nenhum dataset encontrado na pasta.")
        return None

    print("📂 Datasets disponíveis:")
    for i, nome in enumerate(arquivos, 1):
        print(f"{i}. {nome}")

    while True:
        escolha = input("Digite o número do dataset que deseja usar (ou 0 para sair): ")
        
        if escolha == '0':
            print("↩️ Operação cancelada pelo usuário.")
            return None

        try:
            escolha = int(escolha)
            if 1 <= escolha <= len(arquivos):
                dataset_escolhido = arquivos[escolha - 1]
                caminho_completo = os.path.join(pasta, dataset_escolhido)
                print(f"✅ Dataset escolhido: {dataset_escolhido}")
                return caminho_completo
            else:
                print("⚠️ Escolha fora do intervalo.")
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número.")
