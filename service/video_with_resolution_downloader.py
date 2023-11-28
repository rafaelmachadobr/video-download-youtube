from pytube import YouTube
from pytube.streams import Stream


class VideoDownloaderWithResolution:
    def download_video(self, video: YouTube, output_path: str = "videos") -> None:
        """
        Baixa o vídeo do YouTube com a resolução mais alta disponível.

        Parâmetros:
        - video (YouTube): Um objeto YouTube representando o vídeo alvo.
        - output_path (str): O caminho para o diretório onde o vídeo será salvo.
                            Padrão é "videos".

        Retorna:
        Nada. O vídeo é baixado e salvo no diretório especificado.

        Exemplo de uso:
        ```python
        from pytube import YouTube
        from service.video_with_resolution_downloader import VideoDownloaderWithResolution

        # Criar objeto YouTube
        video_url = "https://www.youtube.com/watch?v=exemplo"
        yt_video = YouTube(video_url)

        # Instanciar o VideoDownloaderWithResolution
        downloader = VideoDownloaderWithResolution()

        # Baixar o vídeo com a resolução mais alta
        downloader.download_video(yt_video, output_path="caminho/do/diretorio")
        ```
        """
        video_stream: Stream = video.streams.get_highest_resolution()
        print('\nBaixando...')
        video_stream.download(output_path=output_path)
        print('\nDownload concluído.')
