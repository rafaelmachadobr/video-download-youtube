from abc import ABC, abstractmethod
from typing import Tuple


class VideoDownloaderService(ABC):
    """
    Abstração para serviços de download de vídeo.
    Permite a implementação de diferentes estratégias de download
    seguindo o Dependency Inversion Principle.
    """

    @abstractmethod
    def download(self, url: str) -> Tuple[str, str]:
        """
        Faz o download de um vídeo a partir de uma URL.

        Args:
            url: URL do vídeo a ser baixado

        Returns:
            Tuple contendo (título do vídeo, caminho do arquivo)

        Raises:
            Exception: Caso ocorra erro no download
        """
        pass
