"""
Testes unitários para YTDLPService.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
import yt_dlp

from src.domain.exceptions import DownloadFailedException
from src.infrastructure.yt_dlp_service import YTDLPService


class TestYTDLPService:
    """Testes para o serviço de download YTDLPService."""

    @patch("yt_dlp.YoutubeDL")
    def test_download_success(self, mock_yt_dlp_class):
        """Testa download bem-sucedido."""
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_yt_dlp_class.return_value.__enter__.return_value = mock_ydl_instance

        mock_info = {"title": "Test Video", "ext": "mp4"}
        mock_ydl_instance.extract_info.return_value = mock_info
        mock_ydl_instance.prepare_filename.return_value = "downloads/Test Video.mp4"

        service = YTDLPService()

        # Act
        title, filename = service.download("https://youtube.com/watch?v=test123")

        # Assert
        assert title == "Test Video"
        assert filename == "downloads/Test Video.mp4"
        mock_ydl_instance.extract_info.assert_called_once_with(
            "https://youtube.com/watch?v=test123", download=True
        )

    @patch("yt_dlp.YoutubeDL")
    def test_download_no_info_returned(self, mock_yt_dlp_class):
        """Testa quando não consegue extrair informações."""
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_yt_dlp_class.return_value.__enter__.return_value = mock_ydl_instance
        mock_ydl_instance.extract_info.return_value = None

        service = YTDLPService()

        # Act & Assert
        with pytest.raises(DownloadFailedException) as exc_info:
            service.download("https://youtube.com/watch?v=invalid")

        assert "Não foi possível extrair informações" in str(exc_info.value)

    @patch("yt_dlp.YoutubeDL")
    def test_download_no_title(self, mock_yt_dlp_class):
        """Testa quando não há título disponível."""
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_yt_dlp_class.return_value.__enter__.return_value = mock_ydl_instance

        mock_info = {"ext": "mp4"}  # Sem título
        mock_ydl_instance.extract_info.return_value = mock_info
        mock_ydl_instance.prepare_filename.return_value = "downloads/video.mp4"

        service = YTDLPService()

        # Act
        title, filename = service.download("https://youtube.com/watch?v=test123")

        # Assert
        assert title == "video_sem_titulo"
        assert filename == "downloads/video.mp4"

    @patch("yt_dlp.YoutubeDL")
    def test_download_error(self, mock_yt_dlp_class):
        """Testa erro durante o download."""
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_yt_dlp_class.return_value.__enter__.return_value = mock_ydl_instance
        mock_ydl_instance.extract_info.side_effect = yt_dlp.utils.DownloadError(
            "Video unavailable"
        )

        service = YTDLPService()

        # Act & Assert
        with pytest.raises(DownloadFailedException) as exc_info:
            service.download("https://youtube.com/watch?v=test123")

        assert "Video unavailable" in str(exc_info.value)

    @patch("yt_dlp.YoutubeDL")
    def test_download_unexpected_error(self, mock_yt_dlp_class):
        """Testa erro inesperado durante o download."""
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_yt_dlp_class.return_value.__enter__.return_value = mock_ydl_instance
        mock_ydl_instance.extract_info.side_effect = Exception("Unexpected error")

        service = YTDLPService()

        # Act & Assert
        with pytest.raises(DownloadFailedException) as exc_info:
            service.download("https://youtube.com/watch?v=test123")

        assert "Erro inesperado" in str(exc_info.value)
        assert "Unexpected error" in str(exc_info.value)

    def test_custom_output_template(self):
        """Testa criação de serviço com template customizado."""
        # Act
        service = YTDLPService(output_template="custom/path/%(title)s.%(ext)s")

        # Assert
        assert service.output_template == "custom/path/%(title)s.%(ext)s"

    @patch("yt_dlp.YoutubeDL")
    def test_download_with_custom_template(self, mock_yt_dlp_class):
        """Testa download com template customizado."""
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_yt_dlp_class.return_value.__enter__.return_value = mock_ydl_instance

        mock_info = {"title": "Custom Video", "ext": "mp4"}
        mock_ydl_instance.extract_info.return_value = mock_info
        mock_ydl_instance.prepare_filename.return_value = "custom/path/Custom Video.mp4"

        service = YTDLPService(output_template="custom/path/%(title)s.%(ext)s")

        # Act
        title, filename = service.download("https://youtube.com/watch?v=test")

        # Assert
        assert filename == "custom/path/Custom Video.mp4"

        # Verifica se o template foi usado
        call_args = mock_yt_dlp_class.call_args
        assert call_args[0][0]["outtmpl"] == "custom/path/%(title)s.%(ext)s"
