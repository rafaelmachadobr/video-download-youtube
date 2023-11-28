class VideoDownloaderWithResolution:
    def download_video(self, video, output_path="videos"):
        video_stream = video.streams.get_highest_resolution()
        print('Baixando...')
        video_stream.download(output_path=output_path)
        print('Download concluído.')
