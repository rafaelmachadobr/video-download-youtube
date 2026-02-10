from abc import ABC, abstractmethod
from src.domain.entities import Video

class VideoRepository(ABC):
    @abstractmethod
    def save(self, video: Video) -> None:
        pass
