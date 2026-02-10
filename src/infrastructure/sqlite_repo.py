import sqlite3

from src.domain.entities import Video
from src.domain.repositories import VideoRepository


class SQLiteVideoRepository(VideoRepository):
    def __init__(self, db_path="db.sqlite3"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY,
                url TEXT,
                title TEXT,
                file_path TEXT,
                downloaded_at TEXT
            )
        """
        )

    def save(self, video: Video):
        self.conn.execute(
            "INSERT INTO videos (url, title, file_path, downloaded_at) VALUES (?, ?, ?, ?)",
            (video.url, video.title, video.file_path, video.downloaded_at.isoformat()),
        )
        self.conn.commit()
