from datetime import datetime
from src.domain.entities import Video
from src.domain.repositories import VideoRepository

class DownloadVideo:
    def __init__(self, downloader_service, video_repo: VideoRepository):
        self.downloader = downloader_service
        self.repo = video_repo

    def execute(self, url: str) -> Video:
        title, path = self.downloader.download(url)

        video = Video(
            url=url,
            title=title,
            file_path=path,
            downloaded_at=datetime.now()
        )

        self.repo.save(video)
        return video
