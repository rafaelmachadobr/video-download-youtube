from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import Video


class VideoRepository(ABC):
    """
    Interface para repositório de vídeos.
    Define o contrato que qualquer implementação deve seguir.
    """

    @abstractmethod
    def save(self, video: Video) -> None:
        """Salva um vídeo no repositório."""
        pass

    @abstractmethod
    def find_by_url(self, url: str) -> Optional[Video]:
        """Busca um vídeo pela URL."""
        pass

    @abstractmethod
    def get_all(self) -> List[Video]:
        """Retorna todos os vídeos salvos."""
        pass
