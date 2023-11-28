import os

from service.video_downloader import VideoDownloader
from service.audio_downloader import AudioDownloader
from service.video_with_resolution_downloader import VideoDownloaderWithResolution
from ui.user_interface import UserInterface

if __name__ == "__main__":
    video_downloader = VideoDownloader()
    audio_downloader = AudioDownloader()
    video_with_resolution_downloader = VideoDownloaderWithResolution()
    user_interface = UserInterface()

    os.system('color a')

    while True:
        url = user_interface.get_user_input()
        os.system('cls')

        if video_info := video_downloader.get_video_info(url):
            user_interface.display_video_info(video_info)
            download_format = user_interface.get_download_format()

            if download_format == '1':
                audio_downloader.download_audio(video_info)
            elif download_format == '2':
                video_with_resolution_downloader.download_video(video_info)
            else:
                user_interface.display_invalid_option_message()
