from pytube import YouTube
from pytube.exceptions import RegexMatchError


class VideoDownloader:
    def get_video_info(self, url):
        try:
            return YouTube(url)
        except RegexMatchError:
            print("Vídeo não encontrado, tente novamente.")
            return None
