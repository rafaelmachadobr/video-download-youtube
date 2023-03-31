# Importando as bibliotecas necessárias
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import os

# Definindo a cor do console
os.system('color a')

# Iniciando um loop infinito
while True:
    # Solicitando o link do vídeo ao usuário
    url = input("Digite o link do vídeo: ")
    os.system('cls')

    try:
        # Obtendo os dados do vídeo
        ys = YouTube(url)
        print(f'Video: {ys.title}')

    except RegexMatchError:
        # Exceção caso o vídeo não seja encontrado
        print("Video não encontrado, tente novamente.")

    else:
        # Solicitando o formato de download ao usuário
        answer = input('format:\n1 - MP3\n2 - MP4\n> ')

        if answer == '1':
             # Obtendo apenas o áudio do vídeo
            v = ys.streams.get_audio_only()
            print("Baixando...")

            # Baixando o arquivo de áudio e convertendo para mp3
            out_file = v.download(output_path="videos")
            base, ext = os.path.splitext(out_file)
            new_file = f'{base}.mp3'
            os.rename(out_file, new_file)
            print("Download concluído.")

        elif answer == '2':
            # Obtendo o vídeo com a maior resolução
            v = ys.streams.get_highest_resolution()
            print('Baixando...')
            v.download(output_path="videos")
            print('Download concluído.')
        else:
            # Mensagem de erro caso o usuário digite uma opção inválida
            print("Opção inválida, você precisa digitar '1' para mp3 ou '2' para mp4")