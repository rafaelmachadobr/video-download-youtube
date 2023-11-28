class UserInterface:
    def get_user_input(self):
        return input("Digite o link do vídeo: ")

    def get_download_format(self):
        return input('Formato:\n1 - MP3\n2 - MP4\n> ')

    def display_video_info(self, video):
        print(f'Video: {video.title}')

    def display_invalid_option_message(self):
        print("Opção inválida, você precisa digitar '1' para mp3 ou '2' para mp4")
