import os
from pytube import YouTube
from pytube.streams import Stream


class AudioDownloader:
    """
    Classe responsável por baixar o áudio de um vídeo do YouTube.
    """

    def download_audio(self, video: YouTube, output_path: str = "videos") -> None:
        """
        Baixa o áudio de um vídeo do YouTube.

        Parâmetros:
        - video (YouTube): Um objeto YouTube representando o vídeo alvo.
        - output_path (str): O caminho para o diretório onde o arquivo de áudio será salvo.
                            Padrão é "videos".

        Exceções:
        - pytube.exceptions.VideoUnavailable: Se o vídeo não estiver disponível.
        - pytube.exceptions.RegexMatchError: Se não for possível fazer correspondência com o padrão do vídeo.

        Retorna:
        Nada. O áudio é baixado e salvo no formato MP3.

        Observações:
        - O arquivo de áudio é salvo no mesmo diretório especificado em `output_path`.
        - O nome do arquivo MP3 é baseado no nome original do arquivo de áudio.

        Exemplo de uso:
        ```python
        from pytube import YouTube
        from service.audio_downloader import AudioDownloader

        # Criar objeto YouTube
        video_url = "https://www.youtube.com/watch?v=exemplo"
        yt_video = YouTube(video_url)

        # Instanciar o AudioDownloader
        audio_downloader = AudioDownloader()

        # Baixar o áudio
        audio_downloader.download_audio(yt_video, output_path="caminho/do/diretorio")
        ```
        """

        audio_stream: Stream = video.streams.get_audio_only()
        out_file: str = audio_stream.download(output_path=output_path)
        base, _ = os.path.splitext(out_file)
        new_file: str = f'{base}.mp3'
        os.rename(out_file, new_file)
        print("Download concluído.")
