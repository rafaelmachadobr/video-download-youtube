import os


def run_cli(download_usecase):
    os.system("cls")
    os.system("color a")
    url = input("URL do vídeo: ")
    video = download_usecase.execute(url)

    print("\nDownload concluído!")
    print("Título:", video.title)
    print("Arquivo:", video.file_path)
