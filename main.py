from src.infrastructure.yt_dlp_service import YTDLPService
from src.infrastructure.sqlite_repo import SQLiteVideoRepository
from src.usecases.download_video import DownloadVideo
from src.presentation.cli import run_cli

def main():
    downloader = YTDLPService()
    repo = SQLiteVideoRepository()
    usecase = DownloadVideo(downloader, repo)

    run_cli(usecase)

if __name__ == "__main__":
    main()
