from pytube import YouTube
from pytube.exceptions import RegexMatchError
from typing import Optional


class VideoDownloader:
    """
    Classe responsável por baixar um vídeo do YouTube.
    """

    def get_video_info(self, url: str) -> Optional[YouTube]:
        """
        Obtém informações sobre um vídeo do YouTube.

        Parâmetros:
        - url (str): URL do vídeo do YouTube.

        Exceções:
        - RegexMatchError: se não for possível fazer correspondência com o padrão do vídeo.

        Retorna:
        Um objeto YouTube contendo informações sobre o vídeo, ou None se o vídeo não for encontrado.
        """
        try:
            return YouTube(url)
        except RegexMatchError:
            print("Vídeo não encontrado, tente novamente.")
            return None
