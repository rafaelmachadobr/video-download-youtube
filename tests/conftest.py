"""
Configurações e fixtures compartilhadas para os testes.
"""

import os
import tempfile
from datetime import datetime

import pytest

from src.domain.entities import Video


@pytest.fixture
def sample_video():
    """Fixture que retorna um objeto Video de exemplo."""
    return Video(
        url="https://youtube.com/watch?v=test123",
        title="Test Video",
        file_path="downloads/test_video.mp4",
        downloaded_at=datetime(2024, 1, 1, 12, 0, 0),
    )


@pytest.fixture
def temp_db_path():
    """Fixture que cria um banco de dados temporário."""
    # Cria arquivo temporário
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    yield path

    # Cleanup
    try:
        os.unlink(path)
    except:
        pass


@pytest.fixture
def valid_urls():
    """Fixture com URLs válidas para testes."""
    return [
        "https://youtube.com/watch?v=123",
        "http://youtube.com/watch?v=456",
        "https://www.youtube.com/watch?v=abc",
    ]


@pytest.fixture
def invalid_urls():
    """Fixture com URLs inválidas para testes."""
    return [
        "",
        "   ",
        "not-a-url",
        "ftp://invalid.com",
        "javascript:alert('xss')",
        None,
    ]
