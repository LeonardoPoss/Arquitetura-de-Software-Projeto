import os
import sys

from Models.Logger.Logging import *
from Models.Service.profiling import *
from Controllers.Downloader import KaggleDownloader

logger = setup_logging()
def Main():
    while True:
        try:
            valor = int(input(
                "\nDigite uma opção:\n"
                "1 - Baixar um Dataset\n"
                "2 - Gerar Profiling e Imagem SHAP\n"
                "3 - Treinar com PyCaret\n"
                "4 - Sair\n> "
            ))

            match valor:
                case 1:
                    dataset_nome = input("Digite o nome do dataset (formato: user/dataset): ")
                    logger.info("Iniciando autenticação no Kaggle.")
                    API = KaggleDownloader(dataset_nome)
                    
                    if API:
                        logger.info("Autenticação bem-sucedida! Fazendo download do dataset.")
                        KaggleDownloader.verificar_e_baixar_dataset(API)
                    else:
                        logger.error("Falha na autenticação do Kaggle. Encerrando aplicação.")
                        sys.exit(1)

                case 2:
                    print("Opção 2 selecionada: Gerar profiling e imagem SHAP.")
                    # Chamada para função do profiling aqui
                    # ex: gerar_profiling_e_shap()
                    
                case 3:
                    print("Opção 3 selecionada: Treinamento com PyCaret.")
                    # Chamada para função de treino aqui
                    # ex: treinar_modelo()

                case 4:
                    print("Saindo...")
                    break

                case _:
                    print("Opção inválida. Escolha entre 1 e 4.")

        except ValueError:
            print("Entrada inválida! Digite um número.")

if __name__ == "__main__":
    Main()
