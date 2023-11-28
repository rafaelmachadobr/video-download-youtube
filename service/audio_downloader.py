import os


class AudioDownloader:
    def download_audio(self, video, output_path="videos"):
        audio_stream = video.streams.get_audio_only()
        out_file = audio_stream.download(output_path=output_path)
        base, _ = os.path.splitext(out_file)
        new_file = f'{base}.mp3'
        os.rename(out_file, new_file)
        print("Download concluído.")
