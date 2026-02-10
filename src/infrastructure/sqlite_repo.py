import logging
import sqlite3
from typing import List, Optional

from src.domain.entities import Video
from src.domain.exceptions import VideoNotSavedException
from src.domain.repositories import VideoRepository

logger = logging.getLogger(__name__)


class SQLiteVideoRepository(VideoRepository):
    """
    Implementação SQLite do VideoRepository.
    Usa context manager para gerenciar conexões adequadamente
    e evitar memory leaks.
    """

    def __init__(self, db_path: str = "db.sqlite3"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Inicializa o banco de dados criando a tabela se não existir."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS videos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT NOT NULL,
                        title TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        downloaded_at TEXT NOT NULL,
                        UNIQUE(url)
                    )
                """
                )
                conn.commit()
                logger.info(f"Banco de dados inicializado: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise VideoNotSavedException(f"Erro ao inicializar banco: {e}")

    def save(self, video: Video) -> None:
        """Salva um vídeo no banco de dados usando context manager."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO videos (url, title, file_path, downloaded_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        video.url,
                        video.title,
                        video.file_path,
                        video.downloaded_at.isoformat(),
                    ),
                )
                conn.commit()
                logger.info(f"Vídeo salvo: {video.title}")
        except sqlite3.IntegrityError:
            logger.warning(f"Vídeo já existe no banco: {video.url}")
            # Não levanta exceção para URLs duplicadas
        except sqlite3.Error as e:
            logger.error(f"Erro ao salvar vídeo: {e}")
            raise VideoNotSavedException(f"Erro ao salvar vídeo no banco: {e}")

    def find_by_url(self, url: str) -> Optional[Video]:
        """Busca um vídeo pela URL."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM videos WHERE url = ?", (url,))
                row = cursor.fetchone()

                if row:
                    from datetime import datetime

                    return Video(
                        url=row["url"],
                        title=row["title"],
                        file_path=row["file_path"],
                        downloaded_at=datetime.fromisoformat(row["downloaded_at"]),
                    )
                return None
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar vídeo: {e}")
            return None

    def get_all(self) -> List[Video]:
        """Retorna todos os vídeos salvos."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM videos ORDER BY downloaded_at DESC"
                )
                rows = cursor.fetchall()

                from datetime import datetime

                return [
                    Video(
                        url=row["url"],
                        title=row["title"],
                        file_path=row["file_path"],
                        downloaded_at=datetime.fromisoformat(row["downloaded_at"]),
                    )
                    for row in rows
                ]
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar todos os vídeos: {e}")
            return []
