import sys
import time
import pandas as pd

from Models.Logger.Logging import *
from Models.Service.profiling import *
from Controllers.Downloader import KaggleDownloader
from Models.Service.Archive_Selector import escolher_dataset
from Models.Service.Trainer import PyCaretTrainer

logger = setup_logging()
def Main():
    print("⏳ Aguardando 10 segundos antes de iniciar...")
    time.sleep(10)
    while True:
        try:
            valor = int(input(
                "\nDigite uma opção:\n"
                "1 - Baixar um Dataset\n"
                "2 - Abrir D-Tale\n"
                "3 - Gerar Profiling YData\n"
                "4 - Treinar com PyCaret\n"
                "5 - Sair\n> "
            ))

            match valor:
                case 1:
                    dataset_nome = input("Digite o nome do dataset (formato: user/dataset): ")
                    logger.info("Iniciando autenticação no Kaggle.\n")
                    API = KaggleDownloader(dataset_nome)
                    
                    if API:
                        logger.info("Autenticação bem-sucedida! Fazendo download do dataset.\n")
                        KaggleDownloader.verificar_e_baixar_dataset(API)
                    else:
                        logger.error("\nFalha na autenticação do Kaggle. Encerrando aplicação.\n")
                        sys.exit(1)
                        
                case 2:
                    logger.info("Abrindo D-Tale\n")
                    caminho_dataset = escolher_dataset()
                    if caminho_dataset:
                        try:
                            df = pd.read_csv(caminho_dataset)
                            nome_arquivo = os.path.basename(caminho_dataset)
                            profiling = Profiling(nome_arquivo, df)
                            profiling.generate_dtale()
                        except Exception as e:
                            logger.error(f"Erro ao abrir dataset com D-Tale: {e}")
                    else:
                        logger.info("🚫 Nenhum dataset selecionado.")
                
                case 3:
                    logger.info("Iniciando a geração do arquivo YData e Imagem Shap\n")
                    caminho_dataset = escolher_dataset()
                    if caminho_dataset:
                        try:
                            df = pd.read_csv(caminho_dataset)
                            nome_arquivo = os.path.basename(caminho_dataset)
                            profiling = Profiling(nome_arquivo, df)
                            profiling.generate_ydata()
                        except Exception as e:
                            logger.error(f"Erro na geração {e}")
                    else:
                        logger.info("🚫 Nenhum dataset selecionado.")

                case 4:
                    logger.info("Iniciando o treinamento do modelo com PyCaret\n")        
                    caminho_dataset = escolher_dataset()       
                    if caminho_dataset:
                        try:
                            df = pd.read_csv(caminho_dataset)
                            nome_arquivo = os.path.basename(caminho_dataset)
                            
                            target = "Fraud_Label"
                            trainer = PyCaretTrainer()
                            
                            task_type = "classification"  # Ou "regression" ou "clustering"
                            model = trainer.train_model(df, target, task_type,)
                            logger.info(f"✅ Modelo treinado: {model}")
                        except Exception as e:
                            logger.error(f"Erro no treinamento do modelo: {e}")
                    else:
                        logger.info("🚫 Nenhum dataset selecionado.")
                case 5:
                    print("Saindo...")
                    break

                case _:
                    print("Opção inválida. Escolha entre 1 e 4.")

        except ValueError:
            print("Entrada inválida! Digite um número.")

if __name__ == "__main__":
    Main()
