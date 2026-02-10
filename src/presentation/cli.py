import logging
import os
import platform

from src.domain.exceptions import (
    DownloadFailedException,
    InvalidURLException,
    VideoNotSavedException,
)

logger = logging.getLogger(__name__)


def clear_screen() -> None:
    """Limpa a tela do terminal de forma cross-platform."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def run_cli(download_usecase):
    """
    Interface de linha de comando para download de vídeos.
    Funciona em Windows, Linux e macOS.
    """
    clear_screen()

    print("=" * 60)
    print(" 🎥  YouTube Video Downloader")
    print("=" * 60)
    print()

    try:
        url = input("Digite a URL do vídeo: ").strip()

        if not url:
            print("\n❌ Erro: URL não pode ser vazia!")
            return

        print("\n⏳ Baixando vídeo, aguarde...")

        video = download_usecase.execute(url)

        print("\n" + "=" * 60)
        print("✅ Download concluído com sucesso!")
        print("=" * 60)
        print(f"Título:   {video.title}")
        print(f"Arquivo:  {video.file_path}")
        print(f"Baixado:  {video.downloaded_at.strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)

    except InvalidURLException as e:
        logger.error(f"URL inválida: {e}")
        print(f"\n❌ Erro: {e}")
        print("Por favor, forneça uma URL válida (ex: https://youtube.com/watch?v=...)")

    except DownloadFailedException as e:
        logger.error(f"Falha no download: {e}")
        print(f"\n❌ Erro ao baixar vídeo: {e.reason}")
        print("Verifique se a URL está correta e se você tem conexão com a internet.")

    except VideoNotSavedException as e:
        logger.error(f"Erro ao salvar: {e}")
        print(f"\n❌ Erro ao salvar vídeo no banco de dados: {e}")
        print("O vídeo foi baixado mas não foi registrado no histórico.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelado pelo usuário.")
        logger.info("Download cancelado pelo usuário")

    except Exception as e:
        logger.exception("Erro inesperado na CLI")
        print(f"\n❌ Erro inesperado: {e}")
        print("Por favor, tente novamente ou reporte o problema.")

    print()
