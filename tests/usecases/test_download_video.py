"""
Testes unitários para o caso de uso DownloadVideo.
"""

from datetime import datetime
from unittest.mock import MagicMock, Mock

import pytest

from src.domain.entities import Video
from src.domain.exceptions import DownloadFailedException, InvalidURLException
from src.usecases.download_video import DownloadVideo


class TestDownloadVideo:
    """Testes para o caso de uso DownloadVideo."""

    def test_execute_success(self, sample_video):
        """Testa download bem-sucedido de um vídeo."""
        # Arrange
        mock_downloader = Mock()
        mock_downloader.download.return_value = (
            "Test Video",
            "downloads/test_video.mp4",
        )

        mock_repo = Mock()
        mock_repo.find_by_url.return_value = None  # Vídeo não existe ainda

        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act
        video = usecase.execute("https://youtube.com/watch?v=test123")

        # Assert
        assert video.title == "Test Video"
        assert video.file_path == "downloads/test_video.mp4"
        assert video.url == "https://youtube.com/watch?v=test123"
        assert isinstance(video.downloaded_at, datetime)

        mock_downloader.download.assert_called_once_with(
            "https://youtube.com/watch?v=test123"
        )
        mock_repo.save.assert_called_once()

    def test_execute_with_existing_video(self, sample_video):
        """Testa que vídeo já baixado não é baixado novamente."""
        # Arrange
        mock_downloader = Mock()
        mock_repo = Mock()
        mock_repo.find_by_url.return_value = sample_video  # Vídeo já existe

        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act
        video = usecase.execute(sample_video.url)

        # Assert
        assert video == sample_video
        mock_downloader.download.assert_not_called()  # Não deve baixar novamente
        mock_repo.save.assert_not_called()  # Não deve salvar novamente

    def test_execute_with_empty_url(self):
        """Testa que URL vazia levanta exceção."""
        # Arrange
        mock_downloader = Mock()
        mock_repo = Mock()
        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act & Assert
        with pytest.raises(InvalidURLException) as exc_info:
            usecase.execute("")

        assert "não pode ser vazia" in str(exc_info.value)

    def test_execute_with_invalid_url(self):
        """Testa que URL inválida levanta exceção."""
        # Arrange
        mock_downloader = Mock()
        mock_repo = Mock()
        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act & Assert
        with pytest.raises(InvalidURLException):
            usecase.execute("not-a-valid-url")

    def test_execute_with_non_http_url(self):
        """Testa que URL com protocolo diferente de http/https levanta exceção."""
        # Arrange
        mock_downloader = Mock()
        mock_repo = Mock()
        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act & Assert
        with pytest.raises(InvalidURLException) as exc_info:
            usecase.execute("ftp://example.com/file")

        assert "http://" in str(exc_info.value) or "https://" in str(exc_info.value)

    def test_execute_download_failure(self):
        """Testa que falha no download levanta exceção."""
        # Arrange
        mock_downloader = Mock()
        mock_downloader.download.side_effect = DownloadFailedException(
            "https://youtube.com/watch?v=test", "Vídeo não encontrado"
        )

        mock_repo = Mock()
        mock_repo.find_by_url.return_value = None

        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act & Assert
        with pytest.raises(DownloadFailedException) as exc_info:
            usecase.execute("https://youtube.com/watch?v=test")

        assert "Vídeo não encontrado" in str(exc_info.value)

    def test_validate_url_valid(self, valid_urls):
        """Testa validação de URLs válidas."""
        # Arrange
        mock_downloader = Mock()
        mock_repo = Mock()
        usecase = DownloadVideo(mock_downloader, mock_repo)

        # Act & Assert
        for url in valid_urls:
            # Não deve levantar exceção
            usecase._validate_url(url)

    def test_validate_url_invalid(self):
        """Testa validação de URLs inválidas."""
        # Arrange
        mock_downloader = Mock()
        mock_repo = Mock()
        usecase = DownloadVideo(mock_downloader, mock_repo)

        invalid_urls = ["", "   ", "not-url", "ftp://test.com"]

        # Act & Assert
        for url in invalid_urls:
            with pytest.raises(InvalidURLException):
                usecase._validate_url(url)
