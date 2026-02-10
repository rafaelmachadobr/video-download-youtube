import logging
from typing import Tuple

import yt_dlp

from src.domain.exceptions import DownloadFailedException
from src.domain.services import VideoDownloaderService

logger = logging.getLogger(__name__)


class YTDLPService(VideoDownloaderService):
    """
    Implementação do VideoDownloaderService usando yt-dlp.
    Agora implementa a abstração do domínio, seguindo DIP.
    """

    def __init__(self, output_template: str = "downloads/%(title)s.%(ext)s"):
        self.output_template = output_template

    def download(self, url: str) -> Tuple[str, str]:
        """
        Faz o download de um vídeo usando yt-dlp.

        Args:
            url: URL do vídeo

        Returns:
            Tuple[str, str]: (título, caminho do arquivo)

        Raises:
            DownloadFailedException: Se o download falhar
        """
        ydl_opts = {
            "outtmpl": self.output_template,
            "quiet": True,
            "no_warnings": True,
        }

        try:
            logger.info(f"Iniciando download de: {url}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                if not info:
                    raise DownloadFailedException(
                        url, "Não foi possível extrair informações do vídeo"
                    )

                title = info.get("title")
                if not title:
                    title = "video_sem_titulo"

                filename = ydl.prepare_filename(info)

                logger.info(f"Download concluído: {title}")
                return title, filename

        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Erro no download: {e}")
            raise DownloadFailedException(url, str(e))
        except Exception as e:
            logger.error(f"Erro inesperado no download: {e}")
            raise DownloadFailedException(url, f"Erro inesperado: {e}")
