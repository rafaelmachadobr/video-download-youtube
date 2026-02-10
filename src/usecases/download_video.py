import logging
from datetime import datetime
from urllib.parse import urlparse

from src.domain.entities import Video
from src.domain.exceptions import InvalidURLException
from src.domain.repositories import VideoRepository
from src.domain.services import VideoDownloaderService

logger = logging.getLogger(__name__)


class DownloadVideo:
    """
    Caso de uso para download de vídeos.
    Orquestra a validação, download e persistência de vídeos.
    """

    def __init__(
        self, downloader_service: VideoDownloaderService, video_repo: VideoRepository
    ):
        self.downloader = downloader_service
        self.repo = video_repo

    def _validate_url(self, url: str) -> None:
        """
        Valida se a URL é válida.

        Raises:
            InvalidURLException: Se a URL for inválida
        """
        if not url or not url.strip():
            raise InvalidURLException(url, "URL não pode ser vazia")

        # Valida se é uma URL válida
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise InvalidURLException(url, "URL mal formatada")

            if result.scheme not in ["http", "https"]:
                raise InvalidURLException(
                    url, "URL deve começar com http:// ou https://"
                )
        except Exception as e:
            raise InvalidURLException(url, f"URL inválida: {str(e)}")

    def execute(self, url: str) -> Video:
        """
        Executa o download de um vídeo.

        Args:
            url: URL do vídeo a ser baixado

        Returns:
            Video: Entidade Video com informações do download

        Raises:
            InvalidURLException: Se a URL for inválida
            DownloadFailedException: Se o download falhar
        """
        logger.info(f"Iniciando processo de download para URL: {url}")

        # Valida URL
        self._validate_url(url)
        logger.debug("URL validada com sucesso")

        # Verifica se já foi baixado
        existing_video = self.repo.find_by_url(url)
        if existing_video:
            logger.info(f"Vídeo já foi baixado anteriormente: {existing_video.title}")
            return existing_video

        # Faz o download
        try:
            title, path = self.downloader.download(url)
            logger.info(f"Download concluído: {title}")
        except Exception as e:
            logger.error(f"Erro ao fazer download: {e}")
            raise

        # Cria entidade
        video = Video(
            url=url, title=title, file_path=path, downloaded_at=datetime.now()
        )

        # Persiste
        try:
            self.repo.save(video)
            logger.info(f"Vídeo salvo no repositório: {title}")
        except Exception as e:
            logger.error(f"Erro ao salvar vídeo: {e}")
            raise

        return video
