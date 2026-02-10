"""
Testes unitários para a interface CLI.
"""

from datetime import datetime
from io import StringIO
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.domain.entities import Video
from src.domain.exceptions import (
    DownloadFailedException,
    InvalidURLException,
    VideoNotSavedException,
)
from src.presentation.cli import clear_screen, run_cli


class TestClearScreen:
    """Testes para a função clear_screen."""

    @patch("os.system")
    @patch("platform.system")
    def test_clear_screen_windows(self, mock_platform, mock_os_system):
        """Testa limpeza de tela no Windows."""
        # Arrange
        mock_platform.return_value = "Windows"

        # Act
        clear_screen()

        # Assert
        mock_os_system.assert_called_once_with("cls")

    @patch("os.system")
    @patch("platform.system")
    def test_clear_screen_linux(self, mock_platform, mock_os_system):
        """Testa limpeza de tela no Linux."""
        # Arrange
        mock_platform.return_value = "Linux"

        # Act
        clear_screen()

        # Assert
        mock_os_system.assert_called_once_with("clear")

    @patch("os.system")
    @patch("platform.system")
    def test_clear_screen_macos(self, mock_platform, mock_os_system):
        """Testa limpeza de tela no macOS."""
        # Arrange
        mock_platform.return_value = "Darwin"

        # Act
        clear_screen()

        # Assert
        mock_os_system.assert_called_once_with("clear")


class TestRunCLI:
    """Testes para a interface CLI."""

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_success(self, mock_clear, mock_print, mock_input):
        """Testa execução bem-sucedida da CLI."""
        # Arrange
        mock_input.return_value = "https://youtube.com/watch?v=test123"

        mock_usecase = Mock()
        video = Video(
            url="https://youtube.com/watch?v=test123",
            title="Test Video",
            file_path="downloads/test.mp4",
            downloaded_at=datetime(2024, 1, 1, 12, 0, 0),
        )
        mock_usecase.execute.return_value = video

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_clear.assert_called_once()
        mock_input.assert_called_once()
        mock_usecase.execute.assert_called_once_with(
            "https://youtube.com/watch?v=test123"
        )

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_empty_url(self, mock_clear, mock_print, mock_input):
        """Testa CLI com URL vazia."""
        # Arrange
        mock_input.return_value = ""
        mock_usecase = Mock()

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_not_called()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_whitespace_url(self, mock_clear, mock_print, mock_input):
        """Testa CLI com URL contendo apenas espaços."""
        # Arrange
        mock_input.return_value = "   "
        mock_usecase = Mock()

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_not_called()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_invalid_url_exception(self, mock_clear, mock_print, mock_input):
        """Testa CLI com URL inválida."""
        # Arrange
        mock_input.return_value = "invalid-url"

        mock_usecase = Mock()
        mock_usecase.execute.side_effect = InvalidURLException(
            "invalid-url", "URL mal formatada"
        )

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_called_once()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_download_failed_exception(
        self, mock_clear, mock_print, mock_input
    ):
        """Testa CLI quando download falha."""
        # Arrange
        mock_input.return_value = "https://youtube.com/watch?v=test"

        mock_usecase = Mock()
        mock_usecase.execute.side_effect = DownloadFailedException(
            "https://youtube.com/watch?v=test", "Vídeo não encontrado"
        )

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_called_once()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_video_not_saved_exception(
        self, mock_clear, mock_print, mock_input
    ):
        """Testa CLI quando falha ao salvar."""
        # Arrange
        mock_input.return_value = "https://youtube.com/watch?v=test"

        mock_usecase = Mock()
        mock_usecase.execute.side_effect = VideoNotSavedException(
            "Erro ao salvar no banco"
        )

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_called_once()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_keyboard_interrupt(self, mock_clear, mock_print, mock_input):
        """Testa CLI quando usuário cancela (Ctrl+C)."""
        # Arrange
        mock_input.return_value = "https://youtube.com/watch?v=test"

        mock_usecase = Mock()
        mock_usecase.execute.side_effect = KeyboardInterrupt()

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_called_once()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_unexpected_exception(self, mock_clear, mock_print, mock_input):
        """Testa CLI com exceção inesperada."""
        # Arrange
        mock_input.return_value = "https://youtube.com/watch?v=test"

        mock_usecase = Mock()
        mock_usecase.execute.side_effect = Exception("Unexpected error")

        # Act
        run_cli(mock_usecase)

        # Assert
        mock_usecase.execute.assert_called_once()

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.presentation.cli.clear_screen")
    def test_run_cli_displays_video_info(self, mock_clear, mock_print, mock_input):
        """Testa que CLI exibe informações do vídeo."""
        # Arrange
        mock_input.return_value = "https://youtube.com/watch?v=test"

        video = Video(
            url="https://youtube.com/watch?v=test",
            title="Amazing Video",
            file_path="downloads/amazing.mp4",
            downloaded_at=datetime(2024, 6, 15, 14, 30, 0),
        )

        mock_usecase = Mock()
        mock_usecase.execute.return_value = video

        # Act
        run_cli(mock_usecase)

        # Assert
        # Verifica se print foi chamado com informações do vídeo
        print_calls = [str(call) for call in mock_print.call_args_list]
        all_prints = " ".join(print_calls)

        # Pelo menos uma das chamadas deve conter o título
        assert any("Amazing Video" in str(call) for call in print_calls)
