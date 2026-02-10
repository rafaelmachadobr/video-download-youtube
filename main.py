import logging
import sys
from datetime import datetime
from pathlib import Path

from src.infrastructure.sqlite_repo import SQLiteVideoRepository
from src.infrastructure.yt_dlp_service import YTDLPService
from src.presentation.cli import run_cli
from src.usecases.download_video import DownloadVideo


def setup_logging(level: str = "INFO") -> None:
    """
    Configura o sistema de logging da aplicação.
    Logs são salvos em arquivos separados por data (YYYY-MM-DD.log).
    Não exibe logs no terminal.

    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Cria diretório de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Nome do arquivo com data atual
    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = log_dir / f"{today}.log"

    # Formato do log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configuração básica (apenas arquivo, sem console)
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Log apenas para arquivo
            logging.FileHandler(log_filename, encoding="utf-8"),
        ],
    )

    # Silencia logs muito verbosos de bibliotecas externas
    logging.getLogger("yt_dlp").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado")


def main():
    """Função principal da aplicação."""
    # Configura logging
    setup_logging(level="INFO")

    logger = logging.getLogger(__name__)
    logger.info("Iniciando aplicação de download de vídeos")

    try:
        # Cria diretório de downloads se não existir
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)

        # Instancia dependências
        downloader = YTDLPService()
        repo = SQLiteVideoRepository()
        usecase = DownloadVideo(downloader, repo)

        # Executa CLI
        run_cli(usecase)

    except KeyboardInterrupt:
        logger.info("Aplicação interrompida pelo usuário")
        print("\n\nAté logo! 👋")
    except Exception as e:
        logger.exception("Erro fatal na aplicação")
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
    finally:
        logger.info("Aplicação finalizada")


if __name__ == "__main__":
    main()
