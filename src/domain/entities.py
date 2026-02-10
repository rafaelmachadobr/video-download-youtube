from dataclasses import dataclass
from datetime import datetime

@dataclass
class Video:
    url: str
    title: str
    file_path: str
    downloaded_at: datetime
