from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pytube import YouTube

from service.audio_downloader import AudioDownloader
from service.video_with_resolution_downloader import VideoDownloaderWithResolution

app = FastAPI()


class VideoRequest(BaseModel):
    """
    Classe que representa o modelo de dados para a requisição de download de vídeo.
    """
    url: str
    output_path: str = "videos"


@app.post("/download/audio")
def download_audio(video_request: VideoRequest):
    """
    Endpoint para baixar áudio do YouTube.

    Parâmetros:
    - video_request (VideoRequest): Dados da solicitação contendo a URL do vídeo e o caminho de saída.

    Retorna:
    Um dicionário com a mensagem de sucesso ou uma exceção HTTP em caso de erro.
    """
    try:
        video = YouTube(video_request.url)
        audio_downloader = AudioDownloader()
        audio_downloader.download_audio(video, output_path=video_request.output_path)
        return {"message": "Download concluído com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/download/video")
def download_video(video_request: VideoRequest):
    """
    Endpoint para baixar vídeo do YouTube com a resolução mais alta disponível.

    Parâmetros:
    - video_request (VideoRequest): Dados da solicitação contendo a URL do vídeo e o caminho de saída.

    Retorna:
    Um dicionário com a mensagem de sucesso ou uma exceção HTTP em caso de erro.
    """
    try:
        video = YouTube(video_request.url)
        video_downloader = VideoDownloaderWithResolution()
        video_downloader.download_video(video, output_path=video_request.output_path)
        return {"message": "Download concluído com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
