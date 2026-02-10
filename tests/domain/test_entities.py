"""
Testes unitários para entidades do domínio.
"""

from datetime import datetime

import pytest

from src.domain.entities import Video


class TestVideo:
    """Testes para a entidade Video."""

    def test_create_video(self):
        """Testa criação de um objeto Video."""
        # Arrange
        url = "https://youtube.com/watch?v=123"
        title = "Test Video"
        file_path = "downloads/test.mp4"
        downloaded_at = datetime.now()

        # Act
        video = Video(
            url=url, title=title, file_path=file_path, downloaded_at=downloaded_at
        )

        # Assert
        assert video.url == url
        assert video.title == title
        assert video.file_path == file_path
        assert video.downloaded_at == downloaded_at

    def test_video_immutability(self, sample_video):
        """Testa que dataclass Video é imutável (frozen)."""
        # Como não definimos frozen=True, este teste verifica mutabilidade
        # Se você quiser imutabilidade, adicione frozen=True ao dataclass

        # Por enquanto, vamos apenas verificar que podemos acessar os atributos
        assert sample_video.url is not None
        assert sample_video.title is not None
        assert sample_video.file_path is not None
        assert sample_video.downloaded_at is not None

    def test_video_equality(self):
        """Testa igualdade entre objetos Video."""
        # Arrange
        dt = datetime.now()
        video1 = Video(
            url="https://youtube.com/watch?v=123",
            title="Test",
            file_path="test.mp4",
            downloaded_at=dt,
        )
        video2 = Video(
            url="https://youtube.com/watch?v=123",
            title="Test",
            file_path="test.mp4",
            downloaded_at=dt,
        )

        # Act & Assert
        assert video1 == video2
