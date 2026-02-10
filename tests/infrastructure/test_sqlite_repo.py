"""
Testes unitários para SQLiteVideoRepository.
"""

from datetime import datetime

import pytest

from src.domain.entities import Video
from src.domain.exceptions import VideoNotSavedException
from src.infrastructure.sqlite_repo import SQLiteVideoRepository


class TestSQLiteVideoRepository:
    """Testes para o repositório SQLite."""

    def test_init_creates_database(self, temp_db_path):
        """Testa que o banco de dados é criado na inicialização."""
        # Act
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        # Assert
        import sqlite3

        with sqlite3.connect(temp_db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='videos'"
            )
            assert cursor.fetchone() is not None

    def test_save_video(self, temp_db_path, sample_video):
        """Testa salvar um vídeo."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        # Act
        repo.save(sample_video)

        # Assert
        found = repo.find_by_url(sample_video.url)
        assert found is not None
        assert found.url == sample_video.url
        assert found.title == sample_video.title
        assert found.file_path == sample_video.file_path

    def test_save_duplicate_url(self, temp_db_path, sample_video):
        """Testa que salvar URL duplicada não levanta exceção mas não duplica."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        # Act - salva duas vezes
        repo.save(sample_video)
        repo.save(sample_video)  # Não deve levantar exceção

        # Assert - deve ter apenas um registro
        all_videos = repo.get_all()
        assert len(all_videos) == 1

    def test_find_by_url_found(self, temp_db_path, sample_video):
        """Testa buscar vídeo por URL quando existe."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)
        repo.save(sample_video)

        # Act
        found = repo.find_by_url(sample_video.url)

        # Assert
        assert found is not None
        assert found.url == sample_video.url
        assert found.title == sample_video.title

    def test_find_by_url_not_found(self, temp_db_path):
        """Testa buscar vídeo por URL quando não existe."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        # Act
        found = repo.find_by_url("https://youtube.com/watch?v=nonexistent")

        # Assert
        assert found is None

    def test_get_all_empty(self, temp_db_path):
        """Testa buscar todos quando não há vídeos."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        # Act
        videos = repo.get_all()

        # Assert
        assert videos == []

    def test_get_all_multiple_videos(self, temp_db_path):
        """Testa buscar todos os vídeos quando há múltiplos."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        video1 = Video(
            url="https://youtube.com/watch?v=1",
            title="Video 1",
            file_path="downloads/video1.mp4",
            downloaded_at=datetime(2024, 1, 1, 10, 0, 0),
        )
        video2 = Video(
            url="https://youtube.com/watch?v=2",
            title="Video 2",
            file_path="downloads/video2.mp4",
            downloaded_at=datetime(2024, 1, 2, 10, 0, 0),
        )

        repo.save(video1)
        repo.save(video2)

        # Act
        videos = repo.get_all()

        # Assert
        assert len(videos) == 2
        # Deve retornar ordenado por data (mais recente primeiro)
        assert videos[0].url == video2.url
        assert videos[1].url == video1.url

    def test_context_manager_closes_connection(self, temp_db_path, sample_video):
        """Testa que as conexões são fechadas adequadamente."""
        # Arrange
        repo = SQLiteVideoRepository(db_path=temp_db_path)

        # Act
        repo.save(sample_video)
        found = repo.find_by_url(sample_video.url)
        all_videos = repo.get_all()

        # Assert - se não houver memory leaks, estas operações funcionam
        assert found is not None
        assert len(all_videos) == 1

        # Testa que pode acessar o banco externamente (conexões foram fechadas)
        import sqlite3

        with sqlite3.connect(temp_db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM videos")
            count = cursor.fetchone()[0]
            assert count == 1
