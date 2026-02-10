"""
Testes unitários para exceções customizadas.
"""

import pytest

from src.domain.exceptions import (
    DomainException,
    DownloadFailedException,
    InvalidURLException,
    VideoNotSavedException,
)


class TestExceptions:
    """Testes para exceções do domínio."""

    def test_domain_exception_is_base(self):
        """Testa que DomainException é a exceção base."""
        exc = DomainException("Test error")
        assert isinstance(exc, Exception)
        assert str(exc) == "Test error"

    def test_invalid_url_exception(self):
        """Testa InvalidURLException."""
        url = "invalid-url"
        exc = InvalidURLException(url)

        assert isinstance(exc, DomainException)
        assert exc.url == url
        assert "invalid-url" in str(exc)

    def test_invalid_url_exception_with_custom_message(self):
        """Testa InvalidURLException com mensagem customizada."""
        url = "ftp://test.com"
        message = "Protocolo não suportado"
        exc = InvalidURLException(url, message)

        assert exc.url == url
        assert message in str(exc)
        assert url in str(exc)

    def test_download_failed_exception(self):
        """Testa DownloadFailedException."""
        url = "https://youtube.com/watch?v=123"
        reason = "Vídeo não encontrado"
        exc = DownloadFailedException(url, reason)

        assert isinstance(exc, DomainException)
        assert exc.url == url
        assert exc.reason == reason
        assert url in str(exc)
        assert reason in str(exc)

    def test_video_not_saved_exception(self):
        """Testa VideoNotSavedException."""
        reason = "Database connection failed"
        exc = VideoNotSavedException(reason)

        assert isinstance(exc, DomainException)
        assert reason in str(exc)

    def test_exceptions_can_be_caught_as_domain_exception(self):
        """Testa que todas as exceções podem ser capturadas como DomainException."""
        exceptions = [
            InvalidURLException("test"),
            DownloadFailedException("url", "reason"),
            VideoNotSavedException("reason"),
        ]

        for exc in exceptions:
            assert isinstance(exc, DomainException)
